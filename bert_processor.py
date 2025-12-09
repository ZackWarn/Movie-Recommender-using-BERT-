# bert_processor.py
"""BERT processor for generating and loading movie embeddings (local-only)."""

import logging
import os
import pickle
from typing import List
import psutil
import gc

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from config import Config

logger = logging.getLogger(__name__)


class MovieBERTProcessor:
    def __init__(self, model_name: str = None, lazy_load: bool = False):
        # Use configured model name if not explicitly provided
        self.model_name = model_name or Config.BERT_MODEL_NAME
        self._model = None
        self.movie_embeddings = None
        self.movies_data = None
        self.use_external = False

        if not lazy_load:
            self._model = SentenceTransformer(self.model_name)
            if getattr(Config, "PREWARM_MODEL", False):
                try:
                    _ = self._model.encode(["warmup"], batch_size=1)
                except Exception:
                    pass

    def _get_memory_mb(self):
        """Get current process memory usage in MB"""
        try:
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except Exception:
            return 0

    def _can_safely_load_model(self, threshold_mb=380):
        """Check if we have enough memory headroom to load BERT model (~150MB)"""
        current_mb = self._get_memory_mb()
        available = threshold_mb - current_mb
        logger.info(f"Memory check: {current_mb:.1f}MB used, {available:.1f}MB available before {threshold_mb}MB threshold")
        return available > 150  # Need 150MB for model

    @property
    def model(self) -> SentenceTransformer:
        """Lazy load model only when needed for encoding queries"""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
            if getattr(Config, "PREWARM_MODEL", False):
                try:
                    _ = self._model.encode(["warmup"], batch_size=1)
                except Exception:
                    pass
        return self._model

    def encode(self, texts: List[str], force_semantic=False):
        """
        Encode texts using hybrid approach:
        - If force_semantic=True and memory allows, use BERT model
        - Otherwise, return zeros (triggers keyword fallback in recommendation engine)
        """
        if not isinstance(texts, list):
            texts = [texts]

        # Check if we can safely load the model for semantic encoding
        if force_semantic and self._can_safely_load_model():
            try:
                logger.info("Using BERT model for semantic encoding (memory allows)")
                gc.collect()  # Clean up before loading model
                embeddings = self.model.encode(texts, batch_size=Config.ENCODING_BATCH_SIZE)
                return np.array(embeddings, dtype=np.float32)
            except Exception as e:
                logger.warning(f"Failed to use BERT model: {e}, falling back to zeros")

        # Fallback: return zeros (triggers keyword matching)
        logger.info("Using zero embeddings (triggers keyword matching fallback)")
        embedding_dim = 384  # paraphrase-MiniLM-L3-v2 dimension
        return np.zeros((len(texts), embedding_dim), dtype=np.float32)

    def _encode_external(self, texts: List[str]):
        """Encode texts using Hugging Face Inference API"""
        import requests
        import time

        headers = {}
        if Config.HF_API_TOKEN:
            headers["Authorization"] = f"Bearer {Config.HF_API_TOKEN}"

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    Config.HF_INFERENCE_ENDPOINT,
                    headers=headers,
                    json={"inputs": texts, "options": {"wait_for_model": True}},
                    timeout=30,
                )

                if response.status_code == 200:
                    embeddings = response.json()
                    logger.info("External HF API success")
                    return np.array(embeddings)
                elif response.status_code == 503:
                    # Model loading, retry
                    logger.info("External HF API 503 (model loading), retrying")
                    time.sleep(2**attempt)
                    continue
                else:
                    logger.warning(
                        "External HF API error %s, falling back to local model",
                        response.status_code,
                    )
                    break
            except Exception as e:
                logger.warning(
                    "External HF API failed: %s, falling back to local model", e
                )
                break

        # Fallback to local model
        logger.info("Falling back to local model for encoding")
        batch_size = getattr(Config, "ENCODING_BATCH_SIZE", 32) or 32
        return self.model.encode(texts, batch_size=batch_size)

    def prepare_movie_texts(self, movies_df):
        """Combine movie information into text descriptions"""
        movie_texts = []

        for _, movie in movies_df.iterrows():
            text_parts = [
                f"Title: {movie['clean_title']}",
                f"Genres: {', '.join(movie['genres_list']) if movie['genres_list'] != ['(no genres listed)'] else 'Unknown'}",
                f"Year: {movie['year'] if pd.notna(movie['year']) else 'Unknown'}",
                f"Rating: {movie['avg_rating']:.1f}/5.0 ({movie['rating_count']} reviews)",
            ]

            if movie["combined_tags"]:
                tags = [str(tag) for tag in movie["combined_tags"] if pd.notna(tag)]
                text_parts.append(f"Tags: {', '.join(tags[:10])}")

            movie_texts.append(". ".join(text_parts))

        return movie_texts

    def generate_embeddings(self, movies_df):
        """Generate BERT embeddings for all movies"""
        print("Preparing movie texts...")
        movie_texts = self.prepare_movie_texts(movies_df)

        print(f"Generating embeddings for {len(movie_texts)} movies...")
        batch_size = getattr(Config, "ENCODING_BATCH_SIZE", 32) or 32
        embeddings = []

        for i in range(0, len(movie_texts), batch_size):
            batch = movie_texts[i : i + batch_size]
            batch_embeddings = self.encode(batch)
            embeddings.append(batch_embeddings)

            if (i // batch_size + 1) % 10 == 0:
                print(f"Processed {i + len(batch)}/{len(movie_texts)} movies...")

        self.movie_embeddings = np.vstack(embeddings)
        self.movies_data = movies_df.reset_index(drop=True)

        print("Embeddings generated successfully!")
        return self.movie_embeddings

    def save_embeddings(self, filepath="movie_embeddings.pkl"):
        """Save embeddings and movie data"""
        data = {"embeddings": self.movie_embeddings, "movies_data": self.movies_data}
        resolved_path = (
            filepath
            if os.path.isabs(filepath)
            else os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        )
        with open(resolved_path, "wb") as f:
            pickle.dump(data, f)
        print(f"Embeddings saved to {resolved_path}")

    def load_embeddings(self, filepath="movie_embeddings.pkl"):
        """Load pre-computed embeddings with sparse on-demand loading"""
        # Skip if already loaded
        if self.movies_data is not None:
            return

        candidate_path = (
            filepath
            if os.path.isabs(filepath)
            else os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        )
        if not os.path.exists(candidate_path):
            alt_path = os.path.abspath(filepath)
            if os.path.exists(alt_path):
                candidate_path = alt_path
            else:
                raise FileNotFoundError(
                    f"Embeddings file not found at '{filepath}' or '{candidate_path}'"
                )

        with open(candidate_path, "rb") as f:
            data = pickle.load(f)

        embeddings = data["embeddings"]

        # Store embeddings filepath and metadata only, defer actual embedding array loading
        self._embeddings_file = candidate_path
        self._embeddings_shape = embeddings.shape
        self._embeddings_dtype = embeddings.dtype

        # Store only the movie data, not embeddings
        self.movie_embeddings = None
        self.movies_data = data["movies_data"]

        # Downcast numeric columns to save metadata memory
        for col in self.movies_data.columns:
            col_type = self.movies_data[col].dtype
            if col_type == "float64":
                self.movies_data[col] = self.movies_data[col].astype("float32")
            elif col_type == "int64":
                self.movies_data[col] = self.movies_data[col].astype("int32")

        print(
            f"Embeddings metadata loaded from {candidate_path} (embeddings loaded on-demand)"
        )

    def _get_embeddings(self):
        """Lazy load embeddings on-demand"""
        if self.movie_embeddings is None:
            print("Loading embeddings from disk...")
            self._log_memory("before loading embeddings from disk")

            with open(self._embeddings_file, "rb") as f:
                data = pickle.load(f)
            embeddings = data["embeddings"]

            self._log_memory("after loading raw embeddings")

            # Quantize to uint8: scale from [-1, 1] to [0, 255]
            if embeddings.dtype != np.uint8:
                embeddings = np.clip((embeddings + 1) * 127.5, 0, 255).astype(np.uint8)

            self.movie_embeddings = embeddings
            self._log_memory("after quantization complete")
            print(f"Embeddings loaded into memory: {self.movie_embeddings.shape}")

        return self.movie_embeddings

    def _log_memory(self, stage=""):
        """Log memory usage if psutil is available"""
        try:
            import psutil
            import os

            process = psutil.Process(os.getpid())
            mem_mb = process.memory_info().rss / 1024 / 1024
            print(f"[MEMORY] {stage}: {mem_mb:.2f} MB")
        except:
            pass

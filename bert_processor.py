# bert_processor.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
# External API usage removed to keep local-only encoding
from typing import List
from config import Config


class MovieBERTProcessor:
    def __init__(self, model_name='all-MiniLM-L6-v2', lazy_load=False):
        self.model_name = model_name
        self._model = None
        self.movie_embeddings = None
        self.movies_data = None
        # Always use local model only
        self.use_external = False

        # Only load local model if not lazy loading
        if not lazy_load:
            self._model = SentenceTransformer(model_name)

    @property
    def model(self):
        """Lazy load model only when needed for encoding queries"""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: List[str]):
        """Encode texts into embeddings using either local model or Hugging Face Inference API"""
        if not isinstance(texts, list):
            texts = [texts]
        
        # Local-only path
        return self.model.encode(texts)

    def prepare_movie_texts(self, movies_df):
        """Combine movie information into text descriptions"""
        movie_texts = []

        for idx, movie in movies_df.iterrows():
            # Create comprehensive movie description
            text_parts = [
                f"Title: {movie['clean_title']}",
                f"Genres: {', '.join(movie['genres_list']) if movie['genres_list'] != ['(no genres listed)'] else 'Unknown'}",
                f"Year: {movie['year'] if pd.notna(movie['year']) else 'Unknown'}",
                f"Rating: {movie['avg_rating']:.1f}/5.0 ({movie['rating_count']} reviews)",
            ]

            # Add tags if available
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
        # Generate embeddings in batches to manage memory
        batch_size = 32
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
        # Resolve path relative to this file if a relative path is provided
        resolved_path = (
            filepath
            if os.path.isabs(filepath)
            else os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        )
        with open(resolved_path, "wb") as f:
            pickle.dump(data, f)
        print(f"Embeddings saved to {resolved_path}")

    def load_embeddings(self, filepath="movie_embeddings.pkl"):
        """Load pre-computed embeddings with memory optimization
        Looks for file at absolute path if provided; otherwise resolves relative to this file's directory.
        """
        # Try absolute path, otherwise resolve relative to this file's directory
        candidate_path = (
            filepath
            if os.path.isabs(filepath)
            else os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        )
        if not os.path.exists(candidate_path):
            # Fallback to current working directory if still not found
            alt_path = os.path.abspath(filepath)
            if os.path.exists(alt_path):
                candidate_path = alt_path
            else:
                raise FileNotFoundError(
                    f"Embeddings file not found at '{filepath}' or '{candidate_path}'"
                )

        with open(candidate_path, "rb") as f:
            data = pickle.load(f)

        # Convert embeddings to float16 to save memory (halves memory usage)
        self.movie_embeddings = data["embeddings"].astype("float16")

        # Optimize DataFrame memory usage
        self.movies_data = data["movies_data"]

        # Convert columns to more memory-efficient types
        for col in self.movies_data.columns:
            col_type = self.movies_data[col].dtype
            if col_type == "float64":
                self.movies_data[col] = self.movies_data[col].astype("float32")
            elif col_type == "int64":
                self.movies_data[col] = self.movies_data[col].astype("int32")

        print(
            f"Embeddings loaded successfully from {candidate_path} with memory optimization!"
        )

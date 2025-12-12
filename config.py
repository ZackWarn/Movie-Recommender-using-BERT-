import os
from typing import Optional


class Config:
    """Configuration class for the movie recommendation system"""

    # RapidAPI IMDB Configuration
    RAPIDAPI_IMDB_KEY: Optional[str] = os.getenv("RAPIDAPI_IMDB_KEY")
    RAPIDAPI_IMDB_HOST: str = "imdb8.p.rapidapi.com"

    # Model configuration (local-only)
    # Use TinyBERT (~60MB) to stay under 512MB on Render
    BERT_MODEL_NAME = "sentence-transformers/paraphrase-TinyBERT-L6-v2"
    EMBEDDINGS_FILE = "movie_embeddings.pkl"
    ENCODING_BATCH_SIZE: int = 64
    PREWARM_MODEL: bool = False

    # Memory-constrained mode for Render free tier (512MB limit)
    # When true, uses keyword-only matching (no BERT loading)
    KEYWORD_ONLY_MODE: bool = (
        os.getenv("KEYWORD_ONLY_MODE", "false").lower() == "true"
    )

    # External API disabled by default (HF returns 410 for this model)
    # Use local model which works reliably (~485MB peak memory, within 512MB limit)
    USE_EXTERNAL_EMBEDDINGS: bool = (
        os.getenv("USE_EXTERNAL_EMBEDDINGS", "false").lower() == "true"
    )
    HF_API_TOKEN: Optional[str] = os.getenv("HF_API_TOKEN")
    
    # HF Space endpoint for MiniLM embeddings (e.g., https://username-minilm-space.hf.space)
    HF_SPACE_ENDPOINT: Optional[str] = os.getenv("HF_SPACE_ENDPOINT")
    
    # HF Inference API endpoint (default or custom)
    HF_INFERENCE_ENDPOINT: str = (
        f"https://api-inference.huggingface.co/pipeline/feature-extraction/{BERT_MODEL_NAME}"
    )
    DEFAULT_TOP_K: int = 8
    MAX_SEARCH_RESULTS: int = 8

    # API Rate Limiting
    API_REQUEST_DELAY: float = 1.0  # seconds between API requests

    # File paths
    DATA_DIR: str = "movies_dataset"
    MOVIES_FILE: str = "movies.csv"
    RATINGS_FILE: str = "ratings.csv"
    TAGS_FILE: str = "tags.csv"
    GENOME_SCORES_FILE: str = "genome-scores.csv"
    GENOME_TAGS_FILE: str = "genome-tags.csv"

    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        ok = True
        if not cls.RAPIDAPI_IMDB_KEY:
            print("Warning: RAPIDAPI_IMDB_KEY not set. IMDB features will be limited.")
            ok = False
        return ok

    @classmethod
    def get_imdb_config(cls) -> dict:
        """Get IMDB API configuration"""
        return {
            "api_key": cls.RAPIDAPI_IMDB_KEY,
            "host": cls.RAPIDAPI_IMDB_HOST,
            "request_delay": cls.API_REQUEST_DELAY,
        }

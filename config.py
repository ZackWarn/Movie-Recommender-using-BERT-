import os
from typing import Optional


class Config:
    """Configuration class for the movie recommendation system"""

    # RapidAPI IMDB Configuration
    RAPIDAPI_IMDB_KEY: Optional[str] = os.getenv("RAPIDAPI_IMDB_KEY")
    RAPIDAPI_IMDB_HOST: str = "imdb8.p.rapidapi.com"

    # Model configuration (local-only)
    # Use a smaller model for faster startup on limited environments
    BERT_MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"
    EMBEDDINGS_FILE = "movie_embeddings.pkl"
    ENCODING_BATCH_SIZE: int = 64
    PREWARM_MODEL: bool = False

    # Use external API for embeddings to avoid loading model (saves ~150MB)
    USE_EXTERNAL_EMBEDDINGS: bool = (
        os.getenv("USE_EXTERNAL_EMBEDDINGS", "true").lower() == "true"
    )
    HF_API_TOKEN: Optional[str] = os.getenv("HF_API_TOKEN")
    HF_INFERENCE_ENDPOINT: str = (
        f"https://api-inference.huggingface.co/pipeline/feature-extraction/{BERT_MODEL_NAME}"
    )

    # Recommendation Configuration
    DEFAULT_TOP_K: int = 10
    MAX_SEARCH_RESULTS: int = 20

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

import os
from typing import Optional

class Config:
    """Configuration class for the movie recommendation system"""
    
    # RapidAPI IMDB Configuration
    RAPIDAPI_IMDB_KEY: Optional[str] = os.getenv('RAPIDAPI_IMDB_KEY')
    RAPIDAPI_IMDB_HOST: str = 'imdb8.p.rapidapi.com'
    
    # BERT Model Configuration
    BERT_MODEL_NAME: str = 'distilbert-base-uncased'
    EMBEDDINGS_FILE: str = 'movie_embeddings.pkl'
    
    # Recommendation Configuration
    DEFAULT_TOP_K: int = 10
    MAX_SEARCH_RESULTS: int = 20
    
    # API Rate Limiting
    API_REQUEST_DELAY: float = 1.0  # seconds between API requests
    
    # File paths
    DATA_DIR: str = 'movies_dataset'
    MOVIES_FILE: str = 'movies.csv'
    RATINGS_FILE: str = 'ratings.csv'
    TAGS_FILE: str = 'tags.csv'
    GENOME_SCORES_FILE: str = 'genome-scores.csv'
    GENOME_TAGS_FILE: str = 'genome-tags.csv'
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.RAPIDAPI_IMDB_KEY:
            print("Warning: RAPIDAPI_IMDB_KEY not set. IMDB features will be disabled.")
            return False
        return True
    
    @classmethod
    def get_imdb_config(cls) -> dict:
        """Get IMDB API configuration"""
        return {
            'api_key': cls.RAPIDAPI_IMDB_KEY,
            'host': cls.RAPIDAPI_IMDB_HOST,
            'request_delay': cls.API_REQUEST_DELAY
        }

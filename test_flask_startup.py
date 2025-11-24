"""Test Flask API initialization"""

from rec_engine import MovieRecommendationEngine
from bert_processor import MovieBERTProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    logger.info("Initializing BERT processor...")
    bert_processor = MovieBERTProcessor()

    logger.info("Loading embeddings...")
    bert_processor.load_embeddings()

    logger.info("Creating recommendation engine...")
    engine = MovieRecommendationEngine(bert_processor, use_imdb=False)

    logger.info("SUCCESS! Engine initialized successfully")
    logger.info(f"Loaded {len(engine.movies)} movies")

except Exception as e:
    logger.error(f"FAILED: {e}")
    import traceback

    traceback.print_exc()

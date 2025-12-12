"""Test the hybrid recommendation approach"""
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from bert_processor import MovieBERTProcessor
from rec_engine import MovieRecommendationEngine

def test_hybrid_recommendations():
    """Test hybrid recommendation approach"""
    logger.info("Initializing BERT processor with lazy loading...")
    processor = MovieBERTProcessor(lazy_load=True)
    
    logger.info("Loading movie metadata...")
    from data_prep import load_and_prepare_data
    processor.movies_data = load_and_prepare_data()
    logger.info(f"Loaded {len(processor.movies_data)} movies")
    
    logger.info("\nInitializing recommendation engine...")
    engine = MovieRecommendationEngine(processor, use_imdb=False)
    
    # Test queries
    test_queries = [
        "psychological thriller",
        "space adventure",
        "romantic comedy"
    ]
    
    for query in test_queries:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing query: '{query}'")
        logger.info('='*60)
        
        recommendations = engine.recommend_by_query(query, top_k=8)
        
        if recommendations:
            logger.info(f"Got {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations, 1):
                logger.info(f"  {i}. {rec['title']} ({rec['year']}) - Score: {rec['similarity_score']:.4f}")
                logger.info(f"     Genres: {', '.join(rec['genres'])}")
        else:
            logger.info("No recommendations found")
    
    logger.info(f"\n{'='*60}")
    logger.info("Test complete!")

if __name__ == "__main__":
    try:
        test_hybrid_recommendations()
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)

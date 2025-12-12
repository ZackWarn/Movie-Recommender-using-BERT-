import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from bert_processor import MovieBERTProcessor
from rec_engine import MovieRecommendationEngine
from config import Config


def main():
    print("Loading embeddings...")
    processor = MovieBERTProcessor(model_name=Config.BERT_MODEL_NAME, lazy_load=True)
    processor.load_embeddings(Config.EMBEDDINGS_FILE)
    print(f"Embeddings shape: {processor.movie_embeddings.shape}")
    print(f"Movies loaded: {len(processor.movies_data)}")

    engine = MovieRecommendationEngine(processor, use_imdb=False)
    query = "sci-fi action with mind-bending plot"
    print(f"Running query: {query}")
    recs = engine.recommend_by_query(query, top_k=5)
    for i, r in enumerate(recs, 1):
        print(
            f"{i}. {r['title']} ({r.get('year','?')}) - score {r['similarity_score']:.4f}"
        )

    # Similar by movieId if available
    if len(processor.movies_data) > 0:
        sample_id = int(processor.movies_data.iloc[0]["movieId"])
        print(f"\nSimilar to movieId={sample_id}")
        sim = engine.recommend_similar_movies(sample_id, top_k=5)
        for i, r in enumerate(sim, 1):
            print(
                f"{i}. {r['title']} ({r.get('year','?')}) - score {r['similarity_score']:.4f}"
            )


if __name__ == "__main__":
    main()

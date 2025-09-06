# evaluation.py
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np

class RecommendationEvaluator:
    def __init__(self, engine):
        self.engine = engine
    
    def evaluate_genre_consistency(self, test_queries, expected_genres):
        """Evaluate how well recommendations match expected genres"""
        results = []
        
        for query, expected in zip(test_queries, expected_genres):
            recommendations = self.engine.recommend_by_query(query, top_k=5)
            
            # Extract genres from recommendations
            recommended_genres = set()
            for rec in recommendations:
                recommended_genres.update(rec['genres'])
            
            # Calculate precision and recall
            expected_set = set(expected)
            intersection = recommended_genres.intersection(expected_set)
            
            precision = len(intersection) / len(recommended_genres) if recommended_genres else 0
            recall = len(intersection) / len(expected_set) if expected_set else 0
            
            results.append({
                'query': query,
                'precision': precision,
                'recall': recall,
                'f1': 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            })
        
        return results

# Test evaluation
def run_evaluation():
    test_queries = [
        "action movies with explosions and car chases",
        "romantic comedies from the 1990s",
        "sci-fi movies about space exploration",
        "horror films with supernatural elements"
    ]
    
    expected_genres = [
        ["Action"],
        ["Comedy", "Romance"],
        ["Sci-Fi"],
        ["Horror"]
    ]
    
    # Load your engine here
    # evaluator = RecommendationEvaluator(engine)
    # results = evaluator.evaluate_genre_consistency(test_queries, expected_genres)
    # print(f"Average F1 Score: {np.mean([r['f1'] for r in results]):.3f}")

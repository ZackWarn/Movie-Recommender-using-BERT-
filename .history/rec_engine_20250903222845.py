# recommendation_engine.py
import numpy as np
from torch import cosine_similarity


class MovieRecommendationEngine:
    def __init__(self, bert_processor):
        self.bert_processor = bert_processor
        self.model = bert_processor.model
        self.embeddings = bert_processor.movie_embeddings
        self.movies = bert_processor.movies_data
    
    def recommend_by_query(self, query, top_k=10):
    # Encode query text into embedding vector (usually a list)
        query_embedding = self.bert_processor.model.encode([query])[0]
        # Convert to numpy array and reshape to 2D for cosine_similarity
        query_embedding = np.array(query_embedding).reshape(1, -1)

        # Convert all movie embeddings to numpy array if they aren't already
        embeddings = np.array(self.embeddings)

        # Calculate cosine similarity between query and all movie embeddings
        similarities = cosine_similarity(query_embedding, embeddings)[0]  # shape: (num_movies,)

        # Get indices of top_k most similar movies
        top_indices = similarities.argsort()[::-1][:top_k]
        
        recommendations = []
        for idx in top_indices:
            movie = self.movies.iloc[idx]
            rec = {
                'movieId': movie['movieId'],
                'title': movie['clean_title'],
                'year': movie['year'],
                'genres': movie['genres_list'],
                'avg_rating': movie['avg_rating'],
                'similarity_score': similarities[idx]
            }
            recommendations.append(rec)
        
        return recommendations
    
    def recommend_similar_movies(self, movie_id, top_k=10):
        movie_idx_list = self.movies.index[self.movies['movieId'] == movie_id].tolist()
        if not movie_idx_list:
            return []
        
        movie_idx = movie_idx_list[0]
        movie_embedding = np.array(self.embeddings[movie_idx]).reshape(1, -1)
        embeddings = np.array(self.embeddings)

        similarities = cosine_similarity(movie_embedding, embeddings)[0]

        # Exclude the movie itself from similar results
        similar_indices = [i for i in similarities.argsort()[::-1] if i != movie_idx][:top_k]

        results = []
        for idx in similar_indices:
            movie = self.movies.iloc[idx]
            results.append({
                'movieId': movie['movieId'],
                'title': movie['clean_title'],
                'year': movie['year'],
                'genres': movie['genres_list'],
                'avg_rating': movie['avg_rating'],
                'similarity_score': similarities[idx]
            })
        return results

    
    def search_movies(self, search_term):
        """Search for movies by title"""
        search_term = search_term.lower()
        matches = self.movies[
            self.movies['clean_title'].str.lower().str.contains(search_term, na=False)
        ]
        return matches[['movieId', 'clean_title', 'year', 'genres_list', 'avg_rating']].to_dict('records')
    
    def _generate_explanation(self, similarity_score):
        """Generate explanation for recommendation"""
        if similarity_score > 0.8:
            return f"Excellent match ({similarity_score:.1%}) - Very similar themes and characteristics"
        elif similarity_score > 0.6:
            return f"Good match ({similarity_score:.1%}) - Similar genre and style"
        elif similarity_score > 0.4:
            return f"Fair match ({similarity_score:.1%}) - Some shared elements"
        else:
            return f"Weak match ({similarity_score:.1%}) - Limited similarity"

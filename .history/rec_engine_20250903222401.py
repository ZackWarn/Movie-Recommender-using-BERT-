# recommendation_engine.py
import numpy as np
from torch import cosine_similarity


class MovieRecommendationEngine:
    def __init__(self, bert_processor):
        self.bert_processor = bert_processor
        self.model = bert_processor.model
        self.embeddings = bert_processor.movie_embeddings
        self.movies = bert_processor.movies_data
    
    def recommend_by_query(self, query, top_k=10, threshold=0.1):
        """Recommend movies based on natural language query"""
        print(f"Processing query: '{query}'")
        
        query_emb = self.bert_processor.model.encode([query])[0]  # get 1D vector
        query_emb = np.array(query_emb).reshape(1, -1)            # shape = (1, dim)
        embeddings = np.array(self.embeddings)                    # shape = (num_movies, dim)

        similarities = cosine_similarity(query_emb, embeddings)[0]  # result is 1D similarity array
        
        # Get top recommendations above threshold
        movie_scores = list(enumerate(similarities))
        movie_scores = [(idx, score) for idx, score in movie_scores if score > threshold]
        movie_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k recommendations
        recommendations = []
        for idx, score in movie_scores[:top_k]:
            movie = self.movies.iloc[idx]
            recommendations.append({
                'movie_id': movie['movieId'],
                'title': movie['clean_title'],
                'year': movie['year'],
                'genres': movie['genres_list'],
                'rating': movie['avg_rating'],
                'rating_count': movie['rating_count'],
                'tags': movie['combined_tags'][:5],
                'similarity_score': score,
                'explanation': self._generate_explanation(score)
            })
        
        return recommendations
    
    def recommend_similar_movies(self, movie_id, top_k=10):
        """Find movies similar to a given movie"""
        # Find movie index
        movie_idx = self.movies.index[self.movies['movieId'] == movie_id].tolist()
    if not movie_idx:
        return []
    movie_idx = movie_idx[0]

    target_emb = np.array(self.embeddings[movie_idx]).reshape(1, -1)
    embeddings = np.array(self.embeddings)

    similarities = cosine_similarity(target_emb, embeddings)[0]
        
        # Get similar movies (excluding the movie itself)
        movie_scores = [(idx, score) for idx, score in enumerate(similarities) if idx != movie_idx]
        movie_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k similar movies
        recommendations = []
        for idx, score in movie_scores[:top_k]:
            movie = self.movies.iloc[idx]
            recommendations.append({
                'movie_id': movie['movieId'],
                'title': movie['clean_title'],
                'year': movie['year'],
                'genres': movie['genres_list'],
                'rating': movie['avg_rating'],
                'similarity_score': score,
                'explanation': f"Similar to '{target_movie['clean_title']}' - {self._generate_explanation(score)}"
            })
        
        return recommendations
    
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

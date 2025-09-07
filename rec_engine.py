import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommendationEngine:
    def __init__(self, bert_processor):
        self.bert_processor = bert_processor
        self.movies = bert_processor.movies_data
        self.embeddings = bert_processor.movie_embeddings

    def recommend_by_query(self, query, top_k=10):
        # Encode the query to embedding vector
        query_embedding = self.bert_processor.model.encode([query])[0]
        query_embedding = np.array(query_embedding).reshape(1, -1)

        embeddings = np.array(self.embeddings)

        # Compute cosine similarities
        similarities = cosine_similarity(query_embedding, embeddings)[0]

        # Get indices of top_k highest similarity scores
        top_indices = similarities.argsort()[::-1][:top_k]

        recommendations = []
        for idx in top_indices:
            if idx < 0 or idx >= len(self.movies):
                continue
            movie = self.movies.iloc[idx]
            recommendations.append({
                'movieId': movie['movieId'],
                'title': movie['clean_title'],
                'year': movie.get('year', 'Unknown'),
                'genres': movie.get('genres_list', []),
                'avg_rating': movie.get('avg_rating', 0),
                'similarity_score': float(similarities[idx])
            })
        return recommendations

    def recommend_similar_movies(self, movie_id, top_k=10):
        movie_idx_list = self.movies.index[self.movies['movieId'] == movie_id].tolist()
        if not movie_idx_list:
            # Movie ID not found
            return []
        movie_idx = movie_idx_list[0]

        movie_embedding = np.array(self.embeddings[movie_idx]).reshape(1, -1)
        embeddings = np.array(self.embeddings)

        similarities = cosine_similarity(movie_embedding, embeddings)[0]

        # Sort similarities excluding the movie itself
        sorted_indices = similarities.argsort()[::-1]
        similar_indices = [i for i in sorted_indices if i != movie_idx and 0 <= i < len(self.movies)][:top_k]

        results = []
        for idx in similar_indices:
            if idx < 0 or idx >= len(self.movies):
                continue
            movie = self.movies.iloc[idx]
            results.append({
                'movieId': movie['movieId'],
                'title': movie['clean_title'],
                'year': movie.get('year', 'Unknown'),
                'genres': movie.get('genres_list', []),
                'avg_rating': movie.get('avg_rating', 0),
                'similarity_score': float(similarities[idx])
            })
        return results

    def search_movies(self, search_term, top_k=20):
        """
        Search movies by matching search_term in cleaned title (case-insensitive).
        Returns up to top_k matching movies with basic info.
        """
        matches = self.movies[self.movies['clean_title'].str.contains(search_term, case=False, na=False)]
        results = []
        for _, movie in matches.head(top_k).iterrows():
            results.append({
                'movieId': movie['movieId'],
                'title': movie['clean_title'],
                'year': movie.get('year', 'Unknown'),
                'genres': movie.get('genres_list', []),
                'avg_rating': movie.get('avg_rating', 0),
            })
        return results

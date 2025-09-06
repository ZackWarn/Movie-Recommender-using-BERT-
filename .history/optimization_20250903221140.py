# optimization.py
import faiss
import numpy as np

class OptimizedRecommendationEngine:
    def __init__(self, bert_processor):
        self.bert_processor = bert_processor
        self.embeddings = bert_processor.movie_embeddings
        self.movies = bert_processor.movies_data
        
        # Build FAISS index for fast similarity search
        self.index = faiss.IndexFlatIP(self.embeddings.shape[1])  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        normalized_embeddings = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        self.index.add(normalized_embeddings.astype('float32'))
        
        print(f"FAISS index built with {self.index.ntotal} movies")
    
    def fast_recommend_by_query(self, query, top_k=10):
        """Fast recommendation using FAISS"""
        query_embedding = self.bert_processor.model.encode([query])
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Search with FAISS
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        recommendations = []
        for idx, score in zip(indices[0], scores[0]):
            movie = self.movies.iloc[idx]
            recommendations.append({
                'title': movie['clean_title'],
                'year': movie['year'],
                'similarity_score': float(score),
                'genres': movie['genres_list']
            })
        
        return recommendations

# bert_processor.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
import sys

class MovieBERTProcessor:
    def __init__(self, model_name='all-MiniLM-L6-v2', force_tfidf=False):
        # Try to load BERT model, fallback to TF-IDF if not available
        self.use_tfidf = force_tfidf
        
        if not force_tfidf:
            # Try to check if we can access model files offline first
            try:
                import transformers
                # Set offline mode to avoid hanging on downloads
                os.environ['TRANSFORMERS_OFFLINE'] = '1'
                os.environ['HF_HUB_OFFLINE'] = '1'
                
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(model_name)
                print("✅ Using BERT-based embeddings (sentence-transformers)")
            except Exception as e:
                print(f"⚠️  BERT model not available (offline mode or missing model)")
                print(f"   Error: {str(e)[:150]}")
                print("✅ Falling back to TF-IDF embeddings")
                self.use_tfidf = True
        
        if self.use_tfidf:
            self.model = TfidfVectorizer(max_features=384, ngram_range=(1, 2), min_df=1)
            print("✅ Using TF-IDF vectorizer for embeddings")
        
        self.movie_embeddings = None
        self.movies_data = None
    
    def prepare_movie_texts(self, movies_df):
        """Combine movie information into text descriptions"""
        movie_texts = []
        
        for idx, movie in movies_df.iterrows():
            # Create comprehensive movie description
            text_parts = [
                f"Title: {movie['clean_title']}",
                f"Genres: {', '.join(movie['genres_list']) if movie['genres_list'] != ['(no genres listed)'] else 'Unknown'}",
                f"Year: {movie['year'] if pd.notna(movie['year']) else 'Unknown'}",
                f"Rating: {movie['avg_rating']:.1f}/5.0 ({movie['rating_count']} reviews)",
            ]
            
            # Add tags if available
            if movie['combined_tags']:
                tags = [str(tag) for tag in movie['combined_tags'] if pd.notna(tag)]
                text_parts.append(f"Tags: {', '.join(tags[:10])}")

            
            movie_texts.append('. '.join(text_parts))
        
        return movie_texts
    
    def generate_embeddings(self, movies_df):
        """Generate embeddings for all movies (BERT or TF-IDF based)"""
        print("Preparing movie texts...")
        movie_texts = self.prepare_movie_texts(movies_df)
        
        print(f"Generating embeddings for {len(movie_texts)} movies...")
        
        if self.use_tfidf:
            # Use TF-IDF for embeddings
            self.movie_embeddings = self.model.fit_transform(movie_texts).toarray()
            print(f"✅ TF-IDF embeddings generated ({self.movie_embeddings.shape})")
        else:
            # Generate BERT embeddings in batches to manage memory
            batch_size = 32
            embeddings = []
            
            for i in range(0, len(movie_texts), batch_size):
                batch = movie_texts[i:i + batch_size]
                batch_embeddings = self.model.encode(batch, show_progress_bar=False)
                embeddings.append(batch_embeddings)
                
                if (i // batch_size + 1) % 10 == 0:
                    print(f"Processed {i + len(batch)}/{len(movie_texts)} movies...")
            
            self.movie_embeddings = np.vstack(embeddings)
            print("✅ BERT embeddings generated successfully!")
        
        self.movies_data = movies_df.reset_index(drop=True)
        return self.movie_embeddings
    
    def save_embeddings(self, filepath='movie_embeddings.pkl'):
        """Save embeddings, movie data, and the model (if TF-IDF)"""
        data = {
            'embeddings': self.movie_embeddings,
            'movies_data': self.movies_data,
            'use_tfidf': self.use_tfidf
        }
        
        # Save the fitted TF-IDF model if using TF-IDF
        if self.use_tfidf:
            data['tfidf_model'] = self.model
        
        # Resolve path relative to this file if a relative path is provided
        resolved_path = (
            filepath if os.path.isabs(filepath)
            else os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        )
        with open(resolved_path, 'wb') as f:
            pickle.dump(data, f)
        print(f"Embeddings saved to {resolved_path}")
    
    def load_embeddings(self, filepath='movie_embeddings.pkl'):
        """Load pre-computed embeddings and model
        Looks for file at absolute path if provided; otherwise resolves relative to this file's directory.
        """
        # Try absolute path, otherwise resolve relative to this file's directory
        candidate_path = filepath if os.path.isabs(filepath) else os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        if not os.path.exists(candidate_path):
            # Fallback to current working directory if still not found
            alt_path = os.path.abspath(filepath)
            if os.path.exists(alt_path):
                candidate_path = alt_path
            else:
                raise FileNotFoundError(f"Embeddings file not found at '{filepath}' or '{candidate_path}'")

        with open(candidate_path, 'rb') as f:
            data = pickle.load(f)
        
        self.movie_embeddings = data['embeddings']
        self.movies_data = data['movies_data']
        
        # Load TF-IDF model if it was saved
        if 'use_tfidf' in data and data['use_tfidf']:
            self.use_tfidf = True
            if 'tfidf_model' in data:
                self.model = data['tfidf_model']
                print(f"Embeddings and TF-IDF model loaded successfully from {candidate_path}!")
            else:
                print(f"Embeddings loaded from {candidate_path} (TF-IDF model not found, creating new)")
                self.model = TfidfVectorizer(max_features=384, ngram_range=(1, 2), min_df=1)
        else:
            print(f"Embeddings loaded successfully from {candidate_path}!")

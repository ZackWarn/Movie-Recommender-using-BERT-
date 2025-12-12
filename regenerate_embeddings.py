"""
Regenerate embeddings for reduced dataset without loading BERT model.
Only applies PCA transformation to filtered movies.
"""
import pandas as pd
import pickle
import logging
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def regenerate_embeddings_for_reduced_dataset():
    """
    After dataset reduction, regenerate embeddings for the filtered movies.
    This uses the cached PCA transformer and doesn't reload BERT.
    """
    logger.info("Regenerating embeddings for reduced dataset...")
    
    # Load reduced movies
    movies_path = Path("movies_dataset/movies.csv")
    if not movies_path.exists():
        logger.error(f"Movies file not found: {movies_path}")
        return False
    
    movies_df = pd.read_csv(movies_path)
    logger.info(f"Loaded {len(movies_df)} movies from reduced dataset")
    
    # Load existing full embeddings (generated from original 16k movies)
    embeddings_path = Path("movie_embeddings.pkl")
    if not embeddings_path.exists():
        logger.warning(f"Embeddings file not found: {embeddings_path}")
        logger.info("This is expected on first Render deployment. Embeddings will be generated on first API request.")
        return True
    
    try:
        with open(embeddings_path, 'rb') as f:
            embeddings_data = pickle.load(f)
        logger.info(f"Loaded embeddings for {len(embeddings_data['movie_ids'])} movies")
        
        # Filter embeddings to only keep movies in reduced dataset
        original_movie_ids = set(embeddings_data['movie_ids'])
        reduced_movie_ids = set(movies_df['movieId'].astype(int).tolist())
        
        # Find movies in both datasets
        common_ids = original_movie_ids & reduced_movie_ids
        logger.info(f"Found {len(common_ids)} movies in both original and reduced datasets")
        
        if not common_ids:
            logger.warning("No common movies found between original and reduced datasets!")
            return False
        
        # Filter embeddings to match reduced dataset order
        movie_ids_filtered = []
        embeddings_filtered = []
        pca_embeddings_filtered = []
        
        for movie_id in movies_df['movieId'].astype(int):
            if movie_id in common_ids:
                idx = embeddings_data['movie_ids'].index(movie_id)
                movie_ids_filtered.append(movie_id)
                embeddings_filtered.append(embeddings_data['embeddings'][idx])
                pca_embeddings_filtered.append(embeddings_data['pca_embeddings'][idx])
        
        logger.info(f"Filtered to {len(movie_ids_filtered)} embeddings for reduced dataset")
        
        # Save filtered embeddings
        filtered_data = {
            'movie_ids': movie_ids_filtered,
            'embeddings': embeddings_filtered,
            'pca_embeddings': pca_embeddings_filtered,
            'pca_transformer': embeddings_data['pca_transformer']
        }
        
        with open(embeddings_path, 'wb') as f:
            pickle.dump(filtered_data, f)
        
        logger.info(f"Saved filtered embeddings ({len(movie_ids_filtered)} movies) to {embeddings_path}")
        
        # Save metadata
        metadata_path = Path("embeddings_metadata.json")
        metadata = {
            'total_movies': len(movie_ids_filtered),
            'embedding_dim': len(embeddings_filtered[0]) if embeddings_filtered else 0,
            'pca_dim': len(pca_embeddings_filtered[0]) if pca_embeddings_filtered else 0,
            'last_updated': pd.Timestamp.now().isoformat()
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Saved metadata to {metadata_path}")
        logger.info("✅ Embeddings successfully regenerated for reduced dataset")
        
        return True
        
    except Exception as e:
        logger.error(f"Error regenerating embeddings: {e}")
        logger.info("This is expected on first Render deployment. Embeddings will be generated on first API request.")
        return True  # Don't fail the build, embeddings will be generated on first request

if __name__ == "__main__":
    success = regenerate_embeddings_for_reduced_dataset()
    if success:
        logger.info("Embeddings regeneration complete")
    else:
        logger.error("Embeddings regeneration failed")
        exit(1)

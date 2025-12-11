#!/usr/bin/env python3
"""
Reduce dataset to top N movies by popularity and quality.
This helps fit within Render's memory limits while maintaining recommendation quality.
"""
import pandas as pd
import numpy as np
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reduce_dataset(target_movies=5000, min_ratings=50):
    """
    Reduce dataset to top N movies by popularity and quality.

    Strategy:
    1. Filter movies with at least min_ratings (removes obscure titles)
    2. Score by: rating_count * avg_rating (popularity × quality)
    3. Keep top N movies
    4. Update both movies.csv and ratings.csv

    Args:
        target_movies: Number of movies to keep (default: 5000)
        min_ratings: Minimum number of ratings required (default: 50)
    """
    logger.info(f"Starting dataset reduction to {target_movies} movies...")

    # Load data
    movies_path = "movies_dataset/movies.csv"
    ratings_path = "movies_dataset/ratings.csv"

    movies = pd.read_csv(movies_path)
    ratings = pd.read_csv(ratings_path)

    logger.info(f"Original dataset: {len(movies):,} movies, {len(ratings):,} ratings")

    # Calculate movie statistics
    movie_stats = ratings.groupby("movieId").agg({"rating": ["count", "mean"]})
    movie_stats.columns = ["rating_count", "avg_rating"]

    # Filter: minimum rating threshold
    qualified_movies = movie_stats[movie_stats["rating_count"] >= min_ratings].copy()
    logger.info(f"Movies with ≥{min_ratings} ratings: {len(qualified_movies):,}")

    # Score movies: popularity × quality
    qualified_movies["score"] = (
        qualified_movies["rating_count"] * qualified_movies["avg_rating"]
    )

    # Select top N movies
    top_movies = qualified_movies.nlargest(target_movies, "score")

    # Filter datasets
    movies_filtered = movies[movies["movieId"].isin(top_movies.index)].copy()
    ratings_filtered = ratings[ratings["movieId"].isin(top_movies.index)].copy()

    # Save filtered datasets
    movies_filtered.to_csv(movies_path, index=False)
    ratings_filtered.to_csv(ratings_path, index=False)

    # Log statistics
    logger.info(f"\n{'='*60}")
    logger.info(f"Dataset Reduction Complete!")
    logger.info(f"{'='*60}")
    logger.info(
        f"Movies: {len(movies):,} → {len(movies_filtered):,} ({len(movies_filtered)/len(movies)*100:.1f}%)"
    )
    logger.info(
        f"Ratings: {len(ratings):,} → {len(ratings_filtered):,} ({len(ratings_filtered)/len(ratings)*100:.1f}%)"
    )
    logger.info(
        f"Average ratings per movie: {len(ratings_filtered)/len(movies_filtered):.1f}"
    )
    logger.info(f"Average rating: {ratings_filtered['rating'].mean():.2f}")
    logger.info(f"{'='*60}\n")

    # Show sample of kept movies
    logger.info("Sample of top movies kept:")
    sample = movies_filtered.merge(
        top_movies[["score", "rating_count", "avg_rating"]],
        left_on="movieId",
        right_index=True,
    )
    logger.info(
        "\n"
        + sample.nlargest(10, "score")[
            ["title", "rating_count", "avg_rating"]
        ].to_string(index=False)
    )

    return movies_filtered, ratings_filtered


if __name__ == "__main__":
    try:
        # Reduce to 5k movies
        reduce_dataset(target_movies=5000, min_ratings=50)

        # Regenerate embeddings with reduced dataset
        logger.info("\n" + "=" * 60)
        logger.info("Next step: Regenerate embeddings")
        logger.info("=" * 60)
        logger.info("Run: python main.py")
        logger.info("This will create new embeddings for the reduced dataset.")

        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to reduce dataset: {e}", exc_info=True)
        sys.exit(1)

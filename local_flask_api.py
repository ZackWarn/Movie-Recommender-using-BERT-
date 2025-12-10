"""
Lightweight local development Flask API for testing
Minimal dependencies compared to production flask_api.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import json
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(
    app, origins="*", allow_headers=["Content-Type"], methods=["GET", "POST", "OPTIONS"]
)

# Try to import the real recommendation engine, but gracefully degrade
try:
    from rec_engine import MovieRecommendationEngine
    from bert_processor import MovieBERTProcessor

    REAL_ENGINE_AVAILABLE = True
except Exception as e:
    logger.warning(f"Could not load real engine: {e}. Using mock responses.")
    REAL_ENGINE_AVAILABLE = False

engine = None


def get_engine():
    """Get or create the recommendation engine (lazy loading)"""
    global engine
    if engine is None and REAL_ENGINE_AVAILABLE:
        try:
            logger.info("Initializing recommendation engine...")
            bert_processor = MovieBERTProcessor(lazy_load=True)
            engine = MovieRecommendationEngine(bert_processor, use_imdb=False)
            logger.info("Engine ready")
        except Exception as e:
            logger.error(f"Failed to initialize recommendation engine: {e}")
            REAL_ENGINE_AVAILABLE = False
    return engine


def mock_recommendations(query, top_k=3):
    """Return mock movie recommendations for testing"""
    mock_db = {
        "inception": [
            {
                "movieId": 79132,
                "title": "Inception",
                "year": 2010,
                "genres": ["Action", "Sci-Fi"],
                "avg_rating": 4.18,
                "similarity_score": 0.98,
            },
            {
                "movieId": 62,
                "title": "The Matrix",
                "year": 1999,
                "genres": ["Action", "Sci-Fi"],
                "avg_rating": 4.26,
                "similarity_score": 0.85,
            },
            {
                "movieId": 47,
                "title": "Seven Samurai",
                "year": 1954,
                "genres": ["Action", "Drama"],
                "avg_rating": 4.42,
                "similarity_score": 0.72,
            },
        ],
        "batman": [
            {
                "movieId": 155,
                "title": "The Dark Knight",
                "year": 2008,
                "genres": ["Action", "Crime"],
                "avg_rating": 4.51,
                "similarity_score": 0.95,
            },
            {
                "movieId": 289,
                "title": "Batman Forever",
                "year": 1995,
                "genres": ["Action", "Crime"],
                "avg_rating": 3.12,
                "similarity_score": 0.88,
            },
            {
                "movieId": 290,
                "title": "Batman & Robin",
                "year": 1997,
                "genres": ["Action", "Comedy"],
                "avg_rating": 2.95,
                "similarity_score": 0.81,
            },
        ],
        "default": [
            {
                "movieId": 1,
                "title": "Toy Story",
                "year": 1995,
                "genres": ["Animation", "Comedy"],
                "avg_rating": 4.15,
                "similarity_score": 0.75,
            },
            {
                "movieId": 2,
                "title": "Jumanji",
                "year": 1995,
                "genres": ["Adventure", "Comedy"],
                "avg_rating": 3.91,
                "similarity_score": 0.70,
            },
            {
                "movieId": 3,
                "title": "Grumpier Old Men",
                "year": 1995,
                "genres": ["Comedy", "Romance"],
                "avg_rating": 3.34,
                "similarity_score": 0.65,
            },
        ],
    }
    key = query.lower().strip()
    results = mock_db.get(key, mock_db["default"])
    return results[:top_k]


@app.route("/api/recommendations/query", methods=["POST"])
def get_recommendations():
    """Get movie recommendations based on query"""
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        top_k = data.get("top_k", 5)

        if not query:
            return jsonify({"error": "Query is required"}), 400

        if REAL_ENGINE_AVAILABLE:
            engine = get_engine()
            if engine:
                results = engine.get_recommendations_for_query(query, top_k)
                return jsonify(
                    {"success": True, "recommendations": results, "count": len(results)}
                )

        # Fall back to mock
        logger.info(f"Using mock recommendations for: {query}")
        results = mock_recommendations(query, top_k)
        return jsonify(
            {"success": True, "recommendations": results, "count": len(results)}
        )

    except Exception as e:
        logger.error(f"Error in recommendations: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/movies/search", methods=["POST"])
def search_movies():
    """Search movies by title"""
    try:
        data = request.get_json()
        search_term = data.get("search_term", "").strip()
        top_k = data.get("top_k", 20)

        if not search_term:
            return jsonify({"error": "Search term is required"}), 400

        if REAL_ENGINE_AVAILABLE:
            engine = get_engine()
            if engine:
                results = engine.search_movies(search_term, top_k)
                return jsonify(
                    {"success": True, "movies": results, "count": len(results)}
                )

        # Mock search
        logger.info(f"Mock search for: {search_term}")
        return jsonify({"success": True, "movies": [], "count": 0})

    except Exception as e:
        logger.error(f"Error in search: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "ok",
            "engine_available": REAL_ENGINE_AVAILABLE,
            "mode": "production" if REAL_ENGINE_AVAILABLE else "mock",
        }
    )


if __name__ == "__main__":
    logger.info("Starting local development API...")
    logger.info(f"Engine mode: {'PRODUCTION' if REAL_ENGINE_AVAILABLE else 'MOCK'}")
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True)

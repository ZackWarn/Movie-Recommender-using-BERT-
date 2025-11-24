from flask import Flask, request, jsonify
from flask_cors import CORS
from rec_engine import MovieRecommendationEngine
from bert_processor import MovieBERTProcessor
from config import Config
import logging
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Allow CORS from local dev and production domains
CORS(
    app,
    origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        "https://movie-recommender-using-bert.onrender.com",
    ],
    supports_credentials=True,
)

# Global variables for caching
engine = None


def get_engine():
    """Get or create the recommendation engine"""
    global engine
    if engine is None:
        try:
            bert_processor = MovieBERTProcessor()
            bert_processor.load_embeddings()
            engine = MovieRecommendationEngine(bert_processor, use_imdb=False)
            logger.info("Recommendation engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize recommendation engine: {e}")
            raise
    return engine


def _to_native(value):
    """Convert numpy/pandas scalar types to native Python types for JSON serialization."""
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if value is None:
        return None
    try:
        # Handle NaN
        if np.isnan(value):
            return None
    except Exception:
        pass
    return value


def _normalize(obj):
    """Recursively normalize dicts/lists to be JSON serializable."""
    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_normalize(v) for v in obj]
    return _to_native(obj)


@app.route("/", methods=["GET"])
def index():
    """Root endpoint - API status"""
    return jsonify({
        "service": "Movie Recommendation API",
        "status": "running",
        "version": "1.0",
        "endpoints": {
            "health": "/api/health",
            "recommendations": "/api/recommendations/query",
            "similar": "/api/recommendations/similar",
            "search": "/api/search"
        }
    })


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "imdb_available": Config.validate_config()})


@app.route("/api/recommendations/query", methods=["POST"])
def get_recommendations_by_query():
    """Get recommendations based on natural language query"""
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        top_k = data.get("top_k", 10)

        if not query:
            return jsonify({"error": "Query is required"}), 400

        engine = get_engine()

        # Use local recommendations only (IMDb disabled per request)
        recommendations = engine.recommend_by_query(query, top_k)

        return jsonify(
            {
                "success": True,
                "recommendations": _normalize(recommendations),
                "count": len(recommendations),
            }
        )

    except Exception as e:
        logger.error(f"Error in query recommendations: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/recommendations/similar", methods=["POST"])
def get_similar_movies():
    """Get similar movies based on movie ID"""
    try:
        data = request.get_json()
        movie_id = data.get("movie_id")
        top_k = data.get("top_k", 10)

        if not movie_id:
            return jsonify({"error": "Movie ID is required"}), 400

        engine = get_engine()

        # Use local recommendations only (IMDb disabled per request)
        recommendations = engine.recommend_similar_movies(movie_id, top_k)

        return jsonify(
            {
                "success": True,
                "recommendations": _normalize(recommendations),
                "count": len(recommendations),
            }
        )

    except Exception as e:
        logger.error(f"Error in similar movies: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/search", methods=["POST"])
def search_movies():
    """Search movies by title or keyword"""
    try:
        data = request.get_json()
        search_term = data.get("search_term", "").strip()
        top_k = data.get("top_k", 20)

        if not search_term:
            return jsonify({"error": "Search term is required"}), 400

        engine = get_engine()

        # Use local search only (IMDb disabled per request)
        results = engine.search_movies(search_term, top_k)

        return jsonify(
            {"success": True, "movies": _normalize(results), "count": len(results)}
        )

    except Exception as e:
        logger.error(f"Error in movie search: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/imdb/search", methods=["POST"])
def search_imdb_movies():
    return jsonify({"error": "IMDB features disabled"}), 400


@app.route("/api/imdb/trending", methods=["GET"])
def get_trending_movies():
    return jsonify({"error": "IMDB features disabled"}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Check configuration
    if not Config.validate_config():
        logger.warning("IMDB API key not configured. Some features will be disabled.")

    # Use debug=False for production-like behavior, avoiding reload issues
    app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)

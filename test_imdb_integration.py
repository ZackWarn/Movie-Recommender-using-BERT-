#!/usr/bin/env python3
"""
Test script for IMDB integration
This script tests the IMDB service and recommendation engine integration
"""

import os
import sys
from imdb_service import IMDBService
from config import Config

def test_imdb_service():
    """Test the IMDB service functionality"""
    print("🧪 Testing IMDB Service Integration")
    print("=" * 40)
    
    # Check if API key is configured
    if not Config.validate_config():
        print("❌ IMDB API key not configured")
        print("Please run: python setup_imdb.py")
        return False
    
    try:
        # Initialize IMDB service
        print("🔧 Initializing IMDB service...")
        service = IMDBService(Config.RAPIDAPI_IMDB_KEY)
        print("✅ IMDB service initialized")
        
        # Test movie search
        print("\n🔍 Testing movie search...")
        search_results = service.search_movies("The Matrix", limit=3)
        if search_results:
            print(f"✅ Found {len(search_results)} movies")
            for movie in search_results:
                print(f"   - {movie['title']} ({movie.get('year', 'N/A')})")
        else:
            print("❌ No movies found")
            return False
        
        # Test movie details
        if search_results:
            print("\n📋 Testing movie details...")
            movie_id = search_results[0]['imdb_id']
            details = service.get_movie_details(movie_id)
            if details:
                print("✅ Movie details retrieved")
                print(f"   - Title: {details['title']}")
                print(f"   - Rating: {details.get('rating', 'N/A')}/10")
                print(f"   - Genres: {', '.join(details.get('genres', []))}")
                print(f"   - Has poster: {'Yes' if details.get('image_url') else 'No'}")
            else:
                print("❌ Failed to get movie details")
                return False
        
        print("\n✅ All IMDB service tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing IMDB service: {e}")
        return False

def test_recommendation_engine():
    """Test the recommendation engine with IMDB integration"""
    print("\n🎯 Testing Recommendation Engine with IMDB")
    print("=" * 40)
    
    try:
        from rec_engine import MovieRecommendationEngine
        from bert_processor import MovieBERTProcessor
        
        print("🔧 Loading recommendation engine...")
        bert_processor = MovieBERTProcessor()
        bert_processor.load_embeddings()
        engine = MovieRecommendationEngine(bert_processor, use_imdb=True)
        print("✅ Recommendation engine loaded")
        
        # Test query recommendations with IMDB
        print("\n🔍 Testing query recommendations with IMDB...")
        recommendations = engine.recommend_by_query_with_imdb("action movies", top_k=3)
        
        if recommendations:
            print(f"✅ Found {len(recommendations)} recommendations")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec['title']} ({rec.get('year', 'N/A')})")
                if rec.get('imdb_rating'):
                    print(f"      IMDB Rating: {rec['imdb_rating']}/10")
                if rec.get('poster_url'):
                    print(f"      Has poster: Yes")
        else:
            print("❌ No recommendations found")
            return False
        
        print("\n✅ Recommendation engine tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing recommendation engine: {e}")
        return False

def main():
    """Run all tests"""
    print("🎬 KnowMovies IMDB Integration Test Suite")
    print("=" * 50)
    
    # Test IMDB service
    imdb_success = test_imdb_service()
    
    # Test recommendation engine
    rec_success = test_recommendation_engine()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"IMDB Service: {'✅ PASS' if imdb_success else '❌ FAIL'}")
    print(f"Recommendation Engine: {'✅ PASS' if rec_success else '❌ FAIL'}")
    
    if imdb_success and rec_success:
        print("\n🎉 All tests passed! IMDB integration is working correctly.")
        print("\nYou can now run:")
        print("   - Streamlit: streamlit run app.py")
        print("   - Flask API: python flask_api.py")
        print("   - Next.js: npm run dev")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()

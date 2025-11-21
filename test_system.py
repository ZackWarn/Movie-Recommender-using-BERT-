#!/usr/bin/env python3
"""
Test script to verify the Movie Recommender System is working correctly
"""

import sys
import os
import traceback

def test_imports():
    """Test that all required imports work"""
    print("🧪 Testing imports...")
    try:
        import pandas as pd
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer
        import streamlit
        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_dataset():
    """Test that dataset files exist"""
    print("\n🧪 Testing dataset...")
    required_files = [
        'movies_dataset/movies.csv',
        'movies_dataset/ratings.csv',
        'movies_dataset/tags.csv',
        'movies_dataset/genome-scores.csv',
        'movies_dataset/genome-tags.csv'
    ]
    
    all_exist = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"  ✅ {filepath}")
        else:
            print(f"  ❌ {filepath} not found")
            all_exist = False
    
    return all_exist

def test_embeddings():
    """Test that embeddings file exists"""
    print("\n🧪 Testing embeddings...")
    if os.path.exists('movie_embeddings.pkl'):
        print("  ✅ movie_embeddings.pkl exists")
        return True
    else:
        print("  ❌ movie_embeddings.pkl not found")
        return False

def test_recommendation_engine():
    """Test that the recommendation engine works"""
    print("\n🧪 Testing recommendation engine...")
    try:
        from bert_processor import MovieBERTProcessor
        from rec_engine import MovieRecommendationEngine
        
        # Load processor
        processor = MovieBERTProcessor(force_tfidf=True)
        processor.load_embeddings()
        print("  ✅ Embeddings loaded")
        
        # Create engine
        engine = MovieRecommendationEngine(processor, use_imdb=False)
        print("  ✅ Engine created")
        
        # Test query-based recommendations
        query = "action sci-fi movies"
        recs = engine.recommend_by_query(query, top_k=3)
        if recs and len(recs) > 0:
            print(f"  ✅ Query recommendations work ({len(recs)} results)")
            print(f"     Top result: {recs[0]['title']}")
        else:
            print("  ❌ Query recommendations failed")
            return False
        
        # Test similar movies
        movie_id = processor.movies_data.iloc[0]['movieId']
        similar = engine.recommend_similar_movies(movie_id, top_k=3)
        if similar and len(similar) > 0:
            print(f"  ✅ Similar movie recommendations work ({len(similar)} results)")
        else:
            print("  ❌ Similar movie recommendations failed")
            return False
        
        # Test search
        search_results = engine.search_movies("matrix", top_k=3)
        if search_results:
            print(f"  ✅ Movie search works ({len(search_results)} results)")
        else:
            print("  ⚠️  Movie search returned no results (may be normal)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        traceback.print_exc()
        return False

def test_streamlit_app():
    """Test that Streamlit can load the app"""
    print("\n🧪 Testing Streamlit app...")
    try:
        # Just check if the app file exists and is valid Python
        with open('app.py', 'r') as f:
            code = f.read()
        compile(code, 'app.py', 'exec')
        print("  ✅ app.py is valid Python")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🎬 Movie Recommender System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Dataset", test_dataset),
        ("Embeddings", test_embeddings),
        ("Recommendation Engine", test_recommendation_engine),
        ("Streamlit App", test_streamlit_app),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready to use.")
        print("\n🚀 To run the application:")
        print("   streamlit run app.py")
        print("\n   Or use the convenience script:")
        print("   ./run_app.sh")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

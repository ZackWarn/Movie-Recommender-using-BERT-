#!/usr/bin/env python3
"""
Setup script for IMDB API integration
This script helps you configure the RapidAPI IMDB API key
"""

import os
import sys

def setup_imdb_api():
    """Setup IMDB API configuration"""
    print("🎬 IMDB API Setup for KnowMovies")
    print("=" * 40)
    
    print("\nTo use IMDB features, you need a RapidAPI IMDB API key.")
    print("1. Go to: https://rapidapi.com/rapidapi/api/imdb8")
    print("2. Subscribe to the IMDB8 API (free tier available)")
    print("3. Copy your API key")
    
    api_key = input("\nEnter your RapidAPI IMDB API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Create .env file
        env_content = f"""# RapidAPI IMDB API Configuration
RAPIDAPI_IMDB_KEY={api_key}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Next.js Configuration
NEXT_PUBLIC_API_URL=http://localhost:5000
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ API key saved to .env file")
        print("✅ IMDB features will be available")
    else:
        print("\n⚠️  No API key provided. IMDB features will be disabled.")
        print("You can add the key later by setting the RAPIDAPI_IMDB_KEY environment variable")
    
    print("\n🚀 Setup complete! You can now run:")
    print("   - Streamlit app: streamlit run app.py")
    print("   - Flask API: python flask_api.py")
    print("   - Next.js app: npm run dev")

if __name__ == "__main__":
    setup_imdb_api()

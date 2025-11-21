#!/bin/bash
# run_app.sh - Simple script to run the Movie Recommender application

echo "🎬 KnowMovies - Movie Recommender System"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  Dependencies not installed"
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi
echo "✅ Dependencies OK"

# Check if dataset exists
if [ ! -d "movies_dataset" ] || [ ! -f "movies_dataset/movies.csv" ]; then
    echo ""
    echo "📊 Dataset not found"
    echo "🎯 Creating sample dataset..."
    python3 create_sample_dataset.py
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create dataset"
        exit 1
    fi
fi
echo "✅ Dataset OK"

# Check if embeddings exist
if [ ! -f "movie_embeddings.pkl" ]; then
    echo ""
    echo "🧠 Embeddings not found"
    echo "⚙️  Generating embeddings (this may take a minute)..."
    python3 main.py
    if [ $? -ne 0 ]; then
        echo "❌ Failed to generate embeddings"
        exit 1
    fi
fi
echo "✅ Embeddings OK"

echo ""
echo "========================================"
echo "🚀 Starting Streamlit application..."
echo "========================================"
echo ""
echo "📱 The app will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Streamlit app
streamlit run app.py

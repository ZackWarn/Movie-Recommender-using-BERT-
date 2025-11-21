# 🚀 Quick Setup Guide

This guide will help you get the Movie Recommender System up and running quickly.

## Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (usually comes with Python)
- **(Optional) Node.js 16+** - Only needed for the Next.js frontend

## 🎯 Quick Start (Recommended)

The easiest way to run the application is using the automated setup script:

```bash
# Make the script executable (Linux/Mac)
chmod +x run_app.sh

# Run the application
./run_app.sh
```

The script will automatically:
1. Check for Python dependencies
2. Install dependencies if needed
3. Create sample dataset if not present
4. Generate embeddings if not present
5. Start the Streamlit application

**The app will be available at:** http://localhost:8501

## 📋 Manual Setup

If you prefer to set things up manually, follow these steps:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Prepare the Dataset

Choose one of these options:

#### Option A: Use Sample Dataset (Quick - Recommended for Testing)
```bash
python create_sample_dataset.py
```

This creates a small dataset with 40 popular movies. Perfect for testing and demos.

#### Option B: Download Full MovieLens Dataset (Internet Required)
```bash
python download_dataset.py
```

This downloads the full MovieLens 25M dataset (~250MB). **Note:** Requires internet connection.

### Step 3: Generate Embeddings

```bash
python main.py
```

This processes the movie data and generates embeddings for recommendations. Takes about 1-2 minutes for the sample dataset.

### Step 4: Run the Application

#### Option A: Streamlit App (Recommended)
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

#### Option B: Flask API + Next.js Frontend
```bash
# Terminal 1: Start Flask API
python flask_api.py

# Terminal 2: Install Node dependencies and start Next.js
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

## 🎬 Using the Application

### Streamlit Interface

1. **Natural Language Search**: Enter queries like:
   - "action movies with time travel"
   - "romantic comedies from the 90s"
   - "dark psychological thrillers"

2. **Find Similar Movies**: Search for a movie title and get similar recommendations

3. **Browse Movies**: Explore the movie database

### Features Available

- ✅ Natural language movie recommendations
- ✅ Similar movie discovery
- ✅ Smart search with fuzzy matching
- ✅ Movie ratings and genre information
- ⚠️ IMDB integration (requires API key - see below)

## 🔑 Optional: IMDB Integration

To enable movie posters and IMDB ratings:

1. Get a free API key from [RapidAPI IMDB8](https://rapidapi.com/rapidapi/api/imdb8)

2. Run the setup script:
   ```bash
   python setup_imdb.py
   ```

3. Or manually set the environment variable:
   ```bash
   export RAPIDAPI_IMDB_KEY="your_api_key_here"
   ```

## 🐛 Troubleshooting

### Issue: Dependencies won't install
**Solution:** Make sure you have Python 3.8+ installed:
```bash
python3 --version
```

### Issue: "Module not found" errors
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Embeddings file not found"
**Solution:** Generate embeddings:
```bash
python main.py
```

### Issue: Port 8501 already in use
**Solution:** Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Slow performance
**Solution:** The sample dataset is small and should be fast. For the full dataset, ensure you have enough RAM (8GB+ recommended).

## 🔧 Technical Details

### Embedding Methods

The system supports two embedding methods:

1. **BERT** (sentence-transformers) - Best quality, requires internet to download model first time
2. **TF-IDF** (scikit-learn) - Fallback method, works offline

The system automatically uses TF-IDF if BERT models aren't available.

### Dataset Structure

The application expects these CSV files in `movies_dataset/`:
- `movies.csv` - Movie titles, genres, years
- `ratings.csv` - User ratings
- `tags.csv` - User-generated tags
- `genome-scores.csv` - Tag relevance scores
- `genome-tags.csv` - Tag vocabulary

## 📚 Next Steps

- Read the [main README](README.md) for detailed features and architecture
- Check [README_IMDB.md](README_IMDB.md) for IMDB integration details
- Explore the API documentation in the Flask endpoints

## 🤝 Need Help?

1. Check the troubleshooting section above
2. Review the main README.md
3. Check existing GitHub issues
4. Open a new issue with details about your problem

---

**Happy Movie Discovering! 🍿✨**

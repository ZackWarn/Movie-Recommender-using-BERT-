# 🎬 KnowMovies - AI-Powered Movie Recommendation System

A sophisticated movie recommendation system that combines BERT-based natural language processing with IMDB integration to provide personalized movie suggestions with rich visual and rating data.

## ✨ Features

### 🤖 AI-Powered Recommendations
- **Natural Language Queries**: Describe what you want to watch in plain English
- **BERT-Based Similarity**: Advanced semantic understanding using DistilBERT
- **Similar Movie Discovery**: Find movies similar to ones you love
- **Smart Search**: Intelligent movie search with fuzzy matching

### 🎭 IMDB Integration
- **Movie Posters**: High-quality posters for visual appeal
- **IMDB Ratings**: Real-time ratings and vote counts
- **Rich Details**: Plot summaries, cast information, runtime, genres
- **Trending Movies**: Discover what's popular right now
- **Direct IMDB Links**: Easy access to full movie pages

### 🎨 Multiple Interfaces
- **Streamlit App**: Full-featured web interface with all capabilities
- **Next.js Frontend**: Modern, responsive web application
- **Flask API**: RESTful API for custom integrations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- RapidAPI IMDB API key (free tier available)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd cinematch
```

### 2. Install Dependencies
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
npm install
```

### 3. Configure IMDB API
```bash
# Run the setup script
python setup_imdb.py

# Or manually set environment variable
export RAPIDAPI_IMDB_KEY="your_api_key_here"
```

### 4. Prepare Data (First Time Only)
```bash
# Generate movie embeddings
python main.py
```

### 5. Run Applications

#### Option A: Streamlit App (Recommended)
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501)

#### Option B: Next.js + Flask API
```bash
# Terminal 1: Start Flask API
python flask_api.py

# Terminal 2: Start Next.js frontend
npm run dev
```
Open [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
cinematch/
├── src/                          # Next.js frontend
│   ├── app/
│   │   ├── page.tsx             # Main page
│   │   └── layout.tsx           # App layout
│   └── components/
│       └── MovieCard.tsx        # Movie card component
├── movies_dataset/              # Movie data files
├── app.py                       # Streamlit application
├── flask_api.py                 # Flask REST API
├── main.py                      # Data processing script
├── rec_engine.py                # Recommendation engine
├── bert_processor.py            # BERT model processor
├── imdb_service.py              # IMDB API integration
├── config.py                    # Configuration management
├── setup_imdb.py                # IMDB setup script
└── test_imdb_integration.py     # Integration tests
```

## 🔧 Configuration

### Environment Variables
```bash
RAPIDAPI_IMDB_KEY=your_api_key_here    # Required for IMDB features
FLASK_ENV=development                   # Flask environment
NEXT_PUBLIC_API_URL=http://localhost:5000  # API URL for frontend
```

### API Endpoints
- `GET /api/health` - Health check
- `POST /api/recommendations/query` - Get recommendations by query
- `POST /api/recommendations/similar` - Get similar movies
- `POST /api/search` - Search movies
- `POST /api/imdb/search` - Direct IMDB search
- `GET /api/imdb/trending` - Get trending movies

## 🧪 Testing

```bash
# Test IMDB integration
python test_imdb_integration.py

# Test individual components
python -c "from imdb_service import IMDBService; print('IMDB service OK')"
python -c "from rec_engine import MovieRecommendationEngine; print('Recommendation engine OK')"
```

## 📊 Usage Examples

### Natural Language Queries
- "romantic comedies from the 90s"
- "action movies with time travel"
- "sci-fi films with great soundtracks"
- "dark psychological thrillers"

### Similar Movies
- Search for "The Matrix" → Get similar sci-fi action films
- Search for "Inception" → Find mind-bending movies
- Search for "Pulp Fiction" → Discover similar crime dramas

### IMDB Features
- Browse trending movies
- Search IMDB database directly
- View detailed movie information
- Access high-quality posters

## 🛠️ Technical Details

### AI/ML Stack
- **BERT**: DistilBERT for semantic understanding
- **Scikit-learn**: Cosine similarity for recommendations
- **Pandas**: Data manipulation and processing
- **NumPy**: Numerical computations

### Web Stack
- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Flask, Streamlit
- **API**: RapidAPI IMDB8

### Data Processing
- Movie metadata from MovieLens dataset
- BERT embeddings for semantic similarity
- IMDB data enrichment for visual appeal

## 🚨 Troubleshooting

### Common Issues

1. **No IMDB Data**
   - Check API key configuration
   - Verify internet connection
   - Check API rate limits

2. **Recommendations Not Working**
   - Ensure embeddings are generated (`python main.py`)
   - Check data files in `movies_dataset/`
   - Verify BERT model downloads

3. **Frontend Not Loading**
   - Check Flask API is running
   - Verify CORS configuration
   - Check browser console for errors

### Debug Mode
```bash
# Enable detailed logging
export FLASK_DEBUG=True
python flask_api.py
```

## 📈 Performance

- **Caching**: Streamlit caches recommendations
- **Rate Limiting**: IMDB API calls are rate-limited
- **Optimization**: Next.js Image component for posters
- **Fallbacks**: Graceful degradation without IMDB

## 🔮 Future Enhancements

- User authentication and profiles
- Personalized watchlists
- Social features and sharing
- Movie trailer integration
- Advanced filtering options
- Mobile app development

## 📝 License

This project uses the RapidAPI IMDB8 API. Please review their terms of service before production use.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the [IMDB Integration Guide](README_IMDB.md)
3. Open an issue on GitHub

---

**Happy Movie Discovery! 🍿✨**

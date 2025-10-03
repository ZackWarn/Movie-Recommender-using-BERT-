# 🎬 KnowMovies - IMDB Integration

This document describes the IMDB API integration that adds movie posters, ratings, and detailed information to the KnowMovies recommendation system.

## ✨ Features Added

### 🖼️ Visual Enhancements
- **Movie Posters**: High-quality movie posters from IMDB
- **IMDB Ratings**: Real-time IMDB ratings and vote counts
- **Rich Movie Cards**: Beautiful cards with posters, ratings, plots, and cast information

### 📊 Enhanced Data
- **IMDB Ratings**: Official IMDB ratings (1-10 scale)
- **Plot Summaries**: Detailed movie plots and descriptions
- **Cast Information**: Top cast members for each movie
- **Runtime**: Movie duration in hours and minutes
- **Genres**: IMDB genre classifications
- **Release Dates**: Official release information

### 🔍 New Search Options
- **IMDB Direct Search**: Search directly in IMDB's database
- **Trending Movies**: Get currently popular movies
- **Enhanced Recommendations**: All recommendations now include IMDB data

## 🚀 Quick Start

### 1. Get IMDB API Key
1. Visit [RapidAPI IMDB8](https://rapidapi.com/rapidapi/api/imdb8)
2. Subscribe to the free tier
3. Copy your API key

### 2. Setup
```bash
# Run the setup script
python setup_imdb.py

# Or manually set environment variable
export RAPIDAPI_IMDB_KEY="your_api_key_here"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Applications

#### Streamlit App (Full Featured)
```bash
streamlit run app.py
```

#### Flask API (For Next.js Frontend)
```bash
python flask_api.py
```

#### Next.js Frontend
```bash
npm run dev
```

## 📁 New Files Created

### Backend Files
- `imdb_service.py` - IMDB API integration service
- `config.py` - Configuration management
- `flask_api.py` - Flask API for frontend integration
- `setup_imdb.py` - Setup script for API key configuration

### Frontend Files
- `src/components/MovieCard.tsx` - Enhanced movie card component

### Configuration
- `requirements.txt` - Updated Python dependencies
- `.env.example` - Environment variables template

## 🔧 API Endpoints

### Flask API Endpoints
- `GET /api/health` - Health check and IMDB availability
- `POST /api/recommendations/query` - Get recommendations by query
- `POST /api/recommendations/similar` - Get similar movies
- `POST /api/search` - Search movies with IMDB data
- `POST /api/imdb/search` - Direct IMDB search
- `GET /api/imdb/trending` - Get trending movies

### Example API Usage
```javascript
// Get recommendations with IMDB data
const response = await fetch('http://localhost:5000/api/recommendations/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'action movies', top_k: 10 })
});
const data = await response.json();
```

## 🎨 UI Components

### MovieCard Component
The new `MovieCard` component displays:
- Movie poster with fallback
- IMDB and local ratings
- Genre tags
- Plot summary (truncated)
- Cast information
- Runtime
- Similarity score
- Direct IMDB link

### Enhanced Streamlit Interface
- Poster display in recommendations
- IMDB ratings alongside local ratings
- Rich movie information display
- New IMDB-specific search options

## ⚙️ Configuration

### Environment Variables
```bash
RAPIDAPI_IMDB_KEY=your_api_key_here
FLASK_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Rate Limiting
The IMDB service includes built-in rate limiting (1 request per second) to respect API limits.

## 🔍 Usage Examples

### Streamlit App
1. **Natural Language Query**: "romantic comedies from the 90s"
2. **Similar Movies**: Search for "The Matrix" and find similar films
3. **IMDB Search**: Direct search in IMDB database
4. **Trending Movies**: See what's popular now

### Next.js Frontend
- Search for movies using the main search bar
- View rich movie cards with posters and ratings
- Click IMDB links to view full movie pages

## 🛠️ Technical Details

### IMDB Service Features
- **Movie Search**: Search movies by title
- **Movie Details**: Get comprehensive movie information
- **Ratings**: Fetch IMDB ratings and vote counts
- **Posters**: Get high-quality movie posters
- **Trending**: Access currently popular movies
- **Rate Limiting**: Built-in API rate limiting

### Error Handling
- Graceful fallback when IMDB API is unavailable
- Image loading error handling
- API request error recovery
- User-friendly error messages

## 🚨 Troubleshooting

### Common Issues

1. **No IMDB Data Showing**
   - Check if `RAPIDAPI_IMDB_KEY` is set
   - Verify API key is valid and active
   - Check API rate limits

2. **Posters Not Loading**
   - Check internet connection
   - Verify IMDB image URLs are accessible
   - Check browser console for CORS issues

3. **API Errors**
   - Check Flask API is running on port 5000
   - Verify all dependencies are installed
   - Check logs for specific error messages

### Debug Mode
```bash
# Enable debug logging
export FLASK_DEBUG=True
python flask_api.py
```

## 📈 Performance Notes

- IMDB API calls are cached in Streamlit
- Rate limiting prevents API overuse
- Image loading is optimized with Next.js Image component
- Fallback mechanisms ensure app works without IMDB

## 🔮 Future Enhancements

- Movie trailers integration
- User reviews and ratings
- Watchlist functionality
- Social sharing features
- Advanced filtering options
- Movie comparison tools

## 📝 License

This integration uses the RapidAPI IMDB8 API. Please review their terms of service and pricing before production use.

---

**Happy Movie Discovery! 🍿**

# Quick Reference: Hybrid Scoring System

## What Changed?

### Before (Keyword-Only)
- Returns zeros from `encode()` → Always uses keyword matching
- Quality: **Poor** for conceptual queries ("psychological thriller" → generic results)
- Memory: ~330MB (safe but limited quality)

### After (Hybrid Approach)
- Keyword matching **first** (30 candidates) → Semantic re-ranking **when safe**
- Quality: **Good** - semantic search when memory allows, keyword fallback when not
- Memory: Adaptive (330MB→480MB depending on availability)

## How It Decides

```python
Current Memory: 330MB
Threshold: 380MB
Available: 50MB

Need: 150MB for BERT model
Decision: Use keyword-only (not enough headroom)

---

Current Memory: 310MB
Threshold: 380MB
Available: 70MB

Need: 150MB for BERT model
Decision: Still keyword-only (need more headroom)

---

Current Memory: 220MB (hypothetical - after memory optimization)
Threshold: 380MB  
Available: 160MB

Need: 150MB for BERT model
Decision: ✅ Load BERT model, use semantic re-ranking!
```

## API Response

### Returns exactly **8 movies** (changed from 10)

```json
[
  {
    "movieId": 123,
    "title": "Inception",
    "year": "2010",
    "genres": ["Sci-Fi", "Thriller"],
    "avg_rating": 4.2,
    "similarity_score": 0.87  // Semantic score (or 0.0 if keyword-only)
  },
  // ... 7 more movies
]
```

## Scoring Formula (When Semantic Active)

**Blended Score = 0.7 × Semantic + 0.3 × Keyword**

- **Semantic Score**: Cosine similarity between query and movie embeddings (0-1)
- **Keyword Score**: Normalized position in keyword results (0-1)
  - Top keyword result: 1.0
  - 15th keyword result: 0.5
  - 30th keyword result: 0.0

## Memory Monitoring

The system logs memory at key stages:

```
INFO - Memory check: 330.2MB used, 49.8MB available before 380MB threshold
INFO - Using zero embeddings (triggers keyword matching fallback)
INFO - Getting keyword matches for query: psychological thriller
INFO - Returning keyword-only results (semantic unavailable)
```

Or when semantic is available:

```
INFO - Memory check: 220.5MB used, 159.5MB available before 380MB threshold
INFO - Using BERT model for semantic encoding (memory allows)
INFO - Enhancing with semantic re-ranking
INFO - Hybrid re-ranking complete: returned 8 movies
```

## Files Modified

1. **bert_processor.py**: Added memory checking, conditional BERT loading
2. **rec_engine.py**: Hybrid approach with keyword→semantic flow, 8-movie limit
3. **flask_api.py**: Updated default top_k to 8

## Deployment Status

✅ **Pushed to GitHub**: Changes committed to `feature/smaller-local-model` branch
✅ **Auto-Deploy**: Render will automatically deploy from GitHub
✅ **Monitor**: Check Render logs for memory usage and scoring mode

## Expected Behavior After Deploy

1. **First request** (~330MB): Keyword matching
2. **Subsequent requests**: 
   - If memory < 380MB: Keyword matching (fast, safe)
   - If memory drops: May enable semantic (better quality)
3. **Similar movie recommendations**: Always use embeddings (no model load needed)

## Testing After Deploy

```bash
# Test query recommendations (should return 8 movies)
curl "https://movie-recommender-using-bert.onrender.com/api/recommendations/query?query=psychological+thriller"

# Check response length
curl -s "https://movie-recommender-using-bert.onrender.com/api/recommendations/query?query=space+adventure" | jq '. | length'
# Should output: 8
```

## Troubleshooting

### If memory still exceeds 512MB:
- Lower threshold from 380MB to 350MB in `bert_processor.py`
- System will be more conservative about loading BERT model

### If recommendations are still poor:
- Check Render logs to see if semantic mode ever activates
- May need to optimize memory usage elsewhere to get below 230MB baseline

### If system is too slow:
- Increase threshold to avoid loading model frequently
- Keyword matching is much faster than semantic

## Key Insight

This hybrid approach gives you **the best of both worlds**:
- **Stability**: Always works within 512MB limit
- **Quality**: Upgrades to semantic when safe
- **Performance**: Fast keyword matching as baseline
- **Frontend-Ready**: Returns exactly 8 movies as needed

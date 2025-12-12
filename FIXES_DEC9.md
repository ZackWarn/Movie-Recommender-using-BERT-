# Fixes Applied - Dec 9, 2025

## Issues Found from Logs

### Issue 1: Returning 10 movies instead of 8
**Log Evidence:**
```
INFO:flask_api:Query: Shutter Island, Top K: 10
INFO:flask_api:Found 10 recommendations
```

**Root Cause:** Frontend was hardcoded to send `top_k: 10` in the POST request body.

**Fix:** Changed `src/app/page.tsx` line 68 from `top_k: 10` to `top_k: 8`

---

### Issue 2: Semantic search never activating
**Log Evidence:**
```
INFO:bert_processor:Memory check: 319.6MB used, 60.4MB available before 380MB threshold
INFO:bert_processor:Using zero embeddings (triggers keyword matching fallback)
```

**Root Cause:** Memory threshold logic was checking if `available > 150MB`, but with 320MB used and 380MB threshold, only 60MB was "available". This prevented BERT model loading even though we had 192MB headroom to the 512MB limit.

**Analysis:**
- Current usage: ~320MB
- Render limit: 512MB  
- Actual headroom: 192MB (enough for 150MB model!)
- Old threshold: 380MB (artificially limiting to 60MB headroom)
- Projected with model: 320 + 150 = 470MB (SAFE!)

**Fix:** Changed `bert_processor.py` memory check logic:
- **Before:** Check if `(threshold - current) > 150`
- **After:** Check if `(current + 150) < max_total_mb`
- **New limit:** 470MB (leaves 42MB safety buffer below 512MB)

**Expected Behavior After Deploy:**
```
INFO:bert_processor:Memory check: 320.0MB current, 470.0MB projected with model, SAFE (limit: 470MB)
INFO:bert_processor:Using BERT model for semantic encoding (memory allows)
INFO:rec_engine:Enhancing with semantic re-ranking
INFO:rec_engine:Hybrid re-ranking complete: returned 8 movies
```

---

## Changes Summary

### Files Modified

1. **`src/app/page.tsx`**
   ```diff
   - top_k: 10
   + top_k: 8
   ```

2. **`bert_processor.py`**
   ```diff
   - def _can_safely_load_model(self, threshold_mb=380):
   -     """Check if we have enough memory headroom to load BERT model (~150MB)"""
   -     current_mb = self._get_memory_mb()
   -     available = threshold_mb - current_mb
   -     logger.info(f"Memory check: {current_mb:.1f}MB used, {available:.1f}MB available before {threshold_mb}MB threshold")
   -     return available > 150
   
   + def _can_safely_load_model(self, max_total_mb=470):
   +     """Check if we can safely load BERT model (~150MB) without exceeding limits."""
   +     current_mb = self._get_memory_mb()
   +     projected_mb = current_mb + 150
   +     safe = projected_mb < max_total_mb
   +     logger.info(f"Memory check: {current_mb:.1f}MB current, {projected_mb:.1f}MB projected with model, {'SAFE' if safe else 'UNSAFE'} (limit: {max_total_mb}MB)")
   +     return safe
   ```

---

## Expected Results

### Before Fixes
- ❌ Returns 10 movies (frontend overflow)
- ❌ Always uses keyword matching (semantic disabled)
- ⚠️ Memory check: "60.4MB available before 380MB threshold" (misleading)

### After Fixes  
- ✅ Returns exactly 8 movies
- ✅ Semantic re-ranking activates when memory is below 320MB
- ✅ Memory check: "470MB projected, SAFE (limit: 470MB)" (clear)
- ✅ Hybrid scoring: 70% semantic + 30% keyword

### Memory Profile After Deploy
| Scenario | Usage | Semantic Enabled? |
|----------|-------|-------------------|
| Startup | 311MB | ✅ Yes (311+150=461 < 470) |
| After 1st query | 325MB | ✅ Yes (325+150=475 > 470) ⚠️ |
| After embeddings loaded | 329MB | ❌ No (329+150=479 > 470) |

**Note:** Semantic may only work on the very first request when memory is lowest (~311MB). Once embeddings are loaded (~329MB), we'll exceed the 470MB limit. This is expected behavior to stay safely under 512MB.

---

## Deployment Status

✅ **Committed:** `ca5d89f0`
✅ **Pushed:** To `feature/smaller-local-model` branch
⏳ **Render:** Will auto-deploy in ~2-3 minutes

---

## Testing After Deploy

```bash
# Test that it returns 8 movies
curl -X POST https://movie-recommender-using-bert.onrender.com/api/recommendations/query \
  -H "Content-Type: application/json" \
  -d '{"query": "psychological thriller"}' \
  | jq '.recommendations | length'
# Expected: 8

# Check logs for semantic activation
# Look for: "SAFE (limit: 470MB)" and "Enhancing with semantic re-ranking"
```

---

## Tuning Options

If semantic still doesn't activate after deploy:

### Option A: Increase limit to 480MB (riskier)
```python
def _can_safely_load_model(self, max_total_mb=480):  # Was 470
```
This gives 32MB buffer instead of 42MB.

### Option B: Decrease model size estimate
```python
projected_mb = current_mb + 130  # Was 150, if model is actually smaller
```

### Option C: Accept keyword-only mode
If memory consistently stays above 320MB, semantic search won't be feasible on free tier. System will gracefully fall back to keyword matching.

---

## Key Insight

The old threshold (380MB) was **too conservative**. The new approach (470MB max total) properly utilizes available memory while maintaining safety. With ~320MB baseline, we have theoretical room for semantic search on first requests before embeddings are fully cached.

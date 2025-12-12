# Pull Request: Switch to smaller local model and tune performance

## Summary

This PR removes optional Hugging Face offloading and switches to a smaller local model (`paraphrase-MiniLM-L3-v2`) for faster startup and reduced memory usage on Render.

## Changes

### config.py

- Set `BERT_MODEL_NAME` to `'sentence-transformers/paraphrase-MiniLM-L3-v2'` (smaller, faster model)
- Added `ENCODING_BATCH_SIZE: int = 64` for configurable batch processing
- Added `PREWARM_MODEL: bool = True` to reduce first-query latency

### bert_processor.py

- Removed Hugging Face Inference API integration (reverted to local-only)
- Added optional prewarm in `__init__` when not lazy loading
- Use configurable `ENCODING_BATCH_SIZE` in `encode()` and `generate_embeddings()`
- Keeps all processing local per user requirement

### scripts/smoke_test.py (new)

- Simple validation script to load embeddings and run sample queries
- Tests both query-based and similar-movie recommendations
- Usage: `python scripts/smoke_test.py`

## Goal

Keep the app fully local (no external APIs) while reducing worker timeouts on Render by:

1. Using a smaller, faster model that loads quicker
2. Pre-warming the model to reduce first-query latency
3. Configurable batch sizes for better memory management

## Testing

Run the smoke test locally:

```bash
python scripts/smoke_test.py
```

## Deployment Note

After merging, remember to update the Render dashboard Start Command to:

```bash
gunicorn flask_api:app --bind 0.0.0.0:$PORT --timeout 300 --workers 1 --threads 1 --worker-class sync --max-requests 100 --max-requests-jitter 10
```

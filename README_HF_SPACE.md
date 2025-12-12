# HF Space Setup for MiniLM Embeddings

This branch contains files to deploy an embedding service on Hugging Face Spaces.

## Files

- `hf_space_app.py` - FastAPI app that serves `all-MiniLM-L6-v2` embeddings
- `hf_space_requirements.txt` - Dependencies for the Space
- `README_HF_SPACE.md` - This file

## Deploy to HF Space

### 1. Create a Space on Hugging Face
- Go to https://huggingface.co/spaces
- Click "Create new Space"
- Name: `minilm-space` (or your choice)
- Type: Docker
- Visibility: Public (or Private if you prefer)

### 2. Push Files to the Space

```bash
# Clone your Space repo
git clone https://huggingface.co/spaces/<your-username>/<your-space-name>
cd <your-space-name>

# Copy the app and requirements
cp ../cinematch/hf_space_app.py app.py
cp ../cinematch/hf_space_requirements.txt requirements.txt

# Rename app.py to match HF Space expectations
# HF Spaces look for 'app.py' in the root with a FastAPI/Gradio app

# Commit and push
git add app.py requirements.txt
git commit -m "Add MiniLM embedding service"
git push
```

### 3. Get Your Space URL
Once deployed, HF will give you a Space URL like:
```
https://<your-username>-minilm-space.hf.space
```

### 4. Use in Render

In Render's `render.yaml`, uncomment and set:

```yaml
envVars:
  - key: USE_EXTERNAL_EMBEDDINGS
    value: true
  - key: HF_SPACE_ENDPOINT
    value: https://<your-username>-minilm-space.hf.space
  - key: HF_API_TOKEN
    value: your_hf_token_here
```

### 5. Deploy Render

Push changes and Render will:
- Skip loading the local TinyBERT model
- Call your HF Space for embeddings
- Use 0MB for the model (offloaded to HF)

## How It Works

1. User queries "Batman" on Render
2. Render calls HF Space `/embed` endpoint with the query
3. HF Space's MiniLM encodes and returns embeddings
4. Render applies PCA reduction and finds recommendations
5. Response sent back to user

## API Endpoint

The HF Space provides:

```
POST /embed
Content-Type: application/json

{
  "texts": ["Batman", "action movie"]
}

Response:
{
  "embeddings": [[...384D vector...], [...384D vector...]]
}
```

## Free Tier Note

- Free HF Space sleeps after 48 hours of inactivity
- First request after sleep takes ~30-60s (cold start)
- Paid tier ($7/mo) keeps Space always-on

## Alternative: HF Inference Endpoint

If you don't want your own Space, use the public HF Inference API:

```yaml
envVars:
  - key: USE_EXTERNAL_EMBEDDINGS
    value: true
  - key: HF_API_TOKEN
    value: your_hf_token_here
  # Don't set HF_SPACE_ENDPOINT; defaults to HF Inference API
```

This uses HF's hosted MiniLM (always-on, free with rate limits).

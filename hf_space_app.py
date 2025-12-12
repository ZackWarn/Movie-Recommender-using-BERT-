"""
HF Space API for MiniLM embeddings.
Hosts all-MiniLM-L6-v2 model and provides /embed endpoint.
Deploy to https://huggingface.co/spaces/<username>/<space-name>
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MiniLM Embeddings API")

# Load model once at startup
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
logger.info(f"Loading {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)
logger.info("Model loaded successfully")


class EmbedRequest(BaseModel):
    """Request payload for embeddings"""
    texts: list[str]


class EmbedResponse(BaseModel):
    """Response with embeddings"""
    embeddings: list[list[float]]


@app.post("/embed", response_model=EmbedResponse)
async def embed(request: EmbedRequest):
    """
    Encode texts to embeddings using all-MiniLM-L6-v2.
    
    Request:
        texts: list of strings to encode
    
    Returns:
        embeddings: list of 384D float vectors
    """
    try:
        if not request.texts:
            raise ValueError("texts list is empty")
        
        logger.info(f"Encoding {len(request.texts)} texts...")
        embeddings = model.encode(request.texts, convert_to_numpy=True)
        
        # Convert to list of lists for JSON serialization
        embeddings_list = embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings
        
        logger.info(f"Successfully encoded {len(request.texts)} texts")
        return EmbedResponse(embeddings=embeddings_list)
    
    except Exception as e:
        logger.error(f"Error encoding texts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "model": MODEL_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

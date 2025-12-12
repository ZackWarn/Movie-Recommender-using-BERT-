#!/usr/bin/env python3
"""Pre-cache BERT model during build to avoid download timeout on first request."""

import os
import sys


def cache_model():
    """Download and cache the BERT model."""
    try:
        print("=" * 60)
        print("Starting BERT model download and cache...")
        print("=" * 60)

        from sentence_transformers import SentenceTransformer
        from config import Config

        model_name = Config.BERT_MODEL_NAME
        print(f"\nDownloading model: {model_name}")

        # Download and cache the model
        model = SentenceTransformer(model_name)

        # Verify model loaded successfully and report shape
        test_embedding = model.encode(["test"], show_progress_bar=False)

        print("\n✓ Model cached successfully!")
        print(f"✓ Test embedding shape: {test_embedding.shape}")
        print("=" * 60)

        return 0

    except Exception as e:
        print(f"\n✗ Failed to cache model: {e}", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        # Don't fail the build - model will be downloaded at runtime
        return 0


if __name__ == "__main__":
    sys.exit(cache_model())

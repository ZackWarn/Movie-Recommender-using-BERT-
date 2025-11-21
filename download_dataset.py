#!/usr/bin/env python3
"""
Script to download and prepare the MovieLens dataset
Downloads the MovieLens 25M dataset which includes movies, ratings, tags, and genome data
"""

import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_movielens():
    """Download and extract MovieLens 25M dataset"""
    
    # MovieLens 25M dataset URL
    dataset_url = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"
    zip_filename = "ml-25m.zip"
    extract_dir = "ml-25m"
    target_dir = "movies_dataset"
    
    print("🎬 MovieLens Dataset Downloader")
    print("=" * 50)
    
    # Check if dataset already exists
    if os.path.exists(target_dir) and os.path.exists(f"{target_dir}/movies.csv"):
        print(f"✅ Dataset already exists in '{target_dir}/'")
        response = input("Do you want to re-download? (y/N): ").strip().lower()
        if response != 'y':
            print("Skipping download.")
            return
        # Clean up existing directory
        shutil.rmtree(target_dir)
    
    # Download dataset
    print(f"\n📥 Downloading MovieLens 25M dataset...")
    print(f"   URL: {dataset_url}")
    print("   This may take a few minutes (approx. 250MB)...")
    
    try:
        urllib.request.urlretrieve(dataset_url, zip_filename)
        print("✅ Download complete!")
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return
    
    # Extract dataset
    print(f"\n📦 Extracting dataset...")
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall('.')
        print("✅ Extraction complete!")
    except Exception as e:
        print(f"❌ Error extracting dataset: {e}")
        return
    
    # Create target directory and move files
    print(f"\n📁 Setting up '{target_dir}' directory...")
    os.makedirs(target_dir, exist_ok=True)
    
    # Files we need from the dataset
    required_files = [
        'movies.csv',
        'ratings.csv',
        'tags.csv',
        'genome-scores.csv',
        'genome-tags.csv'
    ]
    
    for filename in required_files:
        source = os.path.join(extract_dir, filename)
        target = os.path.join(target_dir, filename)
        if os.path.exists(source):
            shutil.copy2(source, target)
            print(f"   ✓ {filename}")
        else:
            print(f"   ⚠️  {filename} not found")
    
    # Clean up
    print(f"\n🧹 Cleaning up...")
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print(f"   ✓ Removed {zip_filename}")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
        print(f"   ✓ Removed {extract_dir}/")
    
    print("\n" + "=" * 50)
    print("✅ Dataset setup complete!")
    print(f"📊 Data files are in '{target_dir}/'")
    print("\n🚀 Next steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Generate embeddings: python main.py")
    print("   3. Run the app: streamlit run app.py")
    print("=" * 50)

if __name__ == "__main__":
    download_movielens()

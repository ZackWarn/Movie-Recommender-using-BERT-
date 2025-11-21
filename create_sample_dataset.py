#!/usr/bin/env python3
"""
Create a sample MovieLens-style dataset for testing the application
This creates minimal CSV files that match the expected format
"""

import pandas as pd
import os

def create_sample_dataset():
    """Create sample dataset files"""
    
    dataset_dir = "movies_dataset"
    os.makedirs(dataset_dir, exist_ok=True)
    
    print("🎬 Creating Sample Movie Dataset")
    print("=" * 50)
    
    # Sample movies data
    movies_data = {
        'movieId': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
        'title': [
            'The Matrix (1999)',
            'Inception (2010)',
            'The Dark Knight (2008)',
            'Interstellar (2014)',
            'Pulp Fiction (1994)',
            'The Shawshank Redemption (1994)',
            'The Godfather (1972)',
            'Forrest Gump (1994)',
            'Fight Club (1999)',
            'The Lord of the Rings: The Fellowship of the Ring (2001)',
            'Star Wars: Episode IV - A New Hope (1977)',
            'The Empire Strikes Back (1980)',
            'Return of the Jedi (1983)',
            'Jurassic Park (1993)',
            'Titanic (1997)',
            'Avatar (2009)',
            'The Avengers (2012)',
            'Iron Man (2008)',
            'Spider-Man (2002)',
            'Batman Begins (2005)',
            'The Silence of the Lambs (1991)',
            'Se7en (1995)',
            'The Usual Suspects (1995)',
            'Goodfellas (1990)',
            'The Departed (2006)',
            'Gladiator (2000)',
            'Braveheart (1995)',
            'Saving Private Ryan (1998)',
            "Schindler's List (1993)",
            'The Green Mile (1999)',
            'Terminator 2: Judgment Day (1991)',
            'Alien (1979)',
            'Blade Runner (1982)',
            'The Prestige (2006)',
            'Memento (2000)',
            'The Sixth Sense (1999)',
            'The Truman Show (1998)',
            'Eternal Sunshine of the Spotless Mind (2004)',
            'Toy Story (1995)',
            'Finding Nemo (2003)'
        ],
        'genres': [
            'Action|Sci-Fi|Thriller',
            'Action|Sci-Fi|Thriller',
            'Action|Crime|Drama',
            'Adventure|Drama|Sci-Fi',
            'Crime|Drama|Thriller',
            'Drama',
            'Crime|Drama',
            'Drama|Romance',
            'Drama|Thriller',
            'Adventure|Fantasy',
            'Action|Adventure|Sci-Fi',
            'Action|Adventure|Sci-Fi',
            'Action|Adventure|Sci-Fi',
            'Action|Adventure|Sci-Fi|Thriller',
            'Drama|Romance',
            'Action|Adventure|Fantasy|Sci-Fi',
            'Action|Adventure|Sci-Fi',
            'Action|Adventure|Sci-Fi',
            'Action|Adventure|Sci-Fi',
            'Action|Crime|Drama',
            'Crime|Drama|Thriller',
            'Crime|Drama|Mystery|Thriller',
            'Crime|Mystery|Thriller',
            'Crime|Drama',
            'Crime|Drama|Thriller',
            'Action|Adventure|Drama',
            'Action|Drama|War',
            'Drama|War',
            'Drama|War',
            'Crime|Drama|Fantasy',
            'Action|Sci-Fi|Thriller',
            'Horror|Sci-Fi',
            'Sci-Fi|Thriller',
            'Drama|Mystery|Sci-Fi|Thriller',
            'Mystery|Thriller',
            'Drama|Mystery|Thriller',
            'Comedy|Drama|Sci-Fi',
            'Drama|Romance|Sci-Fi',
            'Animation|Adventure|Comedy',
            'Animation|Adventure|Comedy'
        ]
    }
    
    # Create movies.csv
    movies_df = pd.DataFrame(movies_data)
    movies_df.to_csv(f"{dataset_dir}/movies.csv", index=False)
    print(f"✅ Created movies.csv ({len(movies_df)} movies)")
    
    # Create ratings data (generate realistic ratings)
    ratings_list = []
    import random
    random.seed(42)
    
    # Generate ratings for each movie
    for movie_id in movies_data['movieId']:
        # Each movie gets 50-200 ratings
        num_ratings = random.randint(50, 200)
        for i in range(num_ratings):
            user_id = random.randint(1, 500)
            rating = random.choice([3.0, 3.5, 4.0, 4.5, 5.0] * 3 + [2.0, 2.5] * 1)  # Bias toward higher ratings
            timestamp = random.randint(1000000000, 1600000000)
            ratings_list.append({
                'userId': user_id,
                'movieId': movie_id,
                'rating': rating,
                'timestamp': timestamp
            })
    
    ratings_df = pd.DataFrame(ratings_list)
    ratings_df.to_csv(f"{dataset_dir}/ratings.csv", index=False)
    print(f"✅ Created ratings.csv ({len(ratings_df)} ratings)")
    
    # Create tags data
    sample_tags = [
        'action', 'sci-fi', 'thriller', 'suspense', 'visual effects', 'mind-bending',
        'classic', 'drama', 'intense', 'crime', 'masterpiece', 'thought-provoking',
        'epic', 'adventure', 'fantasy', 'dark', 'atmospheric', 'twist ending',
        'time travel', 'dystopian', 'philosophical', 'violence', 'realistic',
        'emotional', 'inspiring', 'gripping', 'complex', 'iconic'
    ]
    
    tags_list = []
    for movie_id in movies_data['movieId']:
        # Each movie gets 3-8 tags
        num_tags = random.randint(3, 8)
        for i in range(num_tags):
            user_id = random.randint(1, 100)
            tag = random.choice(sample_tags)
            timestamp = random.randint(1000000000, 1600000000)
            tags_list.append({
                'userId': user_id,
                'movieId': movie_id,
                'tag': tag,
                'timestamp': timestamp
            })
    
    tags_df = pd.DataFrame(tags_list)
    tags_df.to_csv(f"{dataset_dir}/tags.csv", index=False)
    print(f"✅ Created tags.csv ({len(tags_df)} tags)")
    
    # Create genome-tags data (tag vocabulary)
    genome_tags_data = {
        'tagId': list(range(1, len(sample_tags) + 1)),
        'tag': sample_tags
    }
    genome_tags_df = pd.DataFrame(genome_tags_data)
    genome_tags_df.to_csv(f"{dataset_dir}/genome-tags.csv", index=False)
    print(f"✅ Created genome-tags.csv ({len(genome_tags_df)} tags)")
    
    # Create genome-scores data (relevance scores)
    genome_scores_list = []
    for movie_id in movies_data['movieId']:
        for tag_id in range(1, len(sample_tags) + 1):
            # Generate relevance score (some tags are more relevant than others)
            relevance = random.random()
            genome_scores_list.append({
                'movieId': movie_id,
                'tagId': tag_id,
                'relevance': relevance
            })
    
    genome_scores_df = pd.DataFrame(genome_scores_list)
    genome_scores_df.to_csv(f"{dataset_dir}/genome-scores.csv", index=False)
    print(f"✅ Created genome-scores.csv ({len(genome_scores_df)} scores)")
    
    print("\n" + "=" * 50)
    print("✅ Sample dataset created successfully!")
    print(f"📊 Location: {dataset_dir}/")
    print("\n📈 Dataset Statistics:")
    print(f"   - Movies: {len(movies_df)}")
    print(f"   - Ratings: {len(ratings_df)}")
    print(f"   - Tags: {len(tags_df)}")
    print(f"   - Genome Tags: {len(genome_tags_df)}")
    print(f"   - Genome Scores: {len(genome_scores_df)}")
    print("\n🚀 Next steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Generate embeddings: python main.py")
    print("   3. Run the app: streamlit run app.py")
    print("=" * 50)

if __name__ == "__main__":
    create_sample_dataset()

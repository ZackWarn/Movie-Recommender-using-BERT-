import streamlit as st
from rec_engine import MovieRecommendationEngine
from bert_processor import MovieBERTProcessor
from config import Config
import os


@st.cache_resource
def load_recommendation_engine():
    bert_processor = MovieBERTProcessor(force_tfidf=True)
    bert_processor.load_embeddings()
    engine = MovieRecommendationEngine(bert_processor, use_imdb=True)
    return engine


def show_recommendations(recommendations):
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            # Create columns for poster and info
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Display poster if available
                if rec.get('poster_url'):
                    st.image(rec['poster_url'], width=150, caption=rec['title'])
                else:
                    st.write("🎬")  # Placeholder if no poster
            
            with col2:
                st.write(f"### {i}. {rec['title']} ({rec.get('year', rec.get('imdb_year', 'N/A'))})")
                
                # Display IMDB rating if available
                if rec.get('imdb_rating', 0) > 0:
                    st.write(f"**IMDB Rating:** ⭐ {rec['imdb_rating']}/10 ({rec.get('imdb_rating_count', 0):,} votes)")
                
                # Display local rating
                if rec.get('avg_rating', 0) > 0:
                    st.write(f"**Local Rating:** {rec['avg_rating']:.1f}/5.0")
                
                # Display genres
                genres = rec.get('imdb_genres', rec.get('genres', []))
                if genres:
                    st.write(f"**Genres:** {', '.join(genres)}")
                
                # Display plot if available
                if rec.get('plot'):
                    st.write(f"**Plot:** {rec['plot'][:200]}{'...' if len(rec.get('plot', '')) > 200 else ''}")
                
                # Display cast if available
                if rec.get('cast'):
                    cast_list = rec['cast'][:5]  # Show first 5 cast members
                    st.write(f"**Cast:** {', '.join(cast_list)}")
                
                # Display runtime if available
                if rec.get('runtime', 0) > 0:
                    hours = rec['runtime'] // 60
                    minutes = rec['runtime'] % 60
                    st.write(f"**Runtime:** {hours}h {minutes}m")
                
                # Display similarity score if available
                if rec.get('similarity_score', 0) > 0:
                    st.write(f"**Similarity Score:** {rec['similarity_score']:.3f}")
                
                # Display IMDB link if available
                if rec.get('imdb_id'):
                    imdb_url = f"https://www.imdb.com/title/{rec['imdb_id']}/"
                    st.write(f"**[View on IMDB]({imdb_url})**")
            
            st.markdown("---")
    else:
        st.info("No recommendations found.")


def main():
    st.title("🎬 BERT Movie Recommendation System")
    st.write("Get personalized movie recommendations using AI!")

    # Load the recommendation engine
    engine = load_recommendation_engine()

    # Check if IMDB is available
    imdb_available = Config.validate_config()
    if not imdb_available:
        st.warning("⚠️ IMDB API key not configured. Some features may be limited.")
    
    # Sidebar for different recommendation types
    st.sidebar.title("Recommendation Type")
    rec_options = ["Natural Language Query", "Similar Movies", "Search Movies"]
    if imdb_available:
        rec_options.extend(["IMDB Search", "Trending Movies"])
    
    rec_type = st.sidebar.radio("Choose recommendation method:", rec_options)

    if rec_type == "Natural Language Query":
        st.header("🔍 Describe what you want to watch")
        query = st.text_input(
            "Enter your preference:",
            placeholder="e.g., romantic comedies from the 90s with great soundtracks"
        )

        if query and st.button("Get Recommendations"):
            with st.spinner("Finding perfect movies for you..."):
                if imdb_available:
                    recommendations = engine.recommend_by_query_with_imdb(query, top_k=10)
                else:
                    recommendations = engine.recommend_by_query(query, top_k=10)

            if recommendations:
                st.success(f"Found {len(recommendations)} recommendations!")
                show_recommendations(recommendations)
            else:
                st.warning("No recommendations found. Try a different query!")

    elif rec_type == "Similar Movies":
        st.header("🎭 Find movies similar to one you like")

        # Movie search
        search_term = st.text_input("Search for a movie:", placeholder="Enter movie title...")

        if search_term:
            search_results = engine.search_movies(search_term)

            if search_results:
                movie_options = {
                    f"{movie.get('title', 'Unknown')} ({movie.get('year', 'N/A')})": movie['movieId']
                    for movie in search_results[:10]
                }

                selected_movie = st.selectbox("Select a movie:", list(movie_options.keys()))

                if selected_movie and st.button("Find Similar Movies"):
                    movie_id = movie_options[selected_movie]

                    with st.spinner("Finding similar movies..."):
                        if imdb_available:
                            similar_movies = engine.recommend_similar_movies_with_imdb(movie_id, top_k=8)
                        else:
                            similar_movies = engine.recommend_similar_movies(movie_id, top_k=8)

                    if similar_movies:
                        st.success("Similar movies found!")
                        show_recommendations(similar_movies)
                    else:
                        st.warning("No similar movies found.")
            else:
                st.warning("No movies found with that search term.")

    elif rec_type == "Search Movies":
        st.header("🔎 Search for movies by title or keyword")

        search_term = st.text_input("Enter movie title or keyword:")

        if search_term and st.button("Search"):
            if imdb_available:
                search_results = engine.search_movies_with_imdb(search_term)
            else:
                search_results = engine.search_movies(search_term)
            if search_results:
                show_recommendations(search_results)
            else:
                st.warning("No movies found for your search.")
    
    elif rec_type == "IMDB Search":
        st.header("🔍 Search IMDB Database")
        st.write("Search directly in IMDB's database for the latest movies and shows.")
        
        search_term = st.text_input("Enter movie title:", placeholder="e.g., The Matrix, Inception")
        
        if search_term and st.button("Search IMDB"):
            with st.spinner("Searching IMDB database..."):
                imdb_results = engine.search_imdb_movies(search_term, limit=10)
            
            if imdb_results:
                st.success(f"Found {len(imdb_results)} movies from IMDB!")
                show_recommendations(imdb_results)
            else:
                st.warning("No movies found in IMDB database.")
    
    elif rec_type == "Trending Movies":
        st.header("🔥 Trending Movies")
        st.write("Discover what's popular right now on IMDB.")
        
        if st.button("Get Trending Movies"):
            with st.spinner("Fetching trending movies..."):
                trending_movies = engine.get_trending_movies(limit=10)
            
            if trending_movies:
                st.success(f"Found {len(trending_movies)} trending movies!")
                show_recommendations(trending_movies)
            else:
                st.warning("Unable to fetch trending movies. Please check your API configuration.")

if __name__ == "__main__":
    main()

# app.py
import streamlit as st
from rec_engine import MovieRecommendationEngine
from bert_processor import MovieBERTProcessor

@st.cache_resource
def load_recommendation_engine():
    bert_processor = MovieBERTProcessor()
    bert_processor.load_embeddings()
    return MovieRecommendationEngine(bert_processor)

def show_recommendations(recommendations):
    if recommendations:
        for rec in recommendations:
            st.write(f"### {rec['title']} ({rec.get('year', 'N/A')})")
            st.write(
                f"**Genres:** {', '.join(rec.get('genres', []))}"
            )
            st.write(
                f"**Rating:** {rec.get('avg_rating', 0):.1f}/5.0 "
                f"({rec.get('rating_count', 'N/A')} reviews)"
            )
            st.write(f"**Similarity Score:** {rec.get('similarity_score', 0):.3f}")
            st.markdown("---")
    else:
        st.info("No recommendations found.")




def main():
    st.title("🎬 BERT Movie Recommendation System")
    st.write("Get personalized movie recommendations using AI!")
    
    # Load the recommendation engine
    engine = load_recommendation_engine()
    
    # Sidebar for different recommendation types
    st.sidebar.title("Recommendation Type")
    rec_type = st.sidebar.radio(
        "Choose recommendation method:",
        ["Natural Language Query", "Similar Movies", "Search Movies"]
    )
    
    if rec_type == "Natural Language Query":
        st.header("🔍 Describe what you want to watch")
        query = st.text_input(
            "Enter your preference:",
            placeholder="e.g., romantic comedies from the 90s with great soundtracks"
        )
        
        if query and st.button("Get Recommendations"):
            with st.spinner("Finding perfect movies for you..."):
                recommendations = engine.recommend_by_query(query, top_k=10)
            
            if recommendations:
                st.success(f"Found {len(recommendations)} recommendations!")
                
                for i, rec in enumerate(recommendations, 1):
                    with st.expander(f"{i}. {rec['title']} ({rec['year']}) - Score: {rec['similarity_score']:.3f}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"**Genres:** {', '.join(rec['genres'])}")
                            st.write(f"**Rating:** {rec.get('avg_rating', 0):.1f}/5.0 ({rec.get('rating_count', 'N/A')} reviews)")

                            tags = rec.get('tags', [])
                        if tags:
                            st.write(f"**Tags:** {', '.join(map(str, tags))}")

                        
                        with col2:
                            st.info(rec.get('explanation')'explanation'])
            else:
                st.warning("No recommendations found. Try a different query!")
    
    elif rec_type == "Similar Movies":
        st.header("🎭 Find movies similar to one you like")
        
        # Movie search
        search_term = st.text_input("Search for a movie:", placeholder="Enter movie title...")
        
        if search_term:
            search_results = engine.search_movies(search_term)
            
            if search_results:
                movie_options = {f"{movie['clean_title']} ({movie['year']})": movie['movieId'] 
                               for movie in search_results[:10]}
                
                selected_movie = st.selectbox("Select a movie:", list(movie_options.keys()))
                
                if selected_movie and st.button("Find Similar Movies"):
                    movie_id = movie_options[selected_movie]
                    
                    with st.spinner("Finding similar movies..."):
                        similar_movies = engine.recommend_similar_movies(movie_id, top_k=8)
                    
                    if similar_movies:
                        st.success("Similar movies found!")
                        
                        for i, rec in enumerate(similar_movies, 1):
                            with st.expander(f"{i}. {rec['title']} ({rec['year']}) - Score: {rec['similarity_score']:.3f}"):
                                st.write(f"**Genres:** {', '.join(rec['genres'])}")
                                st.write(f"**Rating:** {rec['rating']:.1f}/5.0")
                                st.info(rec['explanation'])

if __name__ == "__main__":
    main()

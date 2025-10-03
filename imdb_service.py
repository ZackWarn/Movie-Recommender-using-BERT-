import requests
import os
from typing import Dict, List, Optional, Tuple
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IMDBService:
    def __init__(self, api_key: str = None):
        """
        Initialize IMDB service with RapidAPI key
        
        Args:
            api_key: RapidAPI IMDB API key. If None, will try to get from environment variable
        """
        self.api_key = api_key or os.getenv('RAPIDAPI_IMDB_KEY')
        if not self.api_key:
            raise ValueError("RapidAPI IMDB API key is required. Set RAPIDAPI_IMDB_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://imdb236.p.rapidapi.com"
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'imdb236.p.rapidapi.com'
        }
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to the IMDB API with error handling"""
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params or {})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {endpoint}: {e}")
            return None
    
    def search_movies(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for movies by title using RapidAPI imdb236 search.
        """
        endpoint = "api/imdb/search"
        params = { 'query': query }

        data = self._make_request(endpoint, params)
        results = data.get('results', []) if isinstance(data, dict) else (data or [])
        if not isinstance(results, list):
            return []

        movies: List[Dict] = []
        for item in results[:limit]:
            item_type = item.get('type') or item.get('q')
            if item_type not in (None, 'movie', 'tvMovie', 'tvSeries', 'tvMiniSeries', 'video', 'short'):
                pass  # keep flexible; filter later if needed

            thumb = None
            thumbs = item.get('thumbnails')
            if isinstance(thumbs, list) and len(thumbs) > 0:
                thumb = thumbs[0].get('url')
            image_url = item.get('primaryImage') or thumb or ''
            if image_url.startswith('http://'):
                image_url = 'https://' + image_url[len('http://'):]

            movie_info = {
                'imdb_id': item.get('id', ''),
                'title': item.get('primaryTitle') or item.get('title') or item.get('l') or '',
                'year': item.get('startYear') or item.get('year') or item.get('y') or '',
                'image_url': image_url,
                'poster_url': image_url,
                'type': item_type or '',
                'actors': item.get('s', ''),
                'rank': item.get('rank', 0),
            }
            movies.append(movie_info)

        return movies
    
    def get_movie_details(self, imdb_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific movie
        
        Args:
            imdb_id: IMDB ID of the movie
            
        Returns:
            Dictionary with movie details or None if not found
        """
        # Attempt detail endpoints. Some imdb236 paths may not be available for all IDs; return minimal info on failure.
        basic_info = self._make_request(f"api/imdb/title/{imdb_id}") or {}
        if not basic_info:
            return None
        
        # Get ratings
        ratings = self._make_request(f"api/imdb/title/{imdb_id}/ratings")
        
        # Get plot summary
        plot = self._make_request(f"api/imdb/title/{imdb_id}/plots")
        
        # Get cast
        cast = self._make_request(f"api/imdb/title/{imdb_id}/cast")
        
        # Get genres
        genres = self._make_request(f"api/imdb/title/{imdb_id}/genres")
        
        # Combine all information
        title_info = basic_info.get('title') if isinstance(basic_info, dict) else None
        image_url = ''
        if title_info and isinstance(title_info, dict):
            img = title_info.get('image')
            if isinstance(img, dict):
                image_url = img.get('url', '')
        if not image_url:
            thumb = basic_info.get('primaryImage') if isinstance(basic_info, dict) else None
            if isinstance(thumb, str):
                image_url = thumb
        if image_url.startswith('http://'):
            image_url = 'https://' + image_url[len('http://'):]

        movie_details = {
            'imdb_id': imdb_id,
            'title': (title_info or {}).get('title', '') if isinstance(title_info, dict) else basic_info.get('primaryTitle', ''),
            'year': (title_info or {}).get('year', '') if isinstance(title_info, dict) else basic_info.get('startYear', ''),
            'image_url': image_url,
            'poster_url': image_url,
            'plot': (plot.get('plots', [{}])[0].get('text', '') if isinstance(plot, dict) and plot.get('plots') else ''),
            'rating': (ratings.get('rating', 0) if isinstance(ratings, dict) else 0),
            'rating_count': (ratings.get('ratingCount', 0) if isinstance(ratings, dict) else 0),
            'genres': (genres.get('genres', []) if isinstance(genres, dict) else []),
            'cast': self._extract_cast_names(cast) if isinstance(cast, dict) else [],
            'runtime': (title_info or {}).get('runningTimeInMinutes', 0) if isinstance(title_info, dict) else 0,
            'release_date': (title_info or {}).get('releaseDate', '') if isinstance(title_info, dict) else '',
            'type': (title_info or {}).get('titleType', '') if isinstance(title_info, dict) else '',
            'is_series': (title_info or {}).get('isSeries', False) if isinstance(title_info, dict) else False,
        }

        # If we lack any basic info (e.g., 404s), still return a minimal structure
        if not movie_details['title'] and not image_url:
            return {
                'imdb_id': imdb_id,
                'title': '',
                'year': '',
                'image_url': '',
                'poster_url': '',
                'plot': '',
                'rating': 0,
                'rating_count': 0,
                'genres': [],
                'cast': [],
                'runtime': 0,
                'release_date': '',
                'type': '',
                'is_series': False,
            }
        
        return movie_details
    
    def _extract_cast_names(self, cast_data: Dict) -> List[str]:
        """Extract cast member names from cast data"""
        if not cast_data or 'cast' not in cast_data:
            return []
        
        cast_members = []
        for member in cast_data['cast'][:10]:  # Limit to top 10 cast members
            if 'name' in member:
                cast_members.append(member['name'])
        
        return cast_members
    
    def get_movie_ratings(self, imdb_id: str) -> Optional[Dict]:
        """
        Get movie ratings information
        
        Args:
            imdb_id: IMDB ID of the movie
            
        Returns:
            Dictionary with rating information
        """
        ratings = self._make_request(f"title/get-ratings", {'tconst': imdb_id})
        if not ratings:
            return None
        
        return {
            'imdb_rating': ratings.get('rating', 0),
            'rating_count': ratings.get('ratingCount', 0),
            'top_1000_voters_rating': ratings.get('top1000VotersRating', 0),
            'top_1000_voters_count': ratings.get('top1000VotersCount', 0),
            'us_users_rating': ratings.get('usUsersRating', 0),
            'us_users_count': ratings.get('usUsersCount', 0)
        }
    
    def get_trending_movies(self, limit: int = 10) -> List[Dict]:
        """
        Get trending movies
        
        Args:
            limit: Maximum number of movies to return
            
        Returns:
            List of trending movies
        """
        # Get most popular movies
        popular = self._make_request("title/get-most-popular-movies")
        if not popular:
            return []
        
        movies = []
        for imdb_id in popular[:limit]:
            movie_details = self.get_movie_details(imdb_id)
            if movie_details:
                movies.append(movie_details)
        
        return movies
    
    def get_movie_poster(self, imdb_id: str, size: str = "large") -> Optional[str]:
        """
        Get movie poster URL
        
        Args:
            imdb_id: IMDB ID of the movie
            size: Size of the poster ('small', 'medium', 'large')
            
        Returns:
            Poster URL or None if not found
        """
        movie_details = self.get_movie_details(imdb_id)
        if movie_details and movie_details.get('image_url'):
            return movie_details['image_url']
        return None
    
    def search_and_get_details(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for movies and get detailed information for each
        
        Args:
            query: Search query
            limit: Maximum number of movies to return
            
        Returns:
            List of movies with detailed information
        """
        search_results = self.search_movies(query, limit)
        detailed_movies = []
        
        for movie in search_results:
            if movie.get('imdb_id'):
                details = self.get_movie_details(movie['imdb_id'])
                if details:
                    movie.update(details)
                # Always append at least the search result so poster/url shows even if details fail
                detailed_movies.append(movie)
        
        return detailed_movies


# Example usage and testing
if __name__ == "__main__":
    # Test the service (you'll need to set your API key)
    api_key = os.getenv('RAPIDAPI_IMDB_KEY')
    if api_key:
        service = IMDBService(api_key)
        
        # Test search
        print("Testing movie search...")
        results = service.search_movies("The Matrix", 5)
        for movie in results:
            print(f"- {movie['title']} ({movie['year']}) - {movie['imdb_id']}")
        
        # Test detailed info
        if results:
            print(f"\nTesting detailed info for: {results[0]['title']}")
            details = service.get_movie_details(results[0]['imdb_id'])
            if details:
                print(f"Rating: {details['rating']}/10")
                print(f"Genres: {', '.join(details['genres'])}")
                print(f"Plot: {details['plot'][:200]}...")
    else:
        print("Please set RAPIDAPI_IMDB_KEY environment variable to test the service")

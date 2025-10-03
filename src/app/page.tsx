"use client";
import { useState } from "react";
import { FiSearch } from "react-icons/fi";
import MovieCard from "../components/MovieCard";
// Poster grid removed per request

const FilmIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="12"      // half of 24
    height="12"     // half of 24
    viewBox="0 0 24 24"  // keep viewbox same for proper scaling
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
    <line x1="7" y1="2" x2="7" y2="22"></line>
    <line x1="17" y1="2" x2="17" y2="22"></line>
    <line x1="2" y1="12" x2="22" y2="12"></line>
    <line x1="2" y1="7" x2="7" y2="7"></line>
    <line x1="2" y1="17" x2="7" y2="17"></line>
    <line x1="17" y1="17" x2="22" y2="17"></line>
    <line x1="17" y1="7" x2="22" y2="7"></line>
  </svg>
);


export default function CineMatchHero() {
  const [search, setSearch] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  // IMDb posters removed per request

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!search.trim()) return;

    setLoading(true);
    setError("");
    
    try {
      const response = await fetch('/api/recommendations/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: search,
          top_k: 10
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const data = await response.json();
      setRecommendations(data.recommendations || []);

      // Removed IMDb fetch
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex flex-col py-20 bg-gradient-to-br from-[#24033e] via-[#502689] to-[#7423fb] px-4">
      <div className="flex flex-col w-full mx-auto mt-4 px-4 max-w-full">

        <h1 className="text-white text-6xl font-extrabold text-center mb-3 tracking-tight">
          KnowMovies
        </h1>
        <p className="text-purple-100 text-lg text-center mb-7">
          Discover your next favorite movie. Enter a film you love, and we&apos;ll find
          <br />similar gems you&apos;ll enjoy.
        </p>
        <div className="w-full flex justify-center mb-10">
          <form
            className="relative flex items-center bg-white/10 backdrop-blur-sm rounded-lg shadow w-full max-w-2xl"
            onSubmit={handleSearch}
          >
            {/* FilmIcon positioned at the left end */}
            <FilmIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-purple-200" />
            
            <input
              type="text"
              className="flex-grow py-3 pl-12 pr-20 bg-transparent placeholder-purple-200 outline-none text-amber-100 rounded-xl"
              placeholder="Enter a movie to get recommendations"
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-1 top-1/2 -translate-y-1/2 flex items-center space-x-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white font-semibold px-6 py-2 rounded-sm transition hover:from-pink-600 hover:to-purple-800 shadow disabled:opacity-50 disabled:cursor-not-allowed"
              style={{height: "2.4rem"}}
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <FiSearch className="h-5 w-5" />
              )}
              <span className="hidden sm:inline">
                {loading ? "Searching..." : "Find Movies"}
              </span>
            </button>
          </form>
        </div>

        {recommendations.length === 0 && (
  <div className="flex flex-col items-center mt-8 mb-2">
    <span className="text-purple-200 text-6xl mb-4">🎬</span>
    <h2 className="text-white text-2xl font-bold mb-2 text-center">
      Ready to discover amazing movies?
    </h2>
    <p className="text-purple-200 text-center mb-3">
      Search for a movie above to get personalized recommendations
    </p>
  </div>
)}


        {/* Error Message */}
        {error && (
          <div className="mt-8 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
            <p className="text-red-200 text-center">{error}</p>
          </div>
        )}

       

        {/* Recommendations Section */}
        {recommendations.length > 0 && (
  <div className="w-full">
    <h2 className="text-white text-3xl font-bold text-center mb-8">
      Recommendations for &quot;{search.trim()}&quot;
    </h2>
    <div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-6">
  {recommendations.slice(1, 9).map((movie, index) => (
    <MovieCard key={movie.movieId || index} movie={movie} index={index + 1} />
  ))}
</div>

  </div>
)}

      </div>
    </div>
  );
}

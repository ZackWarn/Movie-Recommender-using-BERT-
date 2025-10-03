"use client";
import { useState } from "react";
import Image from "next/image";

interface MovieCardProps {
  movie: {
    title: string;
    year?: string | number;
    imdb_year?: string | number;
    imdb_rating?: number;
    imdb_rating_count?: number;
    avg_rating?: number;
    poster_url?: string;
    plot?: string;
    genres?: string[];
    imdb_genres?: string[];
    cast?: string[];
    runtime?: number;
    similarity_score?: number;
    imdb_id?: string;
  };
  index?: number;
}

export default function MovieCard({ movie, index }: MovieCardProps) {
  const [imageError, setImageError] = useState(false);
  
  const displayYear = movie.imdb_year || movie.year || 'N/A';
  const displayGenres = movie.imdb_genres || movie.genres || [];
  const displayRating = movie.imdb_rating || movie.avg_rating || 0;
  const ratingCount = movie.imdb_rating_count || 0;
  const googleSearchUrl = `https://www.google.com/search?q=${encodeURIComponent(`${movie.title} ${displayYear !== 'N/A' ? displayYear : ''}`.trim())}`;
  
  const formatRuntime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-white/20">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Movie Poster removed per request */}

        {/* Movie Information */}
        <div className="flex-1 space-y-4">
          {/* Title and Year */}
          <div className="flex items-center space-x-2 mb-2">
  <h3 className="text-2xl font-bold text-white">
    {index && `${index}. `}{movie.title}
  </h3>
  <span className="text-purple-200 text-lg">({displayYear})</span>
</div>





{/* Genres */}
{displayGenres.length > 0 && (
  <div>
    <p className="text-purple-200 text-sm mb-2">Genres:</p>
    <div className="flex flex-row gap-2 overflow-x-auto whitespace-nowrap">
      {displayGenres.slice(0, 4).map((genre, idx) => (
        <span
          key={idx}
          className="bg-purple-800/40 text-purple-100 px-1 py-1 rounded-full text-sm"
        >
          {genre}
        </span>
      ))}
    </div>
  </div>
)}







          {/* Similarity Score */}
          {movie.similarity_score && movie.similarity_score > 0 && (
            <div className="flex items-center space-x-2">
              <span className="text-purple-200 text-sm">Match:</span>
              <span className="text-white text-sm">
                {(movie.similarity_score * 100).toFixed(1)}%
              </span>
            </div>
          )}

          {/* Google Search Link */}
          <div className="pt-2">
            <a
              href={googleSearchUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 text-blue-300 hover:text-blue-200 transition-colors"
            >
              <span>Search on Google</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

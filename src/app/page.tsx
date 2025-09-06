"use client";
import { useState } from "react";
import { FiSearch } from "react-icons/fi";

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

  return (
    <div className="min-h-screen w-full flex flex-col py-20 bg-gradient-to-br from-[#24033e] via-[#502689] to-[#7423fb] px-4">
      <div className="flex flex-col max-w-4xl w-full mx-auto mt-4">
        <h1 className="text-white text-6xl font-extrabold text-center mb-3 tracking-tight">
          KnowMovies
        </h1>
        <p className="text-purple-100 text-lg text-center mb-7">
          Discover your next favorite movie. Enter a film you love, and we&apos;ll find
          <br />similar gems you&apos;ll enjoy.
        </p>
        <div className="w-full flex justify-center mb-25">
          <form
            className="relative flex items-center bg-white/10 backdrop-blur-sm rounded-lg shadow w-full max-w-2xl"
            onSubmit={e => { e.preventDefault(); /* search logic here */ }}
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
              className="absolute right-1 top-1/2 -translate-y-1/2 flex items-center space-x-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white font-semibold px-6 py-2 rounded-sm transition hover:from-pink-600 hover:to-purple-800 shadow"
              style={{height: "2.4rem"}}
            >
              <FiSearch className="h-5 w-5" />
              <span className="hidden sm:inline">Find Movies</span>
            </button>
          </form>
        </div>

        <div className="flex flex-col items-center mt-8 mb-2">
          <span className="text-purple-200 text-6xl mb-4">🎬</span>
          <h2 className="text-white text-2xl font-bold mb-2 text-center">
            Ready to discover amazing movies?
          </h2>
          <p className="text-purple-200 text-center mb-3">
            Search for a movie above to get personalized recommendations
          </p>
        </div>
      </div>
    </div>
  );
}

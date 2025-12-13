// SkeletonCard.jsx - Reusable skeleton component
export function SkeletonCard() {
  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 shadow-lg border border-white/20 hover:shadow-xl transition-all duration-300">
      <div className="flex flex-col space-y-4">
        
        {/* Title and Year Skeleton */}
        <div className="flex items-center space-x-2 mb-2">
          {/* Title skeleton */}
          <div className="flex-1 h-8 bg-white/5 rounded shimmer"></div>
          {/* Year skeleton */}
          <div className="h-6 w-20 bg-white/5 rounded shimmer"></div>
        </div>

        {/* Genres Skeleton */}
        <div>
          {/* Genre label skeleton */}
          <div className="h-4 w-16 bg-white/5 rounded shimmer mb-3"></div>
          
          {/* Genre pills skeleton */}
          <div className="flex flex-row gap-2 overflow-x-auto whitespace-nowrap">
            {Array.from({ length: 4 }).map((_, idx) => (
              <div
                key={idx}
                className="h-7 w-24 bg-white/5 rounded-full shimmer flex-shrink-0"
              ></div>
            ))}
          </div>
        </div>

        {/* Match Score Skeleton */}
        <div className="flex items-center space-x-2 pt-2">
          {/* Match label skeleton */}
          <div className="h-4 w-12 bg-white/5 rounded shimmer"></div>
          {/* Match value skeleton */}
          <div className="h-4 w-20 bg-white/5 rounded shimmer"></div>
        </div>

        {/* Google Search Link Skeleton */}
        <div className="pt-2">
          <div className="h-5 w-40 bg-white/5 rounded shimmer"></div>
        </div>
      </div>
    </div>
  );
}

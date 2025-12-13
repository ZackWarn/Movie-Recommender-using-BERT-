export function SkeletonCard({ index = 0 }) {
  const animationDelay = `${index * 0.1}s`;
  
  return (
    <div 
      className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20"
      style={{ animationDelay }}
    >
      <div className="space-y-4">
        {/* Title with stagger */}
        <div 
          className="h-8 w-2/3 bg-white/5 rounded shimmer"
          style={{ animationDelay: `${0.1 + index * 0.1}s` }}
        ></div>

        {/* Year with stagger */}
        <div 
          className="h-5 w-20 bg-white/5 rounded shimmer"
          style={{ animationDelay: `${0.2 + index * 0.1}s` }}
        ></div>

        {/* Genres with stagger */}
        <div className="space-y-2">
          <div 
            className="h-4 w-16 bg-white/5 rounded shimmer"
            style={{ animationDelay: `${0.3 + index * 0.1}s` }}
          ></div>
          <div className="flex gap-2">
            {[0, 1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-6 w-20 bg-white/5 rounded-full shimmer"
                style={{ animationDelay: `${0.4 + (i * 0.1) + (index * 0.1)}s` }}
              ></div>
            ))}
          </div>
        </div>

        {/* Match score with stagger */}
        <div 
          className="h-4 w-28 bg-white/5 rounded shimmer"
          style={{ animationDelay: `${0.5 + index * 0.1}s` }}
        ></div>

        {/* Link with stagger */}
        <div 
          className="h-5 w-36 bg-white/5 rounded shimmer"
          style={{ animationDelay: `${0.6 + index * 0.1}s` }}
        ></div>
      </div>
    </div>
  );
}
export function SkeletonCardStaggered({ index = 0 }) {
  const animationDelay = `${index * 0.1}s`;
  
  return (
    <div 
      className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20"
      style={{ animationDelay }}
    >
      <div className="space-y-4">
        {/* Title with stagger */}
        <div 
          className="h-8 w-2/3 bg-white/5 rounded shimmer"
          style={{ animationDelay: `${0.1 + index * 0.1}s` }}
        ></div>

        {/* Year with stagger */}
        <div 
          className="h-5 w-20 bg-white/5 rounded shimmer"
          style={{ animationDelay: `${0.2 + index * 0.1}s` }}
        ></div>

        {/* Genres with stagger */}
        <div className="space-y-2">
          <div 
            className="h-4 w-16 bg-white/5 rounded shimmer"
            style={{ animationDelay: `${0.3 + index * 0.1}s` }}
          ></div>
          <div className="flex gap-2">
            {[0, 1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-6 w-20 bg-white/5 rounded-full shimmer"
                style={{ animationDelay: `${0.4 + (i * 0.1) + (index * 0.1)}s` }}
              ></div>
            ))}
          </div>
        </div>

        {/* Match score with stagger */}
        <div 
          className="h-4 w-28 bg-white/5 rounded shimmer"
          style={{ animationDelay: `${0.5 + index * 0.1}s` }}
        ></div>

        {/* Link with stagger */}
        <div 
          className="h-5 w-36 bg-white/5 rounded shimmer"
          style={{ animationDelay: `${0.6 + index * 0.1}s` }}
        ></div>
      </div>
    </div>
  );
}

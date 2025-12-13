export function SkeletonCardMinimal() {
  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
      {/* Compact skeleton */}
      <div className="space-y-3">
        <div className="h-7 w-3/4 bg-white/5 rounded shimmer"></div>
        <div className="h-5 w-1/2 bg-white/5 rounded shimmer"></div>
        <div className="flex gap-2">
          {[0, 1, 2].map((i) => (
            <div key={i} className="h-6 w-16 bg-white/5 rounded-full shimmer"></div>
          ))}
        </div>
        <div className="h-4 w-32 bg-white/5 rounded shimmer"></div>
      </div>
    </div>
  );
}

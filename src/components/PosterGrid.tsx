"use client";
import Image from "next/image";
import { useState } from "react";

interface PosterGridProps {
  movies: Array<{
    id?: string;
    title: string;
    poster_url?: string | null;
    year?: number | string;
  }>;
}

export default function PosterGrid({ movies }: PosterGridProps) {
  const [failed, setFailed] = useState<Record<string, boolean>>({});
  const eight = movies.slice(0, 8);
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 w-full">
      {eight.map((m, idx) => (
        <div key={m.id || `${m.title}-${idx}`} className="group">
          <div className="relative w-full aspect-[2/3] overflow-hidden rounded-xl shadow border border-white/10 bg-white/5">
            {m.poster_url && !failed[m.id || `${m.title}-${idx}`] ? (
              <Image
                src={m.poster_url.replace(/^http:\/\//, 'https://')}
                alt={m.title}
                fill
                sizes="(max-width: 640px) 50vw, 25vw"
                className="object-cover group-hover:scale-105 transition-transform duration-300"
                onError={() => setFailed((s) => ({ ...s, [m.id || `${m.title}-${idx}`]: true }))}
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-4xl">🎬</div>
            )}
          </div>
          <div className="mt-2 text-center">
            <p className="text-white text-sm font-medium truncate" title={m.title}>
              {m.title}
            </p>
            {m.year && (
              <p className="text-purple-200 text-xs">{m.year}</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}



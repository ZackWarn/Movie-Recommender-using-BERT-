import type { NextConfig } from "next";

// Force rebuild on Dec 9 - ensures latest frontend code deploys
const nextConfig: NextConfig = {
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: "https",
        hostname: "m.media-amazon.com",
      },
      {
        protocol: "https",
        hostname: "ia.media-imdb.com",
      },
      {
        protocol: "https",
        hostname: "imdb-api.com",
      },
      {
        protocol: "https",
        hostname: "image.tmdb.org",
      },
      {
        protocol: "https",
        hostname: "*.cloudfront.net",
      },
    ],
  },
};

export default nextConfig;

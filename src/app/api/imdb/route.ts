import { NextRequest } from "next/server";

// Simple proxy to RapidAPI IMDb endpoint to fetch movies with poster
// Expects env vars: RAPIDAPI_KEY
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const query = searchParams.get("q") || "popular";
  const take = Number(searchParams.get("take") || 8);

  const apiKey = process.env.RAPIDAPI_KEY;
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "Missing RAPIDAPI_KEY" }), {
      status: 500,
      headers: { "content-type": "application/json" },
    });
  }

  try {
    // The exact endpoint and params depend on the selected RapidAPI. Using imdb236 as provided.
    // We'll try a search followed by filtering for items with image/poster.
    const url = `https://imdb236.p.rapidapi.com/api/imdb/search?query=${encodeURIComponent(
      query
    )}`;

    const resp = await fetch(url, {
      method: "GET",
      headers: {
        "x-rapidapi-key": apiKey,
        "x-rapidapi-host": "imdb236.p.rapidapi.com",
      },
      // RapidAPI requires outbound fetch from server; ensure cache disabled for freshness
      cache: "no-store",
    });

    if (!resp.ok) {
      const text = await resp.text();
      return new Response(JSON.stringify({ error: text || "Upstream error" }), {
        status: 502,
        headers: { "content-type": "application/json" },
      });
    }

    const data = await resp.json();

    // Define interface for IMDB API response items
    interface ImdbItem {
      image?: { url?: string };
      poster?: string;
      poster_url?: string;
      primaryImage?: string;
      thumbnails?: Array<{ url?: string }>;
      id?: string;
      imdb_id?: string;
      imdbID?: string;
      const?: string;
      title?: string;
      l?: string;
      primaryTitle?: string;
      name?: string;
      year?: string | number;
      y?: string | number;
      startYear?: string | number;
    }

    // Normalize to array of items with poster
    const items: ImdbItem[] = Array.isArray(data?.results)
      ? data.results
      : Array.isArray(data)
      ? data
      : [];

    const movies = items
      .filter((it) => !!(it?.image || it?.poster || it?.poster_url || it?.primaryImage || (Array.isArray(it?.thumbnails) && it.thumbnails.length > 0)))
      .slice(0, take)
      .map((it) => {
        const poster =
          it.image?.url ||
          it.poster ||
          it.poster_url ||
          it.primaryImage ||
          (Array.isArray(it.thumbnails) && it.thumbnails[0]?.url) ||
          null;
        return {
          id: it.id || it.imdb_id || it.imdbID || it.const || undefined,
          title: it.title || it.l || it.primaryTitle || it.name || "Unknown",
          year: it.year || it.y || it.startYear || undefined,
          poster_url: poster,
        };
      });

    return new Response(JSON.stringify({ movies }), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  } catch (err: unknown) {
    const errorMessage = err instanceof Error ? err.message : "Unexpected error";
    return new Response(
      JSON.stringify({ error: errorMessage }),
      {
        status: 500,
        headers: { "content-type": "application/json" },
      }
    );
  }
}



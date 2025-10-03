import { NextRequest } from "next/server";

const FLASK_BASE_URL = process.env.FLASK_BASE_URL || "http://localhost:5000";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const resp = await fetch(`${FLASK_BASE_URL}/api/recommendations/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      cache: "no-store",
    });

    const text = await resp.text();
    return new Response(text, {
      status: resp.status,
      headers: { "content-type": resp.headers.get("content-type") || "application/json" },
    });
  } catch (err: any) {
    return new Response(
      JSON.stringify({ error: err?.message || "Proxy request failed" }),
      { status: 500, headers: { "content-type": "application/json" } }
    );
  }
}



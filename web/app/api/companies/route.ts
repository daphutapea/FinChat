import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "https://dahutapea-finchat-api.hf.space";

export const runtime = "nodejs";

export async function GET() {
  if (!BACKEND_URL) {
    return NextResponse.json([]);
  }
  try {
    const res = await fetch(`${BACKEND_URL}/companies`, {
      // Deliberately uncached: this call doubles as a wake-up ping on page load,
      // so a sleeping Space is already warming by the time the user asks. A cold
      // Space can otherwise exceed Vercel's 60s function limit and time out.
      cache: "no-store",
    });
    if (!res.ok) return NextResponse.json([]);
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json([]);
  }
}

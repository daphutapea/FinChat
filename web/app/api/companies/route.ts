import { NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "https://dahutapea-finchat-api.hf.space";

export const runtime = "nodejs";

export async function GET() {
  if (!BACKEND_URL) {
    return NextResponse.json([]);
  }
  try {
    const res = await fetch(`${BACKEND_URL}/companies`, {
      // Companies rarely change - let Next cache the list for an hour.
      next: { revalidate: 3600 },
    });
    if (!res.ok) return NextResponse.json([]);
    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json([]);
  }
}

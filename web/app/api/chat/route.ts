import { NextRequest, NextResponse } from "next/server";

// This route runs on the server (never in the browser), so BACKEND_URL and
// API_SECRET stay private. The browser only ever talks to /api/chat.
const BACKEND_URL = process.env.BACKEND_URL;
const API_SECRET = process.env.API_SECRET;

export const runtime = "nodejs";
// Allow up to 60s: the HF Space may be cold-starting, and the LLM call itself
// can take several seconds.
export const maxDuration = 60;

export async function POST(req: NextRequest) {
  if (!BACKEND_URL) {
    return NextResponse.json(
      { error: "Server is missing BACKEND_URL configuration." },
      { status: 500 }
    );
  }

  let body: { question?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid request body." }, { status: 400 });
  }

  const question = (body.question || "").trim();
  if (!question) {
    return NextResponse.json({ error: "Please enter a question." }, { status: 400 });
  }

  try {
    const res = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(API_SECRET ? { "X-API-Key": API_SECRET } : {}),
      },
      body: JSON.stringify({ question }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const detail =
        (data as { detail?: string; error?: string }).detail ||
        (data as { error?: string }).error ||
        "The FinChat engine returned an error.";
      return NextResponse.json({ error: detail }, { status: res.status });
    }
    return NextResponse.json(data);
  } catch {
    return NextResponse.json(
      {
        error:
          "Couldn't reach the FinChat engine — it may be waking up from sleep. Please try again in a moment.",
      },
      { status: 502 }
    );
  }
}

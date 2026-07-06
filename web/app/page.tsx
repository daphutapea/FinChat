"use client";

import { useEffect, useRef, useState } from "react";
import type { ChatResponse, Company, Source } from "@/lib/types";

interface Message {
  role: "user" | "assistant";
  content: string;
  routed_to?: string | null;
  sources?: Source[];
  error?: boolean;
}

const STARTERS = [
  "What products does Apple sell?",
  "What are Boeing's business segments?",
  "What is Apple's quick ratio?",
  "What are the main risks AMD identifies?",
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [companies, setCompanies] = useState<Company[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch("/api/companies")
      .then((r) => r.json())
      .then((data) => Array.isArray(data) && setCompanies(data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function send(question: string) {
    const q = question.trim();
    if (!q || loading) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: q }]);
    setLoading(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data: ChatResponse = await res.json();
      if (!res.ok || data.error) {
        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            content: data.error || "Something went wrong. Please try again.",
            error: true,
          },
        ]);
      } else {
        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            content: data.answer,
            routed_to: data.routed_to,
            sources: data.sources,
          },
        ]);
      }
    } catch {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content:
            "Couldn't reach the FinChat engine. Please try again in a moment.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send(input);
    }
  }

  const empty = messages.length === 0;

  return (
    <div className="flex h-screen bg-gradient-to-b from-slate-950 to-[#0b1526]">
      {/* ---------------- Sidebar ---------------- */}
      <aside className="hidden md:flex w-72 flex-col border-r border-white/5 bg-slate-950/40">
        <div className="flex items-center gap-2 px-5 py-5">
          <Logo />
          <div>
            <div className="text-lg font-semibold leading-none">FinChat</div>
            <div className="text-[11px] uppercase tracking-wider text-teal-400/80">
              10-K intelligence
            </div>
          </div>
        </div>

        <div className="px-5 pb-3">
          <p className="text-sm leading-relaxed text-slate-400">
            Ask plain-English questions about the SEC 10-K filings of major
            companies. Every answer is grounded in the source and cited.
          </p>
        </div>

        <div className="mt-2 flex items-center justify-between px-5 pb-2">
          <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
            Companies loaded
          </span>
          <span className="rounded-full bg-teal-500/10 px-2 py-0.5 text-xs font-semibold text-teal-300">
            {companies.length || 25}
          </span>
        </div>
        <div className="flex-1 space-y-1 overflow-y-auto px-3 pb-4">
          {companies.map((c) => (
            <div
              key={c.ticker}
              className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm text-slate-300 hover:bg-white/5"
            >
              <span className="w-14 shrink-0 font-mono text-xs font-semibold text-teal-300">
                {c.ticker}
              </span>
              <span className="truncate text-slate-400">{c.name}</span>
            </div>
          ))}
        </div>

        <div className="border-t border-white/5 px-5 py-3 text-[11px] text-slate-500">
          Source: recent SEC 10-K filings (FY2021-2024). Educational project -
          not financial advice.
        </div>
      </aside>

      {/* ---------------- Main ---------------- */}
      <main className="flex flex-1 flex-col">
        {/* Header (mobile-visible brand) */}
        <header className="flex items-center gap-2 border-b border-white/5 px-4 py-3 md:hidden">
          <Logo />
          <span className="font-semibold">FinChat</span>
        </header>

        {/* Messages */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto">
          <div className="mx-auto w-full max-w-3xl px-4 py-6">
            {empty ? (
              <Welcome onPick={send} />
            ) : (
              <div className="space-y-6">
                {messages.map((m, i) => (
                  <MessageBubble key={i} message={m} />
                ))}
                {loading && <TypingIndicator />}
              </div>
            )}
          </div>
        </div>

        {/* Composer */}
        <div className="border-t border-white/5 bg-slate-950/60 px-4 py-3">
          <div className="mx-auto flex w-full max-w-3xl items-end gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKeyDown}
              rows={1}
              placeholder="Ask about a company's 10-K - e.g. What were AMD's main risk factors?"
              className="max-h-40 flex-1 resize-none rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-teal-500/50 focus:outline-none focus:ring-2 focus:ring-teal-500/20"
            />
            <button
              onClick={() => send(input)}
              disabled={loading || !input.trim()}
              className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-teal-500 text-slate-950 transition hover:bg-teal-400 disabled:cursor-not-allowed disabled:opacity-40"
              aria-label="Send"
            >
              <SendIcon />
            </button>
          </div>
          <p className="mx-auto mt-2 max-w-3xl text-center text-[11px] text-slate-600">
            FinChat can only answer from the 25 filings it has. It will say so
            when something isn&apos;t in them.
          </p>
        </div>
      </main>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Sub-components                                                      */
/* ------------------------------------------------------------------ */

function Welcome({ onPick }: { onPick: (q: string) => void }) {
  return (
    <div className="animate-fade-in pt-8 text-center">
      <div className="mx-auto mb-5 grid h-14 w-14 place-items-center rounded-2xl bg-teal-500/10 ring-1 ring-teal-500/30">
        <Logo size={28} />
      </div>
      <h1 className="text-2xl font-semibold text-slate-100">
        Chat with SEC 10-K filings
      </h1>
      <p className="mx-auto mt-2 max-w-md text-sm text-slate-400">
        Grounded, cited answers about 25 major companies&apos; annual reports -
        including financial figures and ratios computed from the filings.
      </p>
      <div className="mx-auto mt-8 grid max-w-xl grid-cols-1 gap-2 sm:grid-cols-2">
        {STARTERS.map((s) => (
          <button
            key={s}
            onClick={() => onPick(s)}
            className="rounded-xl border border-white/10 bg-slate-900/50 px-4 py-3 text-left text-sm text-slate-300 transition hover:border-teal-500/40 hover:bg-slate-900"
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  if (isUser) {
    return (
      <div className="flex animate-fade-in justify-end">
        <div className="max-w-[85%] rounded-2xl rounded-br-md bg-teal-500 px-4 py-2.5 text-sm text-slate-950">
          {message.content}
        </div>
      </div>
    );
  }
  return (
    <div className="flex animate-fade-in gap-3">
      <div className="mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-slate-800 ring-1 ring-white/10">
        <Logo size={16} />
      </div>
      <div className="min-w-0 flex-1">
        <div
          className={`whitespace-pre-wrap text-sm leading-relaxed ${
            message.error ? "text-amber-300" : "text-slate-200"
          }`}
        >
          {message.content}
        </div>
        {message.routed_to && (
          <div className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-slate-800/70 px-2.5 py-1 text-xs text-slate-400">
            <span className="text-teal-400">◎</span> Routed to{" "}
            <span className="font-mono font-semibold text-teal-300">
              {message.routed_to}
            </span>
          </div>
        )}
        {message.sources && message.sources.length > 0 && (
          <Sources sources={message.sources} />
        )}
      </div>
    </div>
  );
}

function Sources({ sources }: { sources: Source[] }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="mt-3">
      <button
        onClick={() => setOpen((o) => !o)}
        className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-teal-300"
      >
        <span className={`transition ${open ? "rotate-90" : ""}`}>▸</span>
        {sources.length} source{sources.length > 1 ? "s" : ""}
      </button>
      {open && (
        <div className="mt-2 space-y-2">
          {sources.map((s) => (
            <div
              key={s.index}
              className="rounded-lg border border-white/5 bg-slate-900/50 p-3"
            >
              <div className="mb-1 flex items-center gap-2 text-xs font-semibold text-teal-300">
                <span className="text-slate-500">[{s.index}]</span>
                {s.source || "source"}
                {s.type === "financials" && (
                  <span className="rounded bg-cyan-500/10 px-1.5 py-0.5 text-[10px] font-medium text-cyan-300">
                    XBRL
                  </span>
                )}
              </div>
              <p className="text-xs leading-relaxed text-slate-400">
                {s.excerpt}
                {s.excerpt.length >= 500 ? "..." : ""}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex animate-fade-in gap-3">
      <div className="mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-slate-800 ring-1 ring-white/10">
        <Logo size={16} />
      </div>
      <div className="flex items-center gap-1 pt-2">
        <Dot delay="0s" />
        <Dot delay="0.2s" />
        <Dot delay="0.4s" />
        <span className="ml-2 text-xs text-slate-500">
          Searching the filings...
        </span>
      </div>
    </div>
  );
}

function Dot({ delay }: { delay: string }) {
  return (
    <span
      className="h-1.5 w-1.5 rounded-full bg-teal-400 animate-blink"
      style={{ animationDelay: delay }}
    />
  );
}

function Logo({ size = 20 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M4 5.5A1.5 1.5 0 0 1 5.5 4h13A1.5 1.5 0 0 1 20 5.5v9A1.5 1.5 0 0 1 18.5 16H9l-4 4v-4H5.5A1.5 1.5 0 0 1 4 14.5v-9Z"
        fill="#0D9488"
      />
      <path
        d="M8 12.5l2.3-2.6 2 1.7L15.5 8"
        stroke="#38BDF8"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <path
        d="M4 12l16-8-8 16-2.5-6.5L4 12Z"
        fill="currentColor"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinejoin="round"
      />
    </svg>
  );
}

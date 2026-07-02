"""Evaluate FinChat against the FinanceBench benchmark (corpus-aligned subset).

Runs FinChat on every FinanceBench 10-K question whose company + fiscal year is
present in our EDGAR corpus, then grades each answer against FinanceBench's gold
answer with an LLM-as-judge. Writes eval/results.md.

FinanceBench is a deliberately hard, expert-written benchmark, so the goal is an
honest, measured score on real questions — not a perfect one.

Run from the project root:
    python -m eval.run_eval
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

# Make `src` and `eval` importable no matter how this is launched.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datasets import load_dataset
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from src import config
from src.rag import answer, get_llm

# Cap the number of questions so a full run fits Groq's free-tier daily token
# budget. Sampled with an even stride across companies for representativeness.
MAX_QUESTIONS = 30
# Grade with a small, cheap, high-rate-limit model (judging is easy); this
# keeps the expensive 70B model's token budget for answering.
JUDGE_MODEL = "llama-3.1-8b-instant"
_judge_llm = None


def get_judge_llm() -> ChatGroq:
    global _judge_llm
    if _judge_llm is None:
        _judge_llm = ChatGroq(model=JUDGE_MODEL, temperature=0.0, max_retries=5)
    return _judge_llm

# Windows consoles default to cp1252 and crash when print() emits Unicode
# (curly quotes etc. from FinanceBench questions). Force UTF-8 output.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# FinanceBench company name -> ticker (aligned with config.TARGET_FILINGS).
FB_COMPANY_TO_TICKER = {
    "AMD": "AMD", "American Express": "AXP", "Boeing": "BA", "PepsiCo": "PEP",
    "Amcor": "AMCR", "3M": "MMM", "Johnson & Johnson": "JNJ", "CVS Health": "CVS",
    "Pfizer": "PFE", "AES Corporation": "AES", "Verizon": "VZ", "Best Buy": "BBY",
    "Adobe": "ADBE", "Ulta Beauty": "ULTA", "Coca-Cola": "KO", "Microsoft": "MSFT",
    "Nike": "NKE", "Corning": "GLW",
}

JUDGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You grade a financial question-answering system against a reference "
            "answer from the FinanceBench benchmark.\n"
            "Grade CORRECT if the system answer agrees with the reference on the "
            "key fact(s) or number(s) (minor wording or rounding is fine), "
            "PARTIAL if it is partially right or incomplete, and INCORRECT if it "
            "is wrong, empty, or says it cannot find the answer.\n"
            "Respond in EXACTLY this format:\n"
            "VERDICT: <CORRECT|PARTIAL|INCORRECT>\n"
            "REASON: <one short sentence>",
        ),
        (
            "human",
            "QUESTION:\n{question}\n\nREFERENCE ANSWER:\n{reference}\n\n"
            "SYSTEM ANSWER:\n{system}",
        ),
    ]
)
SCORE = {"CORRECT": 1.0, "PARTIAL": 0.5, "INCORRECT": 0.0}


def judge(question: str, reference: str, system: str) -> tuple[str, str]:
    text = (JUDGE_PROMPT | get_judge_llm()).invoke(
        {"question": question, "reference": reference, "system": system}
    ).content
    v = re.search(r"VERDICT:\s*(CORRECT|PARTIAL|INCORRECT)", text, re.I)
    r = re.search(r"REASON:\s*(.+)", text, re.I)
    verdict = v.group(1).upper() if v else "INCORRECT"
    reason = r.group(1).strip() if r else "(unparsed)"
    return verdict, reason


def select_questions() -> list[dict]:
    """FinanceBench 10-K questions whose (company, fiscal year) is in our corpus."""
    ingested = {(t, str(y)) for t, _name, y in config.TARGET_FILINGS}
    fb = load_dataset("PatronusAI/financebench", split="train")
    picked = []
    for ex in fb:
        if "10K" not in str(ex.get("doc_name", "")):
            continue
        ticker = FB_COMPANY_TO_TICKER.get(str(ex.get("company")))
        if ticker and (ticker, str(ex.get("doc_period"))) in ingested:
            picked.append(ex)
    return picked


def main() -> None:
    rows = select_questions()
    if len(rows) > MAX_QUESTIONS:                    # even-stride sample
        stride = len(rows) // MAX_QUESTIONS
        rows = rows[::stride][:MAX_QUESTIONS]
    print(f"Evaluating {len(rows)} corpus-aligned FinanceBench 10-K questions.\n")

    results = []
    total = 0.0
    for ex in rows:
        res = answer(ex["question"])
        verdict, reason = judge(ex["question"], ex.get("answer", ""), res["answer"])
        total += SCORE[verdict]
        results.append((ex, res, verdict, reason))
        print(f"[{verdict:9}] {ex.get('company')}: {ex['question'][:70]}")
        time.sleep(1.0)   # ease off the free-tier rate limit

    n = len(rows)
    accuracy = total / n if n else 0.0
    correct = sum(1 for _e, _r, v, _j in results if v == "CORRECT")
    partial = sum(1 for _e, _r, v, _j in results if v == "PARTIAL")

    lines = [
        "# FinChat Evaluation — FinanceBench (corpus-aligned subset)\n",
        "FinChat is graded by an LLM-as-judge against gold answers from the "
        "[FinanceBench](https://huggingface.co/datasets/PatronusAI/financebench) "
        "benchmark, on every 10-K question whose company + fiscal year is in the "
        "corpus. FinanceBench is expert-written and intentionally hard.\n",
        f"- **Questions evaluated:** {n}",
        f"- **CORRECT:** {correct}   **PARTIAL:** {partial}   "
        f"**INCORRECT:** {n - correct - partial}",
        f"- **Score:** {total:.1f} / {n}",
        f"- **Accuracy (CORRECT=1.0, PARTIAL=0.5):** {accuracy:.0%}\n",
    ]

    # Accuracy by FinanceBench question type -> shows the qualitative-vs-numeric
    # split (metrics-generated questions require computation over tables).
    by_type: dict[str, list[float]] = {}
    for ex, _res, verdict, _reason in results:
        agg = by_type.setdefault(str(ex.get("question_type", "unknown")), [0.0, 0])
        agg[0] += SCORE[verdict]
        agg[1] += 1
    print("\nAccuracy by question type:")
    lines += ["**Accuracy by FinanceBench question type:**\n",
              "| Question type | Accuracy | N |", "|---|---|---|"]
    for qt, (s, c) in sorted(by_type.items()):
        print(f"  {qt:24} {s / c:.0%}  ({c})")
        lines.append(f"| {qt} | {s / c:.0%} | {c} |")

    lines += ["\n| # | Company | FY | Verdict | Question |",
              "|---|---------|----|---------|----------|"]
    for i, (ex, _res, verdict, _reason) in enumerate(results, 1):
        q = ex["question"].replace("|", "\\|")
        lines.append(
            f"| {i} | {ex.get('company')} | {ex.get('doc_period')} | {verdict} | {q} |"
        )

    lines += ["\n---\n", "## Detailed results\n"]
    for i, (ex, res, verdict, reason) in enumerate(results, 1):
        lines += [
            f"### {i}. {ex['question']}",
            f"- **Company / FY:** {ex.get('company')} {ex.get('doc_period')}  |  "
            f"**Routed to:** {res['routed_to']}  |  **Verdict:** {verdict}",
            f"- **Judge:** {reason}",
            f"- **FinanceBench gold:** {ex.get('answer', '')}",
            f"- **FinChat:** {res['answer']}\n",
        ]

    out_path = Path(__file__).resolve().parent / "results.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nAccuracy: {accuracy:.0%}  ({total:.1f}/{n})  ->  wrote {out_path}")


if __name__ == "__main__":
    main()

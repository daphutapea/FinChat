"""Qualitative capability evaluation for FinChat.

Runs FinChat on the curated qualitative gold set (business/segments/products --
the document-Q&A task FinChat is designed for) and grades each answer against a
reference with an LLM-as-judge. Writes eval/gold_results.md.

Complements run_eval.py (FinanceBench), which is dominated by numeric questions.

Run from the project root:
    python -m eval.run_gold
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from src.rag import answer
from eval.gold_set import GOLD_SET

JUDGE_MODEL = "llama-3.1-8b-instant"
_judge_llm = None


def get_judge_llm() -> ChatGroq:
    global _judge_llm
    if _judge_llm is None:
        _judge_llm = ChatGroq(model=JUDGE_MODEL, temperature=0.0, max_retries=5)
    return _judge_llm


JUDGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You grade a financial question-answering system against a reference "
            "answer.\n"
            "Grade CORRECT if the system answer conveys the key facts of the "
            "reference (minor omissions or extra detail are fine), PARTIAL if it "
            "captures some but misses important parts, and INCORRECT if it is "
            "wrong, empty, or says it cannot find the answer.\n"
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
    return (v.group(1).upper() if v else "INCORRECT",
            r.group(1).strip() if r else "(unparsed)")


def main() -> None:
    print(f"Evaluating {len(GOLD_SET)} qualitative capability questions.\n")
    results = []
    total = 0.0
    for item in GOLD_SET:
        res = answer(item["question"])
        verdict, reason = judge(item["question"], item["reference"], res["answer"])
        total += SCORE[verdict]
        results.append((item, res, verdict, reason))
        print(f"[{verdict:9}] {item['company']}: {item['question']}")
        time.sleep(1.0)

    n = len(GOLD_SET)
    accuracy = total / n if n else 0.0
    correct = sum(1 for _i, _r, v, _j in results if v == "CORRECT")
    partial = sum(1 for _i, _r, v, _j in results if v == "PARTIAL")

    lines = [
        "# FinChat Evaluation — Qualitative Capability Gold Set\n",
        "FinChat is graded by an LLM-as-judge on document-Q&A questions "
        "(business, segments, products) across the corpus -- the task "
        "it is designed for. Reference answers are drawn from the 10-K filings.\n",
        f"- **Questions:** {n}",
        f"- **CORRECT:** {correct}   **PARTIAL:** {partial}   "
        f"**INCORRECT:** {n - correct - partial}",
        f"- **Accuracy (CORRECT=1.0, PARTIAL=0.5):** {accuracy:.0%}\n",
        "| # | Company | Verdict | Question |",
        "|---|---------|---------|----------|",
    ]
    for i, (item, _res, verdict, _reason) in enumerate(results, 1):
        lines.append(f"| {i} | {item['company']} | {verdict} | {item['question']} |")

    lines += ["\n---\n", "## Detailed results\n"]
    for i, (item, res, verdict, reason) in enumerate(results, 1):
        lines += [
            f"### {i}. {item['question']}",
            f"- **Company:** {item['company']}  |  "
            f"**Routed to:** {res['routed_to']}  |  **Verdict:** {verdict}",
            f"- **Judge:** {reason}",
            f"- **Reference:** {item['reference']}",
            f"- **FinChat:** {res['answer']}\n",
        ]

    out_path = Path(__file__).resolve().parent / "gold_results.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nCapability accuracy: {accuracy:.0%}  ({total:.1f}/{n})  ->  wrote {out_path}")


if __name__ == "__main__":
    main()

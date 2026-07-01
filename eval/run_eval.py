"""Evaluate FinChat on the curated gold set with an LLM-as-judge score.

For each question, FinChat produces an answer, then a separate LLM "judge"
grades that answer against the reference: CORRECT (1.0), PARTIAL (0.5), or
INCORRECT (0.0). Results and the overall accuracy are written to
eval/results.md.

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

from langchain_core.prompts import ChatPromptTemplate

from src.rag import answer, get_llm
from eval.gold_set import GOLD_SET

JUDGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You grade a financial question-answering system against a reference "
            "answer.\n"
            "Grade CORRECT if the system answer conveys the key facts of the "
            "reference (minor omissions or extra detail are fine), PARTIAL if it "
            "captures some but misses important parts, and INCORRECT if it is "
            "wrong, empty, or unsupported.\n"
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
    text = (JUDGE_PROMPT | get_llm()).invoke(
        {"question": question, "reference": reference, "system": system}
    ).content
    v = re.search(r"VERDICT:\s*(CORRECT|PARTIAL|INCORRECT)", text, re.I)
    r = re.search(r"REASON:\s*(.+)", text, re.I)
    verdict = v.group(1).upper() if v else "INCORRECT"
    reason = r.group(1).strip() if r else "(unparsed)"
    return verdict, reason


def main() -> None:
    results = []
    total = 0.0

    for i, item in enumerate(GOLD_SET, 1):
        res = answer(item["question"])
        verdict, reason = judge(item["question"], item["reference"], res["answer"])
        total += SCORE[verdict]
        results.append((item, res, verdict, reason))
        print(f"[{verdict:9}] {item['company']:5} {item['question']}")
        time.sleep(1.0)   # be gentle with the free-tier rate limit

    n = len(GOLD_SET)
    accuracy = total / n if n else 0.0
    correct = sum(1 for _, _, v, _ in results if v == "CORRECT")
    partial = sum(1 for _, _, v, _ in results if v == "PARTIAL")

    lines = [
        "# FinChat Evaluation — Curated Gold Set\n",
        "FinChat is graded by an LLM-as-judge against reference answers written "
        "from the 2017-2020 10-K filings in the corpus.\n",
        f"- **Questions:** {n}",
        f"- **CORRECT:** {correct}   **PARTIAL:** {partial}   "
        f"**INCORRECT:** {n - correct - partial}",
        f"- **Score:** {total:.1f} / {n}",
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

    out_path = Path(__file__).resolve().parent / "results.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nAccuracy: {accuracy:.0%}  ({total:.1f}/{n})  ->  wrote {out_path}")


if __name__ == "__main__":
    main()

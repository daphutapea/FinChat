"""Extract structured financial figures from a 10-K's XBRL data.

SEC filings carry machine-readable XBRL financials. We pull the income
statement, balance sheet, and cash-flow statement as clean "label: value"
facts and index them alongside the filing text, so FinChat can answer numeric
questions (revenue, net income, assets, ...) that plain text RAG cannot -- the
tables in the filing text collapse into unusable "number soup".
"""
from __future__ import annotations

import re

import pandas as pd
from langchain_core.documents import Document

_STATEMENTS = [
    ("income_statement", "Income Statement"),
    ("balance_sheet", "Balance Sheet"),
    ("cash_flow_statement", "Cash Flow Statement"),
]
# Synonyms in the chunk header so numeric queries retrieve these chunks.
_KEYWORDS = ("revenue, sales, income, earnings, profit, margin, assets, "
            "liabilities, equity, cash flow, expenses, EPS")


def _fmt(value, label: str = "") -> str | None:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if pd.isna(v):
        return None
    a = abs(v)
    if "shares" in label.lower() and "per share" not in label.lower():
        if a >= 1e9:
            return f"{v / 1e9:,.2f} billion shares"
        if a >= 1e6:
            return f"{v / 1e6:,.1f} million shares"
        return f"{v:,.0f} shares"
    if a >= 1e9:
        return f"${v / 1e9:,.2f} billion"
    if a >= 1e6:
        return f"${v / 1e6:,.1f} million"
    if a >= 1000:
        return f"${v:,.0f}"
    return f"{v:,.2f}"


def _value_column(df: pd.DataFrame, fiscal_year: int):
    """The statement column for the filing's primary fiscal year."""
    date_cols = [c for c in df.columns if re.match(r"\d{4}-\d{2}-\d{2}", str(c))]
    for c in date_cols:
        if str(c).startswith(str(fiscal_year)):
            return c
    return date_cols[0] if date_cols else None


def _statement_lines(stmt, fiscal_year: int) -> list[str]:
    try:
        df = stmt.to_dataframe()
    except Exception:
        return []
    col = _value_column(df, fiscal_year)
    if col is None:
        return []
    lines = []
    for _, row in df.iterrows():
        # skip section headers, per-dimension breakdowns, sub-members
        if row.get("abstract") or row.get("is_breakdown") or row.get("dimension"):
            continue
        label = str(row.get("label") or "").strip()
        if not label:
            continue
        value = _fmt(row.get(col), label)
        if value is None:
            continue
        lines.append(f"{label}: {value}")
    return lines


def financial_documents(filing, ticker: str, company: str,
                        fiscal_year: int) -> list[Document]:
    """One Document per financial statement, built from the filing's XBRL data."""
    try:
        tenk = filing.obj()
    except Exception:
        return []

    docs: list[Document] = []
    for attr, name in _STATEMENTS:
        stmt = getattr(tenk, attr, None)
        if stmt is None:
            continue
        lines = _statement_lines(stmt, fiscal_year)
        if not lines:
            continue
        header = (
            f"{company} ({ticker}) FY{fiscal_year} {name} "
            f"(financial figures: {_KEYWORDS}; from SEC XBRL data):"
        )
        docs.append(
            Document(
                page_content=header + "\n" + "\n".join(lines),
                metadata={
                    "ticker": ticker,
                    "company": company,
                    "year": str(fiscal_year),
                    "accession": filing.accession_no,
                    "source": f"{company} 10-K (FY{fiscal_year}) - {name} (XBRL)",
                    "type": "financials",
                },
            )
        )
    return docs

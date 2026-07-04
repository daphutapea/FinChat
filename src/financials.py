"""Extract structured financial figures + computed ratios from a 10-K's XBRL data.

SEC filings carry machine-readable XBRL financials. We pull the income
statement, balance sheet, and cash-flow statement as clean "label: value"
facts, AND compute standard ratios (margins, liquidity, returns, leverage,
free cash flow) deterministically in Python, then index them alongside the
filing text.

This lets FinChat answer numeric questions -- both direct figures ("revenue")
and computed metrics ("quick ratio", "operating margin") -- that plain text RAG
cannot, because the filing's tables collapse into unusable "number soup" and
LLMs are unreliable at arithmetic.
"""
from __future__ import annotations

import re
from collections import defaultdict

import pandas as pd
from langchain_core.documents import Document

_STATEMENTS = [
    ("income_statement", "Income Statement"),
    ("balance_sheet", "Balance Sheet"),
    ("cash_flow_statement", "Cash Flow Statement"),
]
_KEYWORDS = ("revenue, sales, income, earnings, profit, margin, assets, "
            "liabilities, equity, cash flow, expenses, EPS")
_RATIO_KEYWORDS = ("margin, ratio, return, ROE, ROA, liquidity, leverage, "
                  "profitability, quick ratio, current ratio, debt, free cash flow")


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


def _money(v: float) -> str:
    a = abs(v)
    if a >= 1e9:
        return f"${v / 1e9:,.2f} billion"
    if a >= 1e6:
        return f"${v / 1e6:,.1f} million"
    return f"${v:,.0f}"


def _value_column(df: pd.DataFrame, fiscal_year: int):
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


# --- computed ratios --------------------------------------------------------

def _collect_figures(tenk, fiscal_year: int) -> dict[str, list]:
    """Map each XBRL standard_concept -> list of (label, value) for the year."""
    figs: dict[str, list] = defaultdict(list)
    for attr, _name in _STATEMENTS:
        stmt = getattr(tenk, attr, None)
        if stmt is None:
            continue
        try:
            df = stmt.to_dataframe()
        except Exception:
            continue
        col = _value_column(df, fiscal_year)
        if col is None:
            continue
        for _, row in df.iterrows():
            if row.get("is_breakdown") or row.get("dimension"):
                continue
            std = str(row.get("standard_concept") or "").strip()
            if not std or std == "nan":
                continue
            try:
                v = float(row.get(col))
            except (TypeError, ValueError):
                continue
            if not pd.isna(v):
                figs[std].append((str(row.get("label")), v))
    return figs


def _first(figs, concept):
    return figs[concept][0][1] if figs.get(concept) else None


def _operating_cash_flow(figs):
    rows = figs.get("NetCashFromOperatingActivities", [])
    for label, v in rows:
        if "operating activ" in label.lower():   # the total line
            return v
    return None


def _compute_ratios(figs) -> dict[str, str]:
    """Standard ratios, computed only where inputs are reliable for the sector."""
    rev = _first(figs, "Revenue")
    ni = _first(figs, "NetIncome") or _first(figs, "ProfitLoss")
    total_assets = _first(figs, "LiabilitiesAndEquity")   # == total assets
    equity = _first(figs, "AllEquityBalance")
    ca = _first(figs, "CurrentAssetsTotal")
    cl = _first(figs, "CurrentLiabilitiesTotal")
    inv = _first(figs, "Inventories") or 0
    ltd = _first(figs, "LongTermDebt") or 0
    std = _first(figs, "ShortTermDebt") or 0
    capex = _first(figs, "CapitalExpenses")
    ocf = _operating_cash_flow(figs)

    # Banks / financials have no classified balance sheet (no current assets),
    # and their revenue/COGS concepts are unreliable -> only compute ROA & ROE.
    is_financial = ca is None

    pct = lambda x: f"{x * 100:.1f}%"
    rat = lambda x: f"{x:.2f}"
    m: dict[str, str] = {}

    if not is_financial and rev:
        gp = _first(figs, "GrossProfit")
        cogs = _first(figs, "CostOfGoodsAndServicesSold")
        if gp is None and cogs is not None:
            gp = rev - cogs
        oi = _first(figs, "OperatingIncomeLoss")
        for name, num in (("Gross margin", gp), ("Operating margin", oi),
                          ("Net profit margin", ni)):
            if num is not None and abs(num / rev) <= 1.5:   # guard mis-maps
                m[name] = pct(num / rev)
        if capex is not None:
            m["Capital expenditure as % of revenue"] = pct(abs(capex) / rev)
        if total_assets:
            m["Asset turnover"] = rat(rev / total_assets)

    if ni is not None and total_assets:
        m["Return on assets (ROA)"] = pct(ni / total_assets)
    if ni is not None and equity:
        m["Return on equity (ROE)"] = pct(ni / equity)

    if not is_financial and ca and cl and cl > 0:
        m["Current ratio"] = rat(ca / cl)
        m["Quick ratio"] = rat((ca - inv) / cl)
    if not is_financial and equity and (ltd or std):
        m["Debt-to-equity ratio"] = rat((ltd + std) / equity)
    if not is_financial and ocf is not None and capex is not None:
        m["Free cash flow (operating cash flow - capex)"] = _money(ocf - abs(capex))

    return m


def financial_documents(filing, ticker: str, company: str,
                        fiscal_year: int) -> list[Document]:
    """Documents: one per financial statement + one of computed key ratios."""
    try:
        tenk = filing.obj()
    except Exception:
        return []

    def _doc(name: str, content: str) -> Document:
        return Document(
            page_content=content,
            metadata={
                "ticker": ticker,
                "company": company,
                "year": str(fiscal_year),
                "accession": filing.accession_no,
                "source": f"{company} 10-K (FY{fiscal_year}) - {name} (XBRL)",
                "type": "financials",
            },
        )

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
        docs.append(_doc(name, header + "\n" + "\n".join(lines)))

    ratios = _compute_ratios(_collect_figures(tenk, fiscal_year))
    if ratios:
        header = (
            f"{company} ({ticker}) FY{fiscal_year} Key Financial Ratios "
            f"(computed from SEC XBRL data - {_RATIO_KEYWORDS}):"
        )
        body = "\n".join(f"{k}: {v}" for k, v in ratios.items())
        docs.append(_doc("Key Ratios", header + "\n" + body))

    return docs

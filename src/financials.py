"""Extract structured figures, computed ratios, and YoY trends from XBRL data.

SEC filings carry machine-readable XBRL financials. For each filing we build:
  * one "label: value" chunk per statement (income / balance / cash flow),
  * a "Key Ratios" chunk (margins, liquidity, returns, leverage, turnover,
    EBITDA, free cash flow) computed deterministically in Python, and
  * a "Financial Trends (YoY)" chunk comparing this year to the prior year.

This lets FinChat answer numeric questions -- direct figures, computed metrics,
and year-over-year comparisons -- that plain text RAG cannot (the filing's
tables collapse into unusable "number soup", and LLMs are unreliable at math).
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
_RATIO_KEYWORDS = ("margin, ratio, return, ROE, ROA, EBITDA, liquidity, leverage, "
                  "turnover, profitability, quick ratio, current ratio, debt, "
                  "free cash flow")
_TREND_KEYWORDS = ("year-over-year, YoY, trend, change, improved, declined, grew, "
                  "growth, increase, decrease, historical, compared to prior year")

# Figures to show in the year-over-year trends chunk.
_TREND_FIGURES = [
    ("Revenue", "Revenue"),
    ("Gross profit", "GrossProfit"),
    ("Operating income", "OperatingIncomeLoss"),
    ("Net income", "NetIncome"),
    ("Total assets", "LiabilitiesAndEquity"),
    ("Property, plant & equipment (net)", "PlantPropertyEquipmentNet"),
    ("Inventory", "Inventories"),
]


# --- formatting -------------------------------------------------------------

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
    return _money(v) if a >= 1000 else f"{v:,.2f}"


def _money(v: float) -> str:
    a = abs(v)
    if a >= 1e9:
        return f"${v / 1e9:,.2f} billion"
    if a >= 1e6:
        return f"${v / 1e6:,.1f} million"
    return f"${v:,.0f}"


def _fmt_metric(value: float, kind: str) -> str:
    if kind == "pct":
        return f"{value * 100:.1f}%"
    if kind == "x":
        return f"{value:.2f}"
    return _money(value)


# --- extraction -------------------------------------------------------------

def _value_column(df: pd.DataFrame, year: int):
    date_cols = [c for c in df.columns if re.match(r"\d{4}-\d{2}-\d{2}", str(c))]
    for c in date_cols:
        if str(c).startswith(str(year)):
            return c
    return None


def _statement_lines(stmt, year: int) -> list[str]:
    try:
        df = stmt.to_dataframe()
    except Exception:
        return []
    col = _value_column(df, year)
    if col is None:
        # primary statement may label the column with the filing year only
        col = next((c for c in df.columns if re.match(r"\d{4}-\d{2}-\d{2}", str(c))),
                   None)
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


def _collect_figures(tenk, year: int) -> dict[str, list]:
    """{standard_concept: [(label, value), ...]} for a given fiscal year."""
    figs: dict[str, list] = defaultdict(list)
    for attr, _name in _STATEMENTS:
        stmt = getattr(tenk, attr, None)
        if stmt is None:
            continue
        try:
            df = stmt.to_dataframe()
        except Exception:
            continue
        col = _value_column(df, year)
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
    for label, v in figs.get("NetCashFromOperatingActivities", []):
        if "operating activ" in label.lower():
            return v
    return None


# --- ratios -----------------------------------------------------------------

def _compute_ratios(figs) -> dict[str, tuple[float, str]]:
    """{name: (value, kind)} -- computed only where inputs are reliable."""
    g = lambda c: _first(figs, c)
    rev = g("Revenue")
    ni = g("NetIncome") or g("ProfitLoss")
    ta = g("LiabilitiesAndEquity")            # == total assets (identity)
    eq = g("AllEquityBalance")
    ca, cl = g("CurrentAssetsTotal"), g("CurrentLiabilitiesTotal")
    inv = g("Inventories")
    ltd, std = g("LongTermDebt") or 0, g("ShortTermDebt") or 0
    capex, ocf = g("CapitalExpenses"), _operating_cash_flow(figs)
    da, ppe, rec = g("DepreciationExpense"), g("PlantPropertyEquipmentNet"), g("TradeReceivables")
    oi, cogs = g("OperatingIncomeLoss"), g("CostOfGoodsAndServicesSold")

    # Banks / financials: no classified balance sheet, unreliable revenue/COGS.
    is_financial = ca is None
    m: dict[str, tuple[float, str]] = {}

    if not is_financial and rev:
        gp = g("GrossProfit")
        if gp is None and cogs is not None:
            gp = rev - cogs
        for name, num in (("Gross margin", gp), ("Operating margin", oi),
                          ("Net profit margin", ni)):
            if num is not None and abs(num / rev) <= 1.5:
                m[name] = (num / rev, "pct")
        if capex is not None:
            m["Capital expenditure as % of revenue"] = (abs(capex) / rev, "pct")
        if ta:
            m["Asset turnover"] = (rev / ta, "x")
        if cogs is not None and inv:
            m["Inventory turnover"] = (cogs / inv, "x")
        if rec:
            m["Receivables turnover"] = (rev / rec, "x")
        if oi is not None and da is not None:
            ebitda = oi + da
            m["EBITDA"] = (ebitda, "money")
            if capex is not None:
                m["EBITDA less capex"] = (ebitda - abs(capex), "money")

    if ni is not None and ta:
        m["Return on assets (ROA)"] = (ni / ta, "pct")
    if ni is not None and eq:
        m["Return on equity (ROE)"] = (ni / eq, "pct")
    if not is_financial and ca and cl and cl > 0:
        m["Current ratio"] = (ca / cl, "x")
        m["Quick ratio"] = ((ca - (inv or 0)) / cl, "x")
    if not is_financial and eq and (ltd or std):
        m["Debt-to-equity ratio"] = ((ltd + std) / eq, "x")
    if not is_financial and ta and ppe:
        m["Property, plant & equipment as % of assets"] = (ppe / ta, "pct")
    if not is_financial and ocf is not None and capex is not None:
        fcf = ocf - abs(capex)
        m["Free cash flow"] = (fcf, "money")
        if ni:
            m["Free cash flow conversion (FCF / net income)"] = (fcf / ni, "pct")
    return m


def _trend_line(name, cur, prev, kind, cy, py) -> str:
    cs, ps = _fmt_metric(cur, kind), _fmt_metric(prev, kind)
    if kind == "pct":
        d = (cur - prev) * 100
        w = "increased" if d > 0.05 else "decreased" if d < -0.05 else "roughly unchanged"
        return f"{name}: FY{cy} {cs} vs FY{py} {ps} ({w} {abs(d):.1f} pp)"
    if prev == 0:
        return f"{name}: FY{cy} {cs} vs FY{py} {ps}"
    d = (cur - prev) / abs(prev) * 100
    w = "up" if d > 0.5 else "down" if d < -0.5 else "roughly flat"
    return f"{name}: FY{cy} {cs} vs FY{py} {ps} ({w} {abs(d):.1f}%)"


def _trend_lines(figs_cur, figs_prev, cy, py) -> list[str]:
    lines = []
    for name, concept in _TREND_FIGURES:
        cur, prev = _first(figs_cur, concept), _first(figs_prev, concept)
        if cur is not None and prev is not None:
            lines.append(_trend_line(name, cur, prev, "money", cy, py))
    rc, rp = _compute_ratios(figs_cur), _compute_ratios(figs_prev)
    for name, (cur, kind) in rc.items():
        if name in rp:
            lines.append(_trend_line(name, cur, rp[name][0], kind, cy, py))
    return lines


# --- documents --------------------------------------------------------------

def financial_documents(filing, ticker: str, company: str,
                        fiscal_year: int) -> list[Document]:
    try:
        tenk = filing.obj()
    except Exception:
        return []

    def _doc(name: str, content: str) -> Document:
        return Document(
            page_content=content,
            metadata={
                "ticker": ticker, "company": company, "year": str(fiscal_year),
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
        if lines:
            header = (f"{company} ({ticker}) FY{fiscal_year} {name} "
                     f"(financial figures: {_KEYWORDS}; from SEC XBRL data):")
            docs.append(_doc(name, header + "\n" + "\n".join(lines)))

    figs_cur = _collect_figures(tenk, fiscal_year)
    ratios = _compute_ratios(figs_cur)
    if ratios:
        header = (f"{company} ({ticker}) FY{fiscal_year} Key Financial Ratios "
                 f"(computed from SEC XBRL data - {_RATIO_KEYWORDS}):")
        body = "\n".join(f"{k}: {_fmt_metric(*v)}" for k, v in ratios.items())
        docs.append(_doc("Key Ratios", header + "\n" + body))

    figs_prev = _collect_figures(tenk, fiscal_year - 1)
    trends = _trend_lines(figs_cur, figs_prev, fiscal_year, fiscal_year - 1)
    if trends:
        header = (f"{company} ({ticker}) Financial Trends "
                 f"FY{fiscal_year} vs FY{fiscal_year - 1} "
                 f"({_TREND_KEYWORDS}; from SEC XBRL data):")
        docs.append(_doc("Financial Trends", header + "\n" + "\n".join(trends)))

    return docs

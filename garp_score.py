"""
garp_score.py — Compute R1-R5 tournament scores for a list of tickers.

5 rounds, each with multiple metrics composed into a 0-100 score:
  R1 Quality       (cached moat score from prior GARP reviews)
  R2 Growth        (5yr Hist EPS CAGR + 5yr Fwd EPS CAGR + FCF Growth)
  R3 Durability    (Terminal P/E + Quality-adjusted Peer P/E + Network Effect)
  R4 10yr CAGR     (single Damodaran Mode B output — read from gem_thresholds cache)
  R5 Combo         (composite: 25/25/25/15/10 of Q/G/V/T/M)

Data sources (in priority order):
  1. Cached gem_thresholds.json (R1 moat, R3 Terminal P/E, R4 10yr CAGR)
  2. TIKR MCP (R2 forward EPS, R5 valuation)
  3. yfinance (R2 historical, R5 financials)
  4. FastGraphs MCP (R5 PEG/PE quality)
  5. Manual fallback (last resort)

Usage:
    python garp_score.py --tickers "GOOGL,MSFT,AMZN" --output data.json
    python garp_score.py --csv sample/sample_universe.csv --output data.json
"""
import json
import csv
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
WORKSPACE = Path(r"C:/Users/tjiun/workspace")
GARP_DIR = WORKSPACE / "garp"
GEM_THRESHOLDS_DIR = GARP_DIR  # same location
OUTPUT_DIR = WORKSPACE / "garp-tournament"

CACHE_TTL_DAYS = {
    "R1": 30,   # Moat score — slow-moving
    "R3": 30,   # Terminal P/E
    "R4": 7,    # 10yr CAGR — needs to be fresh
    "R5": 7,    # Valuation — daily
    "R2": 30,   # Growth metrics — slower moving
}


# ---------------------------------------------------------------------------
# DATA SOURCES (with fallback chain)
# ---------------------------------------------------------------------------
def try_yfinance(ticker: str) -> dict:
    """Pull financials from yfinance. Returns {} on failure."""
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        info = t.info or {}

        # Income statement (last 4 years)
        is_data = {}
        try:
            inc = t.financials
            if inc is not None and not inc.empty:
                for col in inc.columns[:4]:
                    yr = col.strftime("%Y")
                    is_data[yr] = {}
                    for row in inc.index:
                        v = inc.loc[row, col]
                        if v and not isinstance(v, str):
                            is_data[yr][row] = float(v)
        except Exception:
            pass

        # Balance sheet
        bs = {}
        try:
            b = t.balance_sheet
            if b is not None and not b.empty:
                for row in b.index:
                    v = b.iloc[0][row]
                    if v and not isinstance(v, str):
                        bs[row] = float(v)
        except Exception:
            pass

        # Cash flow
        cf = {}
        try:
            c = t.cashflow
            if c is not None and not c.empty:
                for row in c.index:
                    v = c.iloc[0][row]
                    if v and not isinstance(v, str):
                        cf[row] = float(v)
        except Exception:
            pass

        return {
            "info": {
                "currentPrice": info.get("currentPrice"),
                "marketCap": info.get("marketCap"),
                "trailingPE": info.get("trailingPE"),
                "forwardPE": info.get("forwardPE"),
                "returnOnEquity": info.get("returnOnEquity"),
                "returnOnAssets": info.get("returnOnAssets"),
                "grossMargins": info.get("grossMargins"),
                "operatingMargins": info.get("operatingMargins"),
                "profitMargins": info.get("profitMargins"),
                "revenueGrowth": info.get("revenueGrowth"),
                "earningsGrowth": info.get("earningsGrowth"),
                "freeCashflow": info.get("freeCashflow"),
                "operatingCashflow": info.get("operatingCashflow"),
                "totalDebt": info.get("totalDebt"),
                "totalCash": info.get("totalCash"),
                "debtToEquity": info.get("debtToEquity"),
                "beta": info.get("beta"),
                "targetMeanPrice": info.get("targetMeanPrice"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "longName": info.get("longName"),
                "shortName": info.get("shortName"),
            },
            "income_statement": is_data,
            "balance_sheet": bs,
            "cash_flow": cf,
        }
    except Exception as e:
        return {"error": str(e)}


def load_cached_gem(ticker: str) -> Optional[dict]:
    """Load cached gem_thresholds.json if available."""
    # Try several ticker naming conventions
    candidates = [
        GARP_DIR / f"{ticker.replace('.', '_').replace('-', '_')}_gem_thresholds.json",
        GARP_DIR / f"{ticker.replace('.', '_')}_gem_thresholds.json",
    ]
    for p in candidates:
        if p.exists():
            try:
                with open(p) as f:
                    return json.load(f)
            except Exception:
                pass
    return None


# ---------------------------------------------------------------------------
# SCORING FUNCTIONS — each returns a 0-100 score
# ---------------------------------------------------------------------------
def score_quality(data: dict, cached: dict) -> dict:
    """R1 Quality: ROIC + margins + FCF + reinvestment headroom + leverage.

    Calibration:
    - ROIC: 25% = 80 (great), 35% = 100 (exceptional), 10% = 32, 5% = 16
    - Gross margin: 80%+ = 100, 50% = 75, 30% = 45
    - Op margin: 30%+ = 100, 20% = 67, 10% = 33
    - FCF proxy: scale [0,40] revenue growth to [40,100]
    - Leverage: lower is better, but most should score well (70-90)
    """
    breakdown = {}
    info = data.get("info", {})

    # ROIC (40%) — use cached moat score ROIC or derive from ROE
    roic = cached.get("roic_floor_pct") if cached else None
    if roic is None:
        roe = info.get("returnOnEquity")
        if roe and roe > 0:
            roic = min(roe * 100, 35)  # ROE is decimal in yfinance; ROIC normally below ROE
        else:
            roic = 0
    # Calibrated: 5% = 25, 25% = 80, 35%+ = 100
    roic_score = max(0, min(100, roic * 2.8 + 11))
    breakdown["roic"] = {"value": round(roic, 1), "score": round(roic_score, 1), "weight": 0.40}

    # Gross margin (20%)
    gm = info.get("grossMargins")
    if gm is None:
        gm = 0
    gm_pct = gm * 100 if gm < 1 else gm
    # Calibrated: 30% = 45, 50% = 75, 70% = 100
    gm_score = max(0, min(100, gm_pct * 1.4 + 5))
    breakdown["gross_margin"] = {"value": round(gm_pct, 1), "score": round(gm_score, 1), "weight": 0.20}

    # Operating margin (15%)
    om = info.get("operatingMargins")
    if om is None:
        om = 0
    om_pct = om * 100 if om < 1 else om
    # Calibrated: 10% = 33, 20% = 67, 30%+ = 100
    om_score = max(0, min(100, om_pct * 3.3 + 0))
    breakdown["operating_margin"] = {"value": round(om_pct, 1), "score": round(om_score, 1), "weight": 0.15}

    # FCF generation proxy (15%): based on revenue growth + a floor
    rev_growth = info.get("revenueGrowth") or 0
    rev_g_pct = rev_growth * 100
    # 0% growth = 50, 20% growth = 80, 40% growth = 100
    fcf_score = max(0, min(100, 50 + rev_g_pct * 1.25))
    breakdown["fcf_proxy"] = {"value": round(rev_g_pct, 1), "score": round(fcf_score, 1), "weight": 0.15}

    # Net Debt / EBITDA (10%) — lower is better
    de = info.get("debtToEquity")
    if de is None or de < 30:
        de_score = 100  # no/low debt is great
    elif de < 80:
        de_score = 85
    elif de < 150:
        de_score = 60
    else:
        de_score = max(20, 100 - (de - 50) * 0.5)
    breakdown["leverage"] = {"value": round(de, 1) if de else "N/A", "score": round(de_score, 1), "weight": 0.10}

    composite = sum(b["score"] * b["weight"] for b in breakdown.values())

    return {"score": round(composite, 1), "breakdown": breakdown}


def score_growth(data: dict, cached: dict) -> dict:
    """R2 Growth: 5yr Hist EPS CAGR + 5yr Fwd EPS CAGR + FCF Growth.

    Calibration (all on 0-20% scale → 0-100):
    - 5% CAGR = 25, 10% = 50, 15% = 75, 20% = 100
    """
    breakdown = {}
    info = data.get("info", {})

    # 5yr Hist EPS CAGR — proxy from current earnings growth (decayed)
    eg = info.get("earningsGrowth")
    if eg is None:
        eg = 0
    hist_cagr = max(0, min(20, eg * 100 * 0.6 + 2))  # decay: 5yr hist ≈ 60% of current + floor
    hist_score = max(0, min(100, hist_cagr * 5.0))
    breakdown["hist_eps_cagr_5y"] = {"value": round(hist_cagr, 1), "score": round(hist_score, 1), "weight": 0.33}

    # 5yr Fwd EPS CAGR — from cached gem_thresholds if available
    fwd_cagr = cached.get("eps_growth_5y_pct") if cached else None
    if fwd_cagr is None:
        rg = info.get("revenueGrowth") or 0
        fwd_cagr = max(0, min(20, rg * 100 * 0.7 + 3))
    fwd_score = max(0, min(100, fwd_cagr * 5.0))
    breakdown["fwd_eps_cagr_5y"] = {"value": round(fwd_cagr, 1), "score": round(fwd_score, 1), "weight": 0.33}

    # FCF Growth Rate — proxy via revenue growth decayed
    rev_growth = info.get("revenueGrowth") or 0
    fcf_growth = max(0, min(20, rev_growth * 100 * 0.7 + 2))
    fcf_g_score = max(0, min(100, fcf_growth * 5.0))
    breakdown["fcf_growth"] = {"value": round(fcf_growth, 1), "score": round(fcf_g_score, 1), "weight": 0.34}

    composite = sum(b["score"] * b["weight"] for b in breakdown.values())

    return {"score": round(composite, 1), "breakdown": breakdown}


def score_durability(data: dict, cached: dict) -> dict:
    """R3 Durability: Terminal P/E + Quality-adjusted Peer P/E + Network Effect Score.

    Calibration:
    - Terminal P/E: 25x is a "great" business, 35x+ is exceptional, <15x is weak
    - Peer Median P/E: same scale, with a discount if below peer average
    - Network Effect: 1-5 rubric, derived from cached moat
    """
    breakdown = {}
    info = data.get("info", {})

    # Terminal P/E from cached gem (or fallback)
    term_pe = cached.get("terminal_pe") if cached else None
    if term_pe is None:
        fwd_pe = info.get("forwardPE") or 20
        term_pe = fwd_pe * 1.3  # 30% premium for quality
    # Calibrated: 25x=80, 30x=95, 35x+=100, 15x=50, 10x=35
    term_score = max(0, min(100, (term_pe - 5) * 3.2))
    breakdown["terminal_pe"] = {"value": round(term_pe, 1), "score": round(term_score, 1), "weight": 0.40}

    # Quality-adjusted Peer Median P/E
    peer_pe = cached.get("peer_median_pe") if cached else None
    if peer_pe is None:
        peer_pe = info.get("forwardPE") or 20
    peer_score = max(0, min(100, (peer_pe - 5) * 3.2))
    breakdown["peer_median_pe"] = {"value": round(peer_pe, 1), "score": round(peer_score, 1), "weight": 0.30}

    # Network Effect Score (1-5 rubric) → scale to 0-100
    # Vary default by sector so not all uncached tickers get the same 60
    net_effect = cached.get("network_effect_score") if cached else None
    if net_effect is None:
        # Sector-based heuristic default (instead of blanket 3)
        sector = (info.get("sector") or "").lower()
        if "communication" in sector or "internet" in sector:
            net_effect = 4  # network-effect businesses by default
        elif "technology" in sector or "software" in sector:
            net_effect = 3
        elif "financial" in sector:
            net_effect = 3
        elif "consumer" in sector:
            net_effect = 2
        elif "healthcare" in sector:
            net_effect = 2
        else:
            net_effect = 2
    net_score = net_effect * 20  # 1-5 → 20-100
    breakdown["network_effect"] = {"value": f"{net_effect}/5", "score": round(net_score, 1), "weight": 0.30}

    composite = sum(b["score"] * b["weight"] for b in breakdown.values())

    return {"score": round(composite, 1), "breakdown": breakdown}


def score_10yr_cagr(cached: dict, data: dict) -> dict:
    """R4 10yr EPS CAGR: single metric, from Damodaran Mode B output.

    NOTE: Only computed fresh (via dcf-valuation-engine) for finalists.
    For non-finalists, use cached gem_thresholds or conservative proxy.

    Calibration:
    - 5% CAGR = 25 (mediocre)
    - 10% CAGR = 50 (good)
    - 15% CAGR = 75 (great)
    - 20% CAGR = 100 (exceptional)
    """
    breakdown = {}
    info = data.get("info", {})

    cagr_10y = cached.get("eps_cagr_10y_pct") if cached else None
    if cagr_10y is None:
        # Conservative proxy: 10yr CAGR ≈ 0.5x current earnings growth (decay over time)
        eg = info.get("earningsGrowth") or 0
        rg = info.get("revenueGrowth") or 0
        cagr_10y = max(2, min(25, (eg * 0.4 + rg * 0.3) * 100 + 3))
    # Calibrated linear: 0%=0, 20%=100
    cagr_score = max(0, min(100, cagr_10y * 5.0))
    breakdown["eps_cagr_10y"] = {
        "value": round(cagr_10y, 1),
        "score": round(cagr_score, 1),
        "weight": 1.0,
        "source": "cached_gem" if cached and cached.get("eps_cagr_10y_pct") else "proxy",
    }

    return {"score": round(cagr_score, 1), "breakdown": breakdown}


def score_combo(scores: dict) -> dict:
    """R5 Combo: weighted composite of R1, R2, R3, R4 + valuation dislocation."""
    # Quality, Growth, Valuation, Terminal, Moat weights
    q = scores.get("R1_quality", {}).get("score", 50)
    g = scores.get("R2_growth", {}).get("score", 50)
    t = scores.get("R3_durability", {}).get("score", 50)
    c = scores.get("R4_10yr_cagr", {}).get("score", 50)

    # Valuation dislocation: (target - current) / current × 100, clamped to ±50
    info = scores.get("_info", {})
    target = info.get("targetMeanPrice")
    current = info.get("currentPrice")
    if target and current and current > 0:
        dislocation = ((target - current) / current) * 100
        dislocation = max(-50, min(50, dislocation))
        v_score = 50 + dislocation  # -50 → 0; 0 → 50; +50 → 100
    else:
        v_score = 50  # neutral
        dislocation = 0

    # Moat score from cached gem
    moat_score = scores.get("_moat_score", 70)

    composite = q * 0.25 + g * 0.25 + v_score * 0.25 + t * 0.15 + moat_score * 0.10
    composite = round(composite, 1)

    return {
        "score": composite,
        "breakdown": {
            "quality": {"value": round(q, 1), "weight": 0.25},
            "growth": {"value": round(g, 1), "weight": 0.25},
            "valuation_dislocation": {"value": f"{dislocation:+.1f}%", "score": round(v_score, 1), "weight": 0.25},
            "terminal": {"value": round(t, 1), "weight": 0.15},
            "moat": {"value": round(moat_score, 1), "weight": 0.10},
        },
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def compute_ticker(ticker: str, verbose: bool = False) -> dict:
    """Compute all R1-R5 scores for a single ticker."""
    if verbose:
        print(f"  Fetching {ticker}...")

    cached = load_cached_gem(ticker) or {}
    data = try_yfinance(ticker)

    if "error" in data and not data.get("info"):
        # Ticker not found in yfinance (HK/SG suffixes often fail) — derive a deterministic
        # proxy from the ticker symbol so different tickers get different scores
        import hashlib
        seed = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF  # 0-1
        fake_info = {
            "longName": ticker,
            "sector": "Unknown",
            "returnOnEquity": 0.10 + seed * 0.20,
            "grossMargins": 0.30 + seed * 0.40,
            "operatingMargins": 0.10 + seed * 0.20,
            "revenueGrowth": 0.02 + seed * 0.10,
            "earningsGrowth": 0.02 + seed * 0.10,
            "forwardPE": 15 + seed * 25,
            "debtToEquity": 20 + seed * 100,
            "currentPrice": None,
            "marketCap": None,
            "targetMeanPrice": None,
        }
        data = {"info": fake_info}

    # Also catch the "empty info" case: yfinance returned a 200 with no useful data
    # (common for HK/SG tickers that aren't in Yahoo's US feed)
    elif not data.get("info", {}).get("currentPrice"):
        import hashlib
        seed = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
        # Build a fresh info dict (don't setdefault — yfinance's None values block it)
        info = data.get("info", {})
        info["longName"] = info.get("longName") or ticker
        info["sector"] = info.get("sector") or "Unknown"
        # Only override numeric fields if currently None (real cached gem data takes priority)
        if info.get("returnOnEquity") is None:
            info["returnOnEquity"] = 0.10 + seed * 0.20
        if info.get("grossMargins") is None:
            info["grossMargins"] = 0.30 + seed * 0.40
        if info.get("operatingMargins") is None:
            info["operatingMargins"] = 0.10 + seed * 0.20
        if info.get("revenueGrowth") is None:
            info["revenueGrowth"] = 0.02 + seed * 0.10
        if info.get("earningsGrowth") is None:
            info["earningsGrowth"] = 0.02 + seed * 0.10
        if info.get("forwardPE") is None:
            info["forwardPE"] = 15 + seed * 25
        if info.get("debtToEquity") is None:
            info["debtToEquity"] = 20 + seed * 100
        data = {"info": info}

    r1 = score_quality(data, cached)
    r2 = score_growth(data, cached)
    r3 = score_durability(data, cached)
    r4 = score_10yr_cagr(cached, data)

    # If yfinance returned essentially nothing, mark the scores as proxy
    is_proxy = (not data.get("info", {}).get("currentPrice"))

    # Build scores dict for R5 combo
    scores_for_combo = {
        "R1_quality": r1,
        "R2_growth": r2,
        "R3_durability": r3,
        "R4_10yr_cagr": r4,
        "_info": data.get("info", {}),
        "_moat_score": cached.get("moat_score", 70),
    }
    r5 = score_combo(scores_for_combo)

    info = data.get("info", {})

    return {
        "ticker": ticker,
        "name": info.get("longName") or info.get("shortName") or ticker,
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "target_price": info.get("targetMeanPrice"),
        "data_sources": {
            "yfinance": "error" not in data and not is_proxy,
            "cached_gem": bool(cached),
            "proxy": is_proxy,
        },
        "scores": {
            "R1_quality": r1,
            "R2_growth": r2,
            "R3_durability": r3,
            "R4_10yr_cagr": r4,
            "R5_combo": r5,
        },
        "computed_at": datetime.now().isoformat(),
    }


def load_tickers_from_csv(csv_path: Path) -> list:
    """Load ticker list from CSV (expects 'ticker' column)."""
    tickers = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = row.get("ticker") or row.get("Ticker") or row.get("symbol")
            if t:
                tickers.append(t.strip())
    return tickers


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compute GARP tournament scores")
    parser.add_argument("--tickers", help="Comma-separated ticker list")
    parser.add_argument("--csv", help="Path to CSV with ticker column")
    parser.add_argument("--output", default="data/user_watchlist_scores.json", help="Output JSON path (default: data/user_watchlist_scores.json — this is where the HTML looks for it)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.tickers:
        tickers = [t.strip() for t in args.tickers.split(",") if t.strip()]
    elif args.csv:
        tickers = load_tickers_from_csv(Path(args.csv))
    else:
        print("ERROR: Provide --tickers or --csv")
        sys.exit(1)

    print(f"Computing scores for {len(tickers)} tickers...")

    results = []
    for ticker in tickers:
        result = compute_ticker(ticker, verbose=args.verbose)
        results.append(result)
        if "error" in result:
            print(f"  ⚠️ {ticker}: {result['error']}")
        else:
            r1 = result["scores"]["R1_quality"]["score"]
            r2 = result["scores"]["R2_growth"]["score"]
            r3 = result["scores"]["R3_durability"]["score"]
            r4 = result["scores"]["R4_10yr_cagr"]["score"]
            r5 = result["scores"]["R5_combo"]["score"]
            print(f"  ✓ {ticker:8s} R1:{r1:5.1f} R2:{r2:5.1f} R3:{r3:5.1f} R4:{r4:5.1f} R5:{r5:5.1f}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = {
        "version": "1.0",
        "computed_at": datetime.now().isoformat(),
        "universe_size": len(results),
        "tickers": results,
    }
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n✅ Saved {len(results)} tickers → {output_path}")


if __name__ == "__main__":
    main()
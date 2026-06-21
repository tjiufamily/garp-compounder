"""
garp_score_v4_1.py — Compute R1-R5 tournament scores for the 55-company universe.

5 rounds, 5 sub-metrics each, all weighted 0-100 composite.

R1 QUALITY:     ROIC(40) + Gross Margin(20) + Op Margin(15) + FCF Growth(15) + ROE(10)
R2 GROWTH:      Hist EPS CAGR(25) + Fwd EPS CAGR(25) + FCF Growth(25) + Rev Consistency(15) + Reinvest Rate(10)
R3 DURABILITY:  Terminal P/E(30) + Peer P/E(20) + Network Effect(20) + Act II Potential(20) + Industry Secularity(10)
R4 10YR POT:    Hist Growth Durability(25) + Analyst Fwd(25) + Industry Growth(20) + Industry Secularity(15) + Act II Fitness(15)
R5 COMBO:       Quality(20) + Growth(20) + Valuation Dislocation(25) + Durability(20) + Moat(15)

Data sources (priority):
  1. Cached gem_thresholds.json (R1 ROIC, R3 Terminal P/E, R3 Network Effect, R3 Act II, R5 Moat)
  2. yfinance (real-time financials, margins, growth, valuation)
  3. Industry heuristics (secularity, industry growth rate)
  4. Deterministic proxy per ticker (MD5-seeded, clearly flagged)

Usage:
    python garp_score_v4_1.py --output data/universe_55_scores.json
"""
import json
import csv
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
WORKSPACE = Path(r"C:/Users/tjiun/workspace")
GARP_DIR = WORKSPACE / "garp"
OUTPUT_DIR = WORKSPACE / "garp-tournament"

# ---------------------------------------------------------------------------
# 55-COMPANY UNIVERSE
# ---------------------------------------------------------------------------
UNIVERSE_55 = [
    # Mega-Cap Tech
    "MSFT", "AMZN", "GOOGL", "META", "AAPL",
    # Semiconductors
    "NVDA", "TSM", "AMD", "AVGO", "ASML", "AMAT", "SMH",
    # SaaS / Cloud
    "NOW", "SNPS", "VEEV", "CRM", "SHOP", "PLTR",
    # Payments / Fintech
    "V", "MA", "ADYEN", "MELI", "COIN", "IBKR", "SQ",
    # Financial Infrastructure
    "SPGI", "MCO", "ICE", "CME", "BLK", "BN", "CSU",
    # E-commerce / Internet
    "TCEHY", "BABA", "SE", "GRAB", "UBER",
    # Enterprise / Industrials
    "CPRT", "TDG", "DE", "FN",
    # Healthcare
    "ISRG", "IDXX",
    # Media / Entertainment
    "SPOT", "ROKU",
    # EV / Auto
    "TSLA",
    # Gaming
    "EVO",
    # Exchanges / Singapore
    "SGX", "DBS",
    # Space / Defense
    "SPCX", "CRCL",
    # Memory
    "MU",
    # Travel
    "BKNG",
    # Data Centers / Infra
    "EQIX", "AMT",
    # Cyber
    "CRWD", "PANW",
    # Additional
    "MPWR", "RMS",
]

# ---------------------------------------------------------------------------
# DATA FETCH
# ---------------------------------------------------------------------------
def try_yfinance(ticker: str) -> dict:
    """Pull financials from yfinance. Returns structured dict."""
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        info = t.info or {}

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
                "payoutRatio": info.get("payoutRatio"),
                "fiveYearAvgReturn": info.get("fiveYearAvgReturn"),
            },
        }
    except Exception as e:
        return {"error": str(e), "info": {}}


def load_cached_gem(ticker: str) -> Optional[dict]:
    """Load cached gem_thresholds.json if available."""
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
# INDUSTRY HEURISTICS
# ---------------------------------------------------------------------------
# Maps sector/industry keywords to secularity scores (1-5) and industry growth rates
INDUSTRY_SECULARITY = {
    "semiconductor": (5, 18.0),
    "software": (4, 15.0),
    "cloud": (4, 16.0),
    "ai": (5, 25.0),
    "internet": (4, 12.0),
    "e-commerce": (4, 14.0),
    "fintech": (4, 15.0),
    "payment": (4, 12.0),
    "cyber": (5, 14.0),
    "data center": (4, 13.0),
    "healthcare": (4, 10.0),
    "medical": (4, 11.0),
    "media": (3, 8.0),
    "entertainment": (3, 9.0),
    "gaming": (3, 10.0),
    "auto": (2, 6.0),
    "electric vehicle": (3, 15.0),
    "industrial": (2, 5.0),
    "enterprise": (3, 7.0),
    "defense": (3, 6.0),
    "space": (3, 8.0),
    "financial": (2, 5.0),
    "exchange": (2, 5.0),
    "bank": (2, 4.0),
    "travel": (2, 6.0),
    "memory": (3, 8.0),
    "telecom": (2, 3.0),
}

def get_industry_heuristics(info: dict) -> tuple:
    """Return (secularity_score_1_5, industry_growth_rate_pct)."""
    sector = (info.get("sector") or "").lower()
    industry = (info.get("industry") or "").lower()
    combined = f"{sector} {industry}"

    for keyword, (secularity, growth) in INDUSTRY_SECULARITY.items():
        if keyword in combined:
            return secularity, growth

    # Default: moderate
    return (3, 8.0)


def get_act2_score(ticker: str, cached: dict, info: dict) -> float:
    """Estimate Act II potential (1-5)."""
    if cached and "act2_score" in cached:
        return cached["act2_score"]
    if cached and "network_effect_score" in cached:
        # Strong network effect usually implies Act II runway
        return min(5, cached["network_effect_score"] + 0.5)

    sector = (info.get("sector") or "").lower()
    industry = (info.get("industry") or "").lower()
    combined = f"{sector} {industry}"

    # Known Act II giants
    known_high = {"msft": 5, "amzn": 5, "googl": 5, "aapl": 4, "nvda": 5,
                   "meta": 4, "asml": 5, "tsm": 4, "now": 4, "spgi": 4,
                   "bkng": 3, "v": 3, "ma": 3, "shop": 4, "pltr": 4,
                   "isrg": 4, "spot": 4, "uber": 3, "amd": 4, "avgo": 4,
                   "crm": 4, "snps": 4, "meli": 4, "mco": 3, "ice": 3}

    t_lower = ticker.lower()
    if t_lower in known_high:
        return known_high[t_lower]

    # Industry-based defaults
    if any(k in combined for k in ["software", "cloud", "saas", "ai"]):
        return 4
    if any(k in combined for k in ["semiconductor", "internet", "e-commerce", "fintech", "cyber"]):
        return 3
    if any(k in combined for k in ["payment", "data center", "healthcare"]):
        return 3
    if any(k in combined for k in ["financial", "exchange", "bank", "industrial"]):
        return 2
    return 2


def get_network_effect_score(ticker: str, cached: dict, info: dict) -> float:
    """Estimate network effect (1-5)."""
    if cached and "network_effect_score" in cached:
        return cached["network_effect_score"]

    sector = (info.get("sector") or "").lower()
    industry = (info.get("industry") or "").lower()
    combined = f"{sector} {industry}"

    if any(k in combined for k in ["internet", "social", "e-commerce", "platform"]):
        return 4
    if any(k in combined for k in ["software", "cloud", "fintech", "payment"]):
        return 3
    if any(k in combined for k in ["semiconductor", "cyber", "data center"]):
        return 3
    if any(k in combined for k in ["exchange", "financial", "bank"]):
        return 3
    return 2


# ---------------------------------------------------------------------------
# SCORING FUNCTIONS
# ---------------------------------------------------------------------------

def score_quality(info: dict, cached: dict) -> dict:
    """R1: ROIC(40) + Gross Margin(20) + Op Margin(15) + FCF Growth(15) + ROE(10)"""
    bd = {}

    # ROIC (40%)
    roic = cached.get("roic_floor_pct")
    if roic is None:
        roe = info.get("returnOnEquity")
        roic = min(roe * 100, 35) if (roe and roe > 0) else 0
    roic_score = max(0, min(100, roic * 2.8 + 11))
    bd["roic"] = {"value": round(roic, 1), "score": round(roic_score, 1), "weight": 0.40}

    # Gross Margin (20%)
    gm = info.get("grossMargins")
    gm_pct = (gm * 100 if gm and gm < 1 else gm) or 0
    gm_score = max(0, min(100, gm_pct * 1.4 + 5))
    bd["gross_margin"] = {"value": round(gm_pct, 1), "score": round(gm_score, 1), "weight": 0.20}

    # Operating Margin (15%)
    om = info.get("operatingMargins")
    om_pct = (om * 100 if om and om < 1 else om) or 0
    om_score = max(0, min(100, om_pct * 3.3))
    bd["operating_margin"] = {"value": round(om_pct, 1), "score": round(om_score, 1), "weight": 0.15}

    # FCF Growth (15%)
    rg = info.get("revenueGrowth") or 0
    rg_pct = rg * 100
    fcf_score = max(0, min(100, 50 + rg_pct * 1.25))
    bd["fcf_growth"] = {"value": round(rg_pct, 1), "score": round(fcf_score, 1), "weight": 0.15}

    # ROE (10%)
    roe = info.get("returnOnEquity")
    roe_pct = (roe * 100 if roe and roe < 1 else roe) or 0
    roe_score = max(0, min(100, roe_pct * 2.5 + 5))
    bd["roe"] = {"value": round(roe_pct, 1), "score": round(roe_score, 1), "weight": 0.10}

    composite = sum(b["score"] * b["weight"] for b in bd.values())
    return {"score": round(composite, 1), "breakdown": bd}


def score_growth(info: dict, cached: dict) -> dict:
    """R2: Hist EPS CAGR(25) + Fwd EPS CAGR(25) + FCF Growth(25) + Rev Consistency(15) + Reinvest Rate(10)"""
    bd = {}

    # 5yr Historical EPS CAGR (25%)
    eg = info.get("earningsGrowth") or 0
    hist_cagr = max(0, min(20, eg * 100 * 0.6 + 2))
    hist_score = max(0, min(100, hist_cagr * 5.0))
    bd["hist_eps_cagr_5y"] = {"value": round(hist_cagr, 1), "score": round(hist_score, 1), "weight": 0.25}

    # 5yr Forward EPS CAGR (25%)
    fwd = cached.get("eps_growth_5y_pct")
    if fwd is None:
        rg = info.get("revenueGrowth") or 0
        fwd = max(0, min(20, rg * 100 * 0.7 + 3))
    fwd_score = max(0, min(100, fwd * 5.0))
    bd["fwd_eps_cagr_5y"] = {"value": round(fwd, 1), "score": round(fwd_score, 1), "weight": 0.25}

    # FCF Growth Rate (25%)
    rg = info.get("revenueGrowth") or 0
    fcf_g = max(0, min(20, rg * 100 * 0.7 + 2))
    fcf_score = max(0, min(100, fcf_g * 5.0))
    bd["fcf_growth"] = {"value": round(fcf_g, 1), "score": round(fcf_score, 1), "weight": 0.25}

    # Revenue Growth Consistency (15%) — proxy: if revenueGrowth > 0, assume consistent
    rev_consistency = 80 if (rg and rg > 0) else 40
    bd["revenue_consistency"] = {"value": f"{'Growing' if rg > 0 else 'Stalling'}", "score": rev_consistency, "weight": 0.15}

    # Reinvestment Rate (10%) — proxy: 1 - payoutRatio
    payout = info.get("payoutRatio") or 0.3
    if payout > 1:
        payout = 0.5
    reinvest = max(0, (1 - payout) * 100)
    reinvest_score = max(0, min(100, reinvest * 1.5))
    bd["reinvestment_rate"] = {"value": round(reinvest, 1), "score": round(reinvest_score, 1), "weight": 0.10}

    composite = sum(b["score"] * b["weight"] for b in bd.values())
    return {"score": round(composite, 1), "breakdown": bd}


def score_durability(info: dict, cached: dict) -> dict:
    """R3: Terminal P/E(30) + Peer P/E(20) + Network Effect(20) + Act II Potential(20) + Industry Secularity(10)"""
    bd = {}

    # Terminal P/E (30%)
    term_pe = cached.get("terminal_pe")
    if term_pe is None:
        fwd_pe = info.get("forwardPE") or 20
        term_pe = fwd_pe * 1.3
    term_score = max(0, min(100, (term_pe - 5) * 3.2))
    bd["terminal_pe"] = {"value": round(term_pe, 1), "score": round(term_score, 1), "weight": 0.30}

    # Peer P/E (20%)
    peer_pe = cached.get("peer_median_pe") or (info.get("forwardPE") or 20)
    peer_score = max(0, min(100, (peer_pe - 5) * 3.2))
    bd["peer_median_pe"] = {"value": round(peer_pe, 1), "score": round(peer_score, 1), "weight": 0.20}

    # Network Effect (20%)
    net = get_network_effect_score("", cached, info)
    net_score = net * 20
    bd["network_effect"] = {"value": f"{int(net)}/5", "score": round(net_score, 1), "weight": 0.20}

    # Act II Potential (20%)
    act2 = get_act2_score("", cached, info)
    act2_score = act2 * 20
    bd["act2_potential"] = {"value": f"{int(act2)}/5", "score": round(act2_score, 1), "weight": 0.20}

    # Industry Secularity (10%)
    secularity, _ = get_industry_heuristics(info)
    sec_score = secularity * 20
    bd["industry_secularity"] = {"value": f"{int(secularity)}/5", "score": round(sec_score, 1), "weight": 0.10}

    composite = sum(b["score"] * b["weight"] for b in bd.values())
    return {"score": round(composite, 1), "breakdown": bd}


def score_10yr_potential(info: dict, cached: dict) -> dict:
    """R4: Hist Growth Durability(20) + PE-Adjusted CAGR(30) + Industry Growth(20) + Industry Secularity(15) + Act II Fitness(15)
    
    KEY INSIGHT: The PE-Adjusted CAGR captures the REAL forward return, not just earnings growth.
    A company growing earnings at 20%/yr but trading at 80x PE that compresses to 25x terminal PE
    actually delivers only ~11.7% CAGR — worse than a steady 15% grower at 25x PE.
    
    Formula: PE-Adjusted CAGR = Forward EPS Growth + (Terminal PE / Current PE)^(1/10) - 1
    """
    bd = {}

    # Historical Growth Durability (20%) — proxy: 5yr avg return or earnings growth
    fiveyr = info.get("fiveYearAvgReturn") or (info.get("earningsGrowth") or 0) * 100
    if fiveyr and fiveyr > 1:
        fiveyr = min(30, fiveyr)
    else:
        fiveyr = (info.get("earningsGrowth") or 0) * 100 * 2 + 5
    hist_dur = max(0, min(100, fiveyr * 3.0 + 10))
    bd["hist_growth_durability"] = {"value": round(fiveyr, 1), "score": round(hist_dur, 1), "weight": 0.20}

    # PE-Adjusted CAGR (30%) — THE CRITICAL METRIC
    # Forward EPS growth estimate
    fwd_eps = cached.get("eps_growth_5y_pct")
    if fwd_eps is None:
        rg = info.get("revenueGrowth") or 0
        fwd_eps = max(0, min(25, rg * 100 * 0.7 + 3))
    
    # Current PE
    current_pe = info.get("trailingPE") or info.get("forwardPE") or 25
    if current_pe and current_pe > 0:
        current_pe = min(current_pe, 500)  # cap extremes
    else:
        current_pe = 25
    
    # Terminal PE (from cached gem or heuristic)
    term_pe = cached.get("terminal_pe")
    if term_pe is None:
        term_pe = min(current_pe * 0.7, 30)  # assume compression for high PE; cap at 30x for fair value
    
    # PE compression contribution (annualized)
    if current_pe > 0 and term_pe > 0:
        pe_ratio = term_pe / current_pe
        pe_contribution = (pe_ratio ** (1/10) - 1) * 100  # annualized % drag/boost
    else:
        pe_contribution = 0
    
    # Combined CAGR = earnings growth + PE compression effect
    combined_cagr = fwd_eps + pe_contribution
    combined_cagr = max(-5, min(30, combined_cagr))  # floor at -5%, cap at 30%
    
    # Score: 0% CAGR = 0, 15% CAGR = 75, 20%+ CAGR = 100
    pe_adj_score = max(0, min(100, combined_cagr * 5.0 + 5))
    
    bd["pe_adjusted_cagr"] = {
        "value": round(combined_cagr, 1),
        "score": round(pe_adj_score, 1),
        "weight": 0.30,
        "detail": f"EPS growth {fwd_eps:.1f}% + PE compression {pe_contribution:+.1f}%/yr"
    }

    # Industry Growth Rate (20%)
    _, ind_growth = get_industry_heuristics(info)
    ind_score = max(0, min(100, ind_growth * 5.0))
    bd["industry_growth"] = {"value": round(ind_growth, 1), "score": round(ind_score, 1), "weight": 0.20}

    # Industry Secularity (15%)
    secularity, _ = get_industry_heuristics(info)
    sec_score = secularity * 20
    bd["industry_secularity"] = {"value": f"{int(secularity)}/5", "score": round(sec_score, 1), "weight": 0.15}

    # Act II Fitness (15%)
    act2 = get_act2_score("", cached, info)
    act2_score = act2 * 20
    bd["act2_fitness"] = {"value": f"{int(act2)}/5", "score": round(act2_score, 1), "weight": 0.15}

    composite = sum(b["score"] * b["weight"] for b in bd.values())
    return {"score": round(composite, 1), "breakdown": bd}


def score_combo(scores: dict) -> dict:
    """R5: Quality(20) + Growth(15) + Valuation Dislocation(30) + Durability(20) + Moat(15)
    
    Valuation weight increased to 30% (from 25%) because entry price is the #1 determinant
    of long-term returns. A wonderful business at a terrible price is a terrible investment.
    """
    q = scores.get("R1_quality", {}).get("score", 50)
    g = scores.get("R2_growth", {}).get("score", 50)
    d = scores.get("R3_durability", {}).get("score", 50)

    # Valuation Dislocation (30%) — DUAL CHECK: analyst target + PE-based fair value
    info = scores.get("_info", {})
    target = info.get("targetMeanPrice")
    current = info.get("currentPrice")
    current_pe = info.get("trailingPE") or info.get("forwardPE") or 25
    term_pe = scores.get("_terminal_pe", min(current_pe * 0.7, 30))
    
    # Method 1: Analyst target dislocation
    analyst_score = 50  # neutral default
    if target and current and current > 0:
        dislocation = ((target - current) / current) * 100
        dislocation = max(-50, min(50, dislocation))
        analyst_score = 50 + dislocation
    
    # Method 2: PE-based fair value (the math doesn't lie)
    # If current PE > terminal PE, compression will drag returns
    pe_score = 50  # neutral default
    if current_pe > 0 and term_pe > 0:
        pe_ratio = term_pe / current_pe
        pe_compression = (pe_ratio ** (1/10) - 1) * 100
        # Each 1% annual PE compression = 3 point penalty (amplified because compounding)
        pe_score = 50 + pe_compression * 3
        pe_score = max(10, min(100, pe_score))
    
    # Take the MORE CONSERVATIVE (lower) of the two — protects against analyst optimism
    v_score = min(analyst_score, pe_score)
    v_method = "PE-math" if pe_score < analyst_score else "analyst"
    dislocation = ((target - current) / current) * 100 if (target and current and current > 0) else 0

    moat = scores.get("_moat_score", 70)

    # R5 weights: Valuation elevated to 30% because entry price matters most
    composite = q * 0.20 + g * 0.15 + v_score * 0.30 + d * 0.20 + moat * 0.15
    composite = round(composite, 1)

    return {
        "score": composite,
        "breakdown": {
            "quality": {"value": round(q, 1), "weight": 0.20},
            "growth": {"value": round(g, 1), "weight": 0.15},
            "valuation_dislocation": {
                "value": f"{dislocation:+.1f}%",
                "score": round(v_score, 1),
                "weight": 0.30,
                "method": v_method,
                "analyst_score": round(analyst_score, 1),
                "pe_score": round(pe_score, 1),
            },
            "durability": {"value": round(d, 1), "weight": 0.20},
            "moat": {"value": round(moat, 1), "weight": 0.15},
        },
    }


# ---------------------------------------------------------------------------
# PER-TICKER COMPUTATION
# ---------------------------------------------------------------------------
def compute_ticker(ticker: str, verbose: bool = False) -> dict:
    """Compute all R1-R5 scores for a single ticker."""
    if verbose:
        print(f"  Fetching {ticker}...", flush=True)

    cached = load_cached_gem(ticker) or {}
    data = try_yfinance(ticker)
    info = data.get("info", {})

    # Handle missing data: use deterministic proxy
    is_proxy = False
    if "error" in data and not info:
        is_proxy = True
    elif not info.get("currentPrice"):
        is_proxy = True

    if is_proxy:
        seed = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
        sector_map = {
            "MSFT": "Technology", "AMZN": "Consumer Cyclical", "GOOGL": "Communication Services",
            "META": "Communication Services", "AAPL": "Technology",
            "NVDA": "Technology", "TSM": "Technology", "AMD": "Technology",
            "AVGO": "Technology", "ASML": "Technology", "AMAT": "Technology",
            "SMH": "Technology", "NOW": "Technology", "SNPS": "Technology",
            "VEEV": "Healthcare", "CRM": "Technology", "SHOP": "Technology",
            "PLTR": "Technology", "V": "Financial Services", "MA": "Financial Services",
            "ADYEN": "Technology", "MELI": "Consumer Cyclical", "COIN": "Financial Services",
            "IBKR": "Financial Services", "SQ": "Technology", "SPGI": "Financial Services",
            "MCO": "Financial Services", "ICE": "Financial Services", "CME": "Financial Services",
            "BLK": "Financial Services", "BN": "Financial Services", "CSU": "Technology",
            "TCEHY": "Communication Services", "BABA": "Consumer Cyclical", "SE": "Technology",
            "GRAB": "Technology", "UBER": "Technology", "CPRT": "Industrials",
            "TDG": "Industrials", "DE": "Industrials", "FN": "Technology",
            "ISRG": "Healthcare", "IDXX": "Healthcare", "SPOT": "Communication Services",
            "ROKU": "Communication Services", "TSLA": "Consumer Cyclical",
            "EVO": "Consumer Cyclical", "SGX": "Financial Services", "DBS": "Financial Services",
            "SPCX": "Industrials", "CRCL": "Industrials", "MU": "Technology",
            "BKNG": "Consumer Cyclical", "EQIX": "Real Estate", "AMT": "Real Estate",
            "CRWD": "Technology", "PANW": "Technology", "MPWR": "Technology",
            "RMS": "Technology",
        }
        info = {
            "longName": info.get("longName") or ticker,
            "sector": sector_map.get(ticker.upper(), "Unknown"),
            "returnOnEquity": 0.10 + seed * 0.20 if info.get("returnOnEquity") is None else info["returnOnEquity"],
            "grossMargins": 0.30 + seed * 0.40 if info.get("grossMargins") is None else info["grossMargins"],
            "operatingMargins": 0.10 + seed * 0.20 if info.get("operatingMargins") is None else info["operatingMargins"],
            "revenueGrowth": 0.02 + seed * 0.10 if info.get("revenueGrowth") is None else info["revenueGrowth"],
            "earningsGrowth": 0.02 + seed * 0.10 if info.get("earningsGrowth") is None else info["earningsGrowth"],
            "forwardPE": 15 + seed * 25 if info.get("forwardPE") is None else info["forwardPE"],
            "debtToEquity": 20 + seed * 100 if info.get("debtToEquity") is None else info["debtToEquity"],
            "currentPrice": info.get("currentPrice"),
            "marketCap": info.get("marketCap"),
            "targetMeanPrice": info.get("targetMeanPrice"),
            "payoutRatio": info.get("payoutRatio") or 0.2 + seed * 0.3,
        }

    r1 = score_quality(info, cached)
    r2 = score_growth(info, cached)
    r3 = score_durability(info, cached)
    r4 = score_10yr_potential(info, cached)

    # Pass terminal_pe through for R5 valuation fallback
    term_pe = cached.get("terminal_pe") or (min((info.get("forwardPE") or 25) * 0.7, 30))
    
    scores_for_combo = {
        "R1_quality": r1,
        "R2_growth": r2,
        "R3_durability": r3,
        "R4_10yr_potential": r4,
        "_info": info,
        "_moat_score": cached.get("moat_score", 70),
        "_terminal_pe": term_pe,
    }
    r5 = score_combo(scores_for_combo)

    return {
        "ticker": ticker,
        "name": info.get("longName") or info.get("shortName") or ticker,
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "target_price": info.get("targetMeanPrice"),
        "data_sources": {
            "yfinance": not is_proxy,
            "cached_gem": bool(cached),
            "proxy": is_proxy,
        },
        "scores": {
            "R1_quality": r1,
            "R2_growth": r2,
            "R3_durability": r3,
            "R4_10yr_potential": r4,
            "R5_combo": r5,
        },
        "computed_at": datetime.now().isoformat(),
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Compute GARP tournament scores for 55-company universe")
    parser.add_argument("--output", default="data/universe_55_scores.json", help="Output JSON path")
    parser.add_argument("--tickers", help="Override: comma-separated ticker list")
    parser.add_argument("--workers", type=int, default=8, help="Parallel workers (default: 8)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    tickers = args.tickers.split(",") if args.tickers else UNIVERSE_55
    tickers = [t.strip() for t in tickers if t.strip()]

    print(f"🔢 Computing scores for {len(tickers)} companies ({args.workers} workers)...")
    print(f"   Estimated time: ~{len(tickers) * 2 // args.workers + 30}s")

    results = []
    failures = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(compute_ticker, t, args.verbose): t for t in tickers}
        for i, future in enumerate(as_completed(futures)):
            ticker = futures[future]
            try:
                result = future.result()
                results.append(result)
                r1 = result["scores"]["R1_quality"]["score"]
                r2 = result["scores"]["R2_growth"]["score"]
                r3 = result["scores"]["R3_durability"]["score"]
                r4 = result["scores"]["R4_10yr_potential"]["score"]
                r5 = result["scores"]["R5_combo"]["score"]
                src = "⚠ proxy" if result["data_sources"]["proxy"] else "✓ live"
                print(f"  [{i+1:2d}/{len(tickers)}] {ticker:6s} R1:{r1:5.1f} R2:{r2:5.1f} R3:{r3:5.1f} R4:{r4:5.1f} R5:{r5:5.1f} {src}")
            except Exception as e:
                print(f"  [{i+1:2d}/{len(tickers)}] {ticker:6s} ❌ FAILED: {e}")
                failures.append(ticker)

    # Sort by ticker for clean output
    results.sort(key=lambda r: r["ticker"])

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = {
        "version": "4.1",
        "computed_at": datetime.now().isoformat(),
        "universe_size": len(UNIVERSE_55),
        "computed_count": len(results),
        "failure_count": len(failures),
        "failures": failures,
        "tickers": results,
    }
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n✅ Saved {len(results)} companies → {output_path}")
    if failures:
        print(f"⚠️  {len(failures)} failures: {', '.join(failures)}")
    else:
        print("🎉 All 55 companies scored successfully!")


if __name__ == "__main__":
    main()

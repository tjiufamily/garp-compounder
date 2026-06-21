# Round Criteria Methodology

Detailed specification of the 5 rounds, their scoring formulas, and the reasoning behind each metric.

---

## Round 1: Quality

**Buffett lens:** "A wonderful business at a fair price beats a fair business at a wonderful price."

| Sub-Metric | Weight | Formula | Data Source |
|-----------|--------|---------|-------------|
| ROIC | 40% | Return on Invested Capital | Cached gem_thresholds + yfinance ROE proxy |
| Gross Margin | 20% | Gross profit / Revenue | yfinance grossMargins |
| Operating Margin | 15% | Operating income / Revenue | yfinance operatingMargins |
| FCF Proxy | 15% | Revenue growth × 1.5 + 30 | Derived |
| Leverage | 10% | 100 - max(0, Net Debt/EBITDA - 50) | yfinance debtToEquity |

**Composite:** Weighted sum, scaled 0-100.

**Why:** Filters out everything that can't compound long-term. A business with low ROIC, weak margins, or excessive leverage gets eliminated here.

---

## Round 2: Growth

**Buffett lens:** "The best business to own is one that, over time, will keep putting more money in your pocket."

| Sub-Metric | Weight | Formula | Data Source |
|-----------|--------|---------|-------------|
| 5yr Historical EPS CAGR | 33% | (EPS_2020 / EPS_2015)^(1/5) - 1 | yfinance earningsGrowth scaled |
| 5yr Forward EPS CAGR | 33% | Analyst consensus | TIKR estimates / cached gem |
| FCF Growth Rate | 34% | Revenue growth × 1.5 + 5 | Derived proxy |

**Composite:** Weighted sum, scaled 0-100.

**Why:** Filters out slow-growers from the survivors. Real growth = earnings + cash, not revenue.

---

## Round 3: Durability (Terminal P/E)

**Buffett lens:** "Time is the friend of the wonderful business."

| Sub-Metric | Weight | Formula | Data Source |
|-----------|--------|---------|-------------|
| Terminal P/E | 40% | Damodaran Mode B Step 4B output | Cached gem_thresholds |
| Quality-Adjusted Peer P/E | 30% | Peer median × moat premium | Cached peer_median_pe |
| Network Effect Score | 30% | 1-5 rubric → 20-100 | Cached moat rubric |

**Composite:** Weighted sum, scaled 0-100.

**Why:** If competitors catch up over 10 years, the terminal multiple collapses — and so does your actual return. Only businesses with structural moats command premium multiples in 2036.

---

## Round 4: 10yr EPS CAGR

**Buffett lens:** "Buy businesses, not stocks."

**Single metric:** 10-year forward EPS CAGR (the institutional-grade Damodaran Mode B Turbo output).

**Default proxy formula** (used when cached value unavailable):
```
cagr_10y = max(2, min(30, (earnings_growth × 0.7 + revenue_growth × 0.5) × 100 + 4))
```

**For finalists only:** Run dcf-valuation-engine in Mode B for fresh computation.

**Why:** "This is the most important number. If you can't articulate a 10-year EPS path, you don't understand the business."

---

## Round 5: Combo (incl. Valuation)

**Buffett lens:** "Price is what you pay; value is what you get."

| Component | Weight | Source |
|-----------|--------|--------|
| R1 Quality | 25% | Reuse from Round 1 |
| R2 Growth | 25% | Reuse from Round 2 |
| Valuation Dislocation | 25% | (target - current) / current × 100 |
| R3 Durability (Terminal) | 15% | Reuse from Round 3 |
| Moat Score | 10% | Cached moat rubric |

**Composite:** Weighted sum, scaled 0-100.

**Why:** The holistic check. Cheap wonderful businesses beat expensive ones — but not always. Combo determines who to hold for the long term.

---

## Pairing Algorithm

**Smart seeding by Round 1 Quality:**
1. Compute R1 Quality for all 24 tickers
2. Sort descending
3. Pair: #1 vs #24, #2 vs #23, #3 vs #22, etc.
4. Each subsequent round re-seeds by current round's score

**Why:** Strong parties don't meet each other early. The number 24 seed plays the number 1 seed in Round 1 — only one survives.

---

## Educational Layer

Each round has:
- **Pre-round quote** (Buffett or Munger)
- **Pre-round principle** (1 paragraph)
- **Post-round lesson** (summary of what survivors demonstrated)

These are pre-written in `ROUND_DEFS` constant in `garp_tournament.html`. Edit them there to customize.
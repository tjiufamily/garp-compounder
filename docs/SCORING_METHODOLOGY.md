# Scoring Methodology

Detailed formulas and source priorities for the 5-round scoring engine.

---

## Data Source Priority

| Source | When Used | Speed | Cost |
|--------|-----------|-------|------|
| 1. Cached `gem_thresholds.json` | Always (fastest) | <1s | Free |
| 2. TIKR MCP | When no cache, or >30 days old | ~3s/ticker | API |
| 3. yfinance | When TIKR fails, or no cid | ~2s/ticker | Free |
| 4. FastGraphs MCP | For valuation data fallback | ~5s/ticker | Auth required |
| 5. Manual user input | Last resort | — | User time |

---

## Per-Ticker Scoring Pipeline

For each ticker in the active universe:

```
1. Load cached gem_thresholds.json if exists
2. Fetch yfinance financials (info, income, balance sheet, cash flow)
3. Compute R1-R5 scores using cached values where available
4. Return JSON with full breakdown
```

---

## ROIC Computation

**Primary (cached):** `gem_thresholds.json` → `roic_floor_pct`

**Fallback (yfinance):**
```python
roe = info.get("returnOnEquity")  # decimal
roic = min(roe * 100, 35)  # cap at 35% (ROIC > ROE normally)
```

ROIC > WACC is the fundamental test of a wonderful business. Above 25% = compounder quality.

---

## Terminal P/E Computation

**Primary (cached):** `gem_thresholds.json` → `terminal_pe`

**Fallback:** Forward P/E × 1.3 (30% premium for quality businesses)

---

## 10yr EPS CAGR Computation

**Primary (cached):** `gem_thresholds.json` → `eps_cagr_10y_pct`

**Proxy fallback:**
```python
eg = info.get("earningsGrowth") or 0  # decimal
rg = info.get("revenueGrowth") or 0  # decimal
cagr_10y = max(2, min(30, (eg * 0.7 + rg * 0.5) * 100 + 4))
```

**For finalists only:** Run `dcf-valuation-engine` in Mode B Turbo.

---

## Valuation Dislocation

```python
target = info.get("targetMeanPrice")
current = info.get("currentPrice")
if target and current and current > 0:
    dislocation_pct = ((target - current) / current) * 100
    dislocation_score = 50 + dislocation_pct  # -50% → 0; 0% → 50; +50% → 100
else:
    dislocation_score = 50  # neutral
```

---

## Composite Score (R5 Combo)

```python
composite = (
    0.25 * R1_quality +
    0.25 * R2_growth +
    0.25 * valuation_dislocation +
    0.15 * R3_durability +
    0.10 * moat_score
)
```

---

## Cache TTL

| Round | TTL | Rationale |
|-------|-----|-----------|
| R1 Quality | 30 days | Moat scores move slowly |
| R2 Growth | 30 days | Estimates adjust quarterly |
| R3 Durability | 30 days | Peer comparisons move slowly |
| R4 10yr CAGR | 7 days | Must be fresh for tournament |
| R5 Combo | 7 days | Valuation component needs to be current |

---

## Known Limitations

1. **HK/SG tickers** with `.HK`/`.SG` suffixes may fail yfinance — fallback proxy applied.
2. **Forward EPS** from yfinance is the `earningsGrowth` field, which is recent-quarter YoY — not full 5-year forward.
3. **Terminal P/E** from cached gem is computed via Damodaran Mode B; without cache, falls back to forward P/E × 1.3.
4. **Moat score** without cached gem defaults to 70 (neutral).
5. **Network effect score** without cached gem defaults to 3/5 (neutral).

For tournament-quality results, ensure `gem_thresholds.json` is populated for all tickers first.
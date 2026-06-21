# ⚽ GARP COMPOUNDER CHAMPIONSHIP — v4.1 Proposal (REVISED)

**For:** James T (TJIUNARDI RESEARCH)
**Date:** 21 June 2026
**Status:** PROPOSAL — revised per user feedback

---

## 📋 Changes from v4.0

| # | Change | Reason |
|---|--------|--------|
| 1 | **Winner = weighted composite score**, not "won all metrics" | One-sentence verdict explains which sub-metrics drove the win |
| 2 | **Pre-computation with educational display** — while numbers crunch, user reads through criteria importance + weighting formulas | Keeps user engaged; rewards patience |
| 3 | **Metrics always visible at top/side per round** — football match stat style | Clean, uncluttered, informative |
| 4 | **R1: Leverage → ROE (10%)** | ROE is more predictive of compounder quality |
| 5 | **R4: Replaced single Damodaran CAGR with 5 metrics** | Mode B too slow; 5 sub-metrics capture the same insight |
| 6 | **Default universe: 55 companies** (user's curated list) | No custom tickers needed; all data pre-computable |
| 7 | **Comparison indices: S&P 500, Nasdaq 100, SMH** | 3 benchmarks, not just 1 |
| 8 | **Champion prediction: 50 pts** (was 20) | Higher stakes for the big call |
| 9 | **Commissioner override mode: YES** | User can override AI winner if desired |
| 10 | **Desktop-first design**, mobile secondary | James usually on desktop |
| 11 | **Playback ability** — go back to previous rounds | Review past matches |
| 12 | **Reading rewards** — points for engaging with educational content | Incentivizes patience and learning |
| 13 | **Per-round user scorecard** | Track progress after each round |
| 14 | **Narrative layer per round**: past winners, past failures, why this criterion matters, law of large numbers, Act II/III examples | Deep educational value |
| 15 | **End-game emphasis**: basket of compounders, difficulty of beating indices, durability > growth | Mental model reinforcement |

---

## 🎯 Core Concept (Unchanged)

A 5-round knockout tournament where **32 companies** (selected by user from a 55-company default watchlist) face off. The **AI computes the true winner** based on real weighted metrics — but the **user predicts before each reveal**. User scored on accuracy. Educational narrative runs throughout.

---

## 👥 Default Universe — 55 Companies

The user selects exactly **32** from this pre-curated list. All 55 have data pre-computed before the tournament begins.

| Category | Tickers |
|----------|---------|
| **Mega-Cap Tech** | MSFT, AMZN, GOOGL, META, AAPL |
| **Semiconductors** | NVDA, TSM, AMD, AVGO, ASML, AMAT, SMH |
| **SaaS / Cloud** | NOW, SNPS, VEEV, CRM, SHOP, PLTR |
| **Payments / Fintech** | V, MA, ADYEN, MELI, COIN, IBKR, SQ |
| **Financial Infra** | SPGI, MCO, ICE, CME, BLK, BN, CSU |
| **E-commerce / Internet** | 0700.HK (Tencent), BABA, SE, GRAB, UBER, MELI |
| **Enterprise / Industrials** | CPRT, TDG, DE, FN |
| **Healthcare** | ISRG, IDXX |
| **Media / Entertainment** | SPOT, ROKU |
| **EV / Auto** | TSLA |
| **Gaming / Esports** | EVO |
| **Brokerage / Exchange** | SGX, DBS |
| **Communications** | H (Hydro One), CSGP |
| **Space / Defense** | SPCX, CRCL |
| **Memory / Storage** | MU |
| **Travel / Booking** | BKNG |
| **Data Centers / Infra** | EQIX, AMT |
| **Cyber / Security** | CRWD, PANW |

> *Note: User can deselect any from the 55 but cannot add custom tickers. Minimum 32 must be selected. If < 32, byes added.*

---

## 📊 The 5 Rounds — REVISED Criteria (with 5 sub-metrics each)

---

### **ROUND 1: QUALITY**  
> *"A wonderful business at a fair price beats a fair business at a wonderful price."* — Buffett

**Why this matters:** Quality filters out everything that cannot compound long-term. A business with low returns on capital, weak margins, or no cash generation will eventually run out of fuel. This round eliminates the pretenders.

| # | Sub-Metric | Weight | Plain English | Source |
|---|-----------|--------|---------------|--------|
| 1 | **ROIC** | 40% | For every $100 invested, how much profit comes back? Above 25% = elite compounder. Below 10% = barely above cost of capital. | yfinance + cached gem |
| 2 | **Gross Margin** | 20% | After making the product, how much is left? 70%+ = pricing power. 20% = commodity. | yfinance |
| 3 | **Operating Margin** | 15% | After ALL costs, what remains? Measures efficiency. 30%+ = world-class. | yfinance |
| 4 | **FCF Growth Rate** | 15% | Is cash generation accelerating? FCF funds buybacks, dividends, and reinvestment. | yfinance (revenue growth proxy) |
| 5 | **ROE** (Return on Equity) | 10% | How efficiently does the company use shareholder money? 20%+ = excellent capital allocator. | yfinance |

**Scoring:** Each sub-metric mapped 0-100 via calibrated linear formula, then weighted composite. Max = 100.

**Match Card Display (side-by-side):**
```
⚽ GOOGL  83.4  —  QUALITY SCORES  —  45.7  BABA
   ROIC     35.2%  ████████░░  87.5    18.7%  ████░░░░░░  46.8
   Gross M  56.8%  ██████░░░░  79.5    38.2%  ████░░░░░░  53.5
   Op M     30.1%  ██████░░░░  66.3    15.4%  ███░░░░░░░  33.9
   FCF Gr   22.1%  ██████░░░░  65.3     8.3%  ███░░░░░░░  30.4
   ROE      28.5%  ██████░░░░  71.3    12.1%  ███░░░░░░░  30.3
   TOTAL    83.4              45.7
```

---

### **ROUND 2: GROWTH**  
> *"The best business to own is one that over time will keep putting more money in your pocket."* — Munger

**Why this matters:** Quality without growth is a bond. Growth without quality is a lottery ticket. This round tests whether survivors from R1 can actually grow their earnings at rates that beat the market. Only businesses with expanding addressable markets and pricing power pass.

**Past winners on this criterion:** MSFT (2014-2024: 15%+ EPS CAGR driven by cloud transition), NVDA (2019-2024: 50%+ CAGR from AI).

**Past failures:** GE (grew earnings through financial engineering, not organic FCF — collapsed when accounting was exposed), IBM (revenue growth stalled for years despite buybacks inflating EPS).

| # | Sub-Metric | Weight | Plain English | Source |
|---|-----------|--------|---------------|--------|
| 1 | **5yr Historical EPS CAGR** | 25% | How fast have earnings actually grown? Real numbers, not promises. 15%+ = outstanding. | yfinance |
| 2 | **5yr Forward EPS CAGR** | 25% | What do analysts forecast? Forward-looking consensus. | TIKR estimates (yfinance fallback) |
| 3 | **FCF Growth Rate** (TTM vs 5yr avg) | 25% | Is cash growing? Cash > accounting earnings. | Derived from yfinance |
| 4 | **Revenue Growth Consistency** | 15% | Did revenue grow every year for the last 5 years? Consistency = predictability. 5/5 years = 100. | yfinance |
| 5 | **Reinvestment Rate** | 10% | How much of earnings is being reinvested into future growth? 50%+ = management believes in the business. | Derived (1 − payout ratio proxy) |

---

### **ROUND 3: DURABILITY**  
> *"Time is the friend of the wonderful business."* — Buffett

**Why this matters:** THE most important round. Many companies grow fast for 5 years, then stall. Durability tests whether the business can sustain its competitive advantage for 10+ years. If competitors can copy it, the terminal multiple collapses — and so does your return.

**The Law of Large Numbers problem:** A company growing at 20% for 30 years becomes larger than the US economy. Only businesses that expand into new markets (Act II), launch new products (Act III), or own infrastructure with network effects can defy this gravity.

**Past winners:** Microsoft (Act II: cloud → Act III: AI), Apple (iPod → iPhone → Services), Amazon (Books → Everything → AWS → Ads).

**Past failures:** BlackBerry (dominant in smartphones, failed Act II), Nokia (same), GoPro (one product, no Act II).

| # | Sub-Metric | Weight | Plain English | Source |
|---|-----------|--------|---------------|--------|
| 1 | **Terminal P/E** | 30% | What multiple can this company command in 10 years? 30x+ = exceptional moat. <15x = competitors will erode profits. | Cached gem or fwd P/E × quality factor |
| 2 | **Quality-Adjusted Peer P/E** | 20% | Compared to rivals, is the premium justified? | yfinance peer comparison |
| 3 | **Network Effect Score** (1–5) | 20% | Does it get stronger as more people use it? 5 = Meta, Google. 1 = commodity. | Cached moat rubric |
| 4 | **Act II Potential** (1–5) | 20% | Can the company extend growth into adjacent markets? 5 = MSFT/AMZN-level adjacency. 1 = single-product dependency. | Cached gem + sector analysis |
| 5 | **Industry Secularity** (1–5) | 10% | Is the industry growing structurally, or is it cyclical? 5 = AI/semiconductors. 1 = oil/gas. | Sector-based heuristic |

---

### **ROUND 4: 10-YEAR POTENTIAL** (Replaces Damodaran Mode B)  
> *"Buy businesses, not stocks."* — Munger

**Why this matters:** This is the "what does this look like in 2036?" round. Instead of a single Damodaran computation (too slow), we use 5 metrics that capture the same forward-looking insight. Each metric is a building block of the Damodaran framework.

| # | Sub-Metric | Weight | Plain English | Source |
|---|-----------|--------|---------------|--------|
| 1 | **Historical Growth Durability** | 25% | How long has the company sustained >10% EPS growth? Years of consecutive 10%+ growth. 10+ yrs = 100. | yfinance (earnings history) |
| 2 | **Analyst Forward Growth Consensus** | 25% | What do professional analysts forecast for 5yr forward growth? Weighted average. | TIKR estimates / yfinance |
| 3 | **Industry Growth Rate** | 20% | Is the industry itself growing? A rising tide lifts all boats. 15%+ = strong tailwind. | Industry reports / proxy |
| 4 | **Industry Secularity Score** | 15% | Structural growth vs cyclical? Secular = sustainable. Cyclical = mean-reverts. 5 = AI chips. 1 = shipping. | Sector mapping |
| 5 | **Act II Fitness** | 15% | How well does the company's next growth phase align with its current strengths? MSFT cloud→AI = seamless. GE finance→industrial = mismatch. | Cached gem + qualitative rubric |

**Scoring:** Each sub-metric mapped 0-100, weighted. Max = 100.

---

### **ROUND 5: COMBO (The Holistic Check)**  
> *"Price is what you pay; value is what you get."* — Buffett

**Why this matters:** The final test. A wonderful business at a terrible price is still a bad investment. This round blends quality, growth, durability, and current valuation into a single veredict. The survivor of Round 5 is the compounder with the highest probability of long-term outperformance.

| # | Sub-Metric | Weight | Plain English | Source |
|---|-----------|--------|---------------|--------|
| 1 | R1 Quality (carry-over) | 20% | Quality foundation | Cached |
| 2 | R2 Growth (carry-over) | 20% | Growth trajectory | Cached |
| 3 | **Valuation Dislocation** | 25% | Is the stock under/overvalued? (target − current) / current. +20% = bargain. −20% = expensive. | yfinance |
| 4 | R3 Durability (carry-over) | 20% | Terminal staying power | Cached |
| 5 | Moat Score (carry-over) | 15% | Overall competitive advantage | Cached gem |

---

## 🎮 Game Flow — REVISED

### STEP 0: SELECT YOUR 32
- 55-company grid displayed (grouped by category)
- User checks/unchecks companies
- Counter: "Selected: 28/32 — pick 4 more"
- Cannot proceed until exactly 32 selected
- **Preview:** Each company shows its cached R1 Quality score (if available) as a reference

### STEP 1: PRE-TOURNAMENT PICKS
- 32 selected teams shown in a grid
- User picks **2 predicted semi-finalists** and **1 predicted champion**
- Points: 20 pts per semi-finalist, **50 pts** for champion

### STEP 2: DATA CRUNCH + EDUCATIONAL INTERLUDE (~3 min)
- All 32 companies scored in parallel (background)
- **Front-and-center:** Educational carousel explaining:
  - What each of the 5 rounds tests
  - Why those 5 sub-metrics per round matter
  - How weighted scoring works (visual formula display)
  - Examples of past companies that passed/failed each round
  - The Law of Large Numbers visualization
  - Act II / Act III explainer with real company examples from James's research
- **Reading rewards tracker:** "You've read 3 of 7 lessons — earn up to 21 bonus points!"
- **Progress bar:** "Crunching numbers... ████████░░ 78% (25/32 scored)"

### STEP 3: ROUND 1 — QUALITY (32→16)
- Full bracket visible (left half: 16 teams, right half: 16 teams)
- **Round header banner:** Criteria summary with all 5 sub-metrics and weights
- Match cards with side-by-side metric bars (as designed above)
- User predicts → AI reveals → winner advances
- **After each match:** Winner slides to next round position in bracket
- **Per-round scorecard updates:** "R1: 12/16 correct · 36 pts"
- **Round complete:** confetti + "What We Learned" narrative

### STEP 4-7: ROUNDS 2-5
- Same flow. Each round has its own educational narrative.
- **R2 narrative:** Growth consistency, why revenue matters, GE/IBM cautionary tales
- **R3 narrative:** Durability, Law of Large Numbers, Act II/III examples
- **R4 narrative:** 10-year vision, industry tailwinds, secular vs cyclical
- **R5 narrative:** Valuation matters too, even wonderful businesses can be overpriced

### STEP 8: CHAMPION REVEAL
- Trophy animation + full celebration (horn, confetti, crowd)
- **User Scorecard:**
  ```
  📊 YOUR PERFORMANCE
  ─────────────────────────────────
  Match Predictions:    24/31 correct    72 pts
  Semi-finalist Picks:   1/2 correct     20 pts
  Champion Pick:         1/1 correct     50 pts
  Reading Rewards:       7/7 complete    21 pts
  ─────────────────────────────────
  TOTAL: 163/247 pts  |  RANK: Buffett Apprentice ⭐⭐⭐⭐
  ```

### STEP 9: WEALTH PROJECTION + INDEX COMPARISON

> *"NVDA's 10-year CAGR: 18.2%. Here's what $10,000 becomes vs the indices:"*

| | Year 10 | Year 20 | Year 30 | Year 40 |
|---|---|---|---|---|
| 🏆 **NVDA** (18.2%) | $53,200 | $283,000 | $1,510,000 | $8,040,000 |
| 📈 **S&P 500** (10.5%) | $27,100 | $73,500 | $199,000 | $540,000 |
| 📈 **Nasdaq 100** (13.2%) | $34,600 | $119,000 | $412,000 | $1,423,000 |
| 📈 **SMH** (14.8%) | $39,700 | $157,000 | $623,000 | $2,470,000 |

- **Animated bar chart:** $10K → $8M over 40 years, with index comparison lines

### STEP 10: FINAL LESSONS
- "Only a handful of companies can compound at 15%+ for 30 years."
- "This is why a **basket** of strong compounders beats betting on one."
- "Durability matters most — growth without durability is a trap."
- "The wrong criteria eliminate strong players too early. The right criteria separate the truly wonderful from the temporarily lucky."
- "Even the winner here may fail. Compounding is probabilistic, not certain. Own 8-12 of these."

---

## 🔢 REVISED Scoring System

| Achievement | Points | When Awarded |
|-------------|--------|--------------|
| Correct match prediction | 3 pts | After each match reveal |
| Correct semi-finalist pick | 20 pts | When that team reaches semi-finals |
| Correct champion pick | **50 pts** | When that team wins the final |
| Reading reward (per lesson) | 3 pts | After reading each of 7 educational interludes |
| **Max possible** | **247 pts** | 93 match + 40 semi + 50 champion + 21 reading |

**Rank thresholds:**
- 0-60: Rookie Analyst
- 61-120: Junior Investor
- 121-180: Fund Manager
- 181-230: Buffett Apprentice
- 231+: Oracle of Omaha

---

## 🎨 Visual Design Notes

### Bracket Layout (Desktop)
- Full-width symmetric knockout tree
- Left half: 16 teams descending from left edge
- Right half: 16 teams descending from right edge
- Center: Final match with 🏆 trophy above
- Connector lines: gold (#C9A35A) on dark pitch green (#0d4f1f)
- Winner paths: animated gold highlight after each match

### Round Header (Each Round)
```
┌─────────────────────────────────────────────────────────────┐
│  ⚽ ROUND 1: QUALITY                                        │
│  ─────────────────────────────────────────────────────────  │
│  ROIC 40% · Gross Margin 20% · Op Margin 15%               │
│  FCF Growth 15% · ROE 10%                                   │
│                                                             │
│  ℹ️ Why: Filters out everything that can't compound         │
│  long-term. Wonderful businesses earn above cost of         │
│  capital. Anything else is speculation.                     │
└─────────────────────────────────────────────────────────────┘
```

### Match Card (Each Matchup)
- Side-by-side comparison bars (gold fill proportional to score)
- 5 metric rows with values for both teams
- Weight displayed next to each metric name
- Total weighted score at bottom
- "YOUR PICK" buttons before reveal
- "REVEAL WINNER" button
- After reveal: winner glows gold, one-sentence verdict appears

### Per-Round Scorecard (Side Panel)
```
┌──────────────────────┐
│  🎮 YOUR SCORECARD   │
│  ───────────────────  │
│  R1: 12/16 · 36 pts  │
│  R2:  5/8  · 15 pts  │
│  R3:  2/4  ·  6 pts  │
│  ───────────────────  │
│  Total: 57 pts       │
│  Reading: 4/7 · 12   │
└──────────────────────┘
```

---

## 📚 Educational Narrative Per Round (Summary)

### During Computation (Pre-Tournament)
- Lesson 1: "What Makes a Wonderful Business?" — ROIC, margins, moats explained
- Lesson 2: "The 5 Criteria That Matter Most" — overview of all 5 rounds
- Lesson 3: "How Weighted Scoring Works" — formula visualization
- Lesson 4: "The Law of Large Numbers" — why big companies can't grow forever
- Lesson 5: "Act II & Act III" — how great companies extend their growth runway
- Lesson 6: "Basket vs Single Stock" — why diversification within quality matters
- Lesson 7: "Beating the Index" — how hard it is, why the criteria matter

### Round 1 — Quality
- "Past Winner on Quality": MSFT (ROIC 35%+, Gross Margin 69%)
- "Past Failure on Quality": GE (financial engineering masked poor underlying ROIC)

### Round 2 — Growth
- "Past Winner on Growth": NVDA (EPS CAGR 50%+ during AI boom)
- "Past Failure on Growth": IBM (buybacks inflated EPS, no organic revenue growth)

### Round 3 — Durability
- "Past Winner on Durability": AMZN (Books → Everything → AWS → Ads — three Acts)
- "Past Failure on Durability": BlackBerry (dominant in 2008, irrelevant by 2013)

### Round 4 — 10-Year Potential
- "Past Winner on 10yr Potential": ASML (structural monopoly in EUV lithography — 10+ year visibility)
- "Past Failure on 10yr Potential": GoPro (one product, no Act II, industry commoditized)

### Round 5 — Combo
- "Past Winner on Combo": AAPL (quality + growth + durability + reasonable valuation in 2016)
- "Past Failure on Combo": CSCO (great quality, but priced for perfection in 2000 — never recovered)

---

## 💾 Technical Architecture

### Data Pre-Computation
- All 55 companies scored once, cached to `data/universe_55_scores.json`
- User selects 32 → scores already available (instant)
- If user's selection includes a ticker without cached data, compute on-demand (~2s per ticker)

### Playback
- "Go Back to Round X" button on each screen
- Replay mode: step through each past match, see prediction vs actual
- Full tournament replay from saved JSON

### Commissioner Override
- Toggle in settings: "Commissioner Mode: ON/OFF"
- When ON: after AI reveal, a "⚙️ Override" button appears
- Override logs the change as a commissioner decision

---

## 📱 Mobile Layout
- Bracket collapses to vertical scrollable list
- Match cards stack full-width
- Metric bars remain visible
- Scorecard slides to bottom of screen

Desktop is primary design target. Mobile is adapted, not redesigned.

---

## 🚀 Build Plan (12 hours, 6 phases)

| Phase | What | Files | Est. |
|-------|------|-------|------|
| **1** | Pre-compute all 55 companies, expanded metrics (R4 5-metric), cache JSON | `garp_score_v4_1.py`, `data/universe_55_scores.json` | 2 hrs |
| **2** | Bracket HTML/CSS: symmetric knockout tree, match cards with bars, round headers, scorecard side panel | `garp_tournament_v4_1.html`, `style_v4_1.css` | 4 hrs |
| **3** | JS game logic: predict→reveal→advance, scoring, pre-tournament picks, reading rewards, playback | (in HTML) | 3 hrs |
| **4** | Sound + confetti + champion screen + wealth projection (3 indices) + index comparison graph | (in HTML) | 1.5 hrs |
| **5** | Educational narrative carousel (7 lessons + round-specific stories, past winners/failures) | `assets/narrative.json` | 1.5 hrs |
| **6** | GitHub packaging, README, docs/, CI | `docs/`, `.github/` | 1 hr |

---

## ✅ Ready?

All 55 companies pre-loaded. All criteria finalized. All educational narratives mapped. Commissioner override included. Playback supported. Reading rewards incentivized. Index comparisons (S&P 500, Nasdaq 100, SMH) built in.

Say **GO** and I'll start Phase 1 — computing all 55 companies with the revised 5-metric-per-round scoring engine.

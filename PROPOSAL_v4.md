# ⚽ GARP COMPOUNDER CHAMPIONSHIP — v4 Proposal

**For:** James T (TJIUNARDI RESEARCH)  
**Date:** 21 June 2026  
**Status:** PROPOSAL — not building yet

---

## 🎯 Core Concept

A 5-round knockout tournament where **32 compounder companies** face off.  
The **AI computes the true winner** based on real financial metrics — but the **user predicts before each reveal**.  
The user is scored on how many predictions they get right *and* on their pre-tournament picks for semi-finalists and champion.

> *"It's not who YOU think will win — it's who the DATA says will win. See how well you really know your compounders."*

---

## 👥 Two Modes of Play

### Mode A: Full Predictive (Hard)
1. User assembles 32 companies (minimum) from their watchlist or custom CSV
2. **Before Round 1 kickoff**, user picks **2 predicted semi-finalists** and **1 predicted champion** — these lock in 20 points each if correct
3. Before each match, user picks who they think will win
4. AI reveals the winner based on real computed metrics + a one-sentence data-driven explanation
5. User gets 3 points for each correct match prediction
6. **Max score: 226 points** (72 match predictions × 3 + 2 semi-finalists × 20 + 1 champion × 20)

### Mode B: Spectator (Easy)
1. Same bracket, same AI computation, same reveal
2. No user predictions — just watch and learn
3. AI narrator explains each match outcome in plain English with Buffett/Munger wisdom
4. Perfect for children, students, or casual observers

---

## 🖼️ Visual Bracket Design (Referencing User's Image)

### Layout: Symmetric Knockout Tree

```
                     SEMI-FINAL LEFT          FINAL          SEMI-FINAL RIGHT
                    
  Round 1           Round 2      Round 3      🏆      Round 3      Round 2     Round 1
  (32→16)           (16→8)       (8→4)                (8→4)        (16→8)      (32→16)

  [GOOGL]──┐
           ├──[GOOGL]──┐
  [BABA]───┘           ├──[GOOGL]──┐
                       │           │
  [TSM]────┐           │           │
           ├──[TSM]────┘           │
  [VEEV]───┘                       ├──[GOOGL]────┐
                                                    │
                                  ...              ├──[CHAMPION]─── 🏆
                                                    │
  [MSFT]───┐                       ├──[NVDA]──────┘
           ├──[MSFT]────┐           │
  [BIDU]───┘           ├──[NVDA]──┐ │
                       │           │
  [NVDA]───┐           │           │
           ├──[NVDA]───┘           │
  [BKNG]───┘                       │
                                   │
  [AMZN]───┐                       │
           ├──[AMZN]───┐           │
  [JNJ]────┘           ├──[META]──┐
                       │           │
  [META]───┐           │           │
           ├──[META]───┘           │
  [KO]─────┘                       │
                                   │
  ... more teams ...               │
```

- **Left half:** 16 teams enter from the left, converge toward center
- **Right half:** 16 teams enter from the right, converge toward center
- **Lines/connectors:** Styled as football pitch lines (gold on dark green)
- **Winner path:** Highlighted in gold after each match is decided
- **Progressive reveal:** After each match, the bracket updates live — winner's chip slides to next round

### Match Card Design (Each Matchup)

```
┌─────────────────────────────────────────────┐
│  MATCH 7 — Round 1: QUALITY                  │
│  ─────────────────────────────────────────── │
│                                              │
│  🏠 GOOGL                        BABA 🏟️     │
│  ─────────────────────────────────────────── │
│                                              │
│  🔍 KEY METRICS:                             │
│  ┌──────────────┬──────────┬──────────┐      │
│  │   Metric     │  GOOGL   │   BABA   │      │
│  ├──────────────┼──────────┼──────────┤      │
│  │ ROIC         │  35.2%   │  18.7%   │      │
│  │ Gross Margin │  56.8%   │  38.2%   │      │
│  │ Op Margin    │  30.1%   │  15.4%   │      │
│  │ Debt/Equity  │   0.12   │   0.38   │      │
│  │ FCF Growth   │  22.1%   │   8.3%   │      │
│  ├──────────────┼──────────┼──────────┤      │
│  │ SCORE (0-100)│   83.4   │   45.7   │      │
│  └──────────────┴──────────┴──────────┘      │
│                                              │
│  🤔 YOUR PICK:  [ GOOGL ]  [ BABA ]          │
│                                              │
│  [ PREDICT & REVEAL WINNER ]                 │
└─────────────────────────────────────────────┘
```

The metrics table is **always visible** — no "click to see detail." Every metric has a real value computed from real data.

### After Reveal:

The winner's side glows gold. A one-sentence data verdict appears:

> ✅ **GOOGL advances.** Winner dominated all 5 sub-metrics — ROIC (35.2% vs 18.7%), gross margin (56.8% vs 38.2%), operating margin (30.1% vs 15.4%). Composite score: 83.4 vs 45.7.  
> *You picked correctly! +3 points. 🎯*

---

## 📊 The 5 Rounds — Detailed Criteria

Each round has a **distinct criterion** with multiple weighted sub-metrics.  
The composite score determines the winner (0-100, higher score advances).  
Ties are broken by the first sub-metric in order.

---

### **ROUND 1: QUALITY**  
> *"A wonderful business at a fair price beats a fair business at a wonderful price."* — Buffett  

| # | Sub-Metric | Weight | What It Means (Plain English) | Source |
|---|-----------|--------|-------------------------------|--------|
| 1 | **ROIC** (Return on Invested Capital) | 40% | For every $100 the company invests, how much profit does it generate? Above 25% = exceptional compounder. Below 10% = barely above cost of capital. | yfinance + cached gem |
| 2 | **Gross Margin** | 20% | After paying direct costs to make the product, how much money is left? 70%+ = pricing power (Apple, Microsoft). 20% = commodity business. | yfinance |
| 3 | **Operating Margin** | 15% | After ALL operating costs, what's left? Shows efficiency. 30%+ = elite. 10% = average. | yfinance |
| 4 | **FCF Growth Rate** | 15% | Is free cash flow growing? Cash pays dividends, buys back shares, funds growth. Negative = red flag. | yfinance (revenue growth proxy) |
| 5 | **Leverage (Debt/Equity)** | 10% | How much debt? Low debt = can survive recessions. D/E < 0.5 = fortress. D/E > 2.0 = risky. | yfinance |

**Scoring:** Each sub-metric mapped 0-100 via calibrated formula, then weighted composite.

---

### **ROUND 2: GROWTH**  
> *"The best business to own is one that over time will keep putting more money in your pocket."* — Munger  

| # | Sub-Metric | Weight | What It Means (Plain English) | Source |
|---|-----------|--------|-------------------------------|--------|
| 1 | **5yr Historical EPS CAGR** | 33% | How fast have earnings actually grown over the last 5 years? 15%+ = outstanding. 5% = inflation-level. | yfinance (earnings growth × decay factor) |
| 2 | **5yr Forward EPS CAGR** | 33% | What do analysts expect earnings to grow over the next 5 years? Forward-looking. 15%+ = high expectations. | TIKR estimates (fallback: yfinance) |
| 3 | **FCF Growth Rate** (TTM vs 5yr avg) | 34% | Is the cash-generating engine accelerating or decelerating? Growing FCF = sustainable growth. | Derived from yfinance |

**Scoring:** 0-20% CAGR scale → 0-100 score. 20% CAGR = score 100. Below 2% = score 10.

---

### **ROUND 3: DURABILITY (TERMINAL P/E)**  
> *"Time is the friend of the wonderful business."* — Buffett  

| # | Sub-Metric | Weight | What It Means (Plain English) | Source |
|---|-----------|--------|-------------------------------|--------|
| 1 | **Terminal P/E** | 40% | What P/E multiple can this company command 10 years from now? Derived from Damodaran terminal value analysis. 30x+ = exceptional moat. <15x = competitors will eat margins. | Cached gem_thresholds or forward P/E × 1.3 |
| 2 | **Quality-Adjusted Peer P/E** | 30% | Compared to industry peers, is this company's multiple justified? Above peer median = market recognizes quality premium. Below = undervalued or lower quality. | yfinance peer comparison |
| 3 | **Network Effect Score** (1-5 rubric) | 30% | Does the business get stronger as more people use it? 5/5 = Meta, Google (self-reinforcing). 1/5 = commodity producer. | Cached moat rubric or sector heuristic |

---

### **ROUND 4: 10-YEAR EPS CAGR**  
> *"Buy businesses, not stocks."* — Munger  

| # | Sub-Metric | Weight | What It Means | Source |
|---|-----------|--------|---------------|--------|
| 1 | **10yr Forward EPS CAGR** | 100% | Single most important number. What does this business look like in 2036? Computed via Damodaran Mode B Turbo (or proxy for non-finalists). 15%+ CAGR = double your money in 5 years. 5% = barely beat inflation. | Cached gem_thresholds or dcf-valuation-engine Mode B |

**For finalists only (top ~5):** Fresh Damodaran Mode B computation via dcf-valuation-engine.

---

### **ROUND 5: COMBO (The Holistic Check)**  
> *"Price is what you pay; value is what you get."* — Buffett  

| # | Sub-Metric | Weight | What It Means | Source |
|---|-----------|--------|---------------|--------|
| 1 | R1 Quality (carry-over) | 25% | Reuse the Quality score from Round 1 | Cached |
| 2 | R2 Growth (carry-over) | 25% | Reuse the Growth score from Round 2 | Cached |
| 3 | **Valuation Dislocation** | 25% | Is the stock overvalued or undervalued right now? (Target Price − Current Price) / Current Price × 100. +20% = undervalued. −20% = overvalued. | yfinance (targetMeanPrice vs currentPrice) |
| 4 | R3 Durability (carry-over) | 15% | Reuse the Durability score from Round 3 | Cached |
| 5 | Moat Score (carry-over) | 10% | Overall moat strength from gem framework | Cached gem_thresholds |

---

## 🎮 Game Flow — Step by Step

### STEP 0: ASSEMBLE YOUR UNIVERSE
- Default: 24 GARP watchlist tickers pre-loaded
- User can add tickers (paste or CSV upload)
- User can deselect tickers they don't want in the tournament
- **Minimum 32 teams required** for full 5-round bracket
- If < 32, "byes" are added (auto-advance, no score)
- If > 32, user selects exactly 32 or app randomly seeds extras out

### STEP 1: PRE-TOURNAMENT PICKS
- Screen shows all 32 selected teams in a grid
- User picks **2 predicted semi-finalists** (20 pts each if either reaches semi-finals)
- User picks **1 predicted champion** (20 pts if correct)
- These lock in before any match is played
- Display: "Your Champion Pick: NVDA — if NVDA wins the tournament, you earn 20 bonus points!"

### STEP 2: DATA CRUNCH (Background)
- All 32 companies' scores computed in parallel (yfinance + cached gems)
- Progress bar: "Crunching numbers for 32 compounders... ████████░░ 78%"
- AI narrator explains the upcoming round while waiting:
  - What Quality means for investors
  - Why Buffett cares about ROIC
  - Example: "Coca-Cola earns 40%+ ROIC because of its brand. Generic cola earns 10%. That's the difference between a wonderful business and an average one."
- Educational visuals: animated charts showing ROIC vs WACC, margin trends
- **Max wait: 5 minutes.** If a company fails to fetch data, user is prompted to substitute it.

### STEP 3: ROUND 1 — QUALITY (32→16)
- 16 matches displayed in the bracket
- User clicks a match → match card expands with full metrics table
- User picks who they think will win
- User clicks "PREDICT & REVEAL"
- **AI reveals winner** with one-sentence data verdict
- Winner's chip advances to Round 2 in the bracket
- Loser's chip fades to grey
- **Scoreboard updates:** "Correct: 7/16 | Points: 21"
- After all 16 matches: confetti burst, "Round 1 Complete! 16 survivors advance."

### STEP 4: ROUND 2 — GROWTH (16→8)
- Same flow, new criterion (Growth metrics)
- Bracket shows Round 1 winners in their Round 2 positions
- 8 matches, each with Growth metrics table
- Same predict → reveal → advance cycle

### STEP 5: ROUND 3 — DURABILITY (8→4)
- 4 matches. Terminal P/E + Network Effect metrics.
- Winners become R3 champions → advance to semi-finals

### STEP 6: ROUND 4 — 10-YEAR CAGR (4→2)
- 2 matches. Single metric: who can compound longer?
- Winners become the **two finalists**
- At this point, check user's semi-finalist predictions: "You predicted NVDA would reach semi-finals — CORRECT! +20 pts! 🎯"

### STEP 7: ROUND 5 — COMBO (2→1)
- **THE FINAL.** 1 match. All 5 sub-metrics.
- Special final match card — larger, gold border, trophy icon
- After reveal: GOAL HORN + CONFETTI + CROWD CHEER
- Check user's champion prediction: "You predicted NVDA as champion — CORRECT! +20 pts! 🏆"

### STEP 8: CHAMPION REVEAL + SCORING
- Full champion screen with:
  - Trophy animation
  - Path-to-victory bracket tree (all rounds, winners highlighted)
  - Final scorecard: R1/R2/R3/R4/R5 scores for the champion
  - **User Scorecard:**
    ```
    ┌─────────────────────────────────────┐
    │  🎮 YOUR PERFORMANCE                 │
    │  ─────────────────────────────────── │
    │  Match Predictions:    24/31 correct │
    │  Semi-finalist Picks:   1/2 correct  │
    │  Champion Pick:         0/1 correct  │
    │  ─────────────────────────────────── │
    │  TOTAL SCORE:           92/226       │
    │  ACCURACY:              77%          │
    │  RANK:                  ⭐⭐⭐ (Expert)│
    └─────────────────────────────────────┘
    ```

### STEP 9: WEALTH PROJECTION
- AI computes champion's 10-year EPS CAGR
- Shows a compounding graph:
  > *"NVDA's 10-year CAGR is 18.2%. Here's what $10,000 becomes:"*
  > 
  > | Year 10 | Year 20 | Year 30 | Year 40 |
  > |---------|---------|---------|---------|
  > | $53,200 | $283,000 | $1,510,000 | $8,040,000 |

- Animated bar chart growing from $10K → $8M over 40 years
- Buffett quote: *"Someone's sitting in the shade today because someone planted a tree a long time ago."*

### STEP 10: SAVE & REPLAY
- Save tournament JSON (browser localStorage + download)
- Replay mode: step through each match, see what you predicted vs what happened
- Share link: generates a permalink (no user data exposed)

---

## 🔢 Scoring System

| Achievement | Points | When Awarded |
|-------------|--------|--------------|
| Correct match prediction | 3 pts | After each match reveal |
| Correct semi-finalist pick | 20 pts | When that team reaches semi-finals (R3 winner) |
| Correct champion pick | 20 pts | When that team wins R5 final |
| **Max possible** | **226 pts** | 72 from matches + 40 from picks + 20 champion |

**Rank thresholds:**
- 0-50: Rookie Analyst
- 51-100: Junior Investor
- 101-150: Fund Manager
- 151-200: Buffett Apprentice
- 201+: Oracle of Omaha

---

## 📱 Visual & UX Design

### Color Palette
- **Pitch green** (`#1e7e34`) — main background
- **Scoreboard navy** (`#0a1628`) — headers, champion card
- **Gold** (`#C9A35A`) — accents, winner paths, trophy
- **Winner green** (`#28a745`) — correct predictions
- **Loser red** (`#c9302c`) — incorrect predictions

### Bracket Animation
- After each match reveal: winner slides to next round position (CSS transition, 0.5s)
- Loser fades to 30% opacity with red X
- Connector lines draw in gold as matches are decided (SVG path animation)
- Progress number at top: "Round 1: 12/16 matches played"

### Sound Design
- **Kick-off whistle**: Round start
- **Match reveal**: Single tone
- **Round complete**: Crowd cheer + confetti
- **Champion reveal**: Three-note triumphant horn + sustained crowd roar

### Mobile Support
- Bracket collapses to vertical layout on mobile (scrollable)
- Match cards stack vertically
- All metrics tables collapse to 2-column (metric + tickerA vs tickerB)

---

## 💾 Technical Architecture

### Data Sources (Priority Order)
1. **Cached `gem_thresholds.json`** — R1 moat, R3 terminal P/E, R4 10yr CAGR
2. **yfinance** — real-time financials for all 32 companies
3. **TIKR MCP** — forward EPS estimates (when available)
4. **Deterministic proxy** — for tickers that fail all sources (varied by ticker hash, clearly marked as proxy)

### Computation Strategy (Parallel)
- All 32 companies scored in parallel (Python `ThreadPoolExecutor`, 8 workers)
- yfinance fetches batched: 4 companies per wave, 2-second delay between waves
- Estimated total: **~3 minutes** for 32 companies
- Progress bar updated via server-sent events or polling

### Storage
- Tournament state: browser `localStorage` (last 10 tournaments)
- Scores cache: `data/user_watchlist_scores.json`
- Replay files: downloadable `.json`

### Framework
- **Single-file HTML + vanilla JS** (no React, no npm, no build step)
- **Python HTTP server** for local hosting (`python -m http.server`)
- **All computation client-side or via local Python script**
- **Zero external API dependencies at runtime** (all data pre-fetched)

---

## ⚠️ Data Integrity Guarantee

> *"We need to ensure that they are calculated. This is non-negotiable."*

1. **No company is skipped.** If yfinance fails for a ticker, the user is shown the failure and offered:
   - "Substitute this company with another?" (text input)
   - "Use a proxy estimate?" (deterministic formula based on ticker + sector, clearly labeled)
2. **Proxy scores are clearly marked** with a ⚠️ badge: "Proxy estimate — accuracy limited"
3. **If more than 25% of companies fail** (8+ out of 32), the tournament warns: "Too many data failures — results not reliable. Consider a smaller tournament or check your ticker symbols."

---

## 📚 Educational Content (Engaging While Crunching)

During the 3-minute data computation window, the app shows:

1. **Animated explainer** of the upcoming round's criteria
2. **Buffett/Munger quote carousel** with 30-second rotations
3. **"Did You Know?"** facts about compounders:
   - *"Coca-Cola has paid a dividend every year since 1920."*
   - *"If you invested $10,000 in Berkshire Hathaway in 1965, you'd have $280 million today."*
4. **Progress wheel** showing which companies are being scored, with checkmarks as they complete

---

## 🚀 Build Plan

| Phase | Description | Files | Estimate |
|-------|-------------|-------|----------|
| **1** | Data layer: parallel score engine for 32 companies, proxy fallback, cache integration | `garp_score_v4.py` | 2 hrs |
| **2** | Bracket HTML/CSS: symmetric knockout tree, SVG connectors, match cards with real metrics | `garp_tournament_v4.html`, `style_v4.css` | 4 hrs |
| **3** | JS game logic: predict → reveal → advance, scoring, pre-tournament picks, scoreboard | (in HTML) | 3 hrs |
| **4** | Sound + confetti + champion screen + wealth projection graph | (in HTML), `audio/` | 1.5 hrs |
| **5** | Educational content + loading screen + proxy warning system | (in HTML) | 1.5 hrs |
| **6** | GitHub packaging: README, docs/, sample CSV, MIT, CI | `docs/`, `.github/` | 1 hr |
| **Total** | | | **~12 hrs** |

---

## ❓ Open Questions for James

1. **Minimum 32 teams vs current 24** — Do you want to expand your watchlist to 32 (add 8 more compounders), or should we allow "byes" for a 24-team bracket?

2. **Per-round metric weights** — The weights above (R1: ROIC 40%, etc.) are my proposal. Do you want to adjust any?

3. **Semi-finalist prediction points** — I proposed 20 pts each. Should this be higher/lower? Should the champion pick be worth more (e.g., 50 pts)?

4. **"User chooses any winner" override** — Currently, the AI always determines the winner based on data. Should we allow a "commissioner mode" where the user can override the AI's decision? (Default: off)

5. **Wealth projection currency** — $10,000 over 20/30/40 years as proposed. Any other amounts or timeframes?

6. **Mobile priority** — You're often on Android. Should the mobile bracket layout be the primary design target, with desktop as secondary?

7. **Live TIKR during tournament** — Currently the design pre-computes all scores before the tournament starts. Should we allow "re-fetch live" for a specific match if the user wants fresh data? (This would slow down that single match to ~5 seconds.)

---

## ✅ Ready to Proceed?

Say **GO** and I'll build Phase 1 (data layer) first, then we iterate from there.

Or tell me which of the 7 open questions you want to adjust, and I'll revise the proposal.

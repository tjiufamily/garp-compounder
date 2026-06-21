# ⚽ GARP Compounder Championship v4.1

A Warren Buffett-flavored knockout tournament for long-term compounders. **32 companies selected from a 55-company pre-scored universe** compete across **5 rounds of quantitative filters with P/E compression**. The AI determines the winner based on real financial data — you predict, then the AI reveals. Your score tracks how well you really know your compounders.

> *"It's not who YOU think will win — it's who the DATA says will win."*

---

## 🎮 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Pre-compute all 55 company scores (already done — data/universe_55_scores.json)
#    To regenerate: python garp_score_v4_1.py

# 3. Serve locally
python -m http.server 8791 --bind 127.0.0.1

# 4. Open in browser
open http://127.0.0.1:8791/garp_tournament_v4_1.html   # macOS
start http://127.0.0.1:8791/garp_tournament_v4_1.html  # Windows
```

---

## 🏆 How to Play

1. **Select exactly 32 companies** from the 55-company universe (click to toggle)
2. **Pick 2 predicted semi-finalists + 1 champion** before Round 1 (bonus points!)
3. **Read the 7 educational lessons** while scores load (earn reading points)
4. **Each match:** Click the team you predict will win → AI reveals the actual winner based on weighted composite scores
5. **5 rounds:** 32→16→8→4→2→1 🏆
6. **Champion screen:** Wealth projection ($10K at champion CAGR vs S&P 500 / Nasdaq 100 / SMH over 10/20/30/40 years), your scorecard, key takeaways

---

## 📊 The 5 Rounds (5 sub-metrics each)

| # | Round | Key Metrics | Weights |
|---|-------|-------------|---------|
| **R1** | **QUALITY** | ROIC, Gross Margin, Op Margin, FCF Growth, ROE | 40/20/15/15/10 |
| **R2** | **GROWTH** | Hist EPS CAGR, Fwd EPS CAGR, FCF Growth, Rev Consistency, Reinvestment Rate | 25/25/25/15/10 |
| **R3** | **DURABILITY** | Terminal P/E, Peer P/E, Network Effect, Act II Potential, Industry Secularity | 30/20/20/20/10 |
| **R4** | **10-YR POTENTIAL** | PE-Adjusted CAGR, Hist Durability, Industry Growth, Industry Secularity, Act II Fitness | 30/20/20/15/15 |
| **R5** | **COMBO** | Quality, Growth, Valuation Dislocation (30%!), Durability, Moat | 20/15/30/20/15 |

**🔑 P/E Compression is baked in.** R4's PE-Adjusted CAGR = EPS Growth + (Terminal P/E / Current P/E)^(1/10) − 1. R5 uses a dual valuation check: analyst target vs PE-math fair value (takes the more conservative).

---

## 🎯 Scoring System (Max: 204 pts)

| Achievement | Points | Max |
|-------------|--------|-----|
| Correct match prediction | 3 pts × 31 matches | 93 |
| Semi-finalist pick (pre-R1) | 20 pts × 2 | 40 |
| Champion pick (pre-R1) | 50 pts × 1 | 50 |
| Reading rewards | 3 pts × 7 lessons | 21 |
| **TOTAL** | | **204** |

**Ranks:** 0-50 Rookie · 51-100 Junior · 101-150 Fund Manager · 151-190 Buffett Apprentice · 191+ Oracle of Omaha

---

## 📁 File Structure

```
garp-tournament/
├── README.md
├── PROPOSAL_v4_1.md                  # Full design proposal
├── requirements.txt
├── .gitignore
├── LICENSE (MIT)
│
├── garp_tournament_v4_1.html         # MAIN APP (single-file, zero deps)
├── garp_score_v4_1.py                # 55-company scoring engine
├── garp_tournament_export.py         # Playwright PNG export (optional)
│
├── data/
│   ├── universe_55_scores.json       # All 55 companies pre-scored
│   ├── narrative.json                # Educational content (7 lessons + 5 round stories)
│   └── user_watchlist_scores.json    # User's watchlist scores (gitignored)
│
├── docs/
│   ├── ROUND_CRITERIA.md
│   └── SCORING_METHODOLOGY.md
│
├── sample/
│   ├── sample_universe.csv
│   ├── sample_scores.json
│   └── default_watchlist_template.csv
│
└── .github/workflows/
    └── test.yml                      # CI: verify scores load, HTML validates
```

---

## 📚 Educational Layer

**7 Pre-Tournament Lessons** (shown during score loading):
1. What Makes a Wonderful Business
2. The 5 Criteria That Matter Most
3. How Weighted Scoring Works
4. The Law of Large Numbers
5. Act II & Act III
6. Basket vs Single Stock
7. Beating the Index

**5 Round-Specific Stories** (past winner + past failure per round):
- R1: MSFT vs GE
- R2: NVDA vs IBM
- R3: AMZN vs BlackBerry
- R4: ASML vs GoPro
- R5: AAPL (2016) vs CSCO (2000)

---

## 🔧 Technical Notes

- **Zero external dependencies at runtime** — scores pre-computed, HTML self-contained
- **Desktop-first** responsive design (mobile adapts)
- **Web Audio API** sounds (whistle, tones, goal horn)
- **CSS confetti** animations
- **localStorage** for game saves (last 10 tournaments)
- **Playback** — Go Back button to review previous rounds
- **Commissioner override** — toggle in code to allow manual winner selection

---

## 📈 Wealth Projection

At the end of each tournament, the champion screen shows what $10,000 becomes at the champion's PE-adjusted CAGR vs S&P 500 (10.5%), Nasdaq 100 (13.2%), and SMH (14.8%) over **10 (focus), 20, 30, and 40 years**.

---

> *"The stock market is a device for transferring money from the impatient to the patient." — Warren Buffett*

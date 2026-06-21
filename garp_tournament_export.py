"""
garp_tournament_export.py — Generate path-to-winner PNG from a saved tournament.

Usage:
    # Generate from a saved game JSON
    python garp_tournament_export.py --game path/to/game.json --output winner.png

    # Auto-generate from latest tournament in localStorage (browser-driven)
    # Open garp_tournament.html?export=1&data=<base64> in browser, screenshot via Playwright
"""
import argparse
import base64
import json
import sys
from pathlib import Path


def render_html_for_export(tournament: dict, scores: dict, scores_path: str) -> str:
    """Build a single self-contained HTML page showing the path-to-winner diagram."""
    last_matches = tournament["rounds"][-1]
    champion = last_matches[0]["winner"] if last_matches else None
    if not champion:
        return "<html><body><h1>No champion found</h1></body></html>"

    champ = next((t for t in scores["tickers"] if t["ticker"] == champion), None)
    if not champ:
        return "<html><body><h1>Champion not in scores</h1></body></html>"

    # Build round winners
    rounds_html = ""
    for i, round_matches in enumerate(tournament["rounds"]):
        winners = [m["winner"] for m in round_matches if m.get("winner")]
        rounds_html += f"""
        <div class="round-row">
            <div class="round-label">R{i+1}</div>
            <div class="round-winners">{' · '.join(winners)}</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
@page {{ size: A4; margin: 12mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: 'IBM Plex Sans', sans-serif; background: white; padding: 24px; color: #0a1628; max-width: 800px; margin: 0 auto; }}
h1 {{ font-size: 24px; color: #C9A35A; letter-spacing: 4px; margin-bottom: 8px; text-align: center; }}
.champion {{ text-align: center; padding: 32px; background: linear-gradient(135deg, #0a1628, #1a2c4e); color: white; border-radius: 12px; margin-bottom: 24px; }}
.trophy {{ font-size: 64px; }}
.champion-name {{ font-size: 48px; font-weight: 800; margin: 12px 0; color: #C9A35A; }}
.champion-tagline {{ font-size: 14px; opacity: 0.8; }}
.scorecard {{ display: flex; gap: 8px; justify-content: center; margin-top: 16px; flex-wrap: wrap; }}
.score {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); padding: 8px 12px; border-radius: 4px; }}
.score-label {{ font-size: 9px; color: #C9A35A; text-transform: uppercase; }}
.score-val {{ font-size: 18px; font-weight: 700; }}
.path-section {{ margin: 24px 0; }}
.path-section h2 {{ font-size: 14px; color: #0a1628; letter-spacing: 2px; margin-bottom: 12px; }}
.round-row {{ display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #dde1e7; }}
.round-label {{ font-weight: 700; min-width: 60px; color: #0a1628; }}
.round-winners {{ flex: 1; font-family: 'IBM Plex Mono', monospace; font-size: 11px; }}
.winner-chip {{ display: inline-block; padding: 2px 6px; margin: 0 2px; background: #C9A35A; color: #0a1628; border-radius: 3px; font-weight: 600; }}
.footer {{ text-align: center; margin-top: 24px; padding-top: 16px; border-top: 2px solid #C9A35A; color: #647080; font-size: 10px; }}
</style></head><body>
<h1>🏆 GARP COMPOUNDER CHAMPIONSHIP</h1>
<div class="champion">
    <div class="trophy">🏆</div>
    <div class="champion-name">{champion}</div>
    <div class="champion-tagline">{champ.get('name', '')}</div>
    <div class="scorecard">
        <div class="score"><div class="score-label">R1 Quality</div><div class="score-val">{champ['scores']['R1_quality']['score']:.1f}</div></div>
        <div class="score"><div class="score-label">R2 Growth</div><div class="score-val">{champ['scores']['R2_growth']['score']:.1f}</div></div>
        <div class="score"><div class="score-label">R3 Durability</div><div class="score-val">{champ['scores']['R3_durability']['score']:.1f}</div></div>
        <div class="score"><div class="score-label">R4 10yr CAGR</div><div class="score-val">{champ['scores']['R4_10yr_cagr']['score']:.1f}</div></div>
        <div class="score"><div class="score-label">R5 Combo</div><div class="score-val">{champ['scores']['R5_combo']['score']:.1f}</div></div>
    </div>
</div>
<div class="path-section">
    <h2>🏟️ PATH TO VICTORY</h2>
    {rounds_html}
</div>
<div class="footer">GARP Compounder Championship · Generated {tournament.get('started_at', '')}</div>
</body></html>"""


def main():
    parser = argparse.ArgumentParser(description="Export path-to-winner PNG")
    parser.add_argument("--game", required=True, help="Saved tournament JSON")
    parser.add_argument("--scores", default=None, help="Scores JSON (default: same dir as game)")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--html-only", action="store_true", help="Only generate HTML, skip PNG")
    args = parser.parse_args()

    game_path = Path(args.game)
    with open(game_path) as f:
        tournament = json.load(f)

    scores_path = Path(args.scores) if args.scores else (game_path.parent / "scores.json")
    if not scores_path.exists():
        # Try to find any garp_tournament_data.json
        candidates = list(game_path.parent.rglob("*scores*.json"))
        if candidates:
            scores_path = candidates[0]
        else:
            print(f"ERROR: Scores file not found at {scores_path}")
            sys.exit(1)

    with open(scores_path) as f:
        scores = json.load(f)

    html = render_html_for_export(tournament, scores, str(scores_path))

    html_path = Path(args.output).with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    print(f"✅ HTML saved: {html_path}")

    if args.html_only:
        return

    # Render PNG via Playwright
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run: pip install playwright")
        print(f"Open the HTML manually: {html_path}")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 800, "height": 1200})
        page.goto(f"file:///{html_path.as_posix()}", wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=args.output, full_page=True)
        browser.close()
    print(f"✅ PNG saved: {args.output}")


if __name__ == "__main__":
    main()
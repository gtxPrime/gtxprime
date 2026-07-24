"""
make_lang_chart_svg.py
Renders an animated horizontal bar chart of top programming languages
derived from repo_stats.json. SMIL animations only.
"""

import json, os, sys
from collections import Counter

LANG_COLORS = {
    "Java":       "#b07219",
    "Kotlin":     "#A97BFF",
    "Dart":       "#00B4AB",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Python":     "#3572A5",
    "HTML":       "#e34c26",
    "CSS":        "#563d7c",
    "Shell":      "#89e051",
    "C++":        "#f34b7d",
    "Swift":      "#FA7343",
}

def generate_lang_chart(output_path="lang-chart.svg"):
    repos = []
    if os.path.exists("data/repo_stats.json"):
        with open("data/repo_stats.json") as f:
            repos = json.load(f)

    # Aggregate by language (weighted by stars+1 so active repos dominate)
    counts = Counter()
    for r in repos:
        lang = r.get("language") or "Other"
        weight = r.get("stars", 0) + r.get("forks", 0) * 2 + 1
        counts[lang] += weight

    # Top 7 languages
    top = counts.most_common(7)
    total = sum(v for _, v in top) or 1

    W, H = 860, 280
    bar_h = 22
    bar_max_w = 580
    label_x = 30
    bar_x = 185
    row_gap = 32
    chart_top = 58

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1.5" />')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="38" rx="10" fill="#161b22" />')
    svg.append(f'  <rect x="0" y="28" width="{W}" height="10" fill="#161b22" />')
    svg.append(f'  <rect x="0" y="37" width="{W}" height="1" fill="#30363d" />')
    svg.append(f'  <circle cx="20" cy="16" r="5" fill="#ff5f56" />')
    svg.append(f'  <circle cx="38" cy="16" r="5" fill="#ffbd2e" />')
    svg.append(f'  <circle cx="56" cy="16" r="5" fill="#27c93f" />')
    svg.append(f'  <text x="78" y="21" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#8b949e">language-breakdown --weighted</text>')

    for i, (lang, score) in enumerate(top):
        pct = score / total
        filled_w = round(pct * bar_max_w, 1)
        color = LANG_COLORS.get(lang, "#8b949e")
        y = chart_top + i * row_gap
        delay = round(0.1 + i * 0.1, 2)

        # Language name
        svg.append(f'  <text x="{label_x}" y="{y + 16}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="13" font-weight="600" fill="#c9d1d9" text-anchor="start" opacity="0">{lang}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </text>')

        # Bar track
        svg.append(f'  <rect x="{bar_x}" y="{y+4}" width="{bar_max_w}" height="{bar_h}" rx="{bar_h//2}" fill="#161b22" stroke="#30363d" stroke-width="1" />')

        # Bar fill (animated)
        svg.append(f'  <rect x="{bar_x}" y="{y+4}" width="0" height="{bar_h}" rx="{bar_h//2}" fill="{color}">')
        svg.append(f'    <animate attributeName="width" from="0" to="{filled_w}" dur="0.8s" begin="{delay}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0;1" />')
        svg.append(f'  </rect>')

        # Color dot
        svg.append(f'  <circle cx="{bar_x - 12}" cy="{y + 15}" r="5" fill="{color}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </circle>')

        # Percentage label
        pct_label = f"{pct*100:.1f}%"
        svg.append(f'  <text x="{bar_x + bar_max_w + 10}" y="{y + 17}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" fill="{color}" font-weight="600" opacity="0">{pct_label}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay + 0.4}s" fill="freeze" />')
        svg.append(f'  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated language chart: {output_path}")

if __name__ == "__main__":
    generate_lang_chart()

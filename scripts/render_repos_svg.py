"""
render_repos_svg.py  (v2 – fixed)
Renders a 2x2 grid of top repository cards. Fixes text overflow by
capping description at word boundaries. No emojis. SMIL animations.
"""

import json, os, sys

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
}

STAR_D  = "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
FORK_D  = "M6 3a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm6 18a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm6-18a3 3 0 1 0 0 6 3 3 0 0 0 0-6zM6 9v3a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V9"

def strip_emoji(text):
    import re
    return re.sub(r'[^\x00-\x7F]+', '', text).strip()

def word_wrap(text, max_len=58):
    """Hard-wrap at word boundaries."""
    text = strip_emoji(text)
    if len(text) <= max_len:
        return text, ""
    cut = text[:max_len].rfind(' ')
    if cut < 20:
        cut = max_len
    return text[:cut], text[cut:].strip()[:max_len]

def xml_escape(text):
    return text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def render_repos(json_path="data/repo_stats.json", output_path="repo-showcase.svg"):
    repos = []
    if os.path.exists(json_path):
        with open(json_path) as f:
            repos = json.load(f)

    top4 = (repos + [{}]*4)[:4]

    W  = 860
    cw = 405   # card width
    ch = 130   # card height — taller for two desc lines
    gap = 22
    px = 22
    py = 52

    H = py + 2*(ch+gap) + 18

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1.5" />')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="38" rx="10" fill="#161b22" />')
    svg.append(f'  <rect x="0" y="28" width="{W}" height="10" fill="#161b22" />')
    svg.append(f'  <rect x="0" y="37" width="{W}" height="1" fill="#30363d" />')
    svg.append(f'  <circle cx="20" cy="16" r="5" fill="#ff5f56" />')
    svg.append(f'  <circle cx="38" cy="16" r="5" fill="#ffbd2e" />')
    svg.append(f'  <circle cx="56" cy="16" r="5" fill="#27c93f" />')
    svg.append(f'  <text x="78" y="21" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#8b949e">pinned-repos --top=4</text>')

    for i, repo in enumerate(top4):
        col = i % 2
        row = i // 2
        x = px + col*(cw+gap)
        y = py + row*(ch+gap)
        delay = round(0.1 + i*0.12, 2)

        name  = xml_escape(repo.get("name",""))
        desc  = repo.get("description","") or "No description."
        lang  = repo.get("language","") or "—"
        stars = repo.get("stars", 0)
        forks = repo.get("forks", 0)
        url   = repo.get("html_url","#")
        color = LANG_COLORS.get(lang,"#8b949e")

        d1, d2 = word_wrap(xml_escape(desc))

        # Card
        svg.append(f'  <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="8" fill="#161b22" stroke="#30363d" stroke-width="1" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </rect>')

        # Top accent line
        svg.append(f'  <rect x="{x+1}" y="{y+1}" width="{cw-2}" height="2.5" rx="2" fill="{color}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </rect>')

        # Repo icon (Lucide folder-git)
        folder_d = "M2 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6z M12 11v3M10 13l2-2 2 2"
        scale = 14/24.0
        svg.append(f'  <g opacity="0">')
        svg.append(f'    <path d="{folder_d}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate({x+14},{y+16}) scale({scale:.4f})" />')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </g>')

        # Repo name (clickable style)
        svg.append(f'  <text x="{x+36}" y="{y+29}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="14" font-weight="700" fill="#58a6ff" opacity="0">{name}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </text>')

        # Description line 1
        svg.append(f'  <text x="{x+14}" y="{y+52}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" fill="#8b949e" opacity="0">{d1}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </text>')

        # Description line 2 (if any)
        if d2:
            svg.append(f'  <text x="{x+14}" y="{y+68}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" fill="#8b949e" opacity="0">{d2}')
            svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
            svg.append(f'  </text>')

        # Separator
        svg.append(f'  <line x1="{x+14}" y1="{y+ch-36}" x2="{x+cw-14}" y2="{y+ch-36}" stroke="#21262d" stroke-width="1" />')

        # Lang dot + name
        svg.append(f'  <circle cx="{x+20}" cy="{y+ch-18}" r="5" fill="{color}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </circle>')
        svg.append(f'  <text x="{x+32}" y="{y+ch-13}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11" fill="#8b949e" opacity="0">{xml_escape(lang)}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </text>')

        # Star icon + count
        scale_sm = 12/24.0
        svg.append(f'  <g opacity="0">')
        svg.append(f'    <path d="{STAR_D}" stroke="#f0883e" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate({x+cw-118},{y+ch-26}) scale({scale_sm:.4f})" />')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </g>')
        svg.append(f'  <text x="{x+cw-102}" y="{y+ch-14}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11" fill="#f0883e" font-weight="600" opacity="0">{stars}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </text>')

        # Fork icon + count
        svg.append(f'  <g opacity="0">')
        svg.append(f'    <path d="{FORK_D}" stroke="#8b949e" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate({x+cw-68},{y+ch-26}) scale({scale_sm:.4f})" />')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </g>')
        svg.append(f'  <text x="{x+cw-52}" y="{y+ch-14}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11" fill="#8b949e" opacity="0">{forks}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated repo showcase: {output_path}")

if __name__ == "__main__":
    render_repos()

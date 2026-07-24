import json
import os
import sys

# Language colors matching GitHub's standard theme
LANG_COLORS = {
    "Java": "#b07219",
    "Kotlin": "#A97BFF",
    "Dart": "#00B4AB",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Python": "#3572A5",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051"
}

# SVG Icons
STAR_PATH = "M8 .25a.75.75 0 0 0-1.5 0L5.3 4.25a.75.75 0 0 1-.56.41L.34 5.09a.75.75 0 0 0-.41 1.28L3.2 9.25a.75.75 0 0 1 .22.68l-.87 4.41a.75.75 0 0 0 1.09.79l3.96-2.08a.75.75 0 0 1 .7 0l3.96 2.08a.75.75 0 0 0 1.09-.79l-.87-4.41a.75.75 0 0 1 .22-.68l3.27-2.88a.75.75 0 0 0-.41-1.28L11.26 4.66a.75.75 0 0 1-.56-.41L8 .25Z"
FORK_PATH = "M5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 2.122a2.25 2.25 0 1 0-1.5 0v2.878a2.25 2.25 0 0 0 1.5 0V5.372Zm5 .75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 2.122a2.25 2.25 0 1 0-1.5 0V11.25a.75.75 0 0 0 1.5 0V8.244ZM4.25 9a.75.75 0 0 0-.75.75v1.5a.75.75 0 0 0 .75.75h3.5a.75.75 0 0 0 .75-.75v-1.5A.75.75 0 0 0 7.75 9h-3.5Z"

def limit_description(desc, limit=90):
    if len(desc) <= limit:
        return desc
    return desc[:limit-3] + "..."

def render_repos(json_path="data/repo_stats.json", output_path="repo-showcase.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Please run fetch_repo_stats.py first.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        repos = json.load(f)
        
    # Take top 4 repos
    showcase_repos = repos[:4]
    while len(showcase_repos) < 4:
        # Pad with dummy items if user has less than 4 repos
        showcase_repos.append({
            "name": "Project-Placeholder",
            "description": "A premium software engineering project.",
            "stars": 0,
            "forks": 0,
            "language": "Python",
            "html_url": "https://github.com/gtxprime"
        })
        
    width = 860
    height = 305
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1.5; }')
    svg.append('    .title-bar { fill: #161b22; stroke: #30363d; stroke-width: 1.5; }')
    svg.append('    .title-text { font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; fill: #8b949e; font-weight: bold; }')
    
    # Repo card specific styles
    svg.append('    .card-bg { fill: #161b22; stroke: #30363d; stroke-width: 1.2; transition: all 0.25s ease; }')
    svg.append('    .repo-link:hover .card-bg { fill: #1f242c; stroke: #58a6ff; }')
    svg.append('    .repo-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; fill: #58a6ff; }')
    svg.append('    .repo-desc { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; fill: #8b949e; }')
    svg.append('    .meta-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: #8b949e; }')
    svg.append('    .icon { fill: #8b949e; }')
    
    svg.append('    @keyframes fadeInUpCard {')
    svg.append('      from { transform: translateY(10px); opacity: 0; }')
    svg.append('      to { transform: translateY(0); opacity: 1; }')
    svg.append('    }')
    svg.append('    .repo-card {')
    svg.append('      transform-box: fill-box;')
    svg.append('      transform-origin: center;')
    svg.append('      animation: fadeInUpCard 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;')
    svg.append('      opacity: 0;')
    svg.append('    }')
    svg.append('  </style>')
    
    # Outer terminal panel
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" rx="8" />')
    
    # Title Bar
    svg.append(f'  <path class="title-bar" d="M 1.5,8 A 6.5,6.5 0 0 1 8,1.5 L {width-8},1.5 A 6.5,6.5 0 0 1 {width-1.5},8 L {width-1.5},30 L 1.5,30 Z" />')
    
    # Window controls
    svg.append('  <circle cx="20" cy="16" r="6" fill="#ff5f56" />')
    svg.append('  <circle cx="40" cy="16" r="6" fill="#ffbd2e" />')
    svg.append('  <circle cx="60" cy="16" r="6" fill="#27c93f" />')
    
    svg.append(f'  <text class="title-text" x="80" y="20">gtxprime@term: ~/projects</text>')
    
    # Card layout geometry
    card_w = 395
    card_h = 105
    coords = [
        (25, 55, 0.1),    # Card 0: Col 1, Row 1
        (440, 55, 0.2),   # Card 1: Col 2, Row 1
        (25, 175, 0.3),   # Card 2: Col 1, Row 2
        (440, 175, 0.4)   # Card 3: Col 2, Row 2
    ]
    
    def xml_escape(text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
        
    for idx, repo in enumerate(showcase_repos):
        x, y, delay = coords[idx]
        
        name = xml_escape(repo["name"])
        desc = xml_escape(limit_description(repo["description"]))
        lang = xml_escape(repo["language"])
        stars = repo["stars"]
        forks = repo["forks"]
        url = repo["html_url"]
        
        lang_color = LANG_COLORS.get(lang, "#8b949e")
        
        # Start link element
        svg.append(f'  <a href="{url}" target="_blank" class="repo-link">')
        
        # Wrap card in animated group
        svg.append(f'    <g class="repo-card" style="animation-delay: {delay}s;">')
        
        # Card Background
        svg.append(f'      <rect class="card-bg" x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="6" />')
        
        # Title (Repository Name)
        svg.append(f'      <text class="repo-title" x="{x + 15}" y="{y + 25}">{name}</text>')
        
        # Description
        # If no description, print a default placeholder
        if not desc:
            desc = "No description provided."
        svg.append(f'      <text class="repo-desc" x="{x + 15}" y="{y + 48}">{desc}</text>')
        
        # Language Circle & Text
        svg.append(f'      <circle cx="{x + 20}" cy="{y + 82}" r="5" fill="{lang_color}" />')
        svg.append(f'      <text class="meta-text" x="{x + 32}" y="{y + 86}">{lang}</text>')
        
        # Stars Icon and count
        svg.append(f'      <g transform="translate({x + 250}, {y + 75})">')
        svg.append(f'        <path class="icon" d="{STAR_PATH}" />')
        svg.append(f'        <text class="meta-text" x="18" y="11">{stars}</text>')
        svg.append('      </g>')
        
        # Forks Icon and count
        svg.append(f'      <g transform="translate({x + 320}, {y + 74})">')
        svg.append(f'        <path class="icon" d="{FORK_PATH}" />')
        svg.append(f'        <text class="meta-text" x="15" y="12">{forks}</text>')
        svg.append('      </g>')
        
        svg.append('    </g>')
        svg.append('  </a>')
        
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated repository showcase SVG: {output_path}")

if __name__ == "__main__":
    render_repos()

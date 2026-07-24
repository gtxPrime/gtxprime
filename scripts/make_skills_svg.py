"""
make_skills_svg.py
Generates a tech-stack skills panel with Lucide-style icons, colored badges,
and staggered SMIL fade-in animations. No CSS keyframes (GitHub-safe).
"""

# Color theme per technology
SKILLS = [
    # (label, color, icon_path_d)
    ("Android",     "#3DDC84", "M2 16v-2a6 6 0 0 1 6-6h8a6 6 0 0 1 6 6v2M10 7V5M14 7V5M7 16h10M9 19h6"),
    ("Kotlin",      "#A97BFF", "M2 3h8l10 9-10 9H2l10-9z"),
    ("Java",        "#f89820", "M9 3c-1 3-4 4-4 8h14c0-4-3-5-4-8M7 19h10M8 22h8M12 3v2"),
    ("Dart",        "#00B4AB", "M5 3l14 9-14 9V3zM5 3h6M5 21h6"),
    ("Flutter",     "#54C5F8", "M13 3L2 14l4 4 3-3 8 8 5-5-5-5 5-5zM9 15l-2-2"),
    ("JavaScript",  "#f1e05a", "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h-2v-6h2v6zm0-8h-2V7h2v2z"),
    ("TypeScript",  "#3178c6", "M3 3h18v18H3zM13 17v-4h2.5M13 13h5M7 9h4v2H9v4h2v2H7"),
    ("React",       "#61dafb", "M12 12m-2 0a2 2 0 1 0 4 0a2 2 0 1 0-4 0M12 4c4 0 8 3 8 8s-4 8-8 8-8-3-8-8 4-8 8-8zM4 12h16"),
    ("Python",      "#3572A5", "M12 2c-3 0-5 1.5-5 4v2h10V6c0-2.5-2-4-5-4zM7 8H5c-2 0-3 1-3 3v2c0 2 1 3 3 3h2v-4h10v4h2c2 0 3-1 3-3v-2c0-2-1-3-3-3h-2M9 4h1M14 14h1"),
    ("Firebase",    "#FFA000", "M5 20L8 4l4 8 2-4 5 12H5zM5 20l5-5M5 20l8-3"),
    ("Git",         "#f05032", "M15 18H9M12 21V9M3 9V6a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v3"),
    ("Linux",       "#FCC624", "M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zM8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"),
    ("Jetpack",     "#4285f4", "M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"),
    ("Room DB",     "#39d353", "M4 6a8 3 0 1 0 16 0A8 3 0 0 0 4 6zM4 6v6a8 3 0 0 0 16 0V6M4 12v6a8 3 0 0 0 16 0v-6"),
    ("MVVM",        "#bc8cff", "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z"),
    ("REST APIs",   "#58a6ff", "M21 12H3M3 6h18M3 18h18"),
]

def icon_path(d, ox=0, oy=0, size=14, color="#8b949e"):
    """Render a simple icon as a path using a 24x24 viewBox scaled to size."""
    scale = size / 24.0
    return f'<path d="{d}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate({ox},{oy}) scale({scale:.4f})" />'

def generate_skills(output_path="skills.svg"):
    W = 860

    # Layout: 4 badges per row
    cols = 4
    badge_w = 190
    badge_h = 46
    gap_x = 18
    gap_y = 14
    pad_x = 23
    pad_top = 55

    rows = (len(SKILLS) + cols - 1) // cols
    H = pad_top + rows * (badge_h + gap_y) + 28

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    # ── Section panel ─────────────────────────────────────────────────────────
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1.5" />')

    # Title bar
    svg.append(f'  <rect x="0" y="0" width="{W}" height="38" rx="10" fill="#161b22" />')
    svg.append(f'  <rect x="0" y="28" width="{W}" height="10" fill="#161b22" />')  # square bottom
    svg.append(f'  <rect x="0" y="37" width="{W}" height="1" fill="#30363d" />')  # divider

    # Section title
    svg.append(f'  <circle cx="20" cy="16" r="5" fill="#ff5f56" />')
    svg.append(f'  <circle cx="38" cy="16" r="5" fill="#ffbd2e" />')
    svg.append(f'  <circle cx="56" cy="16" r="5" fill="#27c93f" />')
    svg.append(f'  <text x="78" y="21" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#8b949e">tech-stack --list-all</text>')

    # ── Badges ────────────────────────────────────────────────────────────────
    for i, (label, color, icon_d) in enumerate(SKILLS):
        col_i = i % cols
        row_i = i // cols
        x = pad_x + col_i * (badge_w + gap_x)
        y = pad_top + row_i * (badge_h + gap_y)
        delay = round(0.05 + i * 0.06, 2)

        # Card background
        svg.append(f'  <rect x="{x}" y="{y}" width="{badge_w}" height="{badge_h}" rx="8" fill="#161b22" stroke="{color}" stroke-opacity="0.25" stroke-width="1" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </rect>')

        # Left accent bar
        svg.append(f'  <rect x="{x}" y="{y+10}" width="3" height="{badge_h-20}" rx="1.5" fill="{color}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="0.9" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </rect>')

        # Icon (Lucide-style)
        ix = x + 14
        iy = y + 11
        svg.append(f'  <g opacity="0">')
        svg.append(f'    {icon_path(icon_d, ox=ix, oy=iy, size=16, color=color)}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </g>')

        # Label text
        svg.append(f'  <text x="{x+38}" y="{y+27}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="13" font-weight="600" fill="#e6edf3" opacity="0">{label}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append(f'  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated skills SVG: {output_path}")

if __name__ == "__main__":
    generate_skills()

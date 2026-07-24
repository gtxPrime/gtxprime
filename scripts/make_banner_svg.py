"""
make_banner_svg.py
Generates an animated gradient banner SVG with particle dots,
a typewriter name reveal, and a subtitle fade-in.
All animations are SMIL-only (GitHub safe).
"""

def generate_banner(output_path="banner.svg"):
    W, H = 860, 200

    # Particle positions (hand-tuned to look organic)
    particles = [
        (60,30),(120,55),(200,20),(300,45),(420,18),(540,38),(660,22),(780,50),
        (90,100),(180,80),(270,110),(360,70),(450,95),(570,85),(690,105),(800,75),
        (40,155),(130,145),(230,165),(340,135),(470,158),(590,142),(710,168),(830,148),
        (75,185),(210,175),(380,190),(520,172),(680,188),(820,178),
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    # ── Defs ──────────────────────────────────────────────────────────────────
    svg.append('  <defs>')
    # Background gradient — dark navy to deep slate
    svg.append('    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%"   stop-color="#0a0e17" />')
    svg.append('      <stop offset="50%"  stop-color="#0d1117" />')
    svg.append('      <stop offset="100%" stop-color="#111827" />')
    svg.append('    </linearGradient>')
    # Accent glow gradient (left side)
    svg.append('    <radialGradient id="glowL" cx="0%" cy="50%" r="55%">')
    svg.append('      <stop offset="0%"   stop-color="#1e3a5f" stop-opacity="0.6" />')
    svg.append('      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />')
    svg.append('    </radialGradient>')
    # Accent glow gradient (right side)
    svg.append('    <radialGradient id="glowR" cx="100%" cy="50%" r="55%">')
    svg.append('      <stop offset="0%"   stop-color="#1a2e1a" stop-opacity="0.5" />')
    svg.append('      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />')
    svg.append('    </radialGradient>')
    # Scanline pattern for premium texture
    svg.append('    <pattern id="scan" x="0" y="0" width="1" height="4" patternUnits="userSpaceOnUse">')
    svg.append('      <rect x="0" y="0" width="1" height="1" fill="#ffffff" fill-opacity="0.015" />')
    svg.append('    </pattern>')
    svg.append('  </defs>')

    # ── Background ────────────────────────────────────────────────────────────
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="url(#bgGrad)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="url(#glowL)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="url(#glowR)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="url(#scan)" />')

    # Border
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="none" stroke="#21262d" stroke-width="1.5" />')

    # ── Particles ─────────────────────────────────────────────────────────────
    for i, (px, py) in enumerate(particles):
        # Vary size and color subtly
        r = [1.2, 1.5, 1.8, 1.0][i % 4]
        colors = ["#39d353", "#58a6ff", "#bc8cff", "#f0883e", "#30363d"]
        col = colors[i % len(colors)]
        dur = [3.5, 4.2, 5.0, 3.8, 4.6][i % 5]
        begin = round(i * 0.13, 2)
        svg.append(f'  <circle cx="{px}" cy="{py}" r="{r}" fill="{col}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" values="0;0.7;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" />')
        svg.append('  </circle>')

    # ── Accent line ───────────────────────────────────────────────────────────
    svg.append(f'  <rect x="50" y="62" width="0" height="2" rx="1" fill="#39d353" opacity="0.9">')
    svg.append(f'    <animate attributeName="width" from="0" to="50" dur="0.6s" begin="0.3s" fill="freeze" />')
    svg.append('  </rect>')

    # ── Name text ─────────────────────────────────────────────────────────────
    # Slide up + fade in
    svg.append(f'  <text font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="48" font-weight="700" fill="#e6edf3" x="50" y="112" letter-spacing="-1" opacity="0">')
    svg.append(f'    Garvit Sharma')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.7s" begin="0.4s" fill="freeze" />')
    svg.append(f'    <animate attributeName="x" from="42" to="50" dur="0.6s" begin="0.4s" fill="freeze" />')
    svg.append(f'  </text>')

    # ── Role tagline ──────────────────────────────────────────────────────────
    svg.append(f'  <text font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="15" fill="#8b949e" x="53" y="140" opacity="0">')
    svg.append(f'    Android Engineer  /  Open Source Builder  /  Agentic Developer')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.7s" begin="0.9s" fill="freeze" />')
    svg.append(f'  </text>')

    # ── Stats pills ───────────────────────────────────────────────────────────
    pills = [
        ("149+ Stars", "#39d353", 53),
        ("15+ Forks",  "#58a6ff", 185),
        ("552 Commits", "#bc8cff", 305),
    ]
    for label, color, px in pills:
        svg.append(f'  <rect x="{px}" y="158" width="115" height="24" rx="12" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.4" stroke-width="1" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.2s" fill="freeze" />')
        svg.append(f'  </rect>')
        svg.append(f'  <text x="{px+57}" y="174" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11" font-weight="600" fill="{color}" opacity="0">{label}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.2s" fill="freeze" />')
        svg.append(f'  </text>')

    # ── Decorative grid lines (subtle) ────────────────────────────────────────
    for gy in range(0, H, 40):
        svg.append(f'  <line x1="{W*0.55}" y1="{gy}" x2="{W}" y2="{gy}" stroke="#21262d" stroke-width="0.5" />')
    for gx in range(int(W*0.55), W+1, 40):
        svg.append(f'  <line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="#21262d" stroke-width="0.5" />')

    # ── Right-side decorative avatar placeholder circle ───────────────────────
    cx, cy = 750, 100
    svg.append(f'  <circle cx="{cx}" cy="{cy}" r="68" fill="#161b22" stroke="#30363d" stroke-width="1.5" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.6s" fill="freeze" />')
    svg.append(f'  </circle>')
    # Ring
    svg.append(f'  <circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="#39d353" stroke-width="1.5" stroke-dasharray="8 6" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="0.5" dur="0.6s" begin="0.8s" fill="freeze" />')
    svg.append(f'  </circle>')
    # Initials
    svg.append(f'  <text x="{cx}" y="{cy+6}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="40" font-weight="700" fill="#39d353" opacity="0">GS')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.9s" fill="freeze" />')
    svg.append(f'  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated banner: {output_path}")

if __name__ == "__main__":
    generate_banner()

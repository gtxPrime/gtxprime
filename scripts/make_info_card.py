import os

def generate_info_card(output_path="info-card.svg", static_mode=False):
    # Dimensions matching the 490px width requirement to align with layout
    width = 490
    height = 490
    
    # Check if we should disable animations (static mode)
    if os.environ.get("STATIC") == "1" or static_mode:
        animate_style = "/* Animations disabled (STATIC=1) */"
        row_class_prefix = ""
    else:
        # Generate staggered animation delays for 15 elements
        delays = [round(0.1 + i * 0.08, 2) for i in range(16)]
        animate_style = """
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(8px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    .animate {
      opacity: 0;
      animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
""" + "\n".join([f"    .delay-{i} {{ animation-delay: {delays[i]}s; }}" for i in range(len(delays))])
        row_class_prefix = "animate delay-"
        
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    svg.append('  <style>')
    svg.append(f'    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1.5; }}')
    svg.append('    .title-bar { fill: #161b22; stroke: #30363d; stroke-width: 1.5; }')
    svg.append('    .title-text { font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; fill: #8b949e; font-weight: bold; }')
    svg.append('    .terminal-text { font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; fill: #c9d1d9; line-height: 1.5; }')
    svg.append('    .highlight-blue { fill: #58a6ff; font-weight: bold; }')
    svg.append('    .highlight-green { fill: #39d353; font-weight: bold; }')
    svg.append('    .highlight-purple { fill: #bc8cff; font-weight: bold; }')
    svg.append('    .highlight-orange { fill: #ff9b5e; font-weight: bold; }')
    svg.append('    .muted { fill: #8b949e; }')
    svg.append(animate_style)
    svg.append('  </style>')
    
    # Terminal Window Background
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" rx="8" />')
    
    # Title Bar
    svg.append(f'  <path class="title-bar" d="M 1.5,8 A 6.5,6.5 0 0 1 8,1.5 L {width-8},1.5 A 6.5,6.5 0 0 1 {width-1.5},8 L {width-1.5},30 L 1.5,30 Z" />')
    
    # Title Bar Window Controls
    svg.append('  <circle cx="20" cy="16" r="6" fill="#ff5f56" />')
    svg.append('  <circle cx="40" cy="16" r="6" fill="#ffbd2e" />')
    svg.append('  <circle cx="60" cy="16" r="6" fill="#27c93f" />')
    
    # Title text
    svg.append(f'  <text class="title-text" x="80" y="20">gtxprime@term: ~</text>')
    
    # Main Content Area
    y_start = 65
    y_gap = 24
    
    # Helper to format rows easily
    def make_row(index, y, x_offset, parts):
        cls = f' class="{row_class_prefix}{index} terminal-text"' if row_class_prefix else ' class="terminal-text"'
        t_spans = []
        for text, style in parts:
            if style:
                t_spans.append(f'<tspan class="{style}">{text}</tspan>')
            else:
                t_spans.append(text)
        return f'  <text{cls} x="{x_offset}" y="{y}">{"".join(t_spans)}</text>'
        
    rows = [
        # Line 0: Prompt
        (35, [("gtxprime", "highlight-green"), ("@", "muted"), ("github", "highlight-blue"), (" ~ % neofetch", None)]),
        # Line 1: Username / separator
        (35, [("gtxprime", "highlight-green"), ("-----------------", "muted")]),
        # Line 2: OS
        (35, [("OS", "highlight-blue"), (": Windows 11 Pro / Ubuntu 22.04", None)]),
        # Line 3: Kernel
        (35, [("Kernel", "highlight-blue"), (": Gemini-Agentic-Core v3.5", None)]),
        # Line 4: Uptime
        (35, [("Uptime", "highlight-blue"), (": 24/7 Autopilot", None)]),
        # Line 5: Shell
        (35, [("Shell", "highlight-blue"), (": powershell / zsh (interactive)", None)]),
        # Line 6: Empty spacing / divider
        (35, [(" ", None)]),
        # Line 7: Section Header [About Me]
        (35, [("[About Me]", "highlight-purple")]),
        # Line 8: Now
        (45, [("Now", "highlight-orange"), (": Building self-animating GitHub profile READMEs", None)]),
        # Line 9: Prev
        (45, [("Prev", "highlight-orange"), (": Automating dev environments and code crafting", None)]),
        # Line 10: Stack
        (45, [("Stack", "highlight-orange"), (": Python, JS/TS, React, OpenCV, Docker, Git", None)]),
        # Line 11: Focus
        (45, [("Focus", "highlight-orange"), (": Agentic coding workflows & high-fidelity UX", None)]),
        # Line 12: Empty spacing
        (35, [(" ", None)]),
        # Line 13: Prompt
        (35, [("gtxprime", "highlight-green"), ("@", "muted"), ("github", "highlight-blue"), (" ~ % ", None), ("█", "highlight-green")]),
    ]
    
    current_y = y_start
    for i, (x_off, parts) in enumerate(rows):
        svg.append(make_row(i, current_y, x_off, parts))
        current_y += y_gap
        
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated info card: {output_path}")

if __name__ == "__main__":
    generate_info_card()

import os

def generate_info_card(output_path="info-card.svg", static_mode=False):
    width = 490
    height = 490
    
    is_static = os.environ.get("STATIC") == "1" or static_mode
    
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
    
    # Content rows
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
    
    y_start = 65
    y_gap = 24
    current_y = y_start
    
    def xml_escape(text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
        
    for i, (x_off, parts) in enumerate(rows):
        # Escape content
        escaped_parts = []
        for text, style in parts:
            escaped_parts.append((xml_escape(text), style))
            
        t_spans = []
        for text, style in escaped_parts:
            if style:
                t_spans.append(f'<tspan class="{style}">{text}</tspan>')
            else:
                t_spans.append(text)
                
        if is_static:
            svg.append(f'  <text class="terminal-text" x="{x_off}" y="{current_y}">{"".join(t_spans)}</text>')
        else:
            delay = round(0.1 + i * 0.08, 2)
            svg.append(f'  <text class="terminal-text" x="{x_off}" y="{current_y}" opacity="0">')
            svg.append(f'    {"".join(t_spans)}')
            svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
            svg.append(f'    <animate attributeName="y" from="{current_y + 8}" to="{current_y}" dur="0.4s" begin="{delay}s" fill="freeze" />')
            svg.append(f'  </text>')
            
        current_y += y_gap
        
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated info card: {output_path}")

if __name__ == "__main__":
    generate_info_card()

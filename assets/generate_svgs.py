# Generates assets/terminal.svg and assets/divider.svg
from html import escape
import os
OUT = os.path.dirname(os.path.abspath(__file__)) + "/"

# ---------- terminal ----------
lines = [
  ("prompt", "whoami"),
  ("out",    "dhrishit-seal :: MSc Computer Science @ University College Dublin  (Dublin, IE)"),
  ("prompt", "cat education.log"),
  ("ok",     "[2026-09 → 2027-08]  MSc CS (Negotiated Learning)  @ UCD"),
  ("ok",     "[2022-10 → 2026-05]  B.Tech CSE (Health Informatics) @ VIT Bhopal  · CGPA 8.25"),
  ("prompt", "cat experience.log"),
  ("ok",     "[2025-08 → 2026-01]  SDE Intern @ Nomura    — Spring Boot · Jenkins CI/CD · Autosys · JUnit"),
  ("ok",     "[2024-10 → 2025-01]  SDE Intern @ Reliance  — DSFA · Hurst exponent · 390K-sample OP/PV logs"),
  ("prompt", "cat research.bib | head -1"),
  ("out",    "IEEE Xplore :: ViT vs CNN for retinal disease detection (CNV, DME, Drusen) on OCT"),
  ("prompt", "echo $STATUS"),
  ("hl",     "open_to=[SDE, Backend, DevOps, AI-agents, collaborations]  ✔"),
]
W, LH, TOP, LEFT, CW = 860, 24, 64, 24, 8.6
H = TOP + LH * len(lines) + 14
CYCLE = 24.0
colors = {"prompt": "#C9D1D9", "out": "#8B949E", "ok": "#7EE787", "hl": "#00D9FF"}

css, body = [], []
t = 0.6
for i, (kind, txt) in enumerate(lines):
    y = TOP + i * LH
    typed = kind == "prompt"
    n = len(txt)
    dur = n * 0.045 if typed else 0.35
    start, end = t / CYCLE * 100, (t + dur) / CYCLE * 100
    css.append(f".l{i}{{animation:l{i} {CYCLE}s {'steps(%d)' % n if typed else 'ease-out'} infinite}}"
               f"@keyframes l{i}{{0%,{start:.2f}%{{clip-path:inset(0 100% 0 0);opacity:{1 if typed else 0}}}"
               f"{end:.2f}%,96%{{clip-path:inset(0 0 0 0);opacity:1}}100%{{clip-path:inset(0 0 0 0);opacity:0}}}}")
    t += dur + (0.25 if typed else 0.15)
    if kind == "prompt":
        body.append(f'<text class="l{i}" x="{LEFT}" y="{y}"><tspan fill="#FF7B72">dhrishit</tspan>'
                    f'<tspan fill="#8B949E">@</tspan><tspan fill="#D2A8FF">ucd</tspan>'
                    f'<tspan fill="#8B949E">:~$ </tspan><tspan fill="{colors[kind]}">{escape(txt)}</tspan></text>')
    else:
        body.append(f'<text class="l{i}" x="{LEFT}" y="{y}" fill="{colors[kind]}">{escape(txt)}</text>')

last_y = TOP + (len(lines) - 1) * LH
cursor_x = LEFT + len(lines[-1][1]) * CW + 8
appear = t / CYCLE * 100
css.append(f".cur{{animation:blink 1s steps(1) infinite,show {CYCLE}s linear infinite}}"
           "@keyframes blink{50%{fill-opacity:0}}"
           f"@keyframes show{{0%,{appear:.2f}%{{opacity:0}}{appear+0.1:.2f}%,96%{{opacity:1}}100%{{opacity:0}}}}")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated terminal introducing Dhrishit Seal">
<title>dhrishit@ucd — zsh</title>
<style>
text{{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;font-size:14px;white-space:pre}}
.glow{{animation:glow 4s ease-in-out infinite}}@keyframes glow{{50%{{stroke-opacity:.25}}}}
.scan{{animation:scan 6s linear infinite}}@keyframes scan{{from{{transform:translateY(-40px)}}to{{transform:translateY({H}px)}}}}
{chr(10).join(css)}
</style>
<defs>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00D9FF"/><stop offset="1" stop-color="#A371F7"/></linearGradient>
<linearGradient id="sc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00D9FF" stop-opacity="0"/><stop offset=".5" stop-color="#00D9FF" stop-opacity=".06"/><stop offset="1" stop-color="#00D9FF" stop-opacity="0"/></linearGradient>
<clipPath id="win"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12"/></clipPath>
</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="#0D1117"/>
<rect class="glow" x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="none" stroke="url(#bd)" stroke-width="2"/>
<rect x="1" y="1" width="{W-2}" height="34" rx="12" fill="#161B22"/><rect x="1" y="24" width="{W-2}" height="11" fill="#161B22"/>
<circle cx="22" cy="18" r="6" fill="#FF5F56"/><circle cx="42" cy="18" r="6" fill="#FFBD2E"/><circle cx="62" cy="18" r="6" fill="#27C93F"/>
<text x="{W/2}" y="22" fill="#8B949E" text-anchor="middle" style="font-size:12px">dhrishit@ucd: ~ — zsh</text>
{chr(10).join(body)}
<rect class="cur" x="{cursor_x:.0f}" y="{last_y-14}" width="9" height="17" fill="#00D9FF"/>
<g clip-path="url(#win)"><rect class="scan" x="0" y="0" width="{W}" height="40" fill="url(#sc)"/></g>
</svg>
'''
open(OUT + "terminal.svg", "w").write(svg)

# ---------- divider ----------
div = '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="14" viewBox="0 0 900 14" role="img" aria-label="divider">
<defs>
<linearGradient id="g" x1="0" x2="900" gradientUnits="userSpaceOnUse" spreadMethod="repeat">
<stop offset="0" stop-color="#0D1117" stop-opacity="0"/><stop offset=".25" stop-color="#00D9FF"/>
<stop offset=".5" stop-color="#A371F7"/><stop offset=".75" stop-color="#00D9FF"/><stop offset="1" stop-color="#0D1117" stop-opacity="0"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="900 0" dur="5s" repeatCount="indefinite"/>
</linearGradient>
<radialGradient id="dot"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#00D9FF"/><stop offset="1" stop-color="#00D9FF" stop-opacity="0"/></radialGradient>
</defs>
<rect x="0" y="6" width="900" height="2" rx="1" fill="url(#g)"/>
<circle cy="7" r="7" fill="url(#dot)"><animate attributeName="cx" values="-10;910" dur="3.5s" repeatCount="indefinite"/></circle>
</svg>
'''
open(OUT + "divider.svg", "w").write(div)
print("ok", H, t)

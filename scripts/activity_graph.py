"""Render an animated contribution-activity SVG from the GitHub GraphQL API.

Usage:  GITHUB_TOKEN=... python scripts/activity_graph.py <login> <out.svg> [days]
        python scripts/activity_graph.py --demo <out.svg>     (random data, no network)

Replaces the third-party github-readme-activity-graph service so the README
doesn't break when that free instance goes down.
"""
import json
import os
import random
import sys
import urllib.request
from datetime import date, timedelta

QUERY = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}"""

W, H = 900, 300
PAD_L, PAD_R, PAD_T, PAD_B = 50, 25, 55, 45
BG, GRID, MUTED, TITLE = "#0D1117", "#21262D", "#8B949E", "#00D9FF"
LINE, AREA, POINT = "#A371F7", "#00D9FF", "#FFFFFF"


def fetch(login, token, days):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(f"GraphQL error: {body['errors']}")
    weeks = body["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    flat = [(d["date"], d["contributionCount"]) for w in weeks for d in w["contributionDays"]]
    return flat[-days:]


def demo(days):
    start = date.today() - timedelta(days=days - 1)
    return [((start + timedelta(i)).isoformat(), random.choice([0, 0, 1, 2, 3, 5, 8, 12]))
            for i in range(days)]


def render(series, login):
    n = len(series)
    peak = max(c for _, c in series) or 1
    top = peak + (-peak % 4) or 4                      # round up so 4 gridlines get integer labels
    pw, ph = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    x = lambda i: PAD_L + pw * i / (n - 1)
    y = lambda c: PAD_T + ph * (1 - c / top)
    pts = [(x(i), y(c)) for i, (_, c) in enumerate(series)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = f"{PAD_L},{PAD_T + ph} {line} {PAD_L + pw},{PAD_T + ph}"
    path_len = sum(((pts[i][0] - pts[i - 1][0]) ** 2 + (pts[i][1] - pts[i - 1][1]) ** 2) ** .5
                   for i in range(1, n)) + 10
    total = sum(c for _, c in series)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="{login} contributions over the last {n} days">',
           "<style>",
           'text{font-family:"Segoe UI",Ubuntu,"Helvetica Neue",sans-serif;fill:' + MUTED + ';font-size:11px}',
           f".ln{{stroke-dasharray:{path_len:.0f};stroke-dashoffset:{path_len:.0f};animation:draw 2.6s ease-out .3s forwards}}",
           "@keyframes draw{to{stroke-dashoffset:0}}",
           ".ar{opacity:0;animation:fade 1.2s ease-out 1.8s forwards}@keyframes fade{to{opacity:1}}",
           ".pt{opacity:0;transform-box:fill-box;transform-origin:center}",
           "@keyframes pop{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}",
           "@keyframes pulse{50%{r:7;fill-opacity:.35}}",
           "</style>",
           f'<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AREA}" stop-opacity=".35"/>'
           f'<stop offset="1" stop-color="{AREA}" stop-opacity="0"/></linearGradient></defs>',
           f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>',
           f'<text x="{W / 2}" y="30" text-anchor="middle" style="font-size:18px;font-weight:600;fill:{TITLE}">'
           f'Contribution Activity · last {n} days · {total} total</text>']

    for k in range(5):
        v = top * k / 4
        gy = y(v)
        out.append(f'<line x1="{PAD_L}" x2="{PAD_L + pw}" y1="{gy:.1f}" y2="{gy:.1f}" stroke="{GRID}" stroke-dasharray="3 4"/>')
        out.append(f'<text x="{PAD_L - 10}" y="{gy + 4:.1f}" text-anchor="end">{v:g}</text>')
    step = max(1, n // 10)
    for i in range(0, n, step):
        d = date.fromisoformat(series[i][0])
        out.append(f'<text x="{x(i):.1f}" y="{H - PAD_B + 20}" text-anchor="middle">{d.strftime("%d %b")}</text>')
    out.append(f'<text x="14" y="{PAD_T + ph / 2}" transform="rotate(-90 14 {PAD_T + ph / 2})" text-anchor="middle">contributions</text>')

    out.append(f'<polygon class="ar" points="{area}" fill="url(#a)"/>')
    out.append(f'<polyline class="ln" points="{line}" fill="none" stroke="{LINE}" stroke-width="2.5" '
               'stroke-linejoin="round" stroke-linecap="round"/>')
    peak_i = max(range(n), key=lambda i: series[i][1])
    for i, (px, py) in enumerate(pts):
        delay = 0.3 + 2.6 * i / (n - 1)               # pop each point as the line reaches it
        anim = f"pop .35s ease-out {delay:.2f}s forwards"
        if i == peak_i and series[i][1]:
            anim += ", pulse 1.6s ease-in-out 3.2s infinite"
        out.append(f'<circle class="pt" cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="{POINT}" '
                   f'stroke="{LINE}" stroke-width="1.5" style="animation:{anim}">'
                   f'<title>{series[i][0]}: {series[i][1]}</title></circle>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    if sys.argv[1] == "--demo":
        login, out_path, data = "demo", sys.argv[2], demo(31)
    else:
        login, out_path = sys.argv[1], sys.argv[2]
        data = fetch(login, os.environ["GITHUB_TOKEN"], int(sys.argv[3]) if len(sys.argv) > 3 else 31)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        f.write(render(data, login))
    print(f"wrote {out_path} ({len(data)} days)")

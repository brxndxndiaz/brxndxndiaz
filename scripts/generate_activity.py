from __future__ import annotations
import html, json, os, urllib.request
from datetime import datetime, timezone

USER = "brxndxndiaz"
TOKEN = os.getenv("GITHUB_TOKEN", "")

def get(url: str):
    req = urllib.request.Request(url, headers={"Accept":"application/vnd.github+json","User-Agent":"brxndxndiaz-profile","Authorization":f"Bearer {TOKEN}"} if TOKEN else {"Accept":"application/vnd.github+json","User-Agent":"brxndxndiaz-profile"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

events = get(f"https://api.github.com/users/{USER}/events/public?per_page=12")
rows=[]
for e in events:
    repo=e.get("repo",{}).get("name","")
    typ=e.get("type","").replace("Event","")
    created=e.get("created_at","")
    if repo and typ:
        rows.append((typ, repo, created))
    if len(rows)==4: break

def esc(x): return html.escape(str(x))
y=102
row_svg=[]
for typ,repo,created in rows:
    row_svg.append(f'<circle cx="50" cy="{y-5}" r="4" fill="#f5f5f3"/><text x="70" y="{y}" class="t main" font-size="15">{esc(typ)}</text><text x="230" y="{y}" class="t muted" font-size="15">{esc(repo)}</text>')
    y+=31
updated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260"><style>.t{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}.main{{fill:#f5f5f3}}.muted{{fill:#85878c}}</style><rect width="1200" height="260" rx="18" fill="#151619"/><rect x="1" y="1" width="1198" height="258" rx="17" fill="none" stroke="#fff" stroke-opacity=".11"/><text x="42" y="48" class="t muted" font-size="13" letter-spacing="2">LIVE / PUBLIC GITHUB ACTIVITY</text><text x="1158" y="48" text-anchor="end" class="t muted" font-size="12">{esc(updated)}</text><line x1="42" y1="68" x2="1158" y2="68" stroke="#fff" stroke-opacity=".09"/>{''.join(row_svg)}<text x="1158" y="235" text-anchor="end" class="t muted" font-size="11">AUTO-GENERATED</text></svg>'''
os.makedirs("assets",exist_ok=True)
open("assets/activity.svg","w",encoding="utf-8").write(svg)

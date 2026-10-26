"""Render the DAG evolution (output/evolution/evolution_track.json) as a self-contained HTML page
with inline SVG charts: structure per version, content-driven objectives per iteration, and the
later usage of discovered term types.

    python -m taxonomy.classification.track && python -m taxonomy.classification.evolution_dashboard
"""
from __future__ import annotations

import json
from html import escape

from taxonomy.classification import catalogue as cat

OUT = cat.EVOL / "evolution_dashboard.html"
SERIES = ["var(--s1)", "var(--s2)", "var(--s3)"]


def line_chart(title: str, xs: list[str], series: list[tuple[str, list[float]]], unit: str = "", h: int = 220, ymin0: bool = False) -> str:
    W, H = 520, h
    L, R, T, B = 48, 16, 28, 36
    vals = [v for _, ys in series for v in ys if v is not None]
    lo, hi = (0.0 if ymin0 else min(vals)), max(vals)
    if hi == lo:
        hi = lo + 1
    pad = (hi - lo) * 0.12
    lo2, hi2 = (0.0 if ymin0 else lo - pad), hi + pad
    n = len(xs)
    def X(i): return L + (W - L - R) * (i / max(n - 1, 1))
    def Y(v): return T + (H - T - B) * (1 - (v - lo2) / (hi2 - lo2))
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">']
    ticks = 4
    for k in range(ticks + 1):
        v = lo2 + (hi2 - lo2) * k / ticks
        y = Y(v)
        out.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y:.1f}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{L - 6}" y="{y + 3.5:.1f}" text-anchor="end">{v:.3g}</text>')
    for i, x in enumerate(xs):
        out.append(f'<text class="tick" x="{X(i):.1f}" y="{H - B + 16}" text-anchor="middle">{escape(x)}</text>')
    for si, (name, ys) in enumerate(series):
        pts = [(X(i), Y(v)) for i, v in enumerate(ys) if v is not None]
        col = SERIES[si]
        out.append('<polyline fill="none" stroke="' + col + '" stroke-width="2" stroke-linejoin="round" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')
        for (x, y), v, lab in zip(pts, [v for v in ys if v is not None], [x for x, v in zip(xs, ys) if v is not None]):
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}" stroke="var(--surface)" stroke-width="2"><title>{escape(name)} at {escape(lab)}: {v:g}{escape(unit)}</title></circle>')
        if pts:
            x, y = pts[-1]
            out.append(f'<text class="dlabel" x="{x - 6:.1f}" y="{y - 8:.1f}" text-anchor="end">{escape(name)} {ys[-1]:g}</text>')
    out.append("</svg>")
    legend = "".join(f'<span class="key"><i style="background:{SERIES[i]}"></i>{escape(n)}</span>' for i, (n, _) in enumerate(series)) if len(series) > 1 else ""
    return f'<section class="panel"><h3>{escape(title)}</h3>{legend}{"".join(out)}</section>'


def bar_chart(title: str, rows: list[tuple[str, float, str]], h_per: int = 22) -> str:
    W = 520
    L, R = 230, 60
    H = 30 + h_per * len(rows) + 10
    mx = max((v for _, v, _ in rows), default=1) or 1
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">']
    for i, (lab, v, note) in enumerate(rows):
        y = 24 + i * h_per
        w = (W - L - R) * v / mx
        out.append(f'<text class="tick" x="{L - 8}" y="{y + 11}" text-anchor="end">{escape(lab)}</text>')
        out.append(f'<rect x="{L}" y="{y}" width="{max(w, 1):.1f}" height="{h_per - 6}" rx="3" fill="var(--s1)"><title>{escape(lab)}: {v:g} {escape(note)}</title></rect>')
        out.append(f'<text class="dlabel" x="{L + w + 6:.1f}" y="{y + 11}">{v:g}</text>')
    out.append("</svg>")
    return f'<section class="panel wide"><h3>{escape(title)}</h3>{"".join(out)}</section>'


def table(headers: list[str], rows: list[list]) -> str:
    th = "".join(f"<th>{escape(str(h))}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def main() -> None:
    tr = json.loads((cat.EVOL / "evolution_track.json").read_text(encoding="utf-8"))
    V, I = tr["versions"], tr["iterations"]
    items_by_iter = {e["iteration"]: e["items"] for e in I}
    cum, cums = 0, []
    for v in V:
        if v["iteration"] is not None:
            cum += items_by_iter.get(v["iteration"], 0)
        cums.append(cum)
    vx = [f"v{v['version']}" for v in V]
    ix = [f"iter {e['iteration']}" for e in I]
    total_items = sum(e["items"] for e in I)
    total_cost = round(sum(e["cost"]["total_usd"] for e in I), 2)
    total_min = round(sum((e["time"].get("wall_seconds") or 0) for e in I) / 60, 1)
    last = V[-1]
    tiles = [("catalogue versions", f"v0 → v{last['version']}"), ("items fed in", f"{total_items:,}"),
             ("term types", f"{V[0]['nodes']} → {last['nodes']}"), ("values", f"{V[0]['values']} → {last['values']}"),
             ("API cost", f"${total_cost}"), ("wall time", f"{total_min} min")]
    charts = [
        line_chart("Structure per version", vx, [("nodes", [v["nodes"] for v in V]), ("edges", [v["edges"] for v in V]), ("values", [v["values"] for v in V])], ymin0=True),
        line_chart("Candidate (content-discovered) structure", vx, [("candidate nodes", [v["candidate_nodes"] for v in V]), ("candidate values", [v["candidate_values"] for v in V]), ("leaves", [v["leaves"] for v in V])], ymin0=True),
        line_chart("Prior objectives on the DAG (from is-a weights)", vx, [("bits / descent", [v["prior_bits_per_descent"] for v in V]), ("effective leaves", [v["prior_effective_leaves"] for v in V])]),
        line_chart("Prior AUC of reach-a-leaf", vx, [("AUC", [v["prior_auc"] for v in V])]),
        line_chart("Bits per descent, measured on content", ix, [("bits / descent", [e["objectives"]["bits_per_descent"] for e in I])]),
        line_chart("AUC of reach-a-leaf, measured on content", ix, [("AUC", [e["objectives"]["auc"] for e in I])]),
        line_chart("Effective leaves ÷ nodes, measured on content", ix, [("eff. leaves / nodes", [e["objectives"]["effective_leaves_over_nodes"] for e in I])]),
        line_chart("Discovery per iteration", ix, [("targets", [e["discovery_targets"] for e in I]), ("candidates", [e["candidates"] for e in I]), ("accepted", [e["accepted"] for e in I])], ymin0=True),
    ]
    usage_rows = []
    for tid, u in tr["candidate_usage"].items():
        total = sum(u["usage"].values())
        usage_rows.append((tid.replace("_", " "), total, f"items in later iterations; discovered in iteration {u['discovered_in_iteration']}"))
    usage_rows.sort(key=lambda r: -r[1])
    charts.append(bar_chart("Items tagged on discovered term types in later iterations", usage_rows[:24]))
    t1 = table(["version", "iteration", "cumulative items", "nodes", "candidate nodes", "edges", "values", "candidate values", "leaves", "max depth", "prior bits/descent", "prior AUC", "prior eff. leaves"],
               [[f"v{v['version']}", v["iteration"] if v["iteration"] is not None else "seed", c, v["nodes"], v["candidate_nodes"], v["edges"], v["values"], v["candidate_values"], v["leaves"], v["max_depth"], v["prior_bits_per_descent"], v["prior_auc"], v["prior_effective_leaves"]] for v, c in zip(V, cums)])
    t2 = table(["iteration", "catalogue", "items", "tags/item", "bits/descent", "AUC", "expected depth", "eff. leaves/nodes", "collapsed", "targets", "candidates", "accepted", "cost", "wall min"],
               [[e["iteration"], f"v{e['catalogue_version']}", e["items"], e["tags_per_item"], e["objectives"]["bits_per_descent"], e["objectives"]["auc"], e["objectives"]["expected_depth"], e["objectives"]["effective_leaves_over_nodes"], e["collapsed"], e["discovery_targets"], e["candidates"], e["accepted"], f"${e['cost']['total_usd']}", round((e["time"].get("wall_seconds") or 0) / 60, 1)] for e in I])
    added = []
    for v in V:
        for t in v["new_term_types"]:
            added.append([f"v{v['version']}", t["id"], t["name"], t["category"], ", ".join(t["parents"]), t["values"]])
    t3 = table(["version", "id", "name", "category", "parent(s)", "values"], added)
    html = f'''<title>Taxonomy DAG Evolution</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono&display=swap">
<style>
/* layout: stat row, then a two-column grid of small-multiple panels (one measure per panel), then table views */
:root {{ --bg:#f7f8f6; --fg:#1d2420; --muted:#5d6762; --line:#d3d8d3; --surface:#ffffff; --grid:#e6eae6;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --display:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#151a18; --fg:#e4e8e4; --muted:#9ca69f; --line:#38413c; --surface:#1f2623; --grid:#2c3531; --s1:#3987e5; --s2:#d95926; --s3:#199e70; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#151a18; --fg:#e4e8e4; --muted:#9ca69f; --line:#38413c; --surface:#1f2623; --grid:#2c3531; --s1:#3987e5; --s2:#d95926; --s3:#199e70; color-scheme:dark }}
body {{ background:var(--bg); color:var(--fg); font-family:var(--display); line-height:1.45; padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:28px 48px; }}
main {{ max-width:1120px; margin:0 auto; }}
h1 {{ font-size:1.5rem; font-weight:600; margin:0 0 4px; text-wrap:balance; }}
h2 {{ font-size:1.05rem; font-weight:600; margin:32px 0 10px; }}
h3 {{ font-size:.9rem; font-weight:600; margin:0 0 6px; }}
p.lead {{ color:var(--muted); margin:0 0 18px; max-width:72ch; }}
.tiles {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:10px; }}
.tile {{ background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:10px 12px; }}
.tile b {{ display:block; font-size:1.25rem; font-weight:600; font-variant-numeric:tabular-nums; }}
.tile span {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:14px; }}
.panel {{ background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:12px 12px 6px; min-width:0; }}
.panel.wide {{ grid-column:1 / -1; }}
.chart {{ width:100%; height:auto; display:block; }}
.grid line.grid, .chart line.grid {{ stroke:var(--grid); stroke-width:1; }}
.tick {{ font-size:10.5px; fill:var(--muted); font-family:var(--display); }}
.dlabel {{ font-size:10.5px; fill:var(--fg); font-family:var(--display); }}
.key {{ display:inline-flex; align-items:center; gap:5px; font-size:.78rem; color:var(--muted); margin:0 12px 4px 0; }}
.key i {{ width:10px; height:10px; border-radius:2px; display:inline-block; }}
.tbl {{ overflow-x:auto; background:var(--surface); border:1px solid var(--line); border-radius:8px; }}
table {{ border-collapse:collapse; width:100%; font-size:.84rem; font-variant-numeric:tabular-nums; }}
th,td {{ padding:7px 10px; text-align:left; border-top:1px solid var(--line); white-space:nowrap; }}
th {{ font-size:.7rem; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); border-top:0; }}
</style>
<main>
<h1>Taxonomy DAG evolution</h1>
<p class="lead">How the catalogue (term types, values, is-a DAG) changed as DLT-Corpus content was fed through tagging, measurement, discovery and consolidation. Seed v0 comes from the legal and academic corpus and is never modified; everything added later is marked as content-discovered.</p>
<div class="tiles">{"".join(f'<div class="tile"><b>{escape(v)}</b><span>{escape(k)}</span></div>' for k, v in tiles)}</div>
<h2>Charts</h2>
<div class="grid">{"".join(charts)}</div>
<h2>Structure per version</h2>{t1}
<h2>Content-driven objectives per iteration</h2>{t2}
<h2>Term types added by evolution</h2>{t3}
</main>
'''
    OUT.write_text(html, encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()

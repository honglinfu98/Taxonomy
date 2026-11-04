"""Render the final catalogue DAG as a self-contained HTML dashboard: a radial graph with a DLT hub
at the centre joined to the five category roots, the primary-parent tree of every category laid
out around it, the remaining is-a edges drawn faintly, and a node table underneath.

    python -m taxonomy.classification.dag_dashboard [--version N]
"""
from __future__ import annotations

import argparse
import json
import math
from html import escape

from taxonomy.classification import catalogue as cat
from taxonomy.establishment.is_a import CATEGORIES

CAT_LABEL = {
    "asset": "Assets",
    "technology": "DLT systems",
    "actor": "Actors",
    "activity": "Activities",
    "obligation_or_risk": "Obligations and risks",
}
# Fixed categorical order (validated: adjacent pairs incl. the wrap pair pass CVD and
# normal-vision floors in both modes; light-mode aqua/yellow/magenta rely on the relief rule,
# satisfied by the legend, the direct labels and the table view).
CAT_VAR = {"asset": "--c1", "technology": "--c2", "actor": "--c3", "activity": "--c4", "obligation_or_risk": "--c5"}

R0 = 150.0   # radius of the category roots
STEP = 78.0  # radius added per depth level
HUB = "dlt"


def layout(nodes: dict[str, dict], primary: dict[str, dict]) -> dict[str, tuple[float, float, int]]:
    """Radial tidy layout on the primary-parent tree. Returns id -> (r, angle, depth)."""
    children: dict[str, list[str]] = {i: [] for i in nodes}
    for c, e in primary.items():
        children[e["parent"]].append(c)
    for v in children.values():
        v.sort(key=lambda i: (-len(children[i]), nodes[i]["name"]))
    roots = [i for i in nodes if nodes[i]["root"]]
    roots.sort(key=lambda i: CATEGORIES.index(nodes[i]["category"]))

    def leaves(i: str) -> int:
        return 1 if not children[i] else sum(leaves(c) for c in children[i])

    def size(i: str) -> int:
        return 1 + sum(size(c) for c in children[i])

    # sector span per root: proportional to leaf count plus a share of node count, min 9%
    weights = [leaves(r) + 0.5 * size(r) for r in roots]
    spans = [max(0.09, w / sum(weights)) for w in weights]
    spans = [s / sum(spans) * 2 * math.pi for s in spans]
    gap = 0.06  # radians of breathing room between sectors
    pos: dict[str, tuple[float, float, int]] = {}

    def place(i: str, a0: float, a1: float, depth: int) -> None:
        pos[i] = (R0 + STEP * (depth - 1), (a0 + a1) / 2, depth)
        kids = children[i]
        if not kids:
            return
        tot = sum(leaves(k) for k in kids)
        a = a0
        for k in kids:
            w = (a1 - a0) * leaves(k) / tot
            place(k, a, a + w, depth + 1)
            a += w

    a = -math.pi / 2  # first sector starts at the top
    for r, s in zip(roots, spans):
        place(r, a + gap / 2, a + s - gap / 2, 1)
        a += s
    return pos


def xy(r: float, a: float) -> tuple[float, float]:
    return r * math.cos(a), r * math.sin(a)


def radial_link(r1: float, a1: float, r2: float, a2: float) -> str:
    """Cubic path between two polar points through the mid radius (as d3.linkRadial)."""
    rm = (r1 + r2) / 2
    x1, y1 = xy(r1, a1)
    c1x, c1y = xy(rm, a1)
    c2x, c2y = xy(rm, a2)
    x2, y2 = xy(r2, a2)
    return f"M{x1:.1f},{y1:.1f}C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {x2:.1f},{y2:.1f}"


def bowed_link(x1: float, y1: float, x2: float, y2: float) -> str:
    """Quadratic path bowed toward the centre, for secondary edges."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return f"M{x1:.1f},{y1:.1f}Q{mx * 0.55:.1f},{my * 0.55:.1f} {x2:.1f},{y2:.1f}"


def build(version: int) -> str:
    tts, dag, meta = cat.load_version(version)
    nodes = {n["id"]: n for n in dag["nodes"]}
    tt_by_id = {t["id"]: t for t in tts}
    edges = dag["edges"]
    primary: dict[str, dict] = {}
    for e in edges:
        c = e["child"]
        if c not in primary or e["probability"] > primary[c]["probability"]:
            primary[c] = e
    pos = layout(nodes, primary)
    parents: dict[str, list[dict]] = {i: [] for i in nodes}
    children: dict[str, list[str]] = {i: [] for i in nodes}
    for e in edges:
        parents[e["child"]].append({"id": e["parent"], "w": e["probability"]})
        children[e["parent"]].append(e["child"])
    for v in parents.values():
        v.sort(key=lambda p: -p["w"])

    data_nodes = []
    for i, n in nodes.items():
        t = tt_by_id.get(i, {})
        r, a, d = pos[i]
        x, y = xy(r, a)
        origin = t.get("origin") or {}
        data_nodes.append({
            "id": i, "name": n["name"], "cat": n["category"], "q": n.get("question", ""),
            "depth": d, "x": round(x, 1), "y": round(y, 1), "root": bool(n["root"]),
            "status": t.get("status", "seed"), "iter": origin.get("iteration"),
            "values": [v.get("value", "") for v in t.get("values", [])],
            "parents": parents[i], "children": children[i], "pnone": n.get("p_none"),
        })
    data_edges = [{"c": e["child"], "p": e["parent"], "w": e["probability"],
                   "primary": primary[e["child"]] is e} for e in edges]
    roots = [i for i in nodes if nodes[i]["root"]]
    m = dag["metrics"]
    ov = m["overall"]
    bycat = m["by_category"]

    # ---- static SVG ----
    extent = R0 + STEP * (max(d for _, _, d in pos.values()) - 1) + 110
    vb = f"{-extent:.0f} {-extent:.0f} {2 * extent:.0f} {2 * extent:.0f}"
    svg = [f'<svg id="dag" viewBox="{vb}" role="img" aria-labelledby="dag-title">',
           f'<title id="dag-title">Catalogue v{version}: {len(nodes)} term types around a DLT hub</title>',
           '<g id="rings">']
    maxd = max(d for _, _, d in pos.values())
    for d in range(1, maxd + 1):
        svg.append(f'<circle class="ring" r="{R0 + STEP * (d - 1):.0f}"/>')
    svg.append('</g><g id="edges">')
    for e in data_edges:
        r1, a1, _ = pos[e["c"]]
        r2, a2, _ = pos[e["p"]]
        cls = "edge primary" if e["primary"] else "edge secondary"
        cross = nodes[e["c"]]["category"] != nodes[e["p"]]["category"]
        if e["primary"] and not cross:
            path = radial_link(r1, a1, r2, a2)
        else:
            x1, y1 = xy(r1, a1)
            x2, y2 = xy(r2, a2)
            path = bowed_link(x1, y1, x2, y2)
        svg.append(f'<path class="{cls}" data-c="{e["c"]}" data-p="{e["p"]}" data-w="{e["w"]}" d="{path}"/>')
    svg.append('</g><g id="spokes">')
    for rid in roots:
        x, y = xy(*pos[rid][:2])
        svg.append(f'<line class="spoke" x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}"/>')
    svg.append('</g><g id="nodes">')
    for n in data_nodes:
        nv = len(n["values"])
        rad = 4 + 1.6 * math.sqrt(nv)
        cls = "node" + (" root" if n["root"] else "") + (" cand" if n["status"] == "candidate" else "")
        svg.append(f'<g class="{cls}" data-id="{n["id"]}" data-cat="{n["cat"]}" tabindex="0" '
                   f'transform="translate({n["x"]},{n["y"]})">'
                   f'<circle class="hit" r="{max(rad + 6, 12):.1f}"/>'
                   f'<circle class="dot" r="{rad:.1f}" style="fill:var({CAT_VAR[n["cat"]]})"/>'
                   '</g>')
    svg.append('</g><g id="labels">')
    for n in data_nodes:
        many = len(n["children"]) >= 3
        if not (n["root"] or many):
            continue
        a = math.atan2(n["y"], n["x"])
        flip = math.cos(a) < 0
        anchor = "end" if flip else "start"
        nv = len(n["values"])
        off = 8 + 1.6 * math.sqrt(nv)
        name = n["name"] if len(n["name"]) <= 34 else n["name"][:32].rstrip() + "…"
        if n["root"]:
            # roots read horizontally, pushed off the spoke to the side away from the hub
            dx = (-1 if flip else 1) * (off + 4)
            dy = -16 if n["y"] < 0 else 22
            svg.append(f'<text class="label rootlabel" data-id="{n["id"]}" x="{n["x"] + dx:.1f}" y="{n["y"] + dy:.1f}" '
                       f'text-anchor="{anchor}">{escape(n["name"])}</text>')
            continue
        rot = math.degrees(a) + (180 if flip else 0)
        svg.append(f'<text class="label" data-id="{n["id"]}" '
                   f'transform="translate({n["x"]},{n["y"]}) rotate({rot:.1f})" '
                   f'x="{-off if flip else off:.1f}" dy="0.35em" text-anchor="{anchor}">{escape(name)}</text>')
    svg.append('</g>')
    svg.append('<g id="hub" tabindex="0"><circle class="hubdot" r="34"/>'
               '<text class="hubtext" dy="-0.1em" text-anchor="middle">DLT</text>'
               '<text class="hubsub" dy="1.3em" text-anchor="middle">hub</text></g>')
    svg.append('</svg>')

    # ---- category tiles ----
    tiles = []
    for c in CATEGORIES:
        b = bycat[c]
        n_cand = sum(1 for n in data_nodes if n["cat"] == c and n["status"] == "candidate")
        root = next(n for n in data_nodes if n["cat"] == c and n["root"])
        tiles.append(
            f'<section class="cat" data-cat="{c}"><header><i style="background:var({CAT_VAR[c]})"></i>'
            f'<h3>{escape(CAT_LABEL[c])}</h3><span class="rootname">root: {escape(root["name"])}</span></header>'
            f'<dl><div><dt>Term types</dt><dd>{b["nodes"]} <small>({n_cand} added)</small></dd></div>'
            f'<div><dt>Edges</dt><dd>{b["edges"]}</dd></div>'
            f'<div><dt>Leaves</dt><dd>{b["leaves"]} <small>({b["leaves_needed"]["effective_leaves"]:.1f} eff.)</small></dd></div>'
            f'<div><dt>Max depth</dt><dd>{b["max_depth"]}</dd></div>'
            f'<div><dt>Bits / descent</dt><dd>{b["information_gain"]["bits_per_descent"]:.2f}</dd></div>'
            f'<div><dt>AUC</dt><dd>{b["auc"]["value"]:.2f}</dd></div></dl></section>')

    # ---- table ----
    rows = []
    for n in sorted(data_nodes, key=lambda n: (CATEGORIES.index(n["cat"]), n["depth"], n["name"])):
        pp = primary.get(n["id"])
        ppname = f'{escape(nodes[pp["parent"]]["name"])} ({pp["probability"]:.2f})' if pp else "—"
        rows.append(
            f'<tr data-cat="{n["cat"]}" data-id="{n["id"]}"><td><i class="sw" style="background:var({CAT_VAR[n["cat"]]})"></i>'
            f'{escape(n["name"])}</td><td>{escape(CAT_LABEL[n["cat"]])}</td><td class="num">{n["depth"]}</td>'
            f'<td>{ppname}</td>'
            f'<td class="num">{len(n["parents"])}</td><td class="num">{len(n["children"])}</td>'
            f'<td class="num">{len(n["values"])}</td>'
            f'<td>{"added in iteration " + str(n["iter"]) if n["status"] == "candidate" else "seed"}</td></tr>')

    chips = "".join(
        f'<button type="button" class="chip on" data-cat="{c}" aria-pressed="true">'
        f'<i style="background:var({CAT_VAR[c]})"></i>{escape(CAT_LABEL[c])} '
        f'<small>{bycat[c]["nodes"]}</small></button>' for c in CATEGORIES)

    n_cand_nodes = sum(1 for n in data_nodes if n["status"] == "candidate")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catalogue v{version} DAG</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono&display=swap">
<style>
/* layout: title, stat strip, control row, the radial graph with a detail panel beside it,
   five category tiles, then the node table. Colours by role; the five series slots are the
   category hues in fixed order. */
:root {{ color-scheme: light; --bg:#f7f8f6; --surface:#ffffff; --fg:#1d2420; --muted:#5d6762; --line:#d3d8d3; --grid:#e6eae6;
  --c1:#2a78d6; --c2:#eb6834; --c3:#1baf7a; --c4:#eda100; --c5:#e87ba4; --hub:#1d2420; --edge:#1d2420;
  --display:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ color-scheme:dark; --bg:#151a18; --surface:#1f2623; --fg:#e4e8e4; --muted:#9ca69f; --line:#38413c; --grid:#2c3531;
  --c1:#3987e5; --c2:#d95926; --c3:#199e70; --c4:#c98500; --c5:#d55181; --hub:#e4e8e4; --edge:#e4e8e4; }} }}
:root[data-theme="dark"] {{ color-scheme:dark; --bg:#151a18; --surface:#1f2623; --fg:#e4e8e4; --muted:#9ca69f; --line:#38413c; --grid:#2c3531;
  --c1:#3987e5; --c2:#d95926; --c3:#199e70; --c4:#c98500; --c5:#d55181; --hub:#e4e8e4; --edge:#e4e8e4; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font-family:var(--display); line-height:1.45; padding:28px 16px 48px; }}
main {{ max-width:1240px; margin:0 auto; }}
h1 {{ font-size:1.5rem; font-weight:600; margin:0 0 4px; text-wrap:balance; }}
h2 {{ font-size:1.05rem; font-weight:600; margin:32px 0 10px; }}
h3 {{ font-size:.92rem; font-weight:600; margin:0; }}
p.lede {{ color:var(--muted); margin:0 0 18px; max-width:68ch; }}
.stats {{ display:flex; flex-wrap:wrap; gap:10px; margin:0 0 18px; }}
.stat {{ background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:10px 14px; min-width:128px; }}
.stat b {{ display:block; font-size:1.35rem; font-weight:600; font-variant-numeric:tabular-nums; }}
.stat span {{ color:var(--muted); font-size:.8rem; }}
.controls {{ display:flex; flex-wrap:wrap; gap:8px 14px; align-items:center; margin:0 0 12px; }}
.chip {{ display:inline-flex; align-items:center; gap:6px; font:inherit; font-size:.85rem; color:var(--fg); background:var(--surface); border:1px solid var(--line); border-radius:999px; padding:4px 11px; cursor:pointer; }}
.chip i, .key i, .cat header i, .sw {{ display:inline-block; width:11px; height:11px; border-radius:50%; }}
.chip:not(.on) {{ opacity:.45; text-decoration:line-through; }}
.chip small, .stat small, dd small {{ color:var(--muted); font-weight:400; }}
.chip:focus-visible, .node:focus-visible circle.dot, #hub:focus-visible .hubdot, button:focus-visible, input:focus-visible {{ outline:2px solid var(--c1); outline-offset:2px; }}
label.ctl {{ display:inline-flex; align-items:center; gap:8px; font-size:.85rem; color:var(--muted); }}
label.ctl input[type=range] {{ width:150px; }}
input[type=search] {{ font:inherit; font-size:.85rem; padding:5px 10px; border:1px solid var(--line); border-radius:6px; background:var(--surface); color:var(--fg); min-width:200px; }}
.graphwrap {{ display:grid; grid-template-columns:minmax(0,1fr) 300px; gap:16px; align-items:start; }}
@media (max-width:860px) {{ .graphwrap {{ grid-template-columns:1fr; }} }}
.panel {{ background:var(--surface); border:1px solid var(--line); border-radius:10px; padding:12px; position:relative; }}
#dag {{ width:100%; height:auto; display:block; }}
.ring {{ fill:none; stroke:var(--grid); stroke-width:1; }}
.spoke {{ stroke:var(--hub); stroke-width:2.2; stroke-opacity:.55; }}
.edge {{ fill:none; stroke:var(--edge); stroke-linecap:round; transition:stroke-opacity .15s; }}
.edge.primary {{ stroke-width:1.6; stroke-opacity:.42; }}
.edge.secondary {{ stroke-width:1; stroke-opacity:.12; }}
.edge.hidden {{ display:none; }}
.edge.lit {{ stroke-opacity:.95; stroke-width:2.2; }}
.dim .edge:not(.lit) {{ stroke-opacity:.04; }}
.node circle.hit {{ fill:transparent; cursor:pointer; }}
.node circle.dot {{ stroke:var(--surface); stroke-width:2; transition:opacity .15s; }}
.node.cand circle.dot {{ stroke:var(--fg); stroke-width:1.5; stroke-dasharray:2 2; }}
.node.root circle.dot {{ stroke:var(--fg); stroke-width:2.5; }}
.node.off, .dim .node:not(.lit) {{ opacity:.12; }}
.node.sel circle.dot {{ stroke:var(--fg); stroke-width:3; }}
.node.hit-match circle.dot {{ stroke:var(--fg); stroke-width:3; }}
.hubdot {{ fill:var(--surface); stroke:var(--hub); stroke-width:3; }}
.hubtext {{ font:600 20px var(--display); fill:var(--fg); }}
.hubsub {{ font:11px var(--display); fill:var(--muted); }}
.label {{ font:11px var(--display); fill:var(--fg); pointer-events:none; paint-order:stroke; stroke:var(--surface); stroke-width:3px; stroke-linejoin:round; }}
.label.rootlabel {{ font-weight:600; font-size:14px; }}
.dim .label:not(.lit) {{ opacity:.15; }}
#labels.all .label {{ display:inline; }}
#tip {{ position:fixed; pointer-events:none; background:var(--surface); color:var(--fg); border:1px solid var(--line); border-radius:8px; padding:8px 10px; font-size:.8rem; max-width:300px; box-shadow:0 4px 18px rgba(0,0,0,.12); display:none; z-index:10; }}
#tip b {{ display:block; font-size:.9rem; }}
#tip .tcat {{ color:var(--muted); }}
#detail {{ font-size:.85rem; }}
#detail h3 {{ margin:0 0 2px; }}
#detail .q {{ color:var(--muted); margin:0 0 10px; }}
#detail dt {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); margin-top:10px; }}
#detail dd {{ margin:2px 0 0; }}
#detail ul {{ margin:2px 0 0; padding-left:18px; }}
#detail li {{ margin:1px 0; }}
#detail button.lnk {{ font:inherit; color:var(--fg); background:none; border:0; padding:0; text-decoration:underline; cursor:pointer; text-align:left; }}
#detail .w {{ font-family:var(--mono); color:var(--muted); font-size:.78rem; }}
#detail .pill {{ display:inline-block; font-size:.72rem; border:1px solid var(--line); border-radius:999px; padding:1px 8px; margin-left:6px; color:var(--muted); }}
.hint {{ color:var(--muted); font-size:.8rem; margin:8px 0 0; }}
.legend {{ display:flex; flex-wrap:wrap; gap:6px 16px; font-size:.8rem; color:var(--muted); margin:8px 0 0; }}
.legend svg {{ vertical-align:-3px; }}
.cats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px; }}
.cat {{ background:var(--surface); border:1px solid var(--line); border-radius:10px; padding:12px; }}
.cat header {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:8px; }}
.cat .rootname {{ flex-basis:100%; color:var(--muted); font-size:.78rem; }}
.cat dl {{ display:grid; grid-template-columns:1fr 1fr; gap:6px 10px; margin:0; }}
.cat dl div {{ display:flex; flex-direction:column; }}
.cat dt {{ font-size:.72rem; color:var(--muted); }}
.cat dd {{ margin:0; font-weight:600; font-variant-numeric:tabular-nums; }}
.cat.off {{ opacity:.4; }}
.tablewrap {{ overflow-x:auto; background:var(--surface); border:1px solid var(--line); border-radius:10px; }}
table {{ border-collapse:collapse; width:100%; font-size:.82rem; }}
th, td {{ text-align:left; padding:6px 10px; border-bottom:1px solid var(--grid); vertical-align:top; }}
th {{ color:var(--muted); font-weight:500; position:sticky; top:0; background:var(--surface); }}
td.num, th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
tr.off, tr.nomatch {{ display:none; }}
td .sw {{ margin-right:6px; vertical-align:-1px; }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition:none !important; }} }}
</style>
</head>
<body>
<main>
<h1>Catalogue v{version}: the DAG around a DLT hub</h1>
<p class="lede">All {len(nodes)} term types of the final catalogue version, laid out by category around a central DLT hub.
The hub and its five spokes are not part of the catalogue; the five nodes on the first ring are the roots Task B left
without a more general term type. Solid edges are each node's strongest is-a parent; faint edges are the other
{len(edges) - len(primary)} weighted is-a edges. Dot size follows the number of values a term type carries; a dashed
outline marks a term type discovered during maintenance.</p>

<div class="stats">
  <div class="stat"><b>{ov["nodes"]}</b><span>term types <small>({n_cand_nodes} discovered)</small></span></div>
  <div class="stat"><b>{ov["edges"]}</b><span>is-a edges</span></div>
  <div class="stat"><b>{meta["values"]}</b><span>values <small>({meta["candidate_values"]} discovered)</small></span></div>
  <div class="stat"><b>{ov["information_gain"]["bits_per_descent"]:.2f}</b><span>bits per descent</span></div>
  <div class="stat"><b>{ov["auc"]["value"]:.2f}</b><span>AUC, expected depth {ov["auc"]["expected_depth"]:.1f}</span></div>
  <div class="stat"><b>{ov["leaves_needed"]["effective_leaves"]:.1f}</b><span>effective leaves of {ov["leaves"]}</span></div>
  <div class="stat"><b>{ov["max_depth"]}</b><span>max depth over all edges</span></div>
</div>

<div class="controls" id="controls">
  {chips}
  <label class="ctl" for="thr">Hide edges below <output id="thrv">0.00</output><input type="range" id="thr" min="0" max="1" step="0.05" value="0"></label>
  <label class="ctl"><input type="checkbox" id="showsec" checked> faint edges</label>
  <label class="ctl"><input type="checkbox" id="alllabels"> label every node</label>
  <input type="search" id="q" placeholder="Find a term type" aria-label="Find a term type">
</div>

<div class="graphwrap">
  <div class="panel">
    {"".join(svg)}
    <div class="legend">
      <span><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" stroke="currentColor" stroke-width="1.6" stroke-opacity=".6"/></svg> strongest parent</span>
      <span><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" stroke="currentColor" stroke-width="1" stroke-opacity=".3"/></svg> other is-a edge</span>
      <span><svg width="26" height="10"><line x1="1" y1="5" x2="25" y2="5" stroke="currentColor" stroke-width="2.2" stroke-opacity=".6"/></svg> hub spoke (not in catalogue)</span>
      <span><svg width="14" height="14"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 2"/></svg> discovered in maintenance</span>
      <span><svg width="14" height="14"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="2.5"/></svg> category root</span>
    </div>
    <p class="hint">Hover a dot for its question; click or press Enter to trace every is-a path above and below it. Click the hub or empty space to clear.</p>
  </div>
  <aside class="panel" id="detail" aria-live="polite">
    <h3>DLT hub</h3>
    <p class="q">Distributed ledger technology, the subject every category classifies. Select a term type to see its question, values, parents and children.</p>
    <dt>Category roots</dt>
    <dd><ul>{"".join(f'<li><button type="button" class="lnk" data-go="{rid}">{escape(nodes[rid]["name"])}</button> <span class="w">{escape(CAT_LABEL[nodes[rid]["category"]])}</span></li>' for rid in roots)}</ul></dd>
  </aside>
</div>

<h2>By category</h2>
<div class="cats">{"".join(tiles)}</div>

<h2>Every term type</h2>
<div class="tablewrap"><table id="tbl">
<thead><tr><th>Term type</th><th>Category</th><th class="num">Depth</th><th>Strongest parent (weight)</th><th class="num">Parents</th><th class="num">Children</th><th class="num">Values</th><th>Origin</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
<p class="hint">Depth counts rings from the category root along the strongest-parent path; the paper's maximum depth of {ov["max_depth"]} follows every edge. Source: output/evolution/v{version}/dag.json and term_types.json, created {escape(meta["created"][:10])}.</p>
</main>
<div id="tip" role="tooltip"></div>
<script>
(function () {{
  var NODES = {json.dumps(data_nodes, ensure_ascii=False)};
  var CATL = {json.dumps(CAT_LABEL)};
  var byId = {{}}; NODES.forEach(function (n) {{ byId[n.id] = n; }});
  var svg = document.getElementById('dag');
  var tip = document.getElementById('tip');
  var detail = document.getElementById('detail');
  var edgeEls = Array.prototype.slice.call(svg.querySelectorAll('.edge'));
  var nodeEls = {{}}; svg.querySelectorAll('.node').forEach(function (g) {{ nodeEls[g.dataset.id] = g; }});
  var labelEls = {{}}; svg.querySelectorAll('.label').forEach(function (t) {{ labelEls[t.dataset.id] = t; }});
  var catOn = {{}}; var selected = null;

  function el(tag, text, cls) {{ var e = document.createElement(tag); if (text != null) e.textContent = text; if (cls) e.className = cls; return e; }}

  function ancestors(id, acc) {{ byId[id].parents.forEach(function (p) {{ if (!acc[p.id]) {{ acc[p.id] = true; ancestors(p.id, acc); }} }}); return acc; }}
  function descendants(id, acc) {{ byId[id].children.forEach(function (c) {{ if (!acc[c]) {{ acc[c] = true; descendants(c, acc); }} }}); return acc; }}

  function clearLit() {{
    svg.classList.remove('dim');
    edgeEls.forEach(function (e) {{ e.classList.remove('lit'); }});
    Object.keys(nodeEls).forEach(function (k) {{ nodeEls[k].classList.remove('lit', 'sel'); }});
    Object.keys(labelEls).forEach(function (k) {{ labelEls[k].classList.remove('lit'); }});
  }}

  function select(id) {{
    clearLit(); selected = id;
    if (!id) {{ renderHub(); return; }}
    var fam = {{}}; fam[id] = true; ancestors(id, fam); descendants(id, fam);
    svg.classList.add('dim');
    Object.keys(fam).forEach(function (k) {{ if (nodeEls[k]) nodeEls[k].classList.add('lit'); if (labelEls[k]) labelEls[k].classList.add('lit'); }});
    nodeEls[id].classList.add('sel');
    edgeEls.forEach(function (e) {{ if (fam[e.dataset.c] && fam[e.dataset.p]) e.classList.add('lit'); }});
    renderDetail(byId[id]);
  }}

  function renderHub() {{
    detail.innerHTML = '';
    detail.appendChild(el('h3', 'DLT hub'));
    detail.appendChild(el('p', 'Distributed ledger technology, the subject every category classifies. Select a term type to see its question, values, parents and children.', 'q'));
    detail.appendChild(el('dt', 'Category roots'));
    var dd = el('dd'); var ul = el('ul');
    NODES.filter(function (n) {{ return n.root; }}).forEach(function (n) {{
      var li = el('li'); var b = el('button', n.name, 'lnk'); b.type = 'button'; b.dataset.go = n.id; li.appendChild(b);
      li.appendChild(document.createTextNode(' ')); li.appendChild(el('span', CATL[n.cat], 'w')); ul.appendChild(li);
    }});
    dd.appendChild(ul); detail.appendChild(dd);
  }}

  function linkList(items, fmt) {{
    var ul = el('ul');
    items.forEach(function (it) {{
      var li = el('li'); var b = el('button', byId[it.id].name, 'lnk'); b.type = 'button'; b.dataset.go = it.id; li.appendChild(b);
      if (fmt) {{ li.appendChild(document.createTextNode(' ')); li.appendChild(el('span', fmt(it), 'w')); }}
      ul.appendChild(li);
    }});
    return ul;
  }}

  function renderDetail(n) {{
    detail.innerHTML = '';
    var h = el('h3', n.name); detail.appendChild(h);
    var meta = el('p', CATL[n.cat] + ' · depth ' + n.depth + (n.root ? ' · category root' : ''), 'q');
    meta.appendChild(el('span', n.status === 'candidate' ? 'added in iteration ' + n.iter : 'seed catalogue', 'pill'));
    detail.appendChild(meta);
    detail.appendChild(el('dt', 'Question')); detail.appendChild(el('dd', n.q || '(none recorded)'));
    detail.appendChild(el('dt', 'Values (' + n.values.length + ')'));
    var vd = el('dd'); vd.textContent = n.values.length ? n.values.slice(0, 12).join(' · ') + (n.values.length > 12 ? ' · … ' + (n.values.length - 12) + ' more' : '') : '(none)';
    detail.appendChild(vd);
    detail.appendChild(el('dt', 'Is-a parents (' + n.parents.length + ')'));
    var pd = el('dd');
    if (n.parents.length) pd.appendChild(linkList(n.parents, function (p) {{ return p.w.toFixed(2); }}));
    else pd.textContent = 'none: this is a category root' + (n.pnone != null ? ' (p(none) ' + n.pnone.toFixed(2) + ')' : '');
    detail.appendChild(pd);
    detail.appendChild(el('dt', 'Children (' + n.children.length + ')'));
    var cd = el('dd');
    if (n.children.length) cd.appendChild(linkList(n.children.map(function (c) {{ return {{ id: c }}; }}), null)); else cd.textContent = 'none: a leaf';
    detail.appendChild(cd);
  }}

  detail.addEventListener('click', function (ev) {{
    var b = ev.target.closest('button[data-go]'); if (b) select(b.dataset.go);
  }});

  function showTip(n, ev) {{
    tip.innerHTML = '';
    tip.appendChild(el('b', n.name));
    tip.appendChild(el('span', CATL[n.cat] + ' · ' + n.values.length + ' values · ' + n.parents.length + ' parent' + (n.parents.length === 1 ? '' : 's') + ' · ' + n.children.length + ' child' + (n.children.length === 1 ? '' : 'ren'), 'tcat'));
    if (n.q) {{ tip.appendChild(document.createElement('br')); tip.appendChild(document.createTextNode(n.q)); }}
    tip.style.display = 'block';
    var x = ev.clientX + 14, y = ev.clientY + 14;
    if (x + 310 > window.innerWidth) x = ev.clientX - 310;
    if (y + 120 > window.innerHeight) y = ev.clientY - 110;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  }}
  function hideTip() {{ tip.style.display = 'none'; }}

  Object.keys(nodeEls).forEach(function (id) {{
    var g = nodeEls[id];
    g.addEventListener('pointermove', function (ev) {{ showTip(byId[id], ev); }});
    g.addEventListener('pointerleave', hideTip);
    g.addEventListener('click', function (ev) {{ ev.stopPropagation(); select(selected === id ? null : id); }});
    g.addEventListener('keydown', function (ev) {{ if (ev.key === 'Enter' || ev.key === ' ') {{ ev.preventDefault(); select(selected === id ? null : id); }} }});
    g.addEventListener('focus', function () {{ var r = g.getBoundingClientRect(); showTip(byId[id], {{ clientX: r.left + r.width / 2, clientY: r.top + r.height / 2 }}); }});
    g.addEventListener('blur', hideTip);
  }});
  svg.addEventListener('click', function () {{ select(null); }});
  var hub = document.getElementById('hub');
  hub.addEventListener('keydown', function (ev) {{ if (ev.key === 'Enter') select(null); }});

  // category chips
  var chips = document.querySelectorAll('.chip');
  function applyCats() {{
    NODES.forEach(function (n) {{ nodeEls[n.id].classList.toggle('off', !catOn[n.cat]); if (labelEls[n.id]) labelEls[n.id].style.display = catOn[n.cat] ? '' : 'none'; }});
    applyEdges();
    document.querySelectorAll('.cat[data-cat]').forEach(function (c) {{ c.classList.toggle('off', !catOn[c.dataset.cat]); }});
    document.querySelectorAll('#tbl tbody tr').forEach(function (tr) {{ tr.classList.toggle('off', !catOn[tr.dataset.cat]); }});
  }}
  chips.forEach(function (ch) {{
    catOn[ch.dataset.cat] = true;
    ch.addEventListener('click', function () {{
      catOn[ch.dataset.cat] = !catOn[ch.dataset.cat];
      ch.classList.toggle('on', catOn[ch.dataset.cat]); ch.setAttribute('aria-pressed', String(catOn[ch.dataset.cat]));
      applyCats();
    }});
  }});

  // edge threshold + secondary toggle
  var thr = document.getElementById('thr'), thrv = document.getElementById('thrv'), showsec = document.getElementById('showsec');
  function applyEdges() {{
    var t = parseFloat(thr.value); thrv.textContent = t.toFixed(2);
    edgeEls.forEach(function (e) {{
      var w = parseFloat(e.dataset.w);
      var c = byId[e.dataset.c], p = byId[e.dataset.p];
      var hide = w < t || (!showsec.checked && e.classList.contains('secondary')) || !catOn[c.cat] || !catOn[p.cat];
      e.classList.toggle('hidden', hide);
    }});
  }}
  thr.addEventListener('input', applyEdges);
  showsec.addEventListener('change', applyEdges);

  // labels for every node (built on demand so the resting page stays legible)
  var labelsG = document.getElementById('labels');
  var extra = null;
  document.getElementById('alllabels').addEventListener('change', function (ev) {{
    if (!extra) {{
      extra = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      NODES.forEach(function (n) {{
        if (labelEls[n.id]) return;
        var a = Math.atan2(n.y, n.x), flip = Math.cos(a) < 0;
        var t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        t.setAttribute('class', 'label'); t.dataset.id = n.id;
        t.setAttribute('transform', 'translate(' + n.x + ',' + n.y + ') rotate(' + (a * 180 / Math.PI + (flip ? 180 : 0)).toFixed(1) + ')');
        var off = 8 + 1.6 * Math.sqrt(n.values.length);
        t.setAttribute('x', flip ? -off : off); t.setAttribute('dy', '0.35em'); t.setAttribute('text-anchor', flip ? 'end' : 'start');
        t.textContent = n.name.length > 34 ? n.name.slice(0, 32).trim() + '…' : n.name;
        extra.appendChild(t); labelEls[n.id] = t;
      }});
      labelsG.appendChild(extra);
    }}
    extra.style.display = ev.target.checked ? '' : 'none';
    if (selected) select(selected);
  }});

  // search
  var q = document.getElementById('q');
  q.addEventListener('input', function () {{
    var s = q.value.trim().toLowerCase();
    NODES.forEach(function (n) {{
      var hit = s && (n.name.toLowerCase().indexOf(s) >= 0 || n.values.some(function (v) {{ return v.toLowerCase().indexOf(s) >= 0; }}));
      nodeEls[n.id].classList.toggle('hit-match', !!hit);
    }});
    document.querySelectorAll('#tbl tbody tr').forEach(function (tr) {{
      var n = byId[tr.dataset.id];
      var hit = !s || n.name.toLowerCase().indexOf(s) >= 0 || n.values.some(function (v) {{ return v.toLowerCase().indexOf(s) >= 0; }});
      tr.classList.toggle('nomatch', !hit);
    }});
    if (s) {{
      var first = NODES.filter(function (n) {{ return n.name.toLowerCase().indexOf(s) >= 0; }})[0];
      if (first) select(first.id);
    }} else if (selected) {{ select(null); }}
  }});

  // table rows select too
  document.querySelector('#tbl tbody').addEventListener('click', function (ev) {{
    var tr = ev.target.closest('tr[data-id]'); if (tr) {{ select(tr.dataset.id); document.querySelector('.graphwrap').scrollIntoView({{ behavior: 'smooth', block: 'start' }}); }}
  }});
  applyEdges();
}})();
</script>
</body>
</html>
"""
    return html


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", type=int, default=None, help="catalogue version (default: latest)")
    args = ap.parse_args()
    v = args.version
    if v is None:
        v = max(int(p.name[1:]) for p in cat.EVOL.glob("v*") if p.is_dir() and p.name[1:].isdigit())
    html = build(v)
    out = cat.EVOL / "dag_dashboard.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(html) // 1024} KB) for v{v}")


if __name__ == "__main__":
    main()

"""Competitive analysis page, rendered from compare_data.json (exported from
the original Competitive Analysis.dc.html)."""

import json
from html import escape
from pathlib import Path

from site_layout import cta_band, hero

DATA = json.loads((Path(__file__).parent / "compare_data.json").read_text(encoding="utf-8"))


def _e(s: str) -> str:
    return escape(s, quote=True)


def _landscape() -> str:
    out = []
    for seg in DATA["segments"]:
        items = "".join(
            f'<div style="display:flex;flex-direction:column;gap:4px;padding-top:12px;border-top:.5px solid var(--sep);">'
            f'<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;">'
            f'<b>{_e(c["name"])}</b><span class="tag">{_e(c["price"])}</span></div>'
            f'<p>{_e(c["note"])}</p></div>'
            for c in seg["items"]
        )
        out.append(f'<article class="card"><div class="eyebrow">{_e(seg["seg"])}</div>{items}</article>')
    return '<div class="grid">' + "".join(out) + "</div>"


def _matrix() -> str:
    cols = DATA["matrix"]["cols"]
    us_attr = ' class="us"'
    head = "".join(
        f'<th scope="col"{us_attr if i == 0 else ""}>{_e(c.replace(" v3", ""))}</th>'
        for i, c in enumerate(cols)
    )
    rows = []
    for r in DATA["matrix"]["rows"]:
        cells = []
        for i, on in enumerate(r["on"]):
            cls = ("dot-on" if on else "dot-off") + (" us" if i == 0 else "")
            label = "Yes" if on else "Not found"
            cells.append(f'<td class="{cls}"><span aria-hidden="true">{"●" if on else "○"}</span>'
                         f'<span class="sr">{label}</span></td>')
        rows.append(f'<tr><th scope="row">{_e(r["name"])}</th>{"".join(cells)}</tr>')
    return (
        '<p class="small muted">● Stated in sources reviewed &nbsp; ○ Not found in sources (may exist)</p>'
        '<div class="table-wrap"><table class="matrix">'
        f'<thead><tr><th scope="col">Capability</th>{head}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
        '<p class="note">The Verity column reflects the prototype, not a shipped product. Competitor columns only '
        "mark what the reviewed sources explicitly describe. Confirm with vendors before relying on this.</p>"
    )


def _added() -> str:
    rows = "".join(
        f'<tr><th scope="row">{_e(a["f"])}<div class="note">Seen in {_e(a["who"])}</div></th>'
        f'<td>{_e(a["how"])}</td><td class="muted">{_e(a["where"])}</td></tr>'
        for a in DATA["added"]
    )
    return (
        '<div class="table-wrap"><table><thead><tr><th scope="col">Feature</th><th scope="col">How Verity does it</th>'
        f'<th scope="col">Where in the prototype</th></tr></thead><tbody>{rows}</tbody></table></div>'
    )


def _standards() -> str:
    rows = "".join(
        f'<tr><td><span class="tag">{_e(a["src"])}</span></td><td>{_e(a["req"])}</td>'
        f'<td class="muted">{_e(a["where"])}</td></tr>'
        for a in DATA["standards"]
    )
    return (
        '<div class="table-wrap"><table><thead><tr><th scope="col">Source</th><th scope="col">Requirement</th>'
        f'<th scope="col">Where in Verity</th></tr></thead><tbody>{rows}</tbody></table></div>'
    )


def _bullets(items) -> str:
    lis = "".join(f'<li><span><b>{_e(d["t"])}</b> {_e(d["d"])}</span></li>' for d in items)
    return f'<div class="card"><ul class="list">{lis}</ul></div>'


def _pricing() -> str:
    rows = "".join(
        f'<tr><th scope="row">{_e(p["seg"])}</th><td>{_e(p["range"])}</td><td class="muted">{_e(p["note"])}</td></tr>'
        for p in DATA["pricing"]
    )
    return (
        '<div class="table-wrap"><table><thead><tr><th scope="col">Segment</th><th scope="col">Range</th>'
        f'<th scope="col">Notes</th></tr></thead><tbody>{rows}</tbody></table></div>'
        '<p class="small muted">Takeaway: the proposed $29 Starter tier is below most self-serve medical tools. '
        "$79 Professional sits below the medical self-serve range and is competitive with advisor tools. "
        "Test $79–$99 for medical and therapy, and keep minute quotas rather than unlimited.</p>"
    )


def _sources() -> str:
    lis = "".join(
        f'<li><span><a href="{_e(s["u"])}" target="_blank" rel="noopener noreferrer">{_e(s["t"])}</a></span></li>'
        for s in DATA["sources"]
    )
    return f'<div class="card"><ul class="list">{lis}</ul></div>'


def _sec(n: str, title: str, inner: str, intro: str = "") -> str:
    p = f'<p>{intro}</p>' if intro else ""
    return (f'<section class="section"><div class="section__head"><div class="eyebrow">{n}</div>'
            f"<h2>{title}</h2>{p}</div>{inner}</section>")


def compare_body() -> str:
    return (
        hero("Competitive analysis · October 2026", "Who we’re up against, and what we took from them.",
             "Eleven products across medical, therapy, legal and advisory documentation. Every feature that showed "
             "up repeatedly in the market is now in the "
             '<a href="index.html">Verity prototype</a>. Where we differ on purpose, the reason is stated.')
        + _sec("1", "The landscape", _landscape())
        + _sec("2", "Feature matrix", _matrix())
        + _sec("3", "What we added, and why", _added())
        + _sec("4", "Standards alignment", _standards(),
               "Templates are mapped to published documentation guidance.")
        + _sec("5", "Where Verity is different on purpose", _bullets(DATA["diffs"]))
        + _sec("6", "Not built yet", _bullets(DATA["gaps"]),
               'Also tracked on our <a href="company.html#roadmap">roadmap</a>.')
        + _sec("7", "Pricing check", _pricing())
        + _sec("Sources", "References", _sources())
        + cta_band("See the difference yourself", "The prototype shows every feature above. All data is synthetic.",
                   "Open the prototype", "index.html")
    )

#!/usr/bin/env python3
"""Turn an exported 'Verity Prototype.html' bundle into the site's index.html.

Usage:  python3 tools/patch_prototype.py "path/to/Verity Prototype.html"

The bundle stores its page template as a JSON string inside
<script type="__bundler/template">. We decode it, apply the site fixes,
and re-encode it, so the edits are safe regardless of escaping.
Re-run this after every new export of the prototype.
"""

import json
import re
import sys
from pathlib import Path

from site_layout import CONTACT_EMAIL, FAVICON, OG_IMAGE, SITE_URL, mobile_menu_html, nav_links_html

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_RE = re.compile(r'(<script type="__bundler/template">)(.*?)(</script>)', re.S)
PLACEHOLDER_EMAIL = "hello@verity.example"

HEAD_TAGS = (
    f'<link rel="icon" href="{FAVICON}">\n'
    f'<link rel="canonical" href="{SITE_URL}">\n'
    '<meta property="og:type" content="website">\n'
    '<meta property="og:site_name" content="Verity">\n'
    '<meta property="og:title" content="Interactive prototype — Verity">\n'
    '<meta property="og:description" content="Try the Verity prototype on Mac and iPhone. All data is synthetic.">\n'
    f'<meta property="og:url" content="{SITE_URL}">\n'
    f'<meta property="og:image" content="{OG_IMAGE}">\n'
    '<meta property="og:image:width" content="1200">\n'
    '<meta property="og:image:height" content="630">\n'
    '<meta name="twitter:card" content="summary_large_image">\n'
    f'<meta name="twitter:image" content="{OG_IMAGE}">\n'
)

NAV_STYLE = (
    "<style>.vnav{display:flex;gap:4px;margin-left:auto}"
    ".vnav a{color:var(--l2);font-size:14px;font-weight:500;padding:6px 12px;border-radius:14px;text-decoration:none}"
    ".vnav a:hover{color:var(--label);background:var(--fill)}"
    ".vnav a[aria-current]{color:var(--label);background:var(--fill)}"
    ".vmenu-wrap{display:flex;align-items:center;gap:6px}"
    ".menu{position:relative;display:none}"
    ".menu__btn{list-style:none;cursor:pointer;width:36px;height:36px;border-radius:18px;display:grid;place-items:center;"
    "color:var(--label);background:var(--fill)}"
    ".menu__btn::-webkit-details-marker{display:none}"
    ".menu[open] .menu__btn{background:var(--ink);color:var(--onink)}"
    ".menu__panel{position:absolute;right:-8px;top:calc(100% + 14px);min-width:230px;padding:8px;display:flex;"
    "flex-direction:column;border-radius:20px;background:var(--card);border:.5px solid var(--sep);"
    "box-shadow:0 20px 50px rgba(0,0,0,.16)}"
    ".menu__panel a{color:var(--label);font-size:16px;font-weight:500;padding:12px 14px;border-radius:12px;text-decoration:none}"
    ".menu__panel a:hover,.menu__panel a[aria-current]{background:var(--fill)}"
    "a,button,summary{touch-action:manipulation}"
    "@media(max-width:820px){.vnav{display:none}.menu{display:block}}</style>\n"
)


def _nav_links_html() -> str:
    return f'<div class="vnav">{nav_links_html("index.html")}</div>\n'


def _replace_once(text: str, old: str, new: str, what: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"patch failed: expected 1 occurrence of {what}, found {count}")
    return text.replace(old, new)


def patch_template(tpl: str) -> str:
    if 'class="vnav"' in tpl:
        raise SystemExit("template already patched — pass the original export, not index.html")
    tpl = _replace_once(tpl, "<html><head>", '<html lang="en"><head>', "template html tag")
    tpl = tpl.replace(f"mailto:{PLACEHOLDER_EMAIL}", f"mailto:{CONTACT_EMAIL}")
    tpl = tpl.replace(PLACEHOLDER_EMAIL, CONTACT_EMAIL)
    tpl = _replace_once(tpl, 'href="prototype.html"', 'href="index.html"', "prototype.html link")
    # The loader inserts the raw template into the DOM before the runtime binds it,
    # so a literal src="{{ appUrl }}" makes the browser request that URL (404).
    # The runtime strips the sc-camel- prefix and still binds it as the iframe's src.
    tpl = _replace_once(tpl, '<iframe ref="{{ frameRef }}" src="{{ appUrl }}"',
                        '<iframe ref="{{ frameRef }}" sc-camel-src="{{ appUrl }}"', "iframe src binding")
    tpl = _replace_once(tpl, "</helmet>", HEAD_TAGS + NAV_STYLE + "</helmet>", "</helmet>")
    tpl = _replace_once(tpl, '<a href="pilot.html" style="height:36px',
                        _nav_links_html() + '<div class="vmenu-wrap"><a href="pilot.html#apply" style="height:36px',
                        "nav pilot button")
    tpl = _replace_once(tpl, 'white-space:nowrap;">Join the pilot</a>\n</div>\n</nav>',
                        'white-space:nowrap;">Join the pilot</a>' + mobile_menu_html("index.html") + '</div>\n</div>\n</nav>',
                        "nav end")
    tpl = tpl.replace('text-decoration:none;"><span style="width:12px;height:12px;border-radius:6px;background:var(--red);box-shadow',
                      'text-decoration:none;" translate="no"><span style="width:12px;height:12px;border-radius:6px;background:var(--red);box-shadow')
    return tpl


def patch_bundle(html: str) -> str:
    match = TEMPLATE_RE.search(html)
    if not match:
        raise SystemExit("patch failed: bundle template not found")
    tpl = patch_template(json.loads(match.group(2)))
    # Escape "</" so the JSON can never close the surrounding <script> early.
    encoded = json.dumps(tpl, ensure_ascii=False).replace("</", "<\\/")
    html = html[:match.start(2)] + encoded + html[match.end(2):]
    html = _replace_once(html, '<!DOCTYPE html>\n<html>', '<!DOCTYPE html>\n<html lang="en">', "outer html tag")
    html = _replace_once(html, '<meta charset="utf-8">\n',
                         '<meta charset="utf-8">\n  <link rel="icon" href="' + FAVICON + '">\n'
                         '  <script src="assets/site.js" defer></script>\n', "outer charset")
    return html


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    src = Path(sys.argv[1])
    out = patch_bundle(src.read_text(encoding="utf-8"))
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(f"wrote index.html ({len(out):,} bytes) from {src.name}")


if __name__ == "__main__":
    main()

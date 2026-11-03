#!/usr/bin/env python3
"""Generate the Verity marketing pages into the repo root.

Usage:  python3 tools/build_pages.py
index.html (the interactive prototype bundle) is not generated here;
tools/patch_prototype.py adjusts it.
"""

from pathlib import Path

from compare_page import compare_body
from pages_content import company_body, pricing_body, product_body, trust_body
from pilot_page import pilot_body
from site_layout import SITE_URL, hero, render_page

ROOT = Path(__file__).resolve().parent.parent

PAGES = (
    ("product.html", "How it works",
     "How Verity turns one consented recording into every document your profession needs, with evidence for every line.",
     product_body),
    ("trust.html", "Trust & security",
     "Consent by default, audio you control, no training on your data, and a complete audit trail.",
     trust_body),
    ("pricing.html", "Pricing",
     "Per-seat Verity plans with recording-minute quotas, from Starter to Enterprise.",
     pricing_body),
    ("company.html", "About",
     "Why we're building Verity, what we believe, and our roadmap.",
     company_body),
    ("pilot.html", "Design-partner pilot",
     "Apply to pilot Verity and shape its templates, review flow and pricing.",
     pilot_body),
    ("compare.html", "Competitive analysis",
     "Eleven AI documentation products compared across medical, therapy, legal and advisory work.",
     compare_body),
)


def not_found_body() -> str:
    return hero("404", "This page doesn’t exist.",
                "The link may be old or mistyped. Here are some places to start.",
                '<a class="btn btn--ink" href="index.html">Open the prototype</a>'
                '<a class="btn" href="product.html">How it works</a>'
                '<a class="btn" href="pilot.html">Join the pilot</a>')


def prototype_redirect() -> str:
    # Old links to prototype.html land on the homepage, which is the prototype.
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Interactive prototype — Verity</title>
<link rel="canonical" href="{SITE_URL}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=./">
<script>location.replace("./" + location.hash);</script>
</head>
<body><p><a href="./">Open the Verity interactive prototype</a></p></body>
</html>
"""


def sitemap(files) -> str:
    urls = "".join(f"<url><loc>{SITE_URL}{'' if f == 'index.html' else f}</loc></url>" for f in files)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')


def write(name: str, content: str) -> None:
    (ROOT / name).write_text(content, encoding="utf-8")
    print(f"wrote {name} ({len(content):,} bytes)")


def main() -> None:
    for filename, title, desc, body in PAGES:
        write(filename, render_page(filename=filename, title=title, description=desc, body=body()))
    # 404 is served at arbitrary paths, so pin relative URLs to the site root.
    write("404.html", render_page(filename="404.html", title="Page not found",
                                  description="This page doesn't exist.", body=not_found_body(),
                                  base_href="/verity/",
                                  extra_head='<meta name="robots" content="noindex">\n'))
    write("prototype.html", prototype_redirect())
    write("sitemap.xml", sitemap(["index.html"] + [p[0] for p in PAGES]))


if __name__ == "__main__":
    main()

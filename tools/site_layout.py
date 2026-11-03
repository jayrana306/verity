"""Shared page chrome (head, nav, footer) for the Verity static pages."""

from html import escape

SITE_URL = "https://ambicuity.github.io/verity/"
CONTACT_EMAIL = "jayrana210005@gmail.com"

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E"
    "%3Crect width=%2264%22 height=%2264%22 rx=%2214%22 fill=%22%23007AFF%22/%3E"
    "%3Cg stroke=%22white%22 stroke-width=%224%22 stroke-linecap=%22round%22%3E"
    "%3Cpath d=%22M20 28v8M28 20v24M36 16v32M44 26v12%22/%3E%3C/g%3E%3C/svg%3E"
)

NAV_LINKS = (
    ("product.html", "How it works"),
    ("trust.html", "Trust"),
    ("pricing.html", "Pricing"),
    ("index.html", "Prototype"),
)

FOOTER_COLUMNS = (
    ("Product", (
        ("product.html", "How it works"),
        ("trust.html", "Trust &amp; security"),
        ("pricing.html", "Pricing"),
    )),
    ("Company", (
        ("company.html", "About"),
        ("company.html#roadmap", "Roadmap"),
        ("pilot.html", "Design-partner pilot"),
    )),
    ("Resources", (
        ("index.html", "Interactive prototype"),
        ("compare.html", "Competitive analysis"),
        (f"mailto:{CONTACT_EMAIL}", CONTACT_EMAIL),
    )),
)


def _nav(current: str) -> str:
    current_attr = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}"{current_attr if href == current else ""}>{label}</a>'
        for href, label in NAV_LINKS
    )
    return (
        '<nav class="nav" aria-label="Main"><div class="nav__bar">'
        '<a class="brand" href="index.html"><span class="brand__dot" aria-hidden="true"></span>Verity</a>'
        f'<div class="nav__links">{links}</div>'
        '<a class="btn btn--ink btn--sm" href="pilot.html">Join the pilot</a>'
        "</div></nav>"
    )


def _footer() -> str:
    cols = "".join(
        f'<div class="footer__col"><div class="footer__title">{title}</div>'
        + "".join(f'<a href="{href}">{label}</a>' for href, label in links)
        + "</div>"
        for title, links in FOOTER_COLUMNS
    )
    return (
        '<footer class="footer"><div class="footer__inner"><div class="footer__cols">'
        '<div class="footer__col"><a class="brand" href="index.html">'
        '<span class="brand__dot" aria-hidden="true"></span>Verity</a>'
        '<div class="footer__tag">AI documentation for doctors, lawyers and therapists.</div></div>'
        f"{cols}</div>"
        '<div class="footer__base"><span>© 2026 Verity</span>'
        "<span>Prototype data is synthetic. Pricing is a pilot hypothesis.</span></div>"
        "</div></footer>"
    )


def render_page(*, filename: str, title: str, description: str, body: str,
                extra_head: str = "", base_href: str = "") -> str:
    """Wrap a page body in the shared document shell."""
    full_title = escape(f"{title} — Verity")
    desc = escape(description)
    url = SITE_URL + ("" if filename == "index.html" else filename)
    base = f'<base href="{base_href}">\n' if base_href else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Verity">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#f5f5f7">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="assets/site.css">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{_nav(filename)}
<main id="main">
{body}
</main>
{_footer()}
</body>
</html>
"""


def cta_band(heading: str, text: str, label: str = "Join the pilot", href: str = "pilot.html") -> str:
    return (
        '<section class="cta" aria-label="Call to action"><div class="cta__inner"><div>'
        f"<h2>{heading}</h2><p>{text}</p></div>"
        f'<a class="btn" href="{href}">{label}</a></div></section>'
    )


def hero(eyebrow: str, heading: str, lede: str, actions: str = "") -> str:
    acts = f'<div class="actions">{actions}</div>' if actions else ""
    return (
        '<header class="hero"><div class="hero__inner">'
        f'<div class="eyebrow">{eyebrow}</div><h1>{heading}</h1>'
        f'<p class="lede">{lede}</p>{acts}</div></header>'
    )

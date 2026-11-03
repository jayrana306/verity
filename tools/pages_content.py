"""Body content for the Verity marketing pages. Copy is sourced from the
YC W27 application draft and the competitive analysis — keep claims true."""

from site_layout import CONTACT_EMAIL, cta_band, hero


def _cards(items, cls="grid") -> str:
    return f'<div class="{cls}">' + "".join(
        f'<article class="card">{extra}<h3>{title}</h3><p>{text}</p></article>'
        for extra, title, text in items
    ) + "</div>"


def _section(heading: str, intro: str, inner: str, sid: str = "") -> str:
    id_attr = f' id="{sid}"' if sid else ""
    intro_html = f"<p>{intro}</p>" if intro else ""
    return (
        f'<section class="section"{id_attr}><div class="section__head">'
        f"<h2>{heading}</h2>{intro_html}</div>{inner}</section>"
    )


# ---------------------------------------------------------------- product
def product_body() -> str:
    pipeline = (
        '<ol class="steps">'
        "<li>Capture<span>In person, from a call, by phone or upload — after consent.</span></li>"
        "<li>Transcribe<span>Streaming speech-to-text with speaker separation.</span></li>"
        "<li>Extract<span>Facts pulled out with timestamps.</span></li>"
        "<li>Validate<span>Every claim checked against the transcript.</span></li>"
        "<li>Render<span>Versioned, profession-specific templates.</span></li>"
        "<li>Approve<span>The professional reviews, signs and delivers.</span></li>"
        "</ol>"
    )
    states = (
        '<div class="card"><div style="display:flex;flex-wrap:wrap;gap:8px;">'
        '<span class="tag tag--blue">Source-linked</span>'
        '<span class="tag tag--green">Verified</span>'
        '<span class="tag tag--orange">Needs review</span>'
        '<span class="tag tag--indigo">Explicitly denied</span>'
        '<span class="tag tag--red">Not documented</span></div>'
        "<p>Verity never fills a gap. If an exam wasn’t performed or a jurisdiction wasn’t named, "
        "the document says so — and signing is blocked until the professional resolves it.</p></div>"
    )
    professions = _cards([
        ('<span class="tag tag--blue">Medical</span>', "SOAP note &amp; patient summary",
         "A clinical note, a patient-facing summary, structured data for the record system, and the follow-ups you promised."),
        ('<span class="tag tag--green">Therapy</span>', "DAP / BIRP progress notes",
         "Follows behavioral-health documentation guidance: the golden thread to treatment goals, mental-status findings, risk and CPT time."),
        ('<span class="tag tag--indigo">Legal</span>', "Intake memo &amp; chronology",
         "Law-office memorandum format — Question Presented, Brief Answer, Facts, Discussion, Conclusion — checked live against the firm’s intake checklist."),
        ('<span class="tag tag--orange">Consulting</span>', "Meeting notes &amp; actions",
         "Decisions, owners and follow-ups, delivered as tasks to the tools your team already uses."),
    ])
    pillars = _cards([
        ('<div class="card__num">01</div>', "One recording, many documents",
         "A single consultation produces every document your profession needs — not just a transcript."),
        ('<div class="card__num">02</div>', "Evidence for every line",
         "Each statement links to the moment in the transcript it came from."),
        ('<div class="card__num">03</div>', "Templates behave like software",
         "Create a template, test it on a sample session, review a validation report and publish a version. "
         "Published changes never alter documents that were already signed."),
        ('<div class="card__num">04</div>', "Approval, audit and delivery",
         "Signed documents are read-only; changes go in a dated addendum. Every consent, edit, verification, "
         "signature and delivery is logged."),
        ('<div class="card__num">05</div>', "Apple-native",
         "Liquid Glass on macOS 26 and iOS 26. Start recording on iPhone, finish reviewing on the Mac with Handoff."),
        ('<div class="card__num">06</div>', "No bot in your call",
         "Virtual calls are captured on the Mac — nothing joins the meeting on your behalf."),
    ])
    return (
        hero("How it works", "Record once. Get the documents your profession needs.",
             "Verity is a native macOS and iOS app for client-facing professionals. With everyone’s consent, "
             "it records the conversation and turns it into the exact documents your profession requires — "
             "every line traceable to what was actually said.",
             '<a class="btn btn--ink" href="index.html">Try the prototype</a>'
             '<a class="btn" href="pilot.html">Join the pilot</a>')
        + _section("Six stages, one review step", "The product is the review step, not the transcript. "
                   "Every stage exists to make a draft safe to sign.", pipeline)
        + _section("Five explicit claim states", "Every statement in a draft carries one of five states.", states)
        + _section("Built on real professional standards", "", professions)
        + _section("What makes Verity different", "", pillars)
        + _section("What Verity deliberately doesn’t do", "",
                   '<div class="card"><p>No clinical decision support, diagnoses or legal conclusions. '
                   "Verity documents what was said; the professional decides.</p></div>")
        + cta_band("See it end to end", "Click Play Demo Video for a guided 2½-minute tour. All data is synthetic.",
                   "Open the prototype", "index.html")
    )


# ---------------------------------------------------------------- trust
def trust_body() -> str:
    commitments = _cards([
        ("", "All-party consent by default",
         "Recording starts only after every participant is named and consent is verified and timestamped."),
        ("", "Audio you control",
         "Raw audio is deleted after transcription by default, and a no-audio mode is available."),
        ("", "No training on your data",
         "Customer recordings, transcripts and documents are never used to train models."),
        ("", "Configurable retention",
         "Each organization sets its own retention policy for transcripts and documents."),
        ("", "Complete audit trail",
         "Consent, capture, AI draft, edits, verifications, addenda, approval and delivery — all logged and exportable."),
        ("", "Signed means signed",
         "Approved documents are read-only. Late entries go in a dated, labelled addendum."),
    ])
    architecture = (
        '<ul class="list">'
        "<li><span><b>Tenant isolation.</b> PostgreSQL with row-level isolation between organizations.</span></li>"
        "<li><span><b>Encrypted storage.</b> Recordings and documents live in encrypted object storage.</span></li>"
        "<li><span><b>Access control.</b> MFA for everyone; SSO on the Team plan and above.</span></li>"
        "<li><span><b>Psychotherapy notes kept separate</b> from progress notes, with private session prep.</span></li>"
        "<li><span><b>Privilege safeguards</b> for legal work product, and BAAs for healthcare customers.</span></li>"
        "<li><span><b>Vendor review.</b> Speech and model vendors pass security and contractual review "
        "before any regulated data is processed.</span></li>"
        "</ul>"
    )
    return (
        hero("Trust &amp; security", "Built to be signed, not just generated.",
             "Professionals sign records, so the defensible product is the one that makes a draft safe to sign. "
             "These are the commitments Verity is designed around.")
        + _section("Our commitments", "", commitments)
        + _section("How the platform is built", "", f'<div class="card">{architecture}</div>')
        + _section("Where we are today", "",
                   '<div class="card"><span class="tag tag--orange">Pre-launch</span>'
                   "<p>Verity is in the prototype and design-partner stage. The items above are design commitments "
                   "for the production build, not third-party certifications. Pilots start with synthetic or "
                   "properly authorized data only. Ask us for details at "
                   f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p></div>')
        + cta_band("Have a security questionnaire?", "Send it over — we’ll answer it in writing.",
                   "Email us", f"mailto:{CONTACT_EMAIL}?subject=Verity%20security%20questions")
    )


# ---------------------------------------------------------------- pricing
_PLANS = (
    ("Starter", "$29", "/mo", "For trying Verity on a light caseload.",
     ("Limited recording minutes", "Standard templates", "Evidence review &amp; audit trail"), False),
    ("Professional", "$79–$99", "/mo", "For an individual professional.",
     ("More recording minutes", "Custom templates", "Mac + iPhone with Handoff"), True),
    ("Team", "$199+", "/mo", "For practices and firms.",
     ("Shared templates", "Review roles &amp; admin", "SSO"), False),
    ("Enterprise", "Custom", "", "For larger organizations.",
     ("SSO &amp; integrations", "Retention controls", "Security &amp; contractual review"), False),
)


def _plan_card(name, price, per, who, features, featured) -> str:
    feats = "".join(f"<li><span>{f}</span></li>" for f in features)
    badge = '<span class="tag tag--blue">For most professionals</span>' if featured else ""
    cls = "card card--feature" if featured else "card"
    return (
        f'<article class="{cls}">{badge}<h3>{name}</h3>'
        f'<div class="price">{price}<small>{per}</small></div><p>{who}</p>'
        f'<ul class="list">{feats}</ul></article>'
    )


def pricing_body() -> str:
    plans = '<div class="grid">' + "".join(_plan_card(*p) for p in _PLANS) + "</div>"
    market = (
        '<div class="table-wrap"><table><caption>Typical published prices, per provider or user per month.</caption>'
        '<thead><tr><th scope="col">Segment</th><th scope="col">Typical range</th><th scope="col">Examples</th></tr></thead><tbody>'
        '<tr><th scope="row">Medical self-serve</th><td>~$39–$150</td><td>Freed, Heidi, Nabla — free tiers are common</td></tr>'
        '<tr><th scope="row">Medical enterprise</th><td>~$250–$900+</td><td>Abridge, Dragon Copilot — annual contracts</td></tr>'
        '<tr><th scope="row">Therapy</th><td>Free – ~$39+</td><td>Upheal flat $39; Mentalyc tiered</td></tr>'
        '<tr><th scope="row">Financial advisors</th><td>~$67–$100</td><td>Zocks, Jump</td></tr>'
        "</tbody></table></div>"
    )
    return (
        hero("Pricing", "Simple per-seat plans with recording-minute quotas.",
             "These prices are hypotheses we’re testing with design partners. Pilot participants help us set them.",
             '<a class="btn btn--ink" href="pilot.html">Join the pilot</a>')
        + _section("Plans", "", plans)
        + _section("How this compares", "Market check from our competitive analysis.",
                   market + '<p class="note">See the full <a href="compare.html">competitive analysis</a> for sources.</p>')
        + cta_band("Help us get pricing right", "Design partners use Verity early and shape what it costs.")
    )


# ---------------------------------------------------------------- company
def company_body() -> str:
    roadmap = (
        '<div class="timeline">'
        '<article class="card"><span class="tag tag--green">Done</span><h3>Full-workflow prototype</h3>'
        "<p>Interactive, high-fidelity macOS and iOS prototype across medical, therapy, legal and consulting: "
        "onboarding, consent, live capture, generation, evidence review, editing, approval, delivery, audit and the "
        "template studio.</p></article>"
        '<article class="card"><span class="tag tag--green">Done</span><h3>Market &amp; standards research</h3>'
        "<p>A competitive analysis of 11 products, with templates mapped to published documentation standards.</p></article>"
        '<article class="card"><span class="tag tag--orange">In progress</span><h3>Production build</h3>'
        "<p>Native Swift/SwiftUI apps, the backend, and the speech-to-text and LLM pipeline.</p></article>"
        '<article class="card"><span class="tag tag--blue">Next</span><h3>Design-partner pilots</h3>'
        '<p>Working with a small group of practices and firms. <a href="pilot.html">Apply to join</a>.</p></article>'
        "</div>"
    )
    later = (
        '<div class="card"><ul class="list">'
        "<li><span><b>Financial advisor pack.</b> Suitability language, risk-tolerance changes, beneficiary flags, "
        "archiving to compliance systems.</span></li>"
        "<li><span><b>Group and couples notes.</b> One note per member with separate access.</span></li>"
        "<li><span><b>Deeper EHR integration.</b> Today approved documents are pushed into the record system.</span></li>"
        "<li><span><b>Contradiction finder.</b> Compare an intake interview with a later deposition.</span></li>"
        "<li><span><b>More template packs.</b> Dental, veterinary, insurance and more.</span></li>"
        "</ul></div>"
    )
    beliefs = _cards([
        ("", "The review step is the product",
         "Every competitor produces a draft. We optimize verification, not generation."),
        ("", "Standards are the moat",
         "Each profession already has published structures. We encode them as versioned, testable templates."),
        ("", "One engine, many professions",
         "Capture, evidence and approval are the same everywhere. A new profession is a new template pack."),
        ("", "Apple-native is a wedge",
         "Independent professionals live on Macs and iPhones. A native app feels like a tool, not another tab."),
    ], "grid grid--2")
    return (
        hero("About Verity", "Documentation professionals can trust enough to sign.",
             "Clinicians, therapists and lawyers spend hours a week on documentation outside client time. "
             "AI scribes proved they’ll pay to get that time back. The problem left is trust — invented details, "
             "mixed-up speakers and heavy editing before a note can be signed. Verity is built to fix that.")
        + _section("What we believe", "", beliefs)
        + _section("Roadmap", "Where Verity is today and what comes next.", roadmap, sid="roadmap")
        + _section("Later", "Gaps we know about and intend to close.", later)
        + _section("Contact", "",
                   f'<div class="card"><p>Questions, partnerships or press: <a href="mailto:{CONTACT_EMAIL}">'
                   f"{CONTACT_EMAIL}</a></p></div>")
        + cta_band("Shape what we build next", "Design partners get early access and a direct line to the team.")
    )

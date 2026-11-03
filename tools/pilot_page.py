"""Design-partner pilot page.

GitHub Pages is a static host, so there is no form: visitors apply by email.
The "Email your application" button opens a pre-filled mailto link, and the
address can be copied for people without a mail app. ?plan= and ?profession=
(from the pricing page and profession cards) are added to the email.
"""

import json
from urllib.parse import quote

from site_layout import CONTACT_EMAIL

SUBJECT = "Verity pilot application"
BODY = (
    "Hi Verity team,\n\n"
    "I'd like to join the design-partner pilot.\n\n"
    "Name:\n"
    "Role / profession:\n"
    "Practice or firm:\n"
    "Practice size:\n"
    "What takes the most time in my documentation today:\n\n"
    "Thanks!"
)


def _mailto(subject: str = SUBJECT, body: str = BODY) -> str:
    return f"mailto:{CONTACT_EMAIL}?subject={quote(subject)}&body={quote(body)}"


MAIL_ICON = (
    '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
)


def _apply_card() -> str:
    return f"""
<div class="apply card" id="apply">
  <div class="apply__head">
    <h2 class="apply__title">Apply by email</h2>
    <p class="small muted">Send us a short note. We reply within a few days.</p>
  </div>
  <p class="plan-pill" id="plan-pill" hidden>Interested in the <b id="plan-name"></b> plan · <a href="pricing.html">change</a></p>
  <div class="include">
    <div class="include__title">Tell us</div>
    <ol class="include__list">
      <li>Your name and role</li>
      <li>Your profession and practice size</li>
      <li>What takes the most time in your documentation today</li>
    </ol>
  </div>
  <a class="btn btn--ink apply__submit" id="apply-mail" href="{_mailto()}">{MAIL_ICON}Email your application</a>
  <div class="address">
    <span class="address__label">Or write to</span>
    <div class="address__row">
      <a class="address__email" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
      <button class="btn btn--sm" type="button" id="copy-email" data-email="{CONTACT_EMAIL}">Copy address</button>
    </div>
    <p class="form__status" id="copy-status" role="status" aria-live="polite"></p>
  </div>
  <p class="note">The button opens your email app with a template filled in. No email app set up? Copy the address and write from any account.</p>
</div>
"""


_SCRIPT = r"""
<script>
(function () {
  var TO = "__EMAIL__";
  var PLANS = ["Starter", "Professional", "Team"];
  var PROFESSIONS = ["Medical", "Therapy", "Legal", "Advisory"];
  var BODY = __BODY__;

  // Personalise the email from ?plan= and ?profession= (allow-listed values only).
  var q = new URLSearchParams(location.search);
  var plan = PLANS.indexOf(q.get("plan")) >= 0 ? q.get("plan") : "";
  var prof = PROFESSIONS.indexOf(q.get("profession")) >= 0 ? q.get("profession") : "";
  if (plan || prof) {
    var subject = "Verity pilot application" + (prof ? " — " + prof : "") + (plan ? " (" + plan + " plan)" : "");
    var body = BODY
      .replace("Role / profession:", "Role / profession:" + (prof ? " " + prof : ""))
      .replace("Thanks!", (plan ? "Plan I'm interested in: " + plan + "\n\n" : "") + "Thanks!");
    document.getElementById("apply-mail").href =
      "mailto:" + TO + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
  }
  if (plan) {
    document.getElementById("plan-name").textContent = plan;
    document.getElementById("plan-pill").hidden = false;
  }

  // Copy address, with a fallback for browsers without the async Clipboard API.
  var btn = document.getElementById("copy-email");
  var status = document.getElementById("copy-status");
  function done(ok) {
    status.textContent = ok ? "Address copied." : "Couldn’t copy — select the address above instead.";
    btn.textContent = ok ? "Copied" : "Copy address";
    if (ok) setTimeout(function () { btn.textContent = "Copy address"; status.textContent = ""; }, 2500);
  }
  function legacyCopy(text) {
    var t = document.createElement("textarea");
    t.value = text; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0";
    document.body.appendChild(t); t.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    t.remove();
    return ok;
  }
  btn.addEventListener("click", function () {
    var text = btn.getAttribute("data-email");
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(legacyCopy(text)); });
    } else {
      done(legacyCopy(text));
    }
  });
})();
</script>
"""


def _hero() -> str:
    facts = (
        '<ul class="facts">'
        "<li><b>Mac + iPhone</b><span>Native apps with Handoff</span></li>"
        "<li><b>Your templates</b><span>Built to your standards</span></li>"
        "<li><b>Safe data</b><span>Synthetic or authorized only</span></li>"
        "</ul>"
    )
    return (
        '<header class="hero"><div class="hero__inner split">'
        '<div class="split__copy">'
        '<div class="eyebrow">Design-partner pilot</div>'
        "<h1>Help build documentation you can sign.</h1>"
        '<p class="lede">We’re inviting a small group of doctors, therapists, lawyers and advisors to use Verity '
        "early and shape its templates, review flow and pricing.</p>"
        f"{facts}"
        '<p class="small muted">Want to see it first? <a href="index.html">Try the interactive prototype</a>.</p>'
        "</div>"
        f"{_apply_card()}"
        "</div></header>"
    )


_APPLY_LABELS = {
    "Medical": "Apply as a clinician",
    "Therapy": "Apply as a therapist",
    "Legal": "Apply as an attorney",
    "Advisory": "Apply as an advisor",
}


def _who() -> str:
    cards = (
        ("tag--blue", "Medical", "Clinicians who want a SOAP note and patient summary they can sign without heavy editing."),
        ("tag--green", "Therapy", "Therapists who need DAP or BIRP notes that keep the golden thread to treatment goals."),
        ("tag--indigo", "Legal", "Attorneys who want intake memos and chronologies that never invent a conclusion."),
        ("tag--orange", "Advisory", "Advisors and consultants who need meeting notes, follow-ups and tasks delivered."),
    )
    items = "".join(
        f'<article class="card"><span class="tag {t}">{name}</span><p>{text}</p>'
        f'<a class="card__link" href="pilot.html?profession={name}#apply">{_APPLY_LABELS[name]} →</a></article>'
        for t, name, text in cards
    )
    return (
        '<section class="section"><div class="section__head"><h2>Who we’re looking for</h2>'
        "<p>Professionals who document client conversations every day and want to cut that time "
        "without giving up control of the record.</p></div>"
        f'<div class="grid">{items}</div></section>'
    )


def _how() -> str:
    return (
        '<section class="section"><div class="section__head"><h2>How the pilot works</h2></div>'
        '<ol class="steps">'
        "<li>Apply<span>Tell us about your practice. It takes a minute.</span></li>"
        "<li>Intro call<span>We learn how you document today and agree pilot terms.</span></li>"
        "<li>Template setup<span>We encode your note formats and checklists together.</span></li>"
        "<li>Use Verity<span>Record, review and sign with synthetic or authorized data.</span></li>"
        "<li>Shape the product<span>Regular feedback decides what ships next.</span></li>"
        "</ol></section>"
    )


def _exchange() -> str:
    return (
        '<section class="section"><div class="grid grid--2">'
        '<article class="card"><h3>What you get</h3><ul class="list">'
        "<li><span><b>Early access</b> to Verity on Mac and iPhone as the production build lands.</span></li>"
        "<li><span><b>Templates for your practice</b>, versioned and tested before you use them.</span></li>"
        "<li><span><b>A direct line to the team.</b> Your feedback decides what ships next.</span></li>"
        "<li><span><b>A say in pricing</b> before it’s set.</span></li>"
        "</ul></article>"
        '<article class="card"><h3>What we ask</h3><ul class="list">'
        "<li><span><b>Honest feedback</b> on drafts, review flow and templates.</span></li>"
        "<li><span><b>Sample documents</b> or checklists so we can encode your standards.</span></li>"
        "<li><span><b>Only synthetic or properly authorized data</b> during the pilot.</span></li>"
        "<li><span><b>A short check-in</b> now and then to tell us what’s working.</span></li>"
        "</ul></article>"
        "</div></section>"
    )


def _faq() -> str:
    qa = (
        ("What does the pilot cost?",
         "Pilot terms are agreed on the intro call. Our planned plans are listed on the "
         '<a href="pricing.html">pricing page</a>, and they’re still hypotheses: design partners help us set them.'),
        ("Is my clients’ data safe?",
         "Pilots start with synthetic or properly authorized data only. Verity is designed around all-party consent, "
         'no training on customer data, configurable retention and a full audit trail. See <a href="trust.html">Trust &amp; security</a>.'),
        ("What devices do I need?",
         "A Mac running macOS 26, and optionally an iPhone running iOS 26 to start recordings on the go."),
        ("Do I have to change my record system?",
         "No. Approved documents are delivered to your EHR, practice-management or matter system."),
        ("Does Verity make clinical or legal decisions?",
         "No. Verity documents what was said. The professional reviews, decides and signs."),
    )
    items = "".join(f"<details class=\"faq\"><summary>{q}</summary><p>{a}</p></details>" for q, a in qa)
    return (
        '<section class="section"><div class="section__head"><h2>Questions</h2></div>'
        f'<div class="card faq-list">{items}</div>'
        f'<p class="small muted">Something else? Email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>'
        "</section>"
    )


def pilot_body() -> str:
    script = _SCRIPT.replace("__EMAIL__", CONTACT_EMAIL).replace("__BODY__", json.dumps(BODY))
    return _hero() + _who() + _how() + _exchange() + _faq() + script

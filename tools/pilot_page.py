"""Design-partner pilot page.

GitHub Pages is static, so applications are POSTed to FormSubmit
(https://formsubmit.co), which delivers them to CONTACT_EMAIL. The first
submission triggers a one-time activation email that must be confirmed.
If the request fails, the form falls back to a pre-filled mailto link.
"""

from site_layout import CONTACT_EMAIL

ENDPOINT = f"https://formsubmit.co/ajax/{CONTACT_EMAIL}"

_PROFESSIONS = ("Medical", "Therapy", "Legal", "Advisory", "Other")
_SIZES = ("Just me", "2–10", "11–50", "50+")


def _chips(name: str, options, required: bool) -> str:
    req = " required" if required else ""
    return "".join(
        f'<label class="chip"><input type="radio" name="{name}" value="{o}"{req if i == 0 else ""}>'
        f"<span>{o}</span></label>"
        for i, o in enumerate(options)
    )


def _form() -> str:
    return f"""
<div class="apply card" id="apply">
  <div class="apply__head" id="apply-head">
    <h2 class="apply__title">Apply to the pilot</h2>
    <p class="small muted">Takes about a minute. We reply within a few days.</p>
  </div>
  <form id="pilot-form" novalidate>
    <input type="hidden" name="plan" id="f-plan" value="">
    <p class="plan-pill" id="plan-pill" hidden>Interested in the <b id="plan-name"></b> plan · <a href="pricing.html">change</a></p>
    <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="field">
      <label for="f-name">Full name</label>
      <input id="f-name" name="name" autocomplete="name" required maxlength="100" placeholder="Jane Doe…">
      <div class="field__error" id="e-name" aria-live="polite"></div>
    </div>
    <div class="field">
      <label for="f-email">Work email</label>
      <input id="f-email" name="email" type="email" inputmode="email" autocomplete="email" spellcheck="false" autocapitalize="off" required maxlength="200" placeholder="jane@practice.com…">
      <div class="field__error" id="e-email" aria-live="polite"></div>
    </div>
    <fieldset class="field">
      <legend>Profession</legend>
      <div class="chips" id="f-profession">{_chips("profession", _PROFESSIONS, True)}</div>
      <div class="field__error" id="e-profession" aria-live="polite"></div>
    </fieldset>
    <fieldset class="field">
      <legend>Practice size</legend>
      <div class="chips">{_chips("size", _SIZES, False)}</div>
    </fieldset>
    <div class="field">
      <label for="f-org">Practice or firm <span class="muted">(optional)</span></label>
      <input id="f-org" name="organization" autocomplete="organization" maxlength="150" placeholder="Riverside Family Clinic…">
    </div>
    <div class="field">
      <label for="f-notes">What takes the most time in your documentation today? <span class="muted">(optional)</span></label>
      <textarea id="f-notes" name="notes" maxlength="2000" rows="3" placeholder="e.g. Writing progress notes after hours…"></textarea>
    </div>
    <label class="check">
      <input type="checkbox" id="f-consent" name="consent" value="yes" required>
      <span>I agree to be contacted about the Verity pilot.</span>
    </label>
    <div class="field__error" id="e-consent" aria-live="polite"></div>
    <button class="btn btn--ink apply__submit" type="submit" id="f-submit">Send application</button>
    <p class="form__status" id="form-status" role="status" aria-live="polite"></p>
  </form>
  <div class="success" id="pilot-success" hidden tabindex="-1">
    <div class="success__icon" aria-hidden="true">✓</div>
    <h2 class="apply__title">Application received</h2>
    <p class="muted">Thanks, <span id="success-name"></span>. We’ll be in touch at
    <b id="success-email"></b> within a few days.</p>
    <a class="btn" href="index.html">Explore the prototype</a>
  </div>
</div>
"""


_SCRIPT = """
<script>
(function () {
  var ENDPOINT = "__ENDPOINT__";
  var TO = "__EMAIL__";
  var EMAIL_RE = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/;
  var TIMEOUT_MS = 15000;
  var form = document.getElementById("pilot-form");
  if (!form) return;
  var submitBtn = document.getElementById("f-submit");
  var status = document.getElementById("form-status");

  function val(name) { return String(new FormData(form).get(name) || "").trim(); }
  function setError(id, msg, focusEl) {
    var out = document.getElementById("e-" + id);
    var el = focusEl || document.getElementById("f-" + id);
    if (el) el.setAttribute("aria-invalid", msg ? "true" : "false");
    if (out) out.textContent = msg;
    return msg ? el : null;
  }
  function validate() {
    var bad = [
      setError("name", val("name") ? "" : "Please enter your name."),
      setError("email", EMAIL_RE.test(val("email")) ? "" : "Please enter a valid email address."),
      setError("profession", val("profession") ? "" : "Please choose a profession."),
      setError("consent", document.getElementById("f-consent").checked ? "" : "Please confirm we can contact you.")
    ].filter(Boolean);
    if (bad.length) {
      var first = bad[0].querySelector ? (bad[0].querySelector("input") || bad[0]) : bad[0];
      first.focus();
      return false;
    }
    return true;
  }
  function payload() {
    return {
      name: val("name"),
      email: val("email"),
      profession: val("profession"),
      practice_size: val("size") || "Not given",
      organization: val("organization") || "Not given",
      notes: val("notes") || "Not given",
      plan_interest: val("plan") || "Not given",
      _subject: "Verity pilot application — " + val("name"),
      _replyto: val("email"),
      _template: "table",
      _captcha: "false",
      _honey: val("_honey")
    };
  }
  function mailtoHref(d) {
    var body = ["Name: " + d.name, "Email: " + d.email, "Profession: " + d.profession,
      "Practice size: " + d.practice_size, "Practice / firm: " + d.organization,
      "Plan interest: " + d.plan_interest, "", d.notes].join("\\n");
    return "mailto:" + TO + "?subject=" + encodeURIComponent(d._subject) + "&body=" + encodeURIComponent(body);
  }
  function setBusy(busy) {
    submitBtn.disabled = busy;
    submitBtn.textContent = busy ? "Sending…" : "Send application";
    form.setAttribute("aria-busy", busy ? "true" : "false");
  }
  function showSuccess(d) {
    document.getElementById("success-name").textContent = d.name.split(" ")[0];
    document.getElementById("success-email").textContent = d.email;
    form.hidden = true;
    document.getElementById("apply-head").hidden = true;
    var s = document.getElementById("pilot-success");
    s.hidden = false;
    s.focus();
  }
  function showFailure(d) {
    status.className = "form__status form__status--error";
    status.innerHTML = "";
    status.append("We couldn’t send your application. ");
    var a = document.createElement("a");
    a.href = mailtoHref(d);
    a.textContent = "Email it to us instead";
    status.append(a, ".");
  }

  (function prefill() {
    var q = new URLSearchParams(location.search);
    var plan = (q.get("plan") || "").replace(/[^A-Za-z ]/g, "").slice(0, 30);
    var PLANS = ["Starter", "Professional", "Team"];
    if (PLANS.indexOf(plan) >= 0) {
      document.getElementById("f-plan").value = plan;
      document.getElementById("plan-name").textContent = plan;
      document.getElementById("plan-pill").hidden = false;
    }
    var prof = q.get("profession");
    var radio = prof && form.querySelector('input[name="profession"][value="' + prof.replace(/[^A-Za-z]/g, "") + '"]');
    if (radio) radio.checked = true;
  })();

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    status.textContent = "";
    status.className = "form__status";
    if (!validate()) return;
    var d = payload();
    if (d._honey) { showSuccess(d); return; }   // bot filled the hidden field
    setBusy(true);
    var ctrl = "AbortController" in window ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, TIMEOUT_MS);
    fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(d),
      signal: ctrl ? ctrl.signal : undefined
    })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        var ok = res.ok && String(res.j.success) !== "false";
        if (ok) { showSuccess(d); } else { console.error("Pilot form rejected", res.j); showFailure(d); }
      })
      .catch(function (err) { console.error("Pilot form failed", err); showFailure(d); })
      .then(function () { clearTimeout(timer); setBusy(false); });
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
        f"{_form()}"
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
    script = _SCRIPT.replace("__ENDPOINT__", ENDPOINT).replace("__EMAIL__", CONTACT_EMAIL)
    return _hero() + _who() + _how() + _exchange() + _faq() + script

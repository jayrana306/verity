"""Design-partner pilot page. GitHub Pages has no backend, so the form is
validated in the browser and opens a pre-filled email to CONTACT_EMAIL."""

from site_layout import CONTACT_EMAIL, hero

_FORM = """
<form class="form card" id="pilot-form" novalidate>
  <div class="field">
    <label for="f-name">Full name</label>
    <input id="f-name" name="name" autocomplete="name" required maxlength="100">
    <div class="field__error" id="e-name" aria-live="polite"></div>
  </div>
  <div class="field">
    <label for="f-email">Work email</label>
    <input id="f-email" name="email" type="email" autocomplete="email" required maxlength="200">
    <div class="field__error" id="e-email" aria-live="polite"></div>
  </div>
  <div class="field">
    <label for="f-profession">Profession</label>
    <select id="f-profession" name="profession" required>
      <option value="">Choose one</option>
      <option>Medical</option><option>Therapy / behavioral health</option>
      <option>Legal</option><option>Consulting / advisory</option><option>Other</option>
    </select>
    <div class="field__error" id="e-profession" aria-live="polite"></div>
  </div>
  <div class="field">
    <label for="f-size">Practice size</label>
    <select id="f-size" name="size">
      <option>Just me</option><option>2–10 people</option><option>11–50 people</option><option>50+ people</option>
    </select>
    <div class="field__error"></div>
  </div>
  <div class="field field--full">
    <label for="f-org">Practice or firm (optional)</label>
    <input id="f-org" name="org" autocomplete="organization" maxlength="150">
  </div>
  <div class="field field--full">
    <label for="f-notes">What takes the most time in your documentation today? (optional)</label>
    <textarea id="f-notes" name="notes" maxlength="2000"></textarea>
  </div>
  <div class="field--full actions">
    <button class="btn btn--ink" type="submit">Apply by email</button>
  </div>
  <p class="form__status" id="form-status" aria-live="polite">Submitting opens your email app with your answers filled in.
  Prefer to write yourself? Email <a href="mailto:__EMAIL__">__EMAIL__</a>.</p>
</form>
"""

_SCRIPT = """
<script>
(function () {
  var TO = "__EMAIL__";
  var EMAIL_RE = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  var form = document.getElementById("pilot-form");
  if (!form) return;
  function setError(id, msg) {
    var input = document.getElementById("f-" + id);
    var out = document.getElementById("e-" + id);
    if (input) input.setAttribute("aria-invalid", msg ? "true" : "false");
    if (out) out.textContent = msg;
    return !msg;
  }
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var d = new FormData(form);
    var name = String(d.get("name") || "").trim();
    var email = String(d.get("email") || "").trim();
    var profession = String(d.get("profession") || "");
    var ok = [
      setError("name", name ? "" : "Please enter your name."),
      setError("email", EMAIL_RE.test(email) ? "" : "Please enter a valid email address."),
      setError("profession", profession ? "" : "Please choose a profession.")
    ].every(Boolean);
    if (!ok) {
      var first = form.querySelector('[aria-invalid="true"]');
      if (first) first.focus();
      return;
    }
    var lines = [
      "Name: " + name,
      "Email: " + email,
      "Profession: " + profession,
      "Practice size: " + String(d.get("size") || ""),
      "Practice / firm: " + String(d.get("org") || "").trim(),
      "",
      "Biggest documentation time sink:",
      String(d.get("notes") || "").trim()
    ];
    var href = "mailto:" + TO +
      "?subject=" + encodeURIComponent("Verity pilot application — " + name) +
      "&body=" + encodeURIComponent(lines.join("\\n"));
    document.getElementById("form-status").textContent =
      "Opening your email app… If nothing happens, email " + TO + " directly.";
    window.location.href = href;
  });
})();
</script>
"""


def pilot_body() -> str:
    expect = (
        '<div class="card"><h3>What to expect</h3><ul class="list">'
        "<li><span><b>Early access</b> to Verity on Mac and iPhone as the production build lands.</span></li>"
        "<li><span><b>Templates for your practice</b> — we encode your documentation standards together.</span></li>"
        "<li><span><b>A direct line to the team.</b> Your feedback decides what ships next.</span></li>"
        "<li><span><b>Safe by design.</b> Pilots start with synthetic or properly authorized data only.</span></li>"
        "</ul></div>"
    )
    form = _FORM.replace("__EMAIL__", CONTACT_EMAIL)
    return (
        hero("Design-partner pilot", "Help build documentation you can sign.",
             "We’re recruiting a small group of doctors, therapists, lawyers and advisors to pilot Verity "
             "and shape its templates, review flow and pricing.")
        + '<section class="section"><div class="grid grid--2">'
        + expect + form + "</div></section>"
        + _SCRIPT.replace("__EMAIL__", CONTACT_EMAIL)
    )

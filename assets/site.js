// Mobile menu (<details class="menu">): close on Escape, outside click, or link choice.
// Delegated, so it also works when the menu is rendered after load (the prototype page).
(function () {
  function openMenu() { return document.querySelector(".menu[open]"); }
  document.addEventListener("keydown", function (e) {
    var menu = openMenu();
    if (e.key !== "Escape" || !menu) return;
    menu.removeAttribute("open");
    var btn = menu.querySelector("summary");
    if (btn) btn.focus();
  });
  document.addEventListener("click", function (e) {
    var menu = openMenu();
    if (!menu) return;
    if (!menu.contains(e.target) || e.target.closest(".menu__panel a")) menu.removeAttribute("open");
  });
})();

(function () {
  "use strict";

  function initMobileNav() {
    var toggle = document.querySelector(".cisc-menu-toggle");
    var list = document.querySelector(".cisc-nav__list");
    if (!toggle || !list) return;

    toggle.addEventListener("click", function () {
      var open = list.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", function (e) {
      if (!toggle.contains(e.target) && !list.contains(e.target)) {
        list.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  function markActiveNav() {
    var path = window.location.pathname.replace(/\/index\.html$/, "/").replace(/\/$/, "");
    if (path === "" || path.endsWith("/center-industrial-supply.github.io")) {
      path = "/";
    }

    document.querySelectorAll(".cisc-nav__link").forEach(function (link) {
      var href = link.getAttribute("href");
      if (!href || href === "#") return;
      try {
        var linkPath = new URL(href, window.location.origin).pathname.replace(/\/index\.html$/, "/").replace(/\/$/, "");
        if (linkPath === path || (path !== "/" && linkPath !== "/" && path.indexOf(linkPath) === 0)) {
          link.classList.add("is-active");
        }
      } catch (err) {
        /* ignore malformed href */
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initMobileNav();
    markActiveNav();
  });
})();

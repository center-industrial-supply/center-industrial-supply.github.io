(function () {
  "use strict";

  function loadPartial(name, targetId) {
    return fetch("/assets/partials/" + name + ".html")
      .then(function (res) {
        if (!res.ok) throw new Error("Failed to load partial: " + name);
        return res.text();
      })
      .then(function (html) {
        var el = document.getElementById(targetId);
        if (el) el.innerHTML = html;
      });
  }

  function wrapLegacyMain() {
    var siteMain = document.querySelector(".site-main");
    if (!siteMain || document.getElementById("cisc-legacy-wrap")) return;

    var wrap = document.createElement("div");
    wrap.id = "cisc-legacy-wrap";
    wrap.className = "cisc-legacy-content";
    siteMain.parentNode.insertBefore(wrap, siteMain);
    wrap.appendChild(siteMain);

    // Keep legacy content outside `.site` so legacy.css can hide the old shell
    // without hiding the recovered product/category markup.
    var site = document.querySelector("body.cisc-legacy > .site");
    if (site && wrap.parentNode === site) {
      site.parentNode.insertBefore(wrap, site.nextSibling);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.body.classList.add("cisc-legacy");

    var headerMount = document.createElement("div");
    headerMount.id = "cisc-header-mount";
    document.body.insertBefore(headerMount, document.body.firstChild);

    var footerMount = document.createElement("div");
    footerMount.id = "cisc-footer-mount";
    document.body.appendChild(footerMount);

    Promise.all([
      loadPartial("header", "cisc-header-mount"),
      loadPartial("footer", "cisc-footer-mount"),
    ])
      .then(function () {
        wrapLegacyMain();
        if (window.CISC && typeof window.CISC.initSite === "function") {
          window.CISC.initSite();
        } else {
          var script = document.createElement("script");
          script.src = "/assets/js/site.js";
          document.body.appendChild(script);
        }
      })
      .catch(function (err) {
        console.warn("CISC layout:", err);
      });
  });
})();

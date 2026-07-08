(function () {
  "use strict";

  var SITE_ROOT = (function () {
    var parts = window.location.pathname.split("/").filter(Boolean);
    if (parts.length && parts[parts.length - 1] === "index.html") {
      parts.pop();
    }
    return "/" + parts.join("/") + (parts.length ? "/" : "");
  })();

  function rootPrefix() {
    var depth = window.location.pathname.split("/").filter(Boolean).length;
    if (window.location.pathname.endsWith("index.html")) {
      depth -= 1;
    }
  /* For github.io root site, absolute paths from / work */
    return "/";
  }

  function prefixToRoot() {
    var segments = window.location.pathname.split("/").filter(function (s) {
      return s && s !== "index.html";
    });
    if (!segments.length) return "./";
    return segments.map(function () { return ".."; }).join("/") + "/";
  }

  function loadPartial(name, targetId) {
    var prefix = prefixToRoot();
    var url = prefix + "assets/partials/" + name + ".html";
    return fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error("Failed to load " + url);
        return res.text();
      })
      .then(function (html) {
        var el = document.getElementById(targetId);
        if (el) {
          el.innerHTML = html.replace(/\{\{PREFIX\}\}/g, prefix);
        }
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
      loadPartial("footer", "cisc-footer-mount")
    ])
      .then(function () {
        wrapLegacyMain();
        if (window.CISC && typeof window.CISC.initSite === "function") {
          window.CISC.initSite();
        } else {
          var script = document.createElement("script");
          script.src = prefixToRoot() + "assets/js/site.js";
          document.body.appendChild(script);
        }
      })
      .catch(function (err) {
        console.warn("CISC layout:", err);
      });
  });
})();

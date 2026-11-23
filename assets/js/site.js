// HR Connect marketing site: navigation, forms and filters.
(function () {
  // Mobile navigation toggle
  var toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Forms: there is no form backend yet, so submissions open the visitor's
  // email app addressed to the site's contact address (data-mailto).
  document.querySelectorAll("form[data-mailto]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var lines = [];
      new FormData(form).forEach(function (v, k) {
        if (String(v).trim()) lines.push(k + ": " + v);
      });
      var subject = form.getAttribute("data-subject") || "Website enquiry";
      window.location.href = "mailto:" + form.getAttribute("data-mailto") +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      var ok = form.querySelector(".form-ok");
      if (ok) ok.style.display = "block";
    });
  });

  // Live filter for glossary and help articles
  document.querySelectorAll("[data-filter]").forEach(function (input) {
    var items = document.querySelectorAll(input.getAttribute("data-filter"));
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      items.forEach(function (el) {
        el.style.display = !q || el.textContent.toLowerCase().indexOf(q) !== -1 ? "" : "none";
      });
    });
  });

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();

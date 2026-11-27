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

  // Solutions spotlight slider (home page). Tabs, arrows, swipe and keyboard
  // switch slides; it advances on its own when the progress bar fills, and
  // pauses while the pointer or keyboard focus is inside it. With reduced
  // motion turned on, the progress bar doesn't animate, so it never advances.
  document.querySelectorAll(".spotlight").forEach(function (root) {
    var tabs = root.querySelectorAll(".sp-tab");
    var slides = root.querySelectorAll(".sp-slide");
    var track = root.querySelector(".sp-track");
    var bar = root.querySelector(".sp-progress span");
    if (!tabs.length || tabs.length !== slides.length || !track) return;
    var current = 0;
    var hovering = false;
    var focused = false;

    function restartBar() {
      if (!bar) return;
      bar.classList.remove("run");
      void bar.offsetWidth; // restart the CSS animation
      bar.classList.add("run");
    }

    function go(i, focusTab) {
      var n = slides.length;
      current = (i + n) % n;
      track.style.transform = "translateX(" + (-100 * current) + "%)";
      for (var k = 0; k < n; k++) {
        var on = k === current;
        tabs[k].setAttribute("aria-selected", on ? "true" : "false");
        tabs[k].tabIndex = on ? 0 : -1;
        if (on) {
          slides[k].removeAttribute("aria-hidden");
          slides[k].inert = false;
        } else {
          slides[k].setAttribute("aria-hidden", "true");
          slides[k].inert = true;
        }
      }
      if (focusTab) tabs[current].focus();
      // On phones the tab row scrolls sideways; keep the active tab visible.
      var row = tabs[current].parentNode;
      if (row.scrollWidth > row.clientWidth) {
        row.scrollTo({ left: tabs[current].offsetLeft - (row.clientWidth - tabs[current].offsetWidth) / 2, behavior: "smooth" });
      }
      restartBar();
    }

    function setPaused() {
      root.classList.toggle("paused", hovering || focused);
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { go(i); });
    });

    root.querySelector(".sp-tabs").addEventListener("keydown", function (e) {
      var next = { ArrowRight: current + 1, ArrowLeft: current - 1, Home: 0, End: slides.length - 1 }[e.key];
      if (next === undefined) return;
      e.preventDefault();
      go(next, true);
    });

    root.querySelectorAll("[data-sp]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        go(current + (btn.getAttribute("data-sp") === "next" ? 1 : -1));
      });
    });

    if (bar) {
      bar.addEventListener("animationend", function () { go(current + 1); });
    }

    root.addEventListener("mouseenter", function () { hovering = true; setPaused(); });
    root.addEventListener("mouseleave", function () { hovering = false; setPaused(); });
    root.addEventListener("focusin", function () { focused = true; setPaused(); });
    root.addEventListener("focusout", function (e) {
      if (!root.contains(e.relatedTarget)) { focused = false; setPaused(); }
    });

    // Swipe left or right on touch screens
    var viewport = root.querySelector(".sp-viewport");
    var startX = null, startY = null;
    viewport.addEventListener("touchstart", function (e) {
      startX = e.touches[0].clientX; startY = e.touches[0].clientY;
    }, { passive: true });
    viewport.addEventListener("touchend", function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      var dy = e.changedTouches[0].clientY - startY;
      startX = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) go(current + (dx < 0 ? 1 : -1));
    }, { passive: true });

    go(0);
  });

  // Hero slider (home page). Advances every data-interval ms; arrows, dots,
  // swipe and ←/→ change slides. Pauses on hover, while focus is inside and
  // while the browser tab is hidden. No autoplay with reduced motion turned on.
  document.querySelectorAll(".hero-slider").forEach(function (root) {
    var slides = root.querySelectorAll(".hs-slide");
    var dots = root.querySelectorAll(".hs-dot");
    var track = root.querySelector(".hs-track");
    if (slides.length < 2 || !track) return;
    var interval = parseInt(root.getAttribute("data-interval"), 10) || 6000;
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var current = 0, timer = null, hovering = false, focused = false;
    var bgRun = function () {};

    function go(i) {
      var n = slides.length;
      current = (i + n) % n;
      // Background lines stay hidden on slide 1, which has its own hub animation
      root.classList.toggle("hs-first", current === 0);
      track.style.transform = "translateX(" + (-100 * current) + "%)";
      for (var k = 0; k < n; k++) {
        var on = k === current;
        if (on) { slides[k].removeAttribute("aria-hidden"); slides[k].inert = false; }
        else { slides[k].setAttribute("aria-hidden", "true"); slides[k].inert = true; }
        // is-active replays the CSS slide-in animation on the incoming slide's content
        slides[k].classList.toggle("is-active", on);
        if (dots[k]) {
          if (on) dots[k].setAttribute("aria-current", "true");
          else dots[k].removeAttribute("aria-current");
        }
      }
      schedule();
      bgRun();
    }

    function schedule() {
      clearTimeout(timer);
      timer = null;
      if (reduce || hovering || focused || document.hidden) return;
      timer = setTimeout(function () { go(current + 1); }, interval);
    }

    root.querySelectorAll("[data-hs]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        go(current + (btn.getAttribute("data-hs") === "next" ? 1 : -1));
      });
    });
    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () { go(i); });
    });
    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(current + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); go(current - 1); }
    });

    root.addEventListener("mouseenter", function () { hovering = true; schedule(); });
    root.addEventListener("mouseleave", function () { hovering = false; schedule(); });
    root.addEventListener("focusin", function () { focused = true; schedule(); });
    root.addEventListener("focusout", function (e) {
      if (!root.contains(e.relatedTarget)) { focused = false; schedule(); }
    });
    document.addEventListener("visibilitychange", schedule);

    var viewport = root.querySelector(".hs-viewport");
    var startX = null, startY = null;
    viewport.addEventListener("touchstart", function (e) {
      startX = e.touches[0].clientX; startY = e.touches[0].clientY;
    }, { passive: true });
    viewport.addEventListener("touchend", function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      var dy = e.changedTouches[0].clientY - startY;
      startX = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) go(current + (dx < 0 ? 1 : -1));
    }, { passive: true });

    // Background for slides 2+: lines from the logo (centred behind the
    // dashboard image) out to every edge of the section, with dots that pick
    // a random line and speed each time they set off and travel outward.
    var bg = root.querySelector(".hs-bg");
    var svg = bg && bg.querySelector(".hs-lines");
    var col = slides[1].querySelector(".hero-grid > div:last-child");
    if (bg && svg && col) {
      var NS = "http://www.w3.org/2000/svg";
      var LINES = 14, DOTS = 12;
      var jitter = [];
      for (var j = 0; j < LINES; j++) jitter.push((Math.random() - 0.5) * 0.6);
      var lines = [], dotsBg = [], raf = null, last = 0, onScreen = false;

      var launch = function (d, anywhere) {
        d.line = lines[Math.floor(Math.random() * lines.length)];
        d.speed = 30 + Math.random() * 70;         // px per second
        d.p = anywhere ? Math.random() : 0;        // progress 0..1 along the trip
        d.wait = anywhere ? 0 : Math.random() * 2; // short random pause before setting off
      };

      var layout = function () {
        var r = root.getBoundingClientRect();
        var s = slides[1].getBoundingClientRect();
        var v = viewport.getBoundingClientRect();
        var c = col.getBoundingClientRect();
        var w = r.width, h = r.height;
        if (!w || !h || !c.width) return;
        // Slide 2 sits off to the side of the track; measure it relative to
        // its own slide, then place that slide where the viewport is.
        var cx = c.left - s.left + c.width / 2 + (v.left - r.left);
        var cy = c.top - s.top + c.height / 2 + (v.top - r.top);
        bg.style.setProperty("--hs-cx", cx + "px");
        bg.style.setProperty("--hs-cy", cy + "px");
        svg.setAttribute("viewBox", "0 0 " + w + " " + h);
        while (svg.firstChild) svg.removeChild(svg.firstChild);
        lines = [];
        for (var i = 0; i < LINES; i++) {
          var a = (i + 0.5 + jitter[i]) / LINES * Math.PI * 2;
          var dx = Math.cos(a), dy = Math.sin(a);
          // Distance along the ray to the section's edge
          var t = Math.min(dx > 0 ? (w - cx) / dx : dx < 0 ? -cx / dx : Infinity,
                           dy > 0 ? (h - cy) / dy : dy < 0 ? -cy / dy : Infinity);
          var ln = document.createElementNS(NS, "line");
          ln.setAttribute("x1", cx); ln.setAttribute("y1", cy);
          ln.setAttribute("x2", cx + dx * t); ln.setAttribute("y2", cy + dy * t);
          svg.appendChild(ln);
          lines.push({ x: cx, y: cy, dx: dx, dy: dy, len: t });
        }
        dotsBg = [];
        if (reduce) return;
        for (var k = 0; k < DOTS; k++) {
          var el = document.createElementNS(NS, "circle");
          el.setAttribute("r", 3);
          el.setAttribute("opacity", 0);
          svg.appendChild(el);
          var d = { el: el };
          launch(d, true);
          dotsBg.push(d);
        }
      };

      var frame = function (now) {
        var dt = last ? Math.min((now - last) / 1000, 0.1) : 0;
        last = now;
        for (var k = 0; k < dotsBg.length; k++) {
          var d = dotsBg[k], ln = d.line;
          if (d.wait > 0) { d.wait -= dt; continue; }
          d.p += d.speed * dt / ln.len;
          if (d.p >= 1) { launch(d, false); d.el.setAttribute("opacity", 0); continue; }
          var dist = d.p * ln.len; // always from the logo out to the edge
          d.el.setAttribute("cx", ln.x + ln.dx * dist);
          d.el.setAttribute("cy", ln.y + ln.dy * dist);
          d.el.setAttribute("opacity", Math.min(1, d.p / 0.08, (1 - d.p) / 0.08));
        }
        raf = requestAnimationFrame(frame);
      };

      bgRun = function () {
        var run = !reduce && onScreen && !document.hidden && current !== 0 && dotsBg.length > 0;
        if (run && !raf) { last = 0; raf = requestAnimationFrame(frame); }
        else if (!run && raf) { cancelAnimationFrame(raf); raf = null; }
      };

      layout();
      var resizeTimer = null;
      window.addEventListener("resize", function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () { layout(); bgRun(); }, 150);
      });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { layout(); bgRun(); });
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (entries) { onScreen = entries[0].isIntersecting; bgRun(); }).observe(root);
      } else { onScreen = true; }
      document.addEventListener("visibilitychange", bgRun);
    }

    go(0);
  });

  // Scroll reveal: page elements slide in as they come into view. Picks the
  // site's building blocks by selector, so no markup changes are needed.
  // Items in a row (cards, steps, footer columns) are staggered; the two
  // halves of a split slide in from their own side. The hero slider and the
  // Solutions slider animate themselves, so they're left out. Skipped with
  // reduced motion or without IntersectionObserver; nothing is hidden then.
  (function () {
    if (!("IntersectionObserver" in window)) return;
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var SELECTORS = [
      ".hero:not(.hero-slider) .crumbs",
      ".hero:not(.hero-slider) .hero-grid > div:first-child > *:not(.crumbs)",
      ".hero:not(.hero-slider):not(.solo) .hero-grid > div:last-child",
      ".section-head > *",
      ".grid > .card", ".steps > .step", ".stats > .stat", ".plans > .plan",
      ".split > div",
      ".faq > details", ".help-group", ".table-wrap",
      ".cta-box",
      ".prose > *", ".notice",
      ".search", ".az", ".terms > .term",
      ".form-card", ".calc-result",
      ".sp-tabs", ".sp-viewport", ".sp-controls",
      ".foot-grid > div", ".foot-bottom"
    ];
    var SKIP = ".hero-slider, .sp-viewport .sp-track";
    var STAGGER = ".grid, .steps, .stats, .plans, .faq, .terms, .foot-grid, .section-head, .hero-grid > div:first-child";

    var seen = [];
    document.querySelectorAll(SELECTORS.join(",")).forEach(function (el) {
      if (el.closest(SKIP) || seen.indexOf(el) !== -1) return;
      // Don't animate something whose ancestor is already animating
      for (var i = 0; i < seen.length; i++) if (seen[i].contains(el)) return;
      seen.push(el);
    });
    if (!seen.length) return;

    seen.forEach(function (el) {
      var dir = "rv-up";
      var parent = el.parentElement;
      if (parent && parent.classList.contains("split")) {
        var pr = parent.getBoundingClientRect(), r = el.getBoundingClientRect();
        // Side-by-side halves come in from their own side; stacked ones rise
        if (pr.width > 0 && r.width < pr.width * 0.8) {
          dir = (r.left + r.width / 2) < (pr.left + pr.width / 2) ? "rv-left" : "rv-right";
        }
      } else if (el.matches(".hero:not(.solo) .hero-grid > div:last-child")) {
        dir = "rv-right";
      }
      var delay = 0;
      if (parent && parent.matches(STAGGER)) {
        delay = Math.min(Array.prototype.indexOf.call(parent.children, el), 6) * 90;
      }
      el.classList.add("rv", dir);
      if (delay) el.style.setProperty("--rv-delay", delay + "ms");
    });
    document.documentElement.classList.add("rv-ready");

    function done(el) {
      el.classList.remove("rv", "rv-up", "rv-left", "rv-right", "rv-in");
      el.style.removeProperty("--rv-delay");
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        io.unobserve(el);
        el.classList.add("rv-in");
        // Hand the element back to its normal styles (hover effects etc.)
        el.addEventListener("transitionend", function end(e) {
          if (e.target !== el || e.propertyName !== "transform") return;
          el.removeEventListener("transitionend", end);
          done(el);
        });
        setTimeout(function () { if (el.classList.contains("rv")) done(el); }, 2000);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0 });
    // Start observing on the next frame so on-screen items animate in too
    requestAnimationFrame(function () {
      seen.forEach(function (el) { io.observe(el); });
    });
  })();

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();

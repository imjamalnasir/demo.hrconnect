// Free tools: KSA end-of-service, UAE gratuity and leave balance calculators.
// KSA and UAE rules follow the HR Connect app (hrconnect-frontend/src/lib/eosb/ksa.ts and uae.ts).
(function () {
  var DAY = 1000 * 60 * 60 * 24;

  function years(from, to) {
    var ms = new Date(to).getTime() - new Date(from).getTime();
    return ms > 0 ? ms / (DAY * 365.25) : 0;
  }
  function money(n, cur) {
    return cur + " " + (Math.round(n * 100) / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function num(n, d) {
    return n.toLocaleString("en-US", { maximumFractionDigits: d == null ? 2 : d });
  }
  function render(root, amount, rows, notes) {
    root.querySelector("[data-out=amount]").textContent = amount;
    root.querySelector("[data-out=rows]").innerHTML = rows.map(function (r) {
      return "<li><span>" + r[0] + "</span><span>" + r[1] + "</span></li>";
    }).join("");
    root.querySelector("[data-out=notes]").textContent = notes.join(" ");
  }
  function val(form, name) { return form.elements[name].value; }

  function ksa(form, root) {
    var basic = parseFloat(val(form, "salary")) || 0;
    var y = years(val(form, "start"), val(form, "end"));
    var reason = val(form, "reason");
    var first = (basic / 2) * Math.min(y, 5);
    var second = basic * Math.max(y - 5, 0);
    var full = first + second;
    var factor = 1, note;
    if (reason === "resignation") {
      if (y < 2) { factor = 0; note = "Resigned with less than 2 years of service: no end-of-service award."; }
      else if (y < 5) { factor = 1 / 3; note = "Resigned after 2–5 years: one third of the full award."; }
      else if (y < 10) { factor = 2 / 3; note = "Resigned after 5–10 years: two thirds of the full award."; }
      else { note = "Resigned after 10 or more years: full award."; }
    } else {
      note = "Full award for this reason for leaving.";
    }
    var amount = full * factor;
    render(root, money(amount, "SAR"), [
      ["Years of service", num(y, 2)],
      ["First 5 years (½ month per year)", money(first, "SAR")],
      ["After 5 years (1 month per year)", money(second, "SAR")],
      ["Resignation adjustment", money(amount - full, "SAR")]
    ], [note]);
  }

  function uae(form, root) {
    var basic = parseFloat(val(form, "salary")) || 0;
    var y = years(val(form, "start"), val(form, "end"));
    if (y < 1) {
      render(root, money(0, "AED"), [["Years of service", num(y, 2)]],
        ["Less than 1 year of service: no gratuity is payable."]);
      return;
    }
    var daily = basic / 30;
    var first = daily * 21 * Math.min(y, 5);
    var second = daily * 30 * Math.max(y - 5, 0);
    var total = first + second, notes = [];
    var cap = basic * 24;
    if (total > cap) { total = cap; notes.push("Capped at 2 years of basic salary."); }
    notes.push("Under the 2021 UAE Labour Law, the full gratuity applies whatever the reason for leaving.");
    render(root, money(total, "AED"), [
      ["Years of service", num(y, 2)],
      ["Daily basic salary", money(daily, "AED")],
      ["First 5 years (21 days per year)", money(first, "AED")],
      ["After 5 years (30 days per year)", money(second, "AED")]
    ], notes);
  }

  function leave(form, root) {
    var ent = parseFloat(val(form, "entitlement")) || 0;
    var start = new Date(val(form, "start"));
    var asOf = new Date(val(form, "asof"));
    var carried = parseFloat(val(form, "carried")) || 0;
    var taken = parseFloat(val(form, "taken")) || 0;
    var days = Math.max(0, Math.min(365, Math.floor((asOf - start) / DAY) + 1));
    var earned = ent * days / 365;
    var balance = earned + carried - taken;
    render(root, num(Math.round(balance * 2) / 2, 1) + " days", [
      ["Days counted this leave year", num(days, 0)],
      ["Leave earned so far", num(earned, 2) + " days"],
      ["Carried forward", num(carried, 2) + " days"],
      ["Already taken", "− " + num(taken, 2) + " days"]
    ], [balance < 0 ? "The employee has taken more leave than they have earned so far." :
      "Balance rounded to the nearest half day. Leave is earned evenly across a 365-day leave year."]);
  }

  var CALCS = { ksa: ksa, uae: uae, leave: leave };
  document.querySelectorAll("[data-calc]").forEach(function (root) {
    var form = root.querySelector("form");
    var fn = CALCS[root.getAttribute("data-calc")];
    var today = new Date().toISOString().slice(0, 10);
    root.querySelectorAll("input[data-today]").forEach(function (i) { if (!i.value) i.value = today; });
    function run() { try { fn(form, root); } catch (e) { /* incomplete input */ } }
    form.addEventListener("input", run);
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    run();
  });
})();

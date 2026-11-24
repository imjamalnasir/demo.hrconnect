// Free tools: leave balance calculator.
(function () {
  var DAY = 1000 * 60 * 60 * 24;

  function years(from, to) {
    var ms = new Date(to).getTime() - new Date(from).getTime();
    return ms > 0 ? ms / (DAY * 365.25) : 0;
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
      ["Carried over", num(carried, 2) + " days"],
      ["Already taken", "− " + num(taken, 2) + " days"]
    ], [balance < 0 ? "The employee has taken more leave than they have earned so far." :
      "Balance rounded to the nearest half day. Leave is earned evenly across a 365-day leave year."]);
  }

  var CALCS = { leave: leave };
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

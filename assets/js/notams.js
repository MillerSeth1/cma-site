(function () {
  var root = document.getElementById("kols-notams");
  if (!root) return;
  var endpoint = root.getAttribute("data-endpoint");
  var official = root.getAttribute("data-official") || "https://www.notams.faa.gov/dinsQueryWeb/";
  var statusEl = root.querySelector("[data-notams=status]");
  var listEl = root.querySelector("[data-notams=list]");
  if (!endpoint || !statusEl || !listEl) return;

  function fallback(message) {
    statusEl.textContent = message;
    listEl.replaceChildren();
  }

  fetch(endpoint, { headers: { Accept: "application/json" } })
    .then(function (res) {
      if (!res.ok) throw new Error("bad status");
      return res.json();
    })
    .then(function (data) {
      if (!data || data.ok !== true || !Array.isArray(data.notams)) throw new Error("bad payload");
      var items = data.notams;
      if (!items.length) {
        fallback("No active NOTAMs found.");
        return;
      }
      statusEl.textContent =
        items.length === 1 ? "1 active NOTAM for KOLS." : items.length + " active NOTAMs for KOLS.";
      var frag = document.createDocumentFragment();
      items.forEach(function (n) {
        var li = document.createElement("li");
        li.className = "notam";
        var id = document.createElement("div");
        id.className = "notam-id";
        id.textContent = n.number || "NOTAM";
        var times = document.createElement("div");
        times.className = "notam-times";
        var start = n.effectiveStart || "Unknown start";
        var end = n.effectiveEnd || "Unknown end";
        times.textContent = "Effective " + start + " – " + end;
        var text = document.createElement("p");
        text.className = "notam-text";
        text.textContent = n.text || "";
        li.appendChild(id);
        li.appendChild(times);
        if (n.text) li.appendChild(text);
        frag.appendChild(li);
      });
      listEl.replaceChildren(frag);
    })
    .catch(function () {
      fallback("Live NOTAMs couldn’t be loaded. Use the official FAA link below.");
    });
})();

/* Style / size / color picker for merch cards. Updates price, mockup, and lightbox target. */
(function () {
  function parseData(card) {
    var el = card.querySelector("script.product-data");
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }

  function apply(card, data, styleId, colorId) {
    var style = data.styles[styleId];
    if (!style) return;
    var color = style.colors.find(function (c) { return c.id === colorId; }) || style.colors[0];
    if (!color) return;

    var priceEl = card.querySelector("[data-price]");
    if (priceEl) priceEl.textContent = style.price;

    var brow = card.querySelector(".eyebrow");
    if (brow) {
      var parts = [style.label, color.label];
      if (data.note) parts.push(data.note);
      brow.textContent = parts.join(" · ");
    }

    var btn = card.querySelector(".zoom-media");
    var img = card.querySelector(".media img");
    var picture = card.querySelector(".media picture");
    if (btn) {
      btn.setAttribute("data-full", color.full);
      btn.setAttribute("data-alt", color.alt || "");
    }
    if (img) {
      img.src = color.full;
      img.srcset = color.jpg;
      img.sizes = color.sizes;
      img.alt = color.alt || "";
      img.width = color.width;
      img.height = color.height;
    }
    if (picture) {
      var sources = picture.querySelectorAll("source");
      sources.forEach(function (s) {
        var type = s.getAttribute("type") || "";
        if (type.indexOf("avif") !== -1) s.setAttribute("srcset", color.avif);
        else if (type.indexOf("webp") !== -1) s.setAttribute("srcset", color.webp);
        s.setAttribute("sizes", color.sizes);
      });
    }

    card.setAttribute("data-style", styleId);
    card.setAttribute("data-color", color.id);
  }

  function fillSelect(sel, items, selected) {
    if (!sel) return;
    sel.innerHTML = "";
    items.forEach(function (item) {
      var o = document.createElement("option");
      o.value = item.id;
      o.textContent = item.label;
      if (item.id === selected) o.selected = true;
      sel.appendChild(o);
    });
  }

  function bind(card) {
    var data = parseData(card);
    if (!data) return;
    var styleSel = card.querySelector("[data-opt=style]");
    var colorSel = card.querySelector("[data-opt=color]");
    var styleId = data.defaultStyle;
    var colorId = data.defaultColor;

    function onStyle() {
      styleId = styleSel.value;
      var style = data.styles[styleId];
      var keep = style.colors.some(function (c) { return c.id === colorId; });
      colorId = keep ? colorId : style.colors[0].id;
      fillSelect(colorSel, style.colors, colorId);
      apply(card, data, styleId, colorId);
    }
    function onColor() {
      colorId = colorSel.value;
      apply(card, data, styleId, colorId);
    }

    if (styleSel) styleSel.addEventListener("change", onStyle);
    if (colorSel) colorSel.addEventListener("change", onColor);
    apply(card, data, styleId, colorId);
  }

  document.querySelectorAll(".product-card").forEach(bind);
})();

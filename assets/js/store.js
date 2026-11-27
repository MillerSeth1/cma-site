/* Style / size / color picker for merch cards. Updates price, mockup, and lightbox target. */
(function () {
  function parseData(card) {
    var el = card.querySelector("script.product-data");
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }

  function showImage(card, src, alt) {
    var btn = card.querySelector(".zoom-media");
    var img = card.querySelector(".media img");
    var picture = card.querySelector(".media picture");
    if (btn) {
      btn.setAttribute("data-full", src.full);
      btn.setAttribute("data-alt", alt || "");
    }
    if (img) {
      img.src = src.full;
      img.srcset = src.jpg;
      img.sizes = src.sizes;
      img.alt = alt || "";
      img.width = src.width;
      img.height = src.height;
    }
    if (picture) {
      picture.querySelectorAll("source").forEach(function (s) {
        var type = s.getAttribute("type") || "";
        if (type.indexOf("avif") !== -1) s.setAttribute("srcset", src.avif);
        else if (type.indexOf("webp") !== -1) s.setAttribute("srcset", src.webp);
        s.setAttribute("sizes", src.sizes);
      });
    }
  }

  function renderThumbs(card, color) {
    var box = card.querySelector(".media-thumbs");
    if (!box) return;
    box.innerHTML = "";
    var views = color.views || [];
    box.hidden = views.length < 2;
    views.forEach(function (v, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "thumb" + (i === 0 ? " is-active" : "");
      b.setAttribute("aria-label", v.label);
      b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
      var im = document.createElement("img");
      im.src = (v.jpg || v.full).split(",")[0].trim().split(" ")[0];
      im.alt = "";
      im.loading = "lazy";
      im.decoding = "async";
      im.width = 96; im.height = 96;
      var cap = document.createElement("span");
      cap.textContent = v.label;
      b.appendChild(im); b.appendChild(cap);
      b.addEventListener("click", function () {
        box.querySelectorAll(".thumb").forEach(function (t) {
          var on = t === b;
          t.classList.toggle("is-active", on);
          t.setAttribute("aria-pressed", on ? "true" : "false");
        });
        showImage(card, v, v.alt);
      });
      box.appendChild(b);
    });
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
      var parts = data.hideColor ? [style.label] : [style.label, color.label];
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

    renderThumbs(card, color);
    updateBuy(card, style, color.id);
    card.setAttribute("data-style", styleId);
    card.setAttribute("data-color", color.id);
  }

  /* Checkout flag on: point the Buy link at the checkout for the chosen color + size. */
  function updateBuy(card, style, colorId) {
    var a = card.querySelector("a[data-buy]");
    if (!a || !style.links) return;
    var sizeSel = card.querySelector("[data-opt=size]");
    var size = sizeSel ? sizeSel.value : "";
    var url = style.links[colorId + "|" + size];
    if (url) {
      a.href = url;
      a.removeAttribute("aria-disabled");
      a.classList.remove("is-unavailable");
    } else {
      a.removeAttribute("href");
      a.setAttribute("aria-disabled", "true");
      a.classList.add("is-unavailable");
    }
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
    var sizeSel = card.querySelector("[data-opt=size]");
    var styleId = data.defaultStyle;
    var colorId = data.defaultColor;

    function onStyle() {
      styleId = styleSel.value;
      var style = data.styles[styleId];
      var keep = style.colors.some(function (c) { return c.id === colorId; });
      colorId = keep ? colorId : style.colors[0].id;
      fillSelect(colorSel, style.colors, colorId);
      if (sizeSel && style.sizes && style.sizes.length) {
        var cur = sizeSel.value;
        var want = style.sizes.indexOf(cur) >= 0 ? cur
          : (style.sizes.indexOf("M") >= 0 ? "M" : style.sizes[Math.min(1, style.sizes.length - 1)]);
        var labels = style.sizeLabels || {};
        fillSelect(sizeSel, style.sizes.map(function (s) { return { id: s, label: labels[s] || s }; }), want);
        var longest = 0;
        style.sizes.forEach(function (s) { longest = Math.max(longest, (labels[s] || s).length); });
        if (sizeSel.parentNode) sizeSel.parentNode.classList.toggle("opt-wide", longest > 14);
      }
      apply(card, data, styleId, colorId);
    }
    function onColor() {
      colorId = colorSel.value;
      apply(card, data, styleId, colorId);
    }

    if (styleSel) styleSel.addEventListener("change", onStyle);
    if (colorSel) colorSel.addEventListener("change", onColor);
    if (sizeSel) sizeSel.addEventListener("change", function () { apply(card, data, styleId, colorId); });
    apply(card, data, styleId, colorId);
  }

  document.querySelectorAll(".product-card").forEach(bind);
})();

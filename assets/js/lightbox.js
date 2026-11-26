/* Shared click-to-enlarge lightbox for store products, the photo gallery, and blog/article images. */
(function () {
  var ES = document.documentElement.lang === "es";
  var T = ES
    ? { viewer: "Visor de imágenes", close: "Cerrar", prev: "Imagen anterior", next: "Imagen siguiente", of: " de " }
    : { viewer: "Image viewer", close: "Close", prev: "Previous image", next: "Next image", of: " of " };

  function closest(el, sel) {
    if (!el) return null;
    if (el.closest) return el.closest(sel);
    while (el && el.nodeType === 1) {
      if (el.matches && el.matches(sel)) return el;
      el = el.parentElement;
    }
    return null;
  }

  function isExcluded(el) {
    if (!el) return true;
    if (closest(el, "header, footer, nav, .site-nav, .logo, .ic, .btn, .social-links, .hero-logo")) return true;
    var img = el.tagName === "IMG" ? el : el.querySelector && el.querySelector("img");
    if (img && img.src && /logo|favicon|icon|apple-touch/i.test(img.getAttribute("src") || "")) return true;
    if (img && (img.width && img.width < 48 && img.height && img.height < 48)) return true;
    return false;
  }

  function fullUrl(trigger) {
    if (!trigger) return "";
    var direct = trigger.getAttribute("data-full") || trigger.getAttribute("href");
    if (direct && !/^#|javascript:/i.test(direct)) return direct;
    var img = trigger.tagName === "IMG" ? trigger : trigger.querySelector && trigger.querySelector("img");
    if (!img) return "";
    if (img.currentSrc) return img.currentSrc;
    var srcset = img.getAttribute("srcset");
    if (srcset) {
      var best = "", bestW = 0;
      srcset.split(",").forEach(function (part) {
        var bits = part.trim().split(/\s+/);
        var w = parseInt(bits[1] || "0", 10);
        if (w >= bestW) {
          bestW = w;
          best = bits[0];
        }
      });
      if (best) return best;
    }
    return img.getAttribute("src") || "";
  }

  function captionOf(trigger) {
    if (trigger.getAttribute("data-caption")) return trigger.getAttribute("data-caption");
    var fig = closest(trigger, "figure");
    if (fig) {
      var cap = fig.querySelector("figcaption");
      if (cap) return cap.textContent.trim();
    }
    return "";
  }

  function altOf(trigger) {
    if (trigger.getAttribute("data-alt")) return trigger.getAttribute("data-alt");
    var img = trigger.tagName === "IMG" ? trigger : trigger.querySelector && trigger.querySelector("img");
    return (img && img.getAttribute("alt")) || "";
  }

  function collectSet(trigger) {
    var root =
      closest(trigger, "[data-gallery], .store-grid, .past-collection, article.article, .article-charts, .gallery") ||
      document;
    var nodes = root.querySelectorAll(
      "a.gallery-item, [data-lightbox], .product-card .media img, .article-fig a, .chart-fig a, .article-fig img, .article-hero img, article.article img, .gallery figure img"
    );
    var seen = [], list = [];
    Array.prototype.forEach.call(nodes, function (node) {
      if (isExcluded(node)) return;
      var t = node;
      if (node.tagName === "IMG") {
        var wrapped = closest(node, "a.gallery-item, [data-lightbox], .article-fig a, .chart-fig a");
        if (wrapped) t = wrapped;
      }
      var url = fullUrl(t);
      if (!url || seen.indexOf(url) !== -1) return;
      seen.push(url);
      list.push(t);
    });
    return list.length ? list : [trigger];
  }

  function isTrigger(el) {
    if (!el) return false;
    // Only images (and the buttons/links/figures that wrap them) — never logos, icons, or article text.
    var t = closest(
      el,
      "a.gallery-item, [data-lightbox], .product-card .media, .article-fig, .chart-fig, .article-hero, .gallery figure, article.article picture, article.article img"
    );
    if (!t || isExcluded(t)) return false;
    return true;
  }

  var dialog = document.createElement("div");
  dialog.className = "lightbox";
  dialog.setAttribute("role", "dialog");
  dialog.setAttribute("aria-modal", "true");
  dialog.setAttribute("aria-label", T.viewer);
  dialog.hidden = true;
  dialog.innerHTML =
    '<div class="lightbox-inner">' +
    '<button type="button" class="lightbox-close" aria-label="' + T.close + '">&times;</button>' +
    '<button type="button" class="lightbox-prev" aria-label="' + T.prev + '">&#10094;</button>' +
    "<figure><img alt=\"\"><figcaption></figcaption></figure>" +
    '<button type="button" class="lightbox-next" aria-label="' + T.next + '">&#10095;</button>' +
    '<p class="lightbox-count" aria-live="polite"></p>' +
    "</div>";
  document.body.appendChild(dialog);

  var img = dialog.querySelector("img");
  var cap = dialog.querySelector("figcaption");
  var countEl = dialog.querySelector(".lightbox-count");
  var closeBtn = dialog.querySelector(".lightbox-close");
  var prevBtn = dialog.querySelector(".lightbox-prev");
  var nextBtn = dialog.querySelector(".lightbox-next");
  var items = [];
  var idx = 0;
  var lastFocus = null;

  function show(i) {
    if (!items.length) return;
    idx = (i + items.length) % items.length;
    var t = items[idx];
    img.src = fullUrl(t);
    img.alt = altOf(t);
    cap.textContent = captionOf(t);
    countEl.textContent = items.length > 1 ? idx + 1 + T.of + items.length : "";
    var many = items.length > 1;
    prevBtn.hidden = !many;
    nextBtn.hidden = !many;
  }
  function open(trigger) {
    items = collectSet(trigger);
    var start = 0;
    var url = fullUrl(trigger);
    items.forEach(function (t, i) {
      if (fullUrl(t) === url) start = i;
    });
    lastFocus = document.activeElement;
    show(start);
    dialog.hidden = false;
    document.body.classList.add("lightbox-open");
    closeBtn.focus();
  }
  function close() {
    dialog.hidden = true;
    document.body.classList.remove("lightbox-open");
    img.removeAttribute("src");
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t) return;
    if (!isTrigger(t)) return;
    var trigger =
      closest(t, "a.gallery-item, [data-lightbox], .article-fig a, .chart-fig a") ||
      closest(t, ".product-card .media img, .article-fig img, .article-hero img, article.article img, .gallery figure img, .chart-fig img");
    if (!trigger || isExcluded(trigger)) return;
    if (closest(t, "a") && !closest(t, "a.gallery-item, .article-fig a, .chart-fig a")) return;
    e.preventDefault();
    open(trigger);
  });

  closeBtn.addEventListener("click", close);
  prevBtn.addEventListener("click", function () { show(idx - 1); });
  nextBtn.addEventListener("click", function () { show(idx + 1); });
  dialog.addEventListener("click", function (e) { if (e.target === dialog) close(); });
  document.addEventListener("keydown", function (e) {
    if (dialog.hidden) return;
    if (e.key === "Escape") close();
    else if (e.key === "ArrowLeft") show(idx - 1);
    else if (e.key === "ArrowRight") show(idx + 1);
  });
})();

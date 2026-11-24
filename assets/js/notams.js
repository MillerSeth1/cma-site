(function () {
  var ES = document.documentElement.lang === "es";
  function redirectLegacyNotamsHash() {
    var h = location.hash;
    if (h !== "#notams") return;
    if (document.getElementById("notams") || document.getElementById("kols-notams")) return;
    var path = location.pathname;
    var dest = null;
    if (/fuel-fbo\.html$/.test(path)) dest = path.replace(/fuel-fbo\.html$/, "notams.html");
    else if (/index\.html$/.test(path)) dest = path.replace(/index\.html$/, "notams.html");
    else if (/\/es\/?$/.test(path)) dest = path.replace(/\/es\/?$/, "/es/notams.html");
    else if (/\/$/.test(path)) dest = path.replace(/\/$/, "/notams.html");
    if (dest) location.replace(dest + h);
  }
  redirectLegacyNotamsHash();
  function tr(en) {
    if (!ES) return en;
    if (SUM[en]) return SUM[en];
    var s = en;
    var pairs = [
      [/^(\S+) is currently unavailable$/, "$1 no está disponible en este momento"],
      [/^Runway (.+) is closed$/, "La pista $1 está cerrada"],
      [/^A runway is closed$/, "Una pista está cerrada"],
      [/^Taxiway (.+) is closed$/, "La calle de rodaje $1 está cerrada"],
      [/^A taxiway is closed$/, "Una calle de rodaje está cerrada"],
      [/^The cargo apron is closed$/, "La plataforma de carga está cerrada"],
      [/^An apron is closed$/, "Una plataforma está cerrada"],
      [/^Construction work on the cargo apron$/, "Obras en la plataforma de carga"],
      [/^Construction work on the apron$/, "Obras en la plataforma"],
      [/^Construction work on the runway$/, "Obras en la pista"],
      [/^Construction work on a taxiway$/, "Obras en una calle de rodaje"],
      [/^Construction work on the field$/, "Obras en el campo"],
      [/^Obstacle lighting is out of service$/, "La iluminación de un obstáculo está fuera de servicio"],
      [/^An obstacle is reported near the airport$/, "Se reporta un obstáculo cerca del aeropuerto"],
      [/^Tower lighting is out of service$/, "La iluminación de la torre está fuera de servicio"],
      [/^Runway lighting is out of service$/, "La iluminación de pista está fuera de servicio"],
      [/^A light is out of service$/, "Una luz está fuera de servicio"],
      [/^Extensive parachute activity near the airport$/, "Actividad extensa de paracaidismo cerca del aeropuerto"],
      [/^Unmanned aircraft activity in the area$/, "Actividad de aeronaves no tripuladas en la zona"],
      [/^Temporary flight restriction in effect$/, "Restricción temporal de vuelo (TFR) en vigor"],
      [/^A local airspace advisory is in effect$/, "Hay un aviso local de espacio aéreo en vigor"],
      [/^See official FAA text for details\.$/, "Consulte el texto oficial de la FAA para más detalles."]
    ];
    for (var i = 0; i < pairs.length; i++) {
      var m = s.match(pairs[i][0]);
      if (m) return s.replace(pairs[i][0], pairs[i][1]);
    }
    return s;
  }
  var TAGS = ES ? {
    Fuel: "Combustible", Runway: "Pista", Taxiway: "Calle de rodaje", Apron: "Plataforma",
    Closed: "Cerrado", Construction: "Obras", Obstacle: "Obstáculo", Lighting: "Iluminación",
    Airspace: "Espacio aéreo", Notice: "Aviso"
  } : {};
  var SUM = {};
  var root = document.getElementById("notams") || document.getElementById("kols-notams");
  var hero = document.getElementById("hero-notams");
  var banner = document.querySelector("[data-notams=fuel-banner]");
  var endpoint = (root && root.getAttribute("data-endpoint")) || (hero && hero.getAttribute("data-endpoint")) || (banner && banner.getAttribute("data-endpoint"));
  if (!endpoint) return;

  var official = (root && root.getAttribute("data-official")) || "";
  var statusEl = root && root.querySelector("[data-notams=status]");
  var listEl = root && root.querySelector("[data-notams=list]");
  var updatedEl = root && root.querySelector("[data-notams=updated]");
  var moreWrap = root && root.querySelector("[data-notams=more-wrap]");
  var toggleBtn = root && root.querySelector("[data-notams=toggle]");

  function heroCopy(count, kind) {
    if (kind === "fail") {
      return { count: "—", label: ES ? "Vea los avisos oficiales de la FAA" : "See official FAA notices" };
    }
    if (kind === "loading") {
      return { count: "—", label: ES ? "Consultando avisos vigentes" : "Checking current notices" };
    }
    if (count === 0) {
      return { count: "0", label: ES ? "Ningún aviso activo" : "No active notices" };
    }
    if (count === 1) {
      return { count: "1", label: ES ? "1 aviso activo" : "1 active notice" };
    }
    return { count: String(count), label: ES ? (count + " avisos activos") : (count + " active notices") };
  }

  function fallback(message) {
    if (statusEl) statusEl.textContent = message;
    if (listEl) listEl.replaceChildren();
    if (moreWrap) moreWrap.hidden = true;
    setHero(heroCopy(null, "fail"), false);
    setFuelBanners([]);
  }

  function setHero(copy, alert) {
    if (!hero) return;
    var countEl = hero.querySelector("[data-notams-hero=count]");
    var labelEl = hero.querySelector("[data-notams-hero=label]");
    var label = copy && copy.label ? copy.label : (ES ? "NOTAM de KOLS" : "KOLS NOTAMs");
    var count = copy && copy.count != null ? copy.count : "—";
    if (countEl) countEl.textContent = count;
    if (labelEl) labelEl.textContent = label;
    if (!countEl && !labelEl) {
      hero.textContent = count !== "—" ? (label + " (" + count + ")") : label;
    }
    var isBtn = hero.classList.contains("btn");
    hero.classList.toggle("hero-status-alert", !!alert && !isBtn);
    hero.classList.toggle("btn-notams-alert", !!alert && isBtn);
    hero.classList.toggle("btn-ghost", isBtn && !alert);
  }

  function setFuelBanners(notams) {
    var banners = document.querySelectorAll("[data-notams=fuel-banner]");
    var fuel = [];
    notams.forEach(function (n) {
      if (n._meta && n._meta.fuelOut) fuel.push(n);
    });
    banners.forEach(function (el) {
      if (!fuel.length) {
        el.hidden = true;
        el.textContent = "";
        return;
      }
      var parts = fuel.map(function (n) {
        var kind = n._meta.fuelKind || (ES ? "El combustible" : "Fuel");
        var num = n.number ? "FAA NOTAM " + n.number : (ES ? "un NOTAM de la FAA" : "an FAA NOTAM");
        return ES ? (kind + " no está disponible, según " + num) : (kind + " currently unavailable per " + num);
      });
      el.textContent = unique(parts).join("; ") + (ES ? " — llame antes de llegar" : " — call ahead");
      el.hidden = false;
    });
  }

  function unique(arr) {
    return arr.filter(function (v, i) { return arr.indexOf(v) === i; });
  }

  function tidy(text) {
    var s = String(text || "").replace(/\s+/g, " ").trim();
    if (!s) return tr("See official FAA text for details.");
    s = s.replace(/^![A-Z0-9]{3}\s+\d{2}\/\d{3}\s+/i, "");
    var map = [
      [/\bCLSD\b/g, "closed"],
      [/\bAVBL\b/g, "available"],
      [/\bNOT AVBL\b/g, "not available"],
      [/\bWIP\b/g, "work in progress"],
      [/\bU\/S\b/g, "unserviceable"],
      [/\bAPN\b/g, "apron"],
      [/\bRWY\b/g, "runway"],
      [/\bTWY\b/g, "taxiway"],
      [/\bAD\b/g, "aerodrome"],
      [/\bAP\b/g, "airport"],
      [/\bLGT\b/g, "light"],
      [/\bOBST\b/g, "obstacle"],
      [/\bUAS\b/g, "unmanned aircraft"],
    ];
    map.forEach(function (pair) { s = s.replace(pair[0], pair[1]); });
    if (s.length > 140) s = s.slice(0, 137).replace(/\s+\S*$/, "") + "…";
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  function classify(n) {
    var raw = ((n.text || "") + " " + (n.number || "") + " " + (n.featureName || "")).toUpperCase();
    var tags = [];
    var high = false;
    var fuelOut = false;
    var fuelKind = "";
    var impact = 90;
    var summary = "";

    function tag(name) {
      if (tags.indexOf(name) === -1) tags.push(name);
    }

    if (/(?:100LL|JET\s*A|AVGAS|FUEL).{0,60}NOT\s+AVBL|(?:100LL|JET\s*A|AVGAS|FUEL).{0,60}NOT\s+AVAILABLE|FUEL\s+NOT\s+AVBL|FUEL\s+NOT\s+AVAILABLE/.test(raw)) {
      tag("Fuel");
      high = true;
      fuelOut = true;
      impact = Math.min(impact, 10);
      fuelKind = /100LL/.test(raw) ? "100LL" : /JET\s*A/.test(raw) ? "Jet A" : /AVGAS/.test(raw) ? "Avgas" : "Fuel";
      summary = fuelKind + " is currently unavailable";
    }

    if (/\b(?:RWY|RUNWAY)\b/.test(raw) && /\b(?:CLSD|CLOSED)\b/.test(raw)) {
      tag("Runway");
      tag("Closed");
      high = true;
      impact = Math.min(impact, 20);
      var rwy = raw.match(/\b(?:RWY|RUNWAY)\s*(\d{1,2}\s*\/\s*\d{1,2}|\d{1,2}[LCR]?)/);
      summary = summary || (rwy ? "Runway " + rwy[1].replace(/\s+/g, "") + " is closed" : "A runway is closed");
    }

    if (/\b(?:TWY|TAXIWAY)\b/.test(raw) && /\b(?:CLSD|CLOSED)\b/.test(raw)) {
      tag("Taxiway");
      tag("Closed");
      high = true;
      impact = Math.min(impact, 30);
      var twy = raw.match(/\b(?:TWY|TAXIWAY)\s*([A-Z0-9]{1,3})/);
      summary = summary || (twy ? "Taxiway " + twy[1] + " is closed" : "A taxiway is closed");
    }

    if (/\b(?:APRON|APN)\b/.test(raw) && /\b(?:CLSD|CLOSED)\b/.test(raw)) {
      tag("Apron");
      tag("Closed");
      high = true;
      impact = Math.min(impact, 40);
      summary = summary || (/CARGO/.test(raw) ? "The cargo apron is closed" : "An apron is closed");
    }

    if (/\bWIP\b|\bCONSTRUCTION\b|WORK IN PROGRESS/.test(raw)) {
      tag("Construction");
      if (/\b(?:APRON|APN)\b/.test(raw)) tag("Apron");
      if (/\b(?:RWY|RUNWAY)\b/.test(raw)) tag("Runway");
      if (/\b(?:TWY|TAXIWAY)\b/.test(raw)) tag("Taxiway");
      if (/\b(?:APRON|APN|RWY|RUNWAY|TWY|TAXIWAY)\b/.test(raw)) {
        high = true;
        impact = Math.min(impact, 45);
      }
      if (!summary) {
        if (/CARGO/.test(raw) && /APRON|APN/.test(raw)) summary = "Construction work on the cargo apron";
        else if (/APRON|APN/.test(raw)) summary = "Construction work on the apron";
        else if (/RWY|RUNWAY/.test(raw)) summary = "Construction work on the runway";
        else if (/TWY|TAXIWAY/.test(raw)) summary = "Construction work on a taxiway";
        else summary = "Construction work on the field";
      }
    }

    if (/\bOBST(?:ACLE)?\b|\bCRANE\b/.test(raw)) {
      tag("Obstacle");
      impact = Math.min(impact, 60);
      if (!summary) {
        summary = /LGT|LIGHT|U\/S|UNSERVICEABLE/.test(raw)
          ? "Obstacle lighting is out of service"
          : "An obstacle is reported near the airport";
      }
    }

    if (/\b(?:LGT|LGTS|LIGHT|LIGHTS)\b/.test(raw) && /\b(?:U\/S|UNSERVICEABLE|OUT OF SERVICE)\b/.test(raw)) {
      tag("Lighting");
      impact = Math.min(impact, 65);
      if (!summary) {
        if (/TOWER|TWR/.test(raw)) summary = "Tower lighting is out of service";
        else if (/RWY|RUNWAY/.test(raw)) summary = "Runway lighting is out of service";
        else summary = "A light is out of service";
      }
    }

    if (/\bAIRSPACE\b|\bTFR\b|\bLTA\b|\bUAS\b|\bUAV\b|\bPARACHUTE\b|\bPJE\b/.test(raw) || /^LTA-/.test(n.number || "")) {
      tag("Airspace");
      impact = Math.min(impact, 70);
      if (!summary) {
        if (/PARACHUTE|PJE/.test(raw)) summary = "Extensive parachute activity near the airport";
        else if (/UAS|UAV/.test(raw)) summary = "Unmanned aircraft activity in the area";
        else if (/\bTFR\b/.test(raw)) summary = "Temporary flight restriction in effect";
        else summary = "A local airspace advisory is in effect";
      }
    }

    if (!summary) summary = tidy(n.text);
    if (!tags.length) tag("Notice");
    var outTags = tags.map(function (tg) { return TAGS[tg] || tg; });
    return { tags: outTags, high: high, fuelOut: fuelOut, fuelKind: fuelKind, impact: impact, summary: tr(summary) };
  }

  function endDate(n) {
    if (n.permanent) return { perm: true };
    if (n.endAt) {
      var d = new Date(n.endAt);
      if (!isNaN(d.getTime())) return { date: d };
    }
    return null;
  }

  function expiresLabel(n) {
    var end = endDate(n);
    if (end && end.perm) return ES ? "Permanente" : "Permanent";
    if (!end || !end.date) return "";
    var ms = end.date.getTime() - Date.now();
    if (ms <= 0) return ES ? "Vencido" : "Expired";
    var mins = Math.round(ms / 60000);
    if (mins < 60) return ES ? ("Vence en " + mins + (mins === 1 ? " minuto" : " minutos")) : ("Expires in " + mins + " minute" + (mins === 1 ? "" : "s"));
    var hours = Math.round(ms / 3600000);
    if (hours < 24) return ES ? ("Vence en " + hours + (hours === 1 ? " hora" : " horas")) : ("Expires in " + hours + " hour" + (hours === 1 ? "" : "s"));
    var days = Math.round(ms / 86400000);
    return ES ? ("Vence en " + days + (days === 1 ? " día" : " días")) : ("Expires in " + days + " day" + (days === 1 ? "" : "s"));
  }

  function formatAzIso(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    if (isNaN(d.getTime())) return "";
    var fmt = new Intl.DateTimeFormat(ES ? "es-MX" : "en-US", {
      timeZone: "America/Phoenix",
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
    return fmt.format(d).replace(/,/g, "") + (ES ? " hora AZ" : " AZ time");
  }

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null && text !== "") node.textContent = text;
    return node;
  }

  function renderItem(n) {
    var li = el("li", "notam" + (n._meta.high ? " notam-high" : " notam-low"));
    if (!n._meta.high) li.hidden = true;

    var top = el("div", "notam-top");
    var id = el("div", "notam-id", n.number || "NOTAM");
    var chips = el("div", "notam-chips");
    n._meta.tags.forEach(function (t) {
      var slug = t.toLowerCase().replace(/[^a-z0-9]+/g, "-");
      chips.appendChild(el("span", "notam-chip notam-chip-" + slug, t));
    });
    top.appendChild(id);
    top.appendChild(chips);
    li.appendChild(top);

    li.appendChild(el("p", "notam-summary", n._meta.summary));

    var times = el("div", "notam-times");
    var start = n.effectiveStart || (ES ? "Inicio desconocido" : "Unknown start");
    var end = n.effectiveEnd || (ES ? "Fin desconocido" : "Unknown end");
    var exp = expiresLabel(n);
    times.textContent = (ES ? "Vigente " : "Effective ") + start + " – " + end + (exp ? " · " + exp : "");
    li.appendChild(times);

    if (n.text) {
      var details = el("details", "notam-raw");
      details.appendChild(el("summary", "", ES ? "Texto oficial de la FAA" : "Raw FAA text"));
      details.appendChild(el("p", "notam-text", n.text));
      li.appendChild(details);
    }
    return li;
  }

  function sortNotams(items) {
    return items.slice().sort(function (a, b) {
      if (a._meta.impact !== b._meta.impact) return a._meta.impact - b._meta.impact;
      var ae = endDate(a), be = endDate(b);
      var at = ae && ae.date ? ae.date.getTime() : Infinity;
      var bt = be && be.date ? be.date.getTime() : Infinity;
      if (at !== bt) return at - bt;
      return String(a.number || "").localeCompare(String(b.number || ""));
    });
  }

  fetch(endpoint, { headers: { Accept: "application/json" } })
    .then(function (res) {
      if (!res.ok) throw new Error("bad status");
      return res.json();
    })
    .then(function (data) {
      if (!data || data.ok !== true || !Array.isArray(data.notams)) throw new Error("bad payload");
      var items = data.notams.map(function (n) {
        n._meta = classify(n);
        return n;
      });
      items = sortNotams(items);

      var highImpact = items.some(function (n) { return n._meta.high; });
      setHero(heroCopy(items.length), highImpact);
      setFuelBanners(items);

      if (updatedEl) {
        var when = formatAzIso(data.fetchedAt);
        if (when) {
          updatedEl.textContent = (ES ? "Actualizado " : "Updated ") + when;
          updatedEl.hidden = false;
        }
      }

      if (!root || !listEl || !statusEl) return;

      if (!items.length) {
        fallback(ES ? "No se encontraron NOTAM activos." : "No active NOTAMs found.");
        setHero(heroCopy(0), false);
        return;
      }

      var highCount = items.filter(function (n) { return n._meta.high; }).length;
      var lowCount = items.length - highCount;
      statusEl.textContent =
        ES ? (items.length === 1 ? "1 NOTAM activo para KOLS." : items.length + " NOTAM activos para KOLS.") : (items.length === 1 ? "1 active NOTAM for KOLS." : items.length + " active NOTAMs for KOLS.");

      var frag = document.createDocumentFragment();
      items.forEach(function (n) { frag.appendChild(renderItem(n)); });
      listEl.replaceChildren(frag);

      if (moreWrap && toggleBtn && lowCount > 0) {
        moreWrap.hidden = false;
        var expanded = false;
        function syncToggle() {
          listEl.querySelectorAll(".notam-low").forEach(function (li) { li.hidden = !expanded; });
          toggleBtn.setAttribute("aria-expanded", expanded ? "true" : "false");
          toggleBtn.textContent = expanded
            ? (ES ? "Ver solo los destacados" : "Show only highlights")
            : (ES ? ("Ver los " + items.length + " NOTAM") : ("Show all " + items.length + " NOTAMs"));
        }
        toggleBtn.onclick = function () {
          expanded = !expanded;
          syncToggle();
        };
        syncToggle();
      } else if (moreWrap) {
        moreWrap.hidden = true;
      }
    })
    .catch(function () {
      fallback(ES ? "No se pudieron cargar los NOTAM en vivo. Use el enlace oficial de la FAA abajo." : "Live NOTAMs couldn’t be loaded. Use the official FAA link below.");
    });
})();

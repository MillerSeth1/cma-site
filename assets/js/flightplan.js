/* Copper Mountain Air — "Plan your flight to KOLS" deep links.
   ForeFlight: official URL scheme, https://foreflight.com/support/app-urls/
   SkyVector: https://skyvector.com/?fpl= and the KOLS airport page.
   Garmin Pilot: community-documented scheme (not officially published by Garmin). */
(function(){
  "use strict";
  var ES = document.documentElement.lang === "es";
  var DEST = "KOLS";
  var BAD_ID = ES
    ? "Ingrese un identificador de aeropuerto de 3 o 4 caracteres, como KTUS."
    : "Enter a 3- or 4-character airport identifier, such as KTUS.";
  var form = document.getElementById("flightplan-form");
  var input = document.getElementById("dep-icao");
  var err = document.getElementById("flightplan-error");
  var ff = document.getElementById("fp-foreflight");
  var gp = document.getElementById("fp-garmin");
  var sv = document.getElementById("fp-skyvector");
  if(!form || !input || !ff || !gp || !sv) return;

  function normalize(raw){
    return String(raw || "").trim().toUpperCase().replace(/[^A-Z0-9]/g, "");
  }
  function isValid(id){
    return !id || /^[A-Z0-9]{3,4}$/.test(id);
  }
  function showError(msg){
    if(!err) return;
    if(msg){
      err.textContent = msg;
      err.hidden = false;
      input.setAttribute("aria-invalid", "true");
    }else{
      err.textContent = "";
      err.hidden = true;
      input.removeAttribute("aria-invalid");
    }
  }
  function departure(){
    var dep = normalize(input.value);
    if(!isValid(dep)) return null;
    if(dep === DEST || dep === "OLS") return "";
    return dep;
  }
  function linksFor(dep){
    if(!dep){
      return {
        foreflight: "foreflightmobile://maps/search?q=" + DEST,
        garmin: "garminpilot://airport?id=" + DEST,
        skyvector: "https://skyvector.com/airport/OLS/Nogales-International-Airport"
      };
    }
    return {
      foreflight: "foreflightmobile://maps/search?q=" + dep + "+" + DEST,
      garmin: "garminpilot://maps?route=" + dep + "." + DEST,
      skyvector: "https://skyvector.com/?fpl=" + encodeURIComponent(dep + " " + DEST)
    };
  }
  function updateHrefs(){
    var dep = departure();
    if(dep === null) return false;
    var L = linksFor(dep);
    ff.setAttribute("href", L.foreflight);
    gp.setAttribute("href", L.garmin);
    sv.setAttribute("href", L.skyvector);
    showError("");
    return true;
  }
  function guard(e){
    input.value = normalize(input.value);
    if(!updateHrefs()){
      e.preventDefault();
      showError(BAD_ID);
      input.focus();
    }
  }

  updateHrefs();
  input.addEventListener("input", function(){
    if(isValid(normalize(input.value))) updateHrefs();
  });
  input.addEventListener("change", function(){
    input.value = normalize(input.value);
    if(!updateHrefs() && normalize(input.value)){
      showError(BAD_ID);
    }
  });
  form.addEventListener("submit", function(e){
    e.preventDefault();
    input.value = normalize(input.value);
    if(updateHrefs()){
      window.open(sv.getAttribute("href"), "_blank", "noopener");
    }else if(normalize(input.value)){
      showError(BAD_ID);
      input.focus();
    }
  });
  [ff, gp, sv].forEach(function(a){ a.addEventListener("click", guard); });
})();

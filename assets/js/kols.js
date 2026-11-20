/* Copper Mountain Air — KOLS live conditions, wind/runway calculator, training map and pathway tabs.
   Weather: NWS API (api.weather.gov, CORS-enabled, no key). Charts: FAA AIS ArcGIS tile services.
   Situational awareness only. Not for navigation or flight planning. */
(function(){
  "use strict";
  var ELEV = 3955;            // ft MSL (surveyed, FAA)
  var VAR_E = 9;              // magnetic variation, 9°E (FAA)
  var RWYS = [{id:"04",mag:37},{id:"22",mag:217}];   // FAA runway magnetic headings
  var API = "https://api.weather.gov/stations/KOLS/observations?limit=12";
  var $ = function(s,r){return (r||document).querySelector(s)};
  var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  function set(sel,txt){$$(sel).forEach(function(e){e.textContent=txt;});}
  function round(n){return Math.round(n);}
  function pad3(n){n=((round(n)%360)+360)%360;if(n===0)n=360;return ("00"+n).slice(-3);}
  function fmtNum(n){return round(n).toLocaleString("en-US");}

  /* ---------- METAR parsing ---------- */
  function parseVis(tokens,i){
    // handles 10SM, P6SM, M1/4SM, 1/2SM, "1 1/2SM"
    var t=tokens[i], m;
    if(/^\d+$/.test(t) && tokens[i+1] && /^\d\/\dSM$/.test(tokens[i+1])){
      var f=tokens[i+1].replace("SM","").split("/");return {v:+t + f[0]/f[1], used:2};
    }
    if((m=t.match(/^([PM])?(\d+)?(?:\/(\d+))?SM$/))){
      var v = m[3] ? (+m[2]/+m[3]) : +m[2];
      return {v:v, used:1, plus:m[1]==="P", minus:m[1]==="M"};
    }
    return null;
  }
  function parseMetar(raw){
    var o={raw:raw,clouds:[]}, tk=raw.trim().split(/\s+/), i=0;
    var rmk=tk.indexOf("RMK"); if(rmk>-1) tk=tk.slice(0,rmk);
    for(i=0;i<tk.length;i++){
      var t=tk[i], m;
      if((m=t.match(/^(\d{3}|VRB)(\d{2,3})(?:G(\d{2,3}))?KT$/))){
        o.wdir = m[1]==="VRB" ? "VRB" : +m[1]; o.wspd=+m[2]; o.wgst=m[3]?+m[3]:null; continue;
      }
      if((m=t.match(/^(\d{3})V(\d{3})$/))){o.wvar=[+m[1],+m[2]];continue;}
      if(o.vis==null){var v=parseVis(tk,i); if(v){o.vis=v.v;o.visPlus=v.plus;o.visMinus=v.minus;i+=v.used-1;continue;}}
      if(t==="CAVOK"){o.vis=6;o.visPlus=true;o.clouds.push({amt:"CLR"});continue;}
      if((m=t.match(/^(FEW|SCT|BKN|OVC|VV)(\d{3}|\/\/\/)(CB|TCU)?$/))){o.clouds.push({amt:m[1],base:m[2]==="///"?null:+m[2]*100,type:m[3]||""});continue;}
      if(/^(CLR|SKC|NSC|NCD)$/.test(t)){o.clouds.push({amt:t});continue;}
      if((m=t.match(/^(M?\d{2})\/(M?\d{2})?$/))){o.temp=+m[1].replace("M","-");if(m[2])o.dew=+m[2].replace("M","-");continue;}
      if((m=t.match(/^A(\d{4})$/))){o.alt=+m[1]/100;continue;}
      if((m=t.match(/^Q(\d{4})$/))){o.alt=+m[1]/33.8639;continue;}
    }
    return o;
  }
  /* ---------- NWS structured fallback ---------- */
  function val(q){return q && q.value!=null ? q.value : null;}
  function fromProps(p){
    var o={clouds:[],raw:p.rawMessage||""};
    var wd=val(p.windDirection), ws=val(p.windSpeed), wg=val(p.windGust);
    if(ws!=null){o.wspd=ws/1.852; if(ws===0) o.wspd=0;}
    if(wd!=null) o.wdir=wd; else if(o.wspd>0) o.wdir="VRB";
    if(wg!=null) o.wgst=wg/1.852;
    var vis=val(p.visibility); if(vis!=null){o.vis=vis/1609.344; if(o.vis>=9.95){o.vis=10;}}
    (p.cloudLayers||[]).forEach(function(c){
      var b=c.base&&c.base.value!=null?c.base.value*3.28084:null;
      var a=c.amount; if(a==="CLR"||a==="SKC") o.clouds.push({amt:a}); else o.clouds.push({amt:a,base:b!=null?Math.round(b/100)*100:null});
    });
    var t=val(p.temperature), d=val(p.dewpoint); if(t!=null)o.temp=t; if(d!=null)o.dew=d;
    var bp=val(p.barometricPressure); if(bp!=null)o.alt=bp/3386.389;
    if(o.wspd!=null) o.wspd=Math.round(o.wspd); if(o.wgst!=null) o.wgst=Math.round(o.wgst);
    return o;
  }
  /* ---------- derived values ---------- */
  function ceiling(o){
    var c=null;o.clouds.forEach(function(l){if((l.amt==="BKN"||l.amt==="OVC"||l.amt==="VV")&&l.base!=null){if(c===null||l.base<c)c=l.base;}});
    return c;
  }
  function category(o){
    var c=ceiling(o), v=o.vis;
    if(v==null && c==null) return null;
    var cv = c==null ? Infinity : c, vv = v==null ? Infinity : v;
    if(cv<500 || vv<1) return "LIFR";
    if(cv<1000 || vv<3) return "IFR";
    if(cv<=3000 || vv<=5) return "MVFR";
    return "VFR";
  }
  function densityAlt(o){
    if(o.temp==null||o.alt==null) return null;
    var pa = ELEV + (29.92 - o.alt)*1000;
    var isa = 15 - 2*(pa/1000);
    return {pa:pa, da:pa + 120*(o.temp - isa), isa:isa};
  }
  function windComponents(o){
    if(o.wspd==null) return null;
    if(o.wspd===0) return {calm:true, best:"22"};
    if(o.wdir==="VRB") return {vrb:true, spd:o.wspd};
    var wm = o.wdir - VAR_E, res = RWYS.map(function(r){
      var a=(wm - r.mag)*Math.PI/180;
      var g=o.wgst||null;
      return {id:r.id, head:o.wspd*Math.cos(a), cross:o.wspd*Math.sin(a), gcross:g?g*Math.sin(a):null, ghead:g?g*Math.cos(a):null};
    });
    res.sort(function(a,b){return b.head-a.head;});
    return {rw:res, best:res[0].id, wm:wm};
  }
  function skyText(o){
    if(!o.clouds.length) return {main:"—",sub:"No sky report"};
    var first=o.clouds[0];
    if(/CLR|SKC|NSC|NCD/.test(first.amt)) return {main:"Clear",sub:first.amt==="CLR"?"No clouds below 12,000 ft (ASOS)":"Sky clear"};
    var names={FEW:"Few",SCT:"Scattered",BKN:"Broken",OVC:"Overcast",VV:"Vertical vis"};
    var c=ceiling(o);
    return {main: c!=null ? fmtNum(c)+" ft" : "No ceiling", sub:o.clouds.map(function(l){return (names[l.amt]||l.amt)+(l.base!=null?" "+fmtNum(l.base):"")+(l.type?" "+l.type:"");}).join(" · ")};
  }
  function cToF(c){return c*9/5+32;}
  function visText(o){if(o.vis==null)return "—";var v=o.vis;var s=v>=10?"10":(v%1? (v<1? (Math.round(v*4)/4).toString():v.toFixed(2).replace(/0$/,"")):String(v));return (o.visPlus?"6+":(o.visMinus?"<"+s:s));}
  function windText(o){
    if(o.wspd==null) return "—";
    if(o.wspd===0) return "Calm";
    return (o.wdir==="VRB"?"Variable":pad3(o.wdir)+"°")+" @ "+o.wspd+(o.wgst?" G"+o.wgst:"")+" kt";
  }
  var TZ_FMT = (function(){try{return new Intl.DateTimeFormat("en-US",{timeZone:"America/Phoenix",hour:"numeric",minute:"2-digit",month:"short",day:"numeric"});}catch(e){return null;}})();
  function zulu(d){return ("0"+d.getUTCDate()).slice(-2)+("0"+d.getUTCHours()).slice(-2)+("0"+d.getUTCMinutes()).slice(-2)+"Z";}
  function mst(d){return TZ_FMT?TZ_FMT.format(d)+" MST":d.toISOString();}
  function ago(d){var m=Math.round((Date.now()-d.getTime())/60000);return m<1?"just now":(m<60?m+" min ago":Math.floor(m/60)+" h "+(m%60)+" min ago");}

  /* ---------- rendering ---------- */
  var CATS={VFR:"VFR",MVFR:"MVFR",IFR:"IFR",LIFR:"LIFR"};
  function render(o, when, sample){
    var cat=category(o), wc=windComponents(o), da=densityAlt(o), sky=skyText(o);
    document.documentElement.setAttribute("data-wx-cat", cat||"");
    $$("[data-cat]").forEach(function(e){e.classList.toggle("on", e.getAttribute("data-cat")===cat);});
    set("[data-wx=cat]", cat||"—");
    set("[data-wx=wind]", windText(o));
    set("[data-wx=wind-sub]", o.wspd===0?"Rwy 22 is the calm-wind runway": (o.wdir==="VRB"?"Direction variable":(o.wvar?"Varying "+pad3(o.wvar[0])+"°–"+pad3(o.wvar[1])+"° · ":"")+"True; ≈"+pad3(o.wdir-VAR_E)+"° magnetic"));
    set("[data-wx=vis]", visText(o));
    set("[data-wx=sky]", sky.main); set("[data-wx=sky-sub]", sky.sub);
    set("[data-wx=temp]", o.temp!=null? o.temp.toFixed(0)+"°C / "+cToF(o.temp).toFixed(0)+"°F":"—");
    set("[data-wx=dew]", o.dew!=null? "Dewpoint "+o.dew.toFixed(0)+"°C / "+cToF(o.dew).toFixed(0)+"°F · spread "+(o.temp!=null?Math.round(o.temp-o.dew)+"°C":"—"):"Dewpoint —");
    set("[data-wx=alt]", o.alt!=null? o.alt.toFixed(2):"—");
    set("[data-wx=alt-sub]", o.alt!=null? "inHg · "+(o.alt*33.8639).toFixed(0)+" hPa":"inHg");
    set("[data-wx=da]", da? fmtNum(Math.round(da.da/10)*10)+" ft":"—");
    set("[data-wx=da-sub]", da? "Pressure alt "+fmtNum(Math.round(da.pa/10)*10)+" ft · "+(da.da-ELEV>=0?"+":"")+fmtNum(Math.round((da.da-ELEV)/10)*10)+" ft vs. field":"Needs temperature and altimeter");
    set("[data-wx=time]", when? zulu(when)+" · "+mst(when):"—");
    set("[data-wx=ago]", when? ago(when):"");
    set("[data-wx=metar]", o.raw || "Raw METAR not included in the latest feed. Values below are from the ASOS observation.");
    set("[data-wx=sample]", sample||"");
    // hero pill
    set("[data-wx=pill]", "KOLS · "+(cat||"—")+" · Wind "+(o.wspd===0?"calm":(o.wdir==="VRB"?"VRB":pad3(o.wdir)+"°")+" @ "+o.wspd+(o.wgst?"G"+o.wgst:"")+" kt")+(o.temp!=null?" · "+o.temp.toFixed(0)+"°C":""));
    // runway
    if(wc){
      if(wc.calm){set("[data-wx=rwy]","Rwy 22");set("[data-wx=head]","0 kt");set("[data-wx=cross]","0 kt");set("[data-wx=rwy-sub]","Calm wind · Rwy 22 is the designated calm-wind runway");}
      else if(wc.vrb){set("[data-wx=rwy]","Either");set("[data-wx=head]","Varies");set("[data-wx=cross]","Up to "+wc.spd+" kt");set("[data-wx=rwy-sub]","Variable wind direction");}
      else{
        var b=wc.rw[0], hw=Math.round(b.head), xw=Math.round(Math.abs(b.cross));
        set("[data-wx=rwy]","Rwy "+b.id);
        set("[data-wx=head]",(hw>=0?hw+" kt head":Math.abs(hw)+" kt tail"));
        set("[data-wx=cross]",xw+" kt "+(b.cross>=0?"from right":"from left")+(b.gcross!=null?" · G"+Math.round(Math.abs(b.gcross)):""));
        set("[data-wx=rwy-sub]","Rwy "+wc.rw[1].id+": "+(Math.round(wc.rw[1].head)>=0?Math.round(wc.rw[1].head)+" kt head":Math.abs(Math.round(wc.rw[1].head))+" kt tail")+", "+Math.round(Math.abs(wc.rw[1].cross))+" kt cross");
      }
    }
    drawRose(o, wc);
  }
  function drawRose(o, wc){
    var arrow=$("#wind-arrow"), lbl=$("#wind-label"); if(!arrow) return;
    if(o.wspd==null||o.wspd===0||o.wdir==="VRB"){arrow.setAttribute("opacity","0"); if(lbl) lbl.textContent=o.wspd===0?"CALM":(o.wdir==="VRB"?"VRB "+o.wspd+" KT":""); return;}
    arrow.setAttribute("opacity","1");
    // Rose is drawn to magnetic north; wind FROM direction, arrow points downwind toward center.
    arrow.setAttribute("transform","rotate("+(o.wdir-VAR_E)+" 160 160)");
    if(lbl) lbl.textContent=pad3(o.wdir-VAR_E)+"° M · "+o.wspd+(o.wgst?"G"+o.wgst:"")+" KT";
    $$(".rwy-end").forEach(function(e){e.classList.toggle("fav", wc && !wc.vrb && e.getAttribute("data-rwy")===wc.best);});
  }
  var last=null;
  var IEM = "https://mesonet.agron.iastate.edu/api/1/currents.json?station=OLS&network=AZ_ASOS";
  function getJSON(u){return fetch(u,{cache:"no-store"}).then(function(r){if(!r.ok)throw new Error("HTTP "+r.status);return r.json();});}
  function settle(pr){return pr.then(function(v){return {ok:true,v:v};},function(e){return {ok:false,e:e};});}
  function load(manual){
    if(!$("[data-wx]")) return;
    document.documentElement.classList.add("wx-loading");
    set("[data-wx=status]", manual?"Refreshing…":"Loading live KOLS data…");
    // Two CORS-enabled public feeds of the same FAA ASOS: NWS API (official) and Iowa Environmental Mesonet (often posts the METAR sooner).
    Promise.all([settle(getJSON(API)), settle(getJSON(IEM))]).then(function(rs){
      var f = rs[0].ok ? (rs[0].v.features||[]).map(function(x){return x.properties;}) : [];
      var cands = [];
      for(var i=0;i<f.length;i++){ if(f[i].rawMessage){ cands.push({raw:f[i].rawMessage, t:new Date(f[i].timestamp), src:"NWS"}); break; } }
      if(rs[1].ok && rs[1].v.data && rs[1].v.data[0] && rs[1].v.data[0].raw){ var d=rs[1].v.data[0]; cands.push({raw:d.raw, t:new Date(d.utc_valid), src:"IEM"}); }
      cands.sort(function(a,b){return b.t-a.t;});
      var latest = f[0] || null, tL = latest ? new Date(latest.timestamp) : null;
      var o, when, sample="", src;
      if(cands.length && (!tL || (tL - cands[0].t) < 90*60000)){
        o = parseMetar(cands[0].raw.replace(/^(METAR|SPECI)\s+/,"")); when = cands[0].t; src = cands[0].src;
        if(tL && tL > when){ var s=fromProps(latest); if(s.wspd!=null) sample="Newer ASOS 5-minute sample at "+mst(tL)+": wind "+windText(s)+(s.temp!=null?", "+s.temp.toFixed(0)+"°C":"")+"."; }
      } else if(latest){ o = fromProps(latest); when = tL; src = "NWS"; }
      else throw new Error("No observations");
      last=o; render(o, when, sample);
      document.documentElement.classList.remove("wx-loading","wx-error");
      set("[data-wx=status]","Live · FAA ASOS"); set("[data-wx=src]","via "+(src==="IEM"?"Iowa Environmental Mesonet":"National Weather Service"));
    }).catch(function(e){
      document.documentElement.classList.remove("wx-loading");document.documentElement.classList.add("wx-error");
      set("[data-wx=status]","Live data unavailable right now");
      set("[data-wx=pill]","KOLS · ASOS 121.125 · 520-287-9332");
      set("[data-wx=metar]","Couldn't reach the live weather feed (network or content blocker). Use the AviationWeather.gov link or call the ASOS at 520-287-9332.");
    });
  }
  function initWx(){
    if(!$("[data-wx]")) return;
    load(false); setInterval(function(){load(false);}, 5*60000);
    var rb=$("#wx-refresh"); if(rb) rb.addEventListener("click",function(){load(true);});
    var cb=$("#wx-copy"); if(cb) cb.addEventListener("click",function(){
      var t=last&&last.raw; if(!t) return;
      var done=function(){cb.textContent="Copied";setTimeout(function(){cb.textContent="Copy METAR";},1600);};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,function(){});}
    });
  }

  /* ---------- map ---------- */
  function initMap(){
    var el=$("#kols-map"); if(!el||!window.L) return;
    var data=JSON.parse($("#xc-data").textContent);
    var K=data.kols, L=window.L;
    var FAA="https://tiles.arcgis.com/tiles/ssFJjBXIUyZDrSYZ/arcgis/rest/services/";
    var faaAttr='Charts: <a href="https://www.faa.gov/air_traffic/flight_info/aeronav/" target="_blank" rel="noopener">FAA Aeronautical Information Services</a>';
    var base={
      "FAA VFR Sectional": L.tileLayer(FAA+"VFR_Sectional/MapServer/tile/{z}/{y}/{x}",{minNativeZoom:8,maxNativeZoom:12,minZoom:7,maxZoom:14,attribution:faaAttr}),
      "FAA IFR Enroute Low": L.tileLayer(FAA+"IFR_AreaLow/MapServer/tile/{z}/{y}/{x}",{minNativeZoom:7,maxNativeZoom:11,minZoom:7,maxZoom:14,attribution:faaAttr}),
      "Satellite": L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",{maxNativeZoom:18,maxZoom:14,minZoom:7,attribution:"Imagery © Esri, Maxar, Earthstar Geographics"}),
      "Terrain": L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",{subdomains:"abc",maxNativeZoom:17,maxZoom:14,minZoom:7,attribution:'© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors, SRTM · <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (CC-BY-SA)'})
    };
    var map=L.map(el,{minZoom:7,maxZoom:14,scrollWheelZoom:false,layers:[base["FAA VFR Sectional"]],zoomSnap:0.5});
    map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    var rings=L.layerGroup(), routes=L.layerGroup(), pins=L.layerGroup();
    [25,50].forEach(function(nm){
      L.circle([K.lat,K.lon],{radius:nm*1852,color:"#c4703d",weight:2,dashArray:"8 6",fill:false,interactive:false}).addTo(rings);
      L.marker([K.lat+nm/60,K.lon],{icon:L.divIcon({className:"ring-label",html:nm+" NM",iconSize:[56,20],iconAnchor:[28,10]}),interactive:false}).addTo(rings);
    });
    var kIcon=L.divIcon({className:"apt-pin home",html:'<span class="dot"></span><span class="lbl">KOLS</span>',iconSize:[18,18],iconAnchor:[9,9]});
    L.marker([K.lat,K.lon],{icon:kIcon,zIndexOffset:1000}).addTo(pins).bindPopup('<strong>KOLS · Nogales International</strong><br>Elev '+K.elev+' ft · Rwy 04/22 7,200 × 100 ft<br>CTAF/UNICOM 122.8 · ASOS 121.125<br>Home of Copper Mountain Air flight training');
    var byId={};
    data.dest.forEach(function(d){
      var ic=L.divIcon({className:"apt-pin "+(d.towered?"twr":"ntwr"),html:'<span class="dot"></span><span class="lbl">'+d.id+'</span>',iconSize:[14,14],iconAnchor:[7,7]});
      var pop='<strong>'+d.id+' · '+d.name+'</strong><br>'+d.dist+' NM from KOLS · '+d.tc+'° true / '+d.mc+'° mag<br>'+d.airspace+'<br><em>'+d.why+'</em>';
      var m=L.marker([d.lat,d.lon],{icon:ic}).addTo(pins).bindPopup(pop);
      L.polyline([[K.lat,K.lon],[d.lat,d.lon]],{color:"#0a141b",weight:2,opacity:.55,dashArray:"2 6",interactive:false}).addTo(routes);
      byId[d.id]=m;
    });
    rings.addTo(map); routes.addTo(map); pins.addTo(map);
    L.control.layers(base,{"25 / 50 NM range rings":rings,"Cross-country routes":routes,"Airports":pins},{collapsed:window.innerWidth<760,position:"topright"}).addTo(map);
    L.control.scale({imperial:true,metric:false,position:"bottomleft"}).addTo(map);
    map.fitBounds(L.latLngBounds(data.dest.map(function(d){return [d.lat,d.lon];}).concat([[K.lat-0.08,K.lon]])),{padding:[24,24]});
    $$("[data-goto]").forEach(function(b){b.addEventListener("click",function(){
      var id=b.getAttribute("data-goto");
      if(id==="KOLS"){map.flyTo([K.lat,K.lon],10);return;}
      var m=byId[id]; if(!m) return;
      map.flyToBounds(L.latLngBounds([[K.lat,K.lon],m.getLatLng()]),{padding:[60,60],maxZoom:10});
      setTimeout(function(){m.openPopup();},700);
      $$("[data-goto]").forEach(function(x){x.classList.toggle("on",x===b);});
    });});
    el.addEventListener("click",function(){map.scrollWheelZoom.enable();});
    el.addEventListener("mouseleave",function(){map.scrollWheelZoom.disable();});
    window.__kolsMap=map;
  }

  /* ---------- pathway tabs ---------- */
  function initTabs(){
    var tabs=$$("[role=tab]"); if(!tabs.length) return;
    function show(t){
      tabs.forEach(function(x){var on=x===t;x.setAttribute("aria-selected",on?"true":"false");x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute("aria-controls"));if(p)p.hidden=!on;});
    }
    tabs.forEach(function(t,i){
      t.addEventListener("click",function(){show(t);});
      t.addEventListener("keydown",function(e){var k=e.key,n=null;if(k==="ArrowRight"||k==="ArrowDown")n=tabs[(i+1)%tabs.length];if(k==="ArrowLeft"||k==="ArrowUp")n=tabs[(i-1+tabs.length)%tabs.length];if(n){e.preventDefault();show(n);n.focus();}});
    });
  }
  window.__kolsParse={metar:parseMetar,category:category,wind:windComponents,da:densityAlt};
  function boot(){initWx();initMap();initTabs();}
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",boot); else boot();
})();

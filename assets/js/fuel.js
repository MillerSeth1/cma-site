(function(){
  var ES = document.documentElement.lang === "es";
  var locale = ES ? "es-MX" : "en-US";
  var T = ES ? {
    call: "Llame para el precio actual",
    callBadge: "Llame para el precio actual · (520) 287-9120",
    callCard: "Llame al (520) 287-9120 para el precio actual.",
    service: "Servicio completo",
    perGal: " / gal",
    updated: "Actualizado {t} según AirNav",
    posted: "Según lo publicado en AirNav",
    guaranteed: "Precio garantizado por AirNav",
    checked: "Consultado {t}",
    az: "hora de AZ",
    badgeOk: "100LL {a}  ·  Jet A {j}  / gal",
    cardOk: "100LL {a} y Jet A {j} por galón, servicio completo."
  } : {
    call: "Call for current price",
    callBadge: "Call for current price · (520) 287-9120",
    callCard: "Call for current price at (520) 287-9120.",
    service: "Full service",
    perGal: " / gal",
    updated: "Updated {t} as reported by AirNav",
    posted: "As posted on AirNav",
    guaranteed: "AirNav guaranteed",
    checked: "Checked {t}",
    az: "AZ time",
    badgeOk: "100LL {a}  ·  Jet A {j}  / gal",
    cardOk: "100LL {a} and Jet A {j} per gallon, full service."
  };

  function roots(){
    var nodes=document.querySelectorAll("[data-fuel][data-endpoint], [data-endpoint][data-fuel], [data-fuel-endpoint]");
    var list=[];
    var seen=new Set();
    document.querySelectorAll("[data-endpoint]").forEach(function(el){
      if(!el.getAttribute("data-fuel") && el.getAttribute("data-fuel")!=="") return;
    });
    document.querySelectorAll("[data-fuel]").forEach(function(el){
      var ep=el.getAttribute("data-endpoint")||el.getAttribute("data-fuel-endpoint");
      if(!ep) return;
      if(seen.has(ep+"@"+el.getAttribute("data-fuel"))) return;
      seen.add(ep+"@"+el.getAttribute("data-fuel"));
      list.push(el);
    });
    return list;
  }
  function find(product, rows){
    if(!rows) return null;
    for(var i=0;i<rows.length;i++){
      if((rows[i].product||"").toLowerCase().indexOf(product)>-1) return rows[i];
    }
    return null;
  }
  function money(row){
    if(!row) return T.call;
    return row.display||T.call;
  }
  function service(row){
    var s = row && row.service ? row.service : T.service;
    if(ES && /^full\s*service$/i.test(s)) return T.service;
    return s;
  }
  function formatChecked(iso){
    if(!iso) return "";
    var d=new Date(iso);
    if(isNaN(d.getTime())) return "";
    try{
      var fmt=new Intl.DateTimeFormat(locale,{timeZone:"America/Phoenix",month:"short",day:"numeric",year:"numeric",hour:"numeric",minute:"2-digit",hour12:true});
      return fmt.format(d).replace(/,/g,"")+" "+T.az;
    }catch(e){return "";}
  }
  function updatedLine(data){
    var bits=[];
    if(data.reportedAtLabel||data.reportedAt){
      bits.push(T.updated.replace("{t}", data.reportedAtLabel||data.reportedAt));
    }else{
      bits.push(T.posted);
    }
    if(data.guaranteed) bits.push(T.guaranteed);
    var checked=formatChecked(data.fetchedAt);
    if(checked) bits.push(T.checked.replace("{t}", checked));
    return bits.join(" · ");
  }
  function formatBadgeTime(iso){
    if(!iso) return "";
    var d=new Date(iso);
    if(isNaN(d.getTime())) return "";
    try{
      var fmt=new Intl.DateTimeFormat(locale,{timeZone:"America/Phoenix",month:"short",day:"numeric",hour:"numeric",minute:"2-digit",hour12:true});
      return fmt.format(d)+" "+T.az;
    }catch(e){return "";}
  }
  function badgeUpdated(data){
    if(data.reportedAtLabel||data.reportedAt){
      return (ES ? "Actualizado " : "Updated ")+(data.reportedAtLabel||data.reportedAt);
    }
    var checked=formatBadgeTime(data.fetchedAt);
    if(checked) return T.checked.replace("{t}", checked);
    return "";
  }
  function fill(data){
    var avgas=find("100ll", data.prices);
    var jeta=find("jet", data.prices);
    document.querySelectorAll("[data-fuel='jeta-price']").forEach(function(el){el.textContent=money(jeta)+T.perGal;});
    document.querySelectorAll("[data-fuel='100ll-price']").forEach(function(el){el.textContent=money(avgas)+T.perGal;});
    document.querySelectorAll("[data-fuel='jeta-service']").forEach(function(el){el.textContent=service(jeta);});
    document.querySelectorAll("[data-fuel='100ll-service']").forEach(function(el){el.textContent=service(avgas);});
    document.querySelectorAll("[data-fuel='updated']").forEach(function(el){
      el.textContent=updatedLine(data);
      el.hidden=false;
    });
    var missing=(!avgas||!avgas.usd)&&(!jeta||!jeta.usd);
    document.querySelectorAll("[data-fuel='badge-100ll']").forEach(function(el){el.textContent=money(avgas);});
    document.querySelectorAll("[data-fuel='badge-jeta']").forEach(function(el){el.textContent=money(jeta);});
    document.querySelectorAll("[data-fuel='badge-text']").forEach(function(el){
      var a=money(avgas), j=money(jeta);
      if(missing){
        el.textContent=T.callBadge;
        el.hidden=false;
      }else{
        el.textContent=T.badgeOk.replace("{a}",a).replace("{j}",j);
        el.hidden=!!el.closest(".hero-status-card");
      }
    });
    document.querySelectorAll(".hero-status-prices").forEach(function(el){el.hidden=missing;});
    document.querySelectorAll("[data-fuel='badge-updated']").forEach(function(el){
      var line=missing?"":badgeUpdated(data);
      el.textContent=line;
      el.hidden=!line;
    });
    document.querySelectorAll("[data-fuel='card']").forEach(function(el){
      var a=money(avgas), j=money(jeta);
      if((!avgas||!avgas.usd)&&(!jeta||!jeta.usd)){
        el.textContent=T.callCard;
      }else{
        el.textContent=T.cardOk.replace("{a}",a).replace("{j}",j);
      }
    });
  }
  function fail(){
    fill({prices:[], fetchedAt:null, guaranteed:false});
  }
  var endpoints=new Set();
  roots().forEach(function(el){
    var ep=el.getAttribute("data-endpoint")||el.getAttribute("data-fuel-endpoint");
    if(ep) endpoints.add(ep);
  });
  // Also pick up pages that only have child data-fuel hooks and one endpoint on a parent.
  document.querySelectorAll("[data-endpoint]").forEach(function(el){
    if(el.hasAttribute("data-fuel")||el.querySelector("[data-fuel]")){
      var ep=el.getAttribute("data-endpoint");
      if(ep) endpoints.add(ep);
    }
  });
  if(!endpoints.size) return;
  endpoints.forEach(function(endpoint){
    fetch(endpoint,{headers:{Accept:"application/json"}}).then(function(res){
      return res.json();
    }).then(function(data){
      if(data&&data.prices) fill(data);
      else fail();
    }).catch(fail);
  });
})();

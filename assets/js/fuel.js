(function(){
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
    if(!row) return "Call for current price";
    return row.display||"Call for current price";
  }
  function service(row){
    return row && row.service ? row.service : "Full service";
  }
  function formatChecked(iso){
    if(!iso) return "";
    var d=new Date(iso);
    if(isNaN(d.getTime())) return "";
    try{
      var fmt=new Intl.DateTimeFormat("en-US",{timeZone:"America/Phoenix",month:"short",day:"numeric",year:"numeric",hour:"numeric",minute:"2-digit",hour12:true});
      return fmt.format(d).replace(/,/g,"")+" AZ time";
    }catch(e){return "";}
  }
  function updatedLine(data){
    var bits=[];
    if(data.reportedAtLabel||data.reportedAt){
      bits.push("Updated "+(data.reportedAtLabel||data.reportedAt)+" as reported by AirNav");
    }else{
      bits.push("As posted on AirNav");
    }
    if(data.guaranteed) bits.push("AirNav guaranteed");
    var checked=formatChecked(data.fetchedAt);
    if(checked) bits.push("Checked "+checked);
    return bits.join(" · ");
  }
  function fill(data){
    var avgas=find("100ll", data.prices);
    var jeta=find("jet", data.prices);
    document.querySelectorAll("[data-fuel='jeta-price']").forEach(function(el){el.textContent=money(jeta)+" / gal";});
    document.querySelectorAll("[data-fuel='100ll-price']").forEach(function(el){el.textContent=money(avgas)+" / gal";});
    document.querySelectorAll("[data-fuel='jeta-service']").forEach(function(el){el.textContent=service(jeta);});
    document.querySelectorAll("[data-fuel='100ll-service']").forEach(function(el){el.textContent=service(avgas);});
    document.querySelectorAll("[data-fuel='updated']").forEach(function(el){
      el.textContent=updatedLine(data);
      el.hidden=false;
    });
    document.querySelectorAll("[data-fuel='badge-text']").forEach(function(el){
      var a=money(avgas), j=money(jeta);
      if((!avgas||!avgas.usd)&&(!jeta||!jeta.usd)){
        el.textContent="Call for current price · (520) 287-9120";
      }else{
        el.textContent="100LL "+a+"  ·  Jet A "+j+"  / gal";
      }
    });
    document.querySelectorAll("[data-fuel='card']").forEach(function(el){
      var a=money(avgas), j=money(jeta);
      if((!avgas||!avgas.usd)&&(!jeta||!jeta.usd)){
        el.textContent="Call for current price at (520) 287-9120.";
      }else{
        el.textContent="100LL "+a+" and Jet A "+j+" per gallon, full service.";
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

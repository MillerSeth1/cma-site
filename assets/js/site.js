(function(){
  var d=document.documentElement;d.classList.remove("no-js");d.classList.add("js");
  var ES = d.lang === "es";
  var I18N = ES ? {
    sendingBtn: "Enviando…",
    sending: "Enviando su mensaje…",
    sent: "Mensaje enviado. Nuestro equipo en KOLS le responderá en breve.",
    fail: "No pudimos enviar su mensaje en este momento. Por favor escriba a {to} o llame al (520) 287-9120.",
    cookieAria: "Aviso de cookies",
    cookieBody: "Usamos cookies para medir cómo se usa el sitio (Google Analytics). No usamos cookies de publicidad. <a href=\"{href}\">Privacidad</a>",
    accept: "Aceptar",
    decline: "Rechazar",
    analyticsOn: "La analítica está activada en este navegador.",
    analyticsOff: "La analítica está desactivada en este navegador.",
    tripSendingBtn: "Enviando…",
    tripSending: "Enviando su solicitud…",
    tripSent: "Solicitud enviada. Nuestro equipo en KOLS le responderá en breve.",
    tripFail: "No pudimos enviar su solicitud en este momento. Por favor escriba a {to} o llame al (520) 287-9120."
  } : {
    sendingBtn: "Sending…",
    sending: "Sending your message…",
    sent: "Message sent. Our team at KOLS will get back to you shortly.",
    fail: "Sorry, we couldn't send your message just now. Please email {to} or call (520) 287-9120 directly.",
    cookieAria: "Cookie notice",
    cookieBody: "We use cookies to measure how the site is used (Google Analytics). We do not use advertising cookies. <a href=\"{href}\">Privacy</a>",
    accept: "Accept",
    decline: "Decline",
    analyticsOn: "Analytics is on for this browser.",
    analyticsOff: "Analytics is off for this browser.",
    tripSendingBtn: "Sending…",
    tripSending: "Sending your request…",
    tripFail: "Sorry, we couldn't send your request just now. Please email {to} or call (520) 287-9120 directly.",
    tripSent: "Request sent. Our team at KOLS will get back to you shortly."
  };
  var t=document.querySelector(".nav-toggle"),n=document.getElementById("site-nav");
  if(t&&n){t.addEventListener("click",function(){var o=n.classList.toggle("open");t.setAttribute("aria-expanded",o?"true":"false");});
    document.addEventListener("keydown",function(e){if(e.key==="Escape"&&n.classList.contains("open")){n.classList.remove("open");t.setAttribute("aria-expanded","false");t.focus();}});}
  var els=document.querySelectorAll(".reveal");
  if(!("IntersectionObserver" in window)||window.matchMedia("(prefers-reduced-motion: reduce)").matches){els.forEach(function(e){e.classList.add("in")});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}})},{rootMargin:"0px 0px -8% 0px"});els.forEach(function(e){io.observe(e)});}
  // Contact form: posts to our contact relay, which emails operations@ via Resend.
  var f=document.getElementById("contact-form");
  if(f){
    var to=f.getAttribute("data-to")||"operations@coppermountainair.com",st=document.getElementById("form-status");
    var btn=document.getElementById("contact-submit")||f.querySelector('button[type="submit"]');
    var endpoint=f.getAttribute("data-endpoint");
    var q=new URLSearchParams(location.search).get("topic");
    if(q){var s=document.getElementById("topic");if(s){for(var i=0;i<s.options.length;i++){if(s.options[i].value===q){s.selectedIndex=i;}}}}
    function v(id){var el=document.getElementById(id);return el?(el.value||"").trim():"";}
    function setStatus(msg,kind){
      if(!st)return;
      st.textContent=msg;
      st.style.color=kind==="ok"?"#1f6b3a":kind==="err"?"#8a2a2a":"";
    }
    var fail=I18N.fail.replace("{to}",to);
    f.addEventListener("submit",function(e){
      e.preventDefault();if(!f.reportValidity())return;
      if(v("form-honey")){setStatus(I18N.sent,"ok");f.reset();return;}
      var orig=btn?btn.innerHTML:"";
      if(btn){btn.disabled=true;btn.innerHTML=I18N.sendingBtn;}
      setStatus(I18N.sending,"");
      fetch(endpoint,{
        method:"POST",
        headers:{"Content-Type":"application/json","Accept":"application/json"},
        body:JSON.stringify({name:v("name"),email:v("email"),phone:v("phone"),company:v("company"),topic:v("topic"),message:v("message"),_honey:v("form-honey")})
      }).then(function(res){
        return res.json().then(function(data){return {ok:res.ok,data:data};}).catch(function(){return {ok:res.ok,data:null};});
      }).then(function(r){
        if(r.ok&&r.data&&r.data.ok){
          setStatus(I18N.sent,"ok");
          f.reset();
        }else if(r.data&&r.data.error&&!r.ok&&r.data.error.indexOf("valid")>-1){
          setStatus(r.data.error,"err");
        }else{
          setStatus(fail,"err");
        }
      }).catch(function(){setStatus(fail,"err");
      }).finally(function(){
        if(btn){btn.disabled=false;btn.innerHTML=orig;}
      });
    });
  }

  // Trip / quote request form.
  var tf=document.getElementById("trip-form");
  if(tf){
    var to=tf.getAttribute("data-to")||"operations@coppermountainair.com",st=document.getElementById("form-status");
    var btn=document.getElementById("trip-submit")||tf.querySelector('button[type="submit"]');
    var endpoint=tf.getAttribute("data-endpoint");
    var q=new URLSearchParams(location.search);
    var want=q.get("service")||q.get("topic")||"";
    if(/charter/i.test(want)){var ch=document.getElementById("service-charter");if(ch) ch.checked=true;}
    else if(/cargo|freight/i.test(want)){var cg=document.getElementById("service-cargo");if(cg) cg.checked=true;}
    function tv(id){var el=document.getElementById(id);return el?(el.value||"").trim():"";}
    function serviceType(){
      var picked=tf.querySelector('input[name="serviceType"]:checked');
      return picked?picked.value:"";
    }
    function setStatus(msg,kind){
      if(!st)return;
      st.textContent=msg;
      st.style.color=kind==="ok"?"#1f6b3a":kind==="err"?"#8a2a2a":"";
    }
    var fail=I18N.tripFail.replace("{to}",to);
    tf.addEventListener("submit",function(e){
      e.preventDefault();if(!tf.reportValidity())return;
      if(tv("form-honey")){setStatus(I18N.tripSent,"ok");tf.reset();return;}
      var orig=btn?btn.innerHTML:"";
      if(btn){btn.disabled=true;btn.innerHTML=I18N.tripSendingBtn;}
      setStatus(I18N.tripSending,"");
      fetch(endpoint,{
        method:"POST",
        headers:{"Content-Type":"application/json","Accept":"application/json"},
        body:JSON.stringify({
          name:tv("name"),
          email:tv("email"),
          phone:tv("phone"),
          company:tv("company"),
          serviceType:serviceType(),
          pickup:tv("pickup"),
          dropoff:tv("dropoff"),
          weight:tv("weight"),
          pieces:tv("pieces"),
          dates:tv("dates"),
          notes:tv("notes"),
          _honey:tv("form-honey")
        })
      }).then(function(res){
        return res.json().then(function(data){return {ok:res.ok,data:data};}).catch(function(){return {ok:res.ok,data:null};});
      }).then(function(r){
        if(r.ok&&r.data&&r.data.ok){
          setStatus(I18N.tripSent,"ok");
          tf.reset();
        }else if(r.data&&r.data.error&&!r.ok){
          setStatus(r.data.error,"err");
        }else{
          setStatus(fail,"err");
        }
      }).catch(function(){setStatus(fail,"err");
      }).finally(function(){
        if(btn){btn.disabled=false;btn.innerHTML=orig;}
      });
    });
  }

  // Cookie notice + GA4 Consent Mode v2 (defaults are set denied in <head>).
  var CONSENT_KEY="cma-cookie-consent";
  function consentValue(){try{return localStorage.getItem(CONSENT_KEY);}catch(e){return null;}}
  function applyConsent(choice){
    try{localStorage.setItem(CONSENT_KEY,choice);}catch(e){}
    if(typeof gtag==="function"){
      gtag("consent","update",{analytics_storage:choice==="granted"?"granted":"denied"});
    }
    document.querySelectorAll("[data-cookie=status]").forEach(function(el){
      el.textContent=choice==="granted"?I18N.analyticsOn:I18N.analyticsOff;
    });
  }
  function hideBar(){
    var b=document.getElementById("cookie-bar");
    if(b) b.remove();
    document.body.classList.remove("cookie-open");
  }
  function showBar(){
    if(document.getElementById("cookie-bar")) return;
    var bar=document.createElement("div");
    bar.id="cookie-bar";
    bar.className="cookie-bar";
    bar.setAttribute("role","region");
    bar.setAttribute("aria-label",I18N.cookieAria);
    var privacy=document.querySelector('a[href$="privacy.html"]');
    var href=privacy?privacy.getAttribute("href"):"privacy.html";
    bar.innerHTML='<div class="inner"><p>'+I18N.cookieBody.replace("{href}",href)+'</p><div class="actions"><button type="button" data-cookie="accept">'+I18N.accept+'</button><button type="button" data-cookie="decline">'+I18N.decline+'</button></div></div>';
    document.body.appendChild(bar);
    document.body.classList.add("cookie-open");
  }
  var saved=consentValue();
  if(saved==="granted"||saved==="denied"){
    document.querySelectorAll("[data-cookie=status]").forEach(function(el){
      el.textContent=saved==="granted"?I18N.analyticsOn:I18N.analyticsOff;
    });
  }else{
    showBar();
  }
  document.addEventListener("click",function(e){
    var btn=e.target.closest("[data-cookie]");
    if(!btn) return;
    var act=btn.getAttribute("data-cookie");
    if(act==="accept"){applyConsent("granted");hideBar();}
    else if(act==="decline"){applyConsent("denied");hideBar();}
  });
})();

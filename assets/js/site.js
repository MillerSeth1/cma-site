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
  function isMobileNav(){return window.matchMedia("(max-width:860px)").matches;}
  function fineHover(){return window.matchMedia("(hover: hover) and (pointer: fine)").matches;}
  function navItems(){return n?Array.prototype.slice.call(n.querySelectorAll(".nav-item.has-sub")):[];}
  var closeTimer=null;
  function clearCloseTimer(){if(closeTimer){clearTimeout(closeTimer);closeTimer=null;}}
  function closeItem(item){
    item.classList.remove("open");
    item.classList.remove("pinned");
    var btn=item.querySelector(".nav-parent");
    if(btn) btn.setAttribute("aria-expanded","false");
  }
  function openItem(item,pin){
    clearCloseTimer();
    navItems().forEach(function(other){if(other!==item) closeItem(other);});
    item.classList.add("open");
    if(pin) item.classList.add("pinned");
    var btn=item.querySelector(".nav-parent");
    if(btn) btn.setAttribute("aria-expanded","true");
  }
  function scheduleClose(item){
    if(item.classList.contains("pinned")) return;
    clearCloseTimer();
    closeTimer=setTimeout(function(){
      closeTimer=null;
      if(!item.classList.contains("pinned")) closeItem(item);
    },250);
  }
  function closeAllNav(){clearCloseTimer();navItems().forEach(closeItem);}
  function subLinks(item){return Array.prototype.slice.call(item.querySelectorAll(".nav-sub a"));}
  if(t&&n){
    t.addEventListener("click",function(){
      var o=n.classList.toggle("open");
      t.setAttribute("aria-expanded",o?"true":"false");
      if(!o) closeAllNav();
    });
    navItems().forEach(function(item){
      var btn=item.querySelector(".nav-parent");
      if(!btn) return;
      btn.addEventListener("click",function(e){
        if(isMobileNav()) return;
        e.preventDefault();
        e.stopPropagation();
        if(item.classList.contains("pinned")) closeItem(item);
        else openItem(item,true);
      });
      btn.addEventListener("keydown",function(e){
        if(isMobileNav()) return;
        if(e.key==="ArrowDown"||e.key==="ArrowUp"){
          e.preventDefault();
          e.stopPropagation();
          openItem(item,true);
          var links=subLinks(item);
          if(!links.length) return;
          (e.key==="ArrowUp"?links[links.length-1]:links[0]).focus();
        }
      });
      item.addEventListener("keydown",function(e){
        if(isMobileNav()) return;
        var links=subLinks(item);
        var i=links.indexOf(document.activeElement);
        if(e.key==="ArrowDown"&&i>-1){e.preventDefault();links[(i+1)%links.length].focus();}
        else if(e.key==="ArrowUp"&&i>-1){e.preventDefault();links[(i-1+links.length)%links.length].focus();}
        else if(e.key==="Home"&&i>-1){e.preventDefault();links[0].focus();}
        else if(e.key==="End"&&i>-1){e.preventDefault();links[links.length-1].focus();}
        else if(e.key==="Escape"){e.preventDefault();closeItem(item);btn.focus();}
      });
      item.addEventListener("focusout",function(e){
        if(isMobileNav()) return;
        if(item.contains(e.relatedTarget)) return;
        if(item.classList.contains("pinned")) return;
        scheduleClose(item);
      });
      item.addEventListener("mouseenter",function(){
        if(!isMobileNav() && fineHover()) openItem(item);
      });
      item.addEventListener("mouseleave",function(){
        if(!isMobileNav() && fineHover()) scheduleClose(item);
      });
    });
    document.addEventListener("click",function(e){
      if(!n.contains(e.target)&&!(t&&t.contains(e.target))){
        closeAllNav();
        if(n.classList.contains("open")&&isMobileNav()){
          n.classList.remove("open");
          t.setAttribute("aria-expanded","false");
        }
      }
    });
    document.addEventListener("keydown",function(e){
      if(e.key!=="Escape") return;
      if(n.classList.contains("open")&&isMobileNav()){
        n.classList.remove("open");
        t.setAttribute("aria-expanded","false");
        closeAllNav();
        t.focus();
        return;
      }
      var opened=navItems().filter(function(item){return item.classList.contains("open");});
      if(opened.length){
        var focusBtn=opened[0].querySelector(".nav-parent");
        closeAllNav();
        if(focusBtn) focusBtn.focus();
      }
    });
    window.addEventListener("resize",function(){
      if(!isMobileNav()){
        n.classList.remove("open");
        if(t) t.setAttribute("aria-expanded","false");
      }
    });
  }
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

(function(){
  function isExternalHref(href){
    if(!href) return false;
    href=String(href).trim();
    if(/^(#|mailto:|tel:|sms:|javascript:|foreflightmobile:|garminpilot:)/i.test(href)) return false;
    try{
      var u=new URL(href, document.baseURI);
      if(u.protocol!=="http:" && u.protocol!=="https:") return false;
      return u.origin!==location.origin;
    }catch(e){return false;}
  }
  function mark(a){
    if(!a || !a.getAttribute) return;
    if(!isExternalHref(a.getAttribute("href"))) return;
    a.setAttribute("target","_blank");
    var rel=(a.getAttribute("rel")||"").split(/\s+/).filter(Boolean);
    ["noopener","noreferrer"].forEach(function(t){ if(rel.indexOf(t)===-1) rel.push(t); });
    a.setAttribute("rel", rel.join(" "));
  }
  function scan(root){
    if(!root) return;
    if(root.nodeType===1 && root.tagName==="A") mark(root);
    if(root.querySelectorAll) root.querySelectorAll("a[href]").forEach(mark);
  }
  scan(document);
  if(window.MutationObserver){
    new MutationObserver(function(muts){
      muts.forEach(function(m){
        if(m.type==="attributes" && m.target && m.target.tagName==="A") mark(m.target);
        m.addedNodes && m.addedNodes.forEach(function(n){ if(n.nodeType===1) scan(n); });
      });
    }).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:["href"]});
  }
})();


(function(){
  // Thanksgiving 2026 hours notice. Hide at midnight Fri Nov 27 in America/Phoenix (UTC-7 year-round).
  if (Date.now() >= Date.parse("2026-11-27T07:00:00.000Z")) return;
  var es = document.documentElement.lang === "es";
  var contact = document.querySelector('a[href$="contact.html"]');
  var href = contact
    ? contact.getAttribute("href").replace(/contact\.html$/, "blog/thanksgiving-hours-2026.html")
    : "blog/thanksgiving-hours-2026.html";
  var html = es
    ? '<div class="wrap"><strong>Horario de Acción de Gracias (jueves 26 de noviembre):</strong> abiertos de 7:00 a.m. a 12:00 p.m. Después del mediodía, llame al <a href="tel:+15206044020">520-604-4020</a>. <a href="'+href+'">Detalles</a></div>'
    : '<div class="wrap"><strong>Thanksgiving hours (Thursday, November 26):</strong> open 7:00 a.m. to 12:00 p.m. After noon, call <a href="tel:+15206044020">520-604-4020</a>. <a href="'+href+'">Details</a></div>';
  var bar = document.createElement("div");
  bar.className = "holiday-hours-banner";
  bar.setAttribute("role", "region");
  bar.setAttribute("aria-label", es ? "Horario de Acción de Gracias" : "Thanksgiving hours");
  bar.innerHTML = html;
  var header = document.querySelector(".site-header");
  var preview = document.querySelector(".preview-bar");
  if (preview && preview.parentNode) preview.parentNode.insertBefore(bar, preview.nextSibling);
  else if (header && header.parentNode) header.parentNode.insertBefore(bar, header);
  else document.body.insertBefore(bar, document.body.firstChild);
})();

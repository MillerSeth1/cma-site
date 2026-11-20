(function(){
  var d=document.documentElement;d.classList.remove("no-js");d.classList.add("js");
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
    var fail="Sorry, we couldn't send your message just now. Please email "+to+" or call (520) 287-9120 directly.";
    f.addEventListener("submit",function(e){
      e.preventDefault();if(!f.reportValidity())return;
      if(v("form-honey")){setStatus("Message sent. Our team at KOLS will get back to you shortly.","ok");f.reset();return;}
      var orig=btn?btn.innerHTML:"";
      if(btn){btn.disabled=true;btn.innerHTML="Sending…";}
      setStatus("Sending your message…","");
      fetch(endpoint,{
        method:"POST",
        headers:{"Content-Type":"application/json","Accept":"application/json"},
        body:JSON.stringify({name:v("name"),email:v("email"),phone:v("phone"),company:v("company"),topic:v("topic"),message:v("message"),_honey:v("form-honey")})
      }).then(function(res){
        return res.json().then(function(data){return {ok:res.ok,data:data};}).catch(function(){return {ok:res.ok,data:null};});
      }).then(function(r){
        if(r.ok&&r.data&&r.data.ok){
          setStatus("Message sent. Our team at KOLS will get back to you shortly.","ok");
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
})();

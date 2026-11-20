(function(){
  var d=document.documentElement;d.classList.remove("no-js");d.classList.add("js");
  var t=document.querySelector(".nav-toggle"),n=document.getElementById("site-nav");
  if(t&&n){t.addEventListener("click",function(){var o=n.classList.toggle("open");t.setAttribute("aria-expanded",o?"true":"false");});
    document.addEventListener("keydown",function(e){if(e.key==="Escape"&&n.classList.contains("open")){n.classList.remove("open");t.setAttribute("aria-expanded","false");t.focus();}});}
  var els=document.querySelectorAll(".reveal");
  if(!("IntersectionObserver" in window)||window.matchMedia("(prefers-reduced-motion: reduce)").matches){els.forEach(function(e){e.classList.add("in")});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}})},{rootMargin:"0px 0px -8% 0px"});els.forEach(function(e){io.observe(e)});}
  // Contact form: posts to FormSubmit so the message is emailed directly.
  var f=document.getElementById("contact-form");
  if(f){
    var to=f.getAttribute("data-to")||"",st=document.getElementById("form-status");
    var btn=document.getElementById("contact-submit")||f.querySelector('button[type="submit"]');
    var endpoint=f.getAttribute("data-endpoint")||("https://formsubmit.co/ajax/"+to);
    var q=new URLSearchParams(location.search).get("topic");
    if(q){var s=document.getElementById("topic");if(s){for(var i=0;i<s.options.length;i++){if(s.options[i].value===q){s.selectedIndex=i;}}}}
    function v(id){var el=document.getElementById(id);return el?(el.value||"").trim():"";}
    function setStatus(msg,kind){
      if(!st)return;
      st.textContent=msg;
      st.style.color=kind==="ok"?"#1f6b3a":kind==="err"?"#8a2a2a":"";
    }
    f.addEventListener("submit",function(e){
      e.preventDefault();if(!f.reportValidity())return;
      if(v("form-honey")){setStatus("Message sent. Our team at KOLS will get back to you shortly.","ok");f.reset();return;}
      var name=v("name"),email=v("email"),phone=v("phone"),company=v("company"),topic=v("topic"),message=v("message");
      var orig=btn?btn.innerHTML:"";
      if(btn){btn.disabled=true;btn.innerHTML="Sending…";}
      setStatus("Sending your message…","");
      fetch(endpoint,{
        method:"POST",
        headers:{"Content-Type":"application/json","Accept":"application/json"},
        body:JSON.stringify({
          name:name,
          email:email,
          phone:phone||"(not provided)",
          company:company||"(not provided)",
          topic:topic,
          message:message,
          _subject:"Website inquiry: "+topic+(company?" — "+company:""),
          _replyto:email,
          _template:"table",
          _captcha:"false",
          _honey:""
        })
      }).then(function(res){
        return res.json().then(function(data){return {ok:res.ok,data:data};}).catch(function(){return {ok:res.ok,data:null};});
      }).then(function(r){
        var data=r.data;
        if(r.ok&&data&&(data.success==="true"||data.success===true)){
          setStatus("Message sent. Our team at KOLS will get back to you shortly.","ok");
          f.reset();
        }else if(data&&typeof data.message==="string"&&/activat/i.test(data.message)){
          setStatus("This form is waiting on one-time email activation at "+to+". In the meantime, please email "+to+" or call (520) 287-9120.","err");
        }else{
          setStatus("We couldn't send your message just now. Please email "+to+" or call (520) 287-9120 directly.","err");
        }
      }).catch(function(){
        setStatus("We couldn't send your message just now. Please email "+to+" or call (520) 287-9120 directly.","err");
      }).finally(function(){
        if(btn){btn.disabled=false;btn.innerHTML=orig;}
      });
    });
  }
})();

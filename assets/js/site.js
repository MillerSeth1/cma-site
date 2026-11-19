(function(){
  var d=document.documentElement;d.classList.remove("no-js");d.classList.add("js");
  var t=document.querySelector(".nav-toggle"),n=document.getElementById("site-nav");
  if(t&&n){t.addEventListener("click",function(){var o=n.classList.toggle("open");t.setAttribute("aria-expanded",o?"true":"false");});
    document.addEventListener("keydown",function(e){if(e.key==="Escape"&&n.classList.contains("open")){n.classList.remove("open");t.setAttribute("aria-expanded","false");t.focus();}});}
  var els=document.querySelectorAll(".reveal");
  if(!("IntersectionObserver" in window)||window.matchMedia("(prefers-reduced-motion: reduce)").matches){els.forEach(function(e){e.classList.add("in")});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}})},{rootMargin:"0px 0px -8% 0px"});els.forEach(function(e){io.observe(e)});}
  // Contact form: builds a mailto with real line breaks; nothing is sent by the site itself.
  var f=document.getElementById("contact-form");
  if(f){
    var to=f.getAttribute("data-to"),st=document.getElementById("form-status");
    var q=new URLSearchParams(location.search).get("topic");
    if(q){var s=document.getElementById("topic");for(var i=0;i<s.options.length;i++){if(s.options[i].value===q){s.selectedIndex=i;}}}
    function v(id){var el=document.getElementById(id);return el?(el.value||"").trim():"";}
    f.addEventListener("submit",function(e){
      e.preventDefault();if(!f.reportValidity())return;
      var subject="Website inquiry: "+v("topic")+(v("company")?" — "+v("company"):"");
      var body=["Name: "+v("name"),"Email: "+v("email"),"Phone: "+(v("phone")||"(not provided)"),"Company: "+(v("company")||"(not provided)"),"Topic: "+v("topic"),"","Message:",v("message")].join("\r\n");
      st.textContent="Opening your email app with a message to "+to+". Review it, then press Send. If nothing opens, email us directly.";
      location.href="mailto:"+to+"?subject="+encodeURIComponent(subject)+"&body="+encodeURIComponent(body);
    });
  }
})();

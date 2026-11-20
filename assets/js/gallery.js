(function(){
  var ES = document.documentElement.lang === "es";
  var T = ES ? {viewer:"Visor de fotos",close:"Cerrar",prev:"Foto anterior",next:"Foto siguiente",of:" de "}
             : {viewer:"Photo viewer",close:"Close",prev:"Previous photo",next:"Next photo",of:" of "};
  var root=document.querySelector("[data-gallery]");
  if(!root) return;
  var items=Array.prototype.slice.call(document.querySelectorAll("a.gallery-item"));
  if(!items.length) return;

  var dialog=document.createElement("div");
  dialog.className="lightbox";
  dialog.setAttribute("role","dialog");
  dialog.setAttribute("aria-modal","true");
  dialog.setAttribute("aria-label",T.viewer);
  dialog.hidden=true;
  dialog.innerHTML='<div class="lightbox-inner">'+
    '<button type="button" class="lightbox-close" aria-label="'+T.close+'">&times;</button>'+
    '<button type="button" class="lightbox-prev" aria-label="'+T.prev+'">&#10094;</button>'+
    '<figure><img alt=""><figcaption></figcaption></figure>'+
    '<button type="button" class="lightbox-next" aria-label="'+T.next+'">&#10095;</button>'+
    '<p class="lightbox-count" aria-live="polite"></p>'+
    '</div>';
  document.body.appendChild(dialog);

  var img=dialog.querySelector("img");
  var cap=dialog.querySelector("figcaption");
  var countEl=dialog.querySelector(".lightbox-count");
  var closeBtn=dialog.querySelector(".lightbox-close");
  var idx=0;
  var lastFocus=null;

  function show(i){
    idx=(i+items.length)%items.length;
    var a=items[idx];
    img.src=a.getAttribute("href");
    img.alt=a.getAttribute("data-alt")||"";
    cap.textContent=a.getAttribute("data-caption")||"";
    countEl.textContent=(idx+1)+T.of+items.length;
  }
  function open(i){
    lastFocus=document.activeElement;
    show(i);
    dialog.hidden=false;
    document.body.classList.add("lightbox-open");
    closeBtn.focus();
  }
  function close(){
    dialog.hidden=true;
    document.body.classList.remove("lightbox-open");
    img.removeAttribute("src");
    if(lastFocus&&typeof lastFocus.focus==="function") lastFocus.focus();
  }

  items.forEach(function(a,i){
    a.addEventListener("click",function(e){
      e.preventDefault();
      open(i);
    });
  });
  closeBtn.addEventListener("click",close);
  dialog.querySelector(".lightbox-prev").addEventListener("click",function(){show(idx-1);});
  dialog.querySelector(".lightbox-next").addEventListener("click",function(){show(idx+1);});
  dialog.addEventListener("click",function(e){if(e.target===dialog) close();});
  document.addEventListener("keydown",function(e){
    if(dialog.hidden) return;
    if(e.key==="Escape") close();
    else if(e.key==="ArrowLeft") show(idx-1);
    else if(e.key==="ArrowRight") show(idx+1);
  });
})();

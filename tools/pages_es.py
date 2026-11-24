"""Spanish page bodies for the Copper Mountain Air site. Imported by tools/build.py."""
import sys, json, html

def B():
    return sys.modules.get("build") or sys.modules["__main__"]

def home(p):
    b = B()
    fp = b.fuel_prices()
    return f"""
<section class="hero" aria-label="Introducción" style="padding:0">
  <div class="hero-media">{b.img("hero", p, eager=True, sizes="full")}</div>
  <div class="wrap hero-inner">
    <p class="eyebrow">Aeropuerto Internacional de Nogales · KOLS</p>
    <h1>Combustible, carga y vuelo <span class="cu">en la frontera.</span></h1>
    <p class="lede">Copper Mountain Air mantiene en movimiento al sur de Arizona: Jet A y Avgas en la rampa, servicio de FBO en KOLS, instrucción de vuelo Part 61, y carga aérea y terrestre desde Nogales.</p>
    <div class="actions"><a class="btn btn-primary" href="{b.LP}contact.html">Contáctenos {b.ARROW}</a><a class="btn btn-ghost" href="{b.LP}trip-request.html">Solicite un viaje / cotización</a><a class="btn btn-ghost" href="{b.LP}fuel-fbo.html">Combustible y FBO</a><a class="btn btn-ghost" href="#plan-flight">Planifique su vuelo</a></div>
    {b.hero_status()}
    <div class="hero-strip"><span>Jet A</span><span>100LL Avgas</span><span>FBO</span><span>Instrucción de vuelo</span><span>Carga aérea y terrestre</span><span>Condado de Santa Cruz, AZ</span></div>
  </div>
</section>

<section><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Lo que hacemos</p><h2>Todo en un solo lugar en KOLS.</h2><p>Ya sea que vaya a cargar combustible en un vuelo de travesía, a quedar la noche o a mover una carga urgente, empiece aquí.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="media">{b.img("fuel", p, sizes="card")}</div><div class="body"><span class="num">01</span><h3>Combustible</h3><p>Jet A y 100LL Avgas en el Aeropuerto Internacional de Nogales.</p><p class="note" data-fuel="card" data-endpoint="{b.FUEL_ENDPOINT}">{fp}</p><a class="more" href="{b.LP}fuel-fbo.html">Detalles de combustible {b.ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{b.img("fbo", p, sizes="card")}</div><div class="body"><span class="num">02</span><h3>Servicios de FBO</h3><p>Atención en tierra, estacionamiento en rampa y amarre, y espacio en hangar en el campo.</p><a class="more" href="{b.LP}fuel-fbo.html#fbo">Servicios de FBO {b.ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{b.img("cargo", p, sizes="card")}</div><div class="body"><span class="num">03</span><h3>Carga y flete</h3><p>Flete urgente desde Nogales por aire y por tierra, incluido el flete expedito bajo demanda.</p><a class="more" href="{b.LP}cargo.html">Servicios de carga {b.ARROW}</a> · <a class="more" href="{b.LP}trip-request.html?service=cargo">Solicite una cotización {b.ARROW}</a></div></article>
  </div>
</div></section>

<figure class="photo-band">{b.img("ramp-band", p, sizes="full")}<figcaption>Hangares en KOLS</figcaption></figure>

<section class="dark"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">¿Viene volando?</p><h2>El Aeropuerto Internacional de Nogales de un vistazo.</h2><p>Una pista de 7,200 pies al pie del valle de Santa Cruz, a unas 7 millas al noreste del centro de Nogales.</p></div>
  {b.airport_facts()}
  {b.notams_panel()}
  {b.flight_plan_widget()}
  {b.kols_link(p, "Lea la guía del piloto de KOLS")}
</div></section>

<section><div class="wrap split">
  <div class="frame reveal">{b.img("training", p)}</div>
  <div class="reveal"><p class="eyebrow">Instrucción de vuelo</p><h2>Aprenda a volar en KOLS.</h2>
    <p>La instrucción de vuelo monomotor FAA Part 61 ya está disponible en el Aeropuerto Internacional de Nogales. La instrucción multimotor llegará en breve, y la certificación como escuela Part 141 está en proceso.</p>
    <p>El servicio de chárter bajo demanda estará disponible pronto y aún no se ofrece.</p>
    <p><a class="btn btn-dark" href="{b.LP}contact.html?topic=Flight%20training">Empiece su instrucción de vuelo {b.ARROW}</a></p>
    <p><a href="{b.LP}flight-training.html">Instrucción de vuelo</a> · <a href="{b.LP}cargo.html">Carga</a> · <a href="{b.LP}charter.html">Chárter</a></p></div>
</div></section>
{b.cta(p)}
"""

def services(p):
    b = B()
    return b.page_hero("Servicios", "Hechos para la frontera.", "Combustible, servicios de FBO y carga en el Aeropuerto Internacional de Nogales (KOLS), al servicio de Nogales, el condado de Santa Cruz y el sur de Arizona.") + f"""
<section id="cargo"><div class="wrap split">
  <div class="frame reveal">{b.img("cargo-sign", p)}</div>
  <div class="reveal"><p class="eyebrow">Carga y flete</p><h2>Aire y tierra, bajo demanda.</h2>
    <p>Cuando un envío no puede esperar, lo movemos. Copper Mountain Air maneja flete urgente desde Nogales por tierra y coordina la carga aérea en KOLS.</p>
    <ul class="checks">
      <li>Transporte terrestre por el sur de Arizona y más allá</li>
      <li>Flete expedito bajo demanda</li>
      <li>Coordinación de carga aérea y manejo en rampa en KOLS</li>
    </ul>
    <p style="display:flex;gap:.6rem;flex-wrap:wrap"><a class="btn btn-dark" href="{b.LP}cargo.html">Carga y flota {b.ARROW}</a><a class="btn" style="border-color:#d9c9b5;color:var(--ink)" href="{b.LP}trip-request.html?service=cargo">Solicite una cotización de flete</a></p></div>
</div>
<div class="wrap" style="padding-top:0">
  <div class="section-head reveal"><p class="eyebrow">Flota</p><h2>Nuestros camiones.</h2><p>Dos unidades para movimientos bajo demanda, desde cargas pequeñas en van hasta flete a altura de andén.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="body">
      <h3>Ford E-150 Cargo Van</h3>
      <ul class="checks">
        <li>Longitud útil de carga: 108 in (9 ft)</li>
        <li>Ancho de la puerta: aprox. 55 in</li>
        <li>Altura máxima de carga: 40 in</li>
        <li>Carga útil máxima: aprox. 1,600 lb</li>
      </ul>
    </div></article>
    <article class="card reveal"><div class="body">
      <h3>Hino 268 Box Truck</h3>
      <p>Caja de 26 pies a altura de andén, con elevador (liftgate)</p>
      <ul class="checks">
        <li>Longitud de la caja: 26 ft (altura de andén)</li>
        <li>Elevador (liftgate) para carga y entrega a nivel de piso</li>
        <li>GVWR: 25,999 lb (peso vacío 16,500 lb)</li>
        <li>Carga útil máxima: hasta 9,499 lb teórica (la carga útil real descuenta conductor, combustible, equipo y límites por eje)</li>
      </ul>
    </div></article>
  </div>
</div></section>
<section class="sand" id="fuel"><div class="wrap split rev">
  <div class="frame reveal">{b.img("fuel", p)}</div>
  <div class="reveal"><p class="eyebrow">Combustible</p><h2>Jet A y 100LL.</h2>
    <p>Tanto el combustible de reacción como el Avgas están disponibles en el campo en el Aeropuerto Internacional de Nogales.</p>
    <ul class="checks"><li>Jet A de servicio completo (también con aditivo)</li><li>100LL Avgas de servicio completo</li><li>Phillips 66</li><li>{b.wingpoints()}</li><li>{b.fuel_prices()}</li></ul>
    <a class="btn btn-dark" href="{b.LP}fuel-fbo.html">Detalles de combustible y FBO {b.ARROW}</a></div>
</div></section>
<section id="fbo"><div class="wrap split">
  <div class="frame reveal">{b.img("fbo", p)}</div>
  <div class="reveal"><p class="eyebrow">FBO</p><h2>Su escala en KOLS.</h2>
    <ul class="checks"><li>Atención en tierra de aeronaves</li><li>Estacionamiento en rampa y amarre</li><li>Renta de hangar — llame o escriba para disponibilidad y tarifas actuales</li><li>Terminal de pasajeros y sala de pilotos con Wi-Fi, baños, café y refrigerios, y un escritorio de planificación de vuelo</li></ul>
    <a class="btn btn-dark" href="{b.LP}fuel-fbo.html#fbo">Ver servicios de FBO {b.ARROW}</a></div>
</div></section>
<section id="training"><div class="wrap split">
  <div class="frame reveal">{b.img("training", p)}</div>
  <div class="reveal"><p class="eyebrow">Instrucción de vuelo</p><h2>Aprenda a volar en KOLS.</h2>
    <p>La instrucción de vuelo monomotor FAA Part 61 ya está disponible en el Aeropuerto Internacional de Nogales.</p>
    <ul class="checks">
      <li>Instrucción monomotor Part 61, disponible ahora</li>
      <li>Instrucción multimotor en breve</li>
      <li>Certificación como escuela FAA Part 141 en proceso</li>
    </ul>
    <a class="btn btn-dark" href="{b.LP}flight-training.html">Detalles de instrucción de vuelo {b.ARROW}</a></div>
</div></section>
<section class="dark" id="charter"><div class="wrap split">
  <div class="frame reveal">{b.img("charter", p)}</div>
  <div class="reveal"><span class="badge soon">Próximamente</span><p class="eyebrow">Chárter</p><h2>Chárter bajo demanda desde KOLS.</h2>
    <p>Un programa de chárter bajo demanda FAA Part 135 está en desarrollo y aún no se ofrece. Únase a la lista de interés y le avisaremos cuando el servicio abra.</p>
    <p style="display:flex;gap:.6rem;flex-wrap:wrap"><a class="btn btn-ghost" href="{b.LP}charter.html">Novedades de chárter {b.ARROW}</a><a class="btn btn-ghost" href="{b.LP}trip-request.html?service=charter">Solicite una cotización de chárter {b.ARROW}</a></p></div>
</div></section>
{b.cta(p)}"""

def fuel_fbo(p):
    b = B()
    return b.page_hero("Combustible y FBO · KOLS", "Cargue combustible en el Aeropuerto Internacional de Nogales.", "Jet A y 100LL Avgas, más rampa, hangar y servicios de atención en tierra en el Aeropuerto Internacional de Nogales (KOLS).") + f"""
<section id="fuel"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Combustible</p><h2>Jet A y 100LL.</h2><p>Precios en vivo de nuestro <a href="{b.AIRNAV}" rel="noopener">listado AirNav de KOLS</a>.</p></div>
  <div class="fuel-notam-banner" data-notams="fuel-banner" hidden></div>
  <table class="price-table reveal" data-fuel="table" data-endpoint="{b.FUEL_ENDPOINT}"><thead><tr><th scope="col">Combustible</th><th scope="col">Servicio</th><th scope="col">Precio actual</th></tr></thead>
  <tbody><tr><td><strong>Jet A</strong> (también con aditivo)</td><td data-fuel="jeta-service">Servicio completo</td><td data-fuel="jeta-price">Cargando el precio actual…</td></tr>
  <tr><td><strong>100LL Avgas</strong></td><td data-fuel="100ll-service">Servicio completo</td><td data-fuel="100ll-price">Cargando el precio actual…</td></tr></tbody></table>
  <p class="note fuel-updated" data-fuel="updated">Los precios se publican en <a href="{b.AIRNAV}" rel="noopener">AirNav</a>. Si un precio no carga, llame al {b.PHONE_LINK}.</p>
  <p class="note" style="margin-top:1rem">Phillips 66 · {b.wingpoints()} · Horario de combustible: {b.hours_text()} · {b.after_hours()} · Pago: {b.cards_text()}.</p>
</div></section>
<section class="sand" id="fbo"><div class="wrap split">
  <div class="frame reveal">{b.img("fbo", p)}</div>
  <div class="reveal"><p class="eyebrow">Servicios de FBO</p><h2>Rampa, hangar y atención en tierra.</h2>
    <ul class="checks"><li>Atención en tierra de aeronaves</li><li>Estacionamiento en rampa y amarre — llame o escriba para tarifas actuales</li><li>Renta de hangar — llame o escriba para disponibilidad y tarifas actuales</li><li>Terminal de pasajeros y sala de pilotos con Wi-Fi, baños, café y refrigerios, y un escritorio de planificación de vuelo. También podemos ayudar con reservaciones de hotel y auto, y con catering.</li></ul>
    <a class="btn btn-dark" href="{b.LP}contact.html?topic=FBO%20%2F%20ramp%20%2F%20hangar">Reserve un lugar en rampa o un hangar {b.ARROW}</a></div>
</div></section>
<section class="dark"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Información del aeropuerto</p><h2>KOLS para pilotos.</h2></div>
  {b.airport_facts()}
  {b.notams_panel()}
  {b.flight_plan_widget()}
  {b.kols_link(p, "Guía completa del piloto de KOLS")}
</div></section>
{b.cta(p, "¿Llega a KOLS?", f"Avísenos su ETA y lo que necesita de combustible. Teléfono: {b.PHONE_LINK}")}"""

def weather(p):
    return B().weather(p)

def flight_training(p):
    b = B()
    xc = b.xc_data()
    airspace_es = {
      "KFHU": "Clase D (Libby Tower 124.95, horario entre semana; Clase G el resto del tiempo)",
      "KTUS": "Clase C (Tucson Tower 118.3)",
      "E95": "Sin torre · CTAF/UNICOM 122.8",
      "KRYN": "Clase D de 6 a.m. a 8 p.m. MST (Tower 125.8)",
      "KAVQ": "Sin torre · CTAF/UNICOM 123.0",
      "KDUG": "Sin torre · CTAF/UNICOM 123.0 (Clase E de 6 a.m. a 9 p.m. MST)",
    }
    xc_json = json.dumps({"kols": b.KOLS, "dest": xc}).replace("</", "<\\/")
    fc = f'<a class="btn btn-glass" href="{b.FLIGHTCIRCLE}" target="_blank" rel="noopener">Portal del estudiante · FlightCircle {b.ARROW}</a>'
    xc_btns = "".join(
        f'<button class="xc" type="button" data-goto="{d["id"]}"><span class="id">{d["id"]}</span><span class="nm">{html.escape(d["name"])}</span><span class="d">{d["dist"]} NM<small>{d["mc"]}° mag</small></span><span class="as">{html.escape(airspace_es.get(d["id"], d["airspace"]))}</span></button>'
        for d in sorted(xc, key=lambda d: d["dist"])
    )
    tus = next(d for d in xc if d["id"] == "KTUS")
    steps = [
      ("01", "Vuelo de prueba", "ask", "Llame para agendar", "Su primera lección.", "Conozca el avión y vuélelo usted mismo, con un instructor a su lado, aquí en KOLS. Es la forma más sencilla de saber si la instrucción de vuelo es para usted.", ["Vuele desde una pista de 7,200 ft", "Vea el valle de Santa Cruz desde el aire", "Hable de sus metas, su horario y los siguientes pasos"]),
      ("02", "Piloto privado", "now", "Part 61 · Inscripciones abiertas", "Obtenga su certificado de piloto privado.", "Instrucción monomotor FAA Part 61, disponible ahora en el Aeropuerto Internacional de Nogales. Entrene a su ritmo, con un horario armado a su medida.", ["Instrucción en tierra y en vuelo hacia el certificado de piloto privado de la FAA", "Vuelos de travesía por el sur de Arizona", "Práctica en espacio aéreo controlado Clase C y Clase D a unos 50 NM"]),
      ("03", "Habilitación IFR", "ask", "Consulte disponibilidad", "Vuele por instrumentos.", "KOLS tiene un VOR/DME en el campo, más las aproximaciones RNAV (GPS)-A y VOR-B, con Tucson Approach en la zona. Pregúntenos sobre la instrucción IFR.", ["VOR/DME de Nogales en el campo (114.65)", "Aproximaciones publicadas RNAV (GPS)-A y VOR-B", "Servicios de Tucson Approach y Center cerca"]),
      ("04", "Piloto comercial", "ask", "Consulte disponibilidad", "Dé el siguiente paso.", "Pregúntenos sobre la instrucción de piloto comercial bajo Part 61 y cómo se articula con lo que ya tiene registrado.", ["Construya sobre su instrucción de piloto privado e IFR", "Vuelo real a elevada elevación y en montaña", "Tramos largos de travesía a KDUG y KAVQ"]),
      ("05", "Multimotor", "soon", "En breve", "Sume un segundo motor.", "La instrucción multimotor llegará en breve a Copper Mountain Air. Únase a la lista y le avisaremos en cuanto abra.", ["Habilitación adicional multimotor", "Únase hoy a la lista de interés", "La certificación Part 141 está en proceso"]),
      ("06", "Revisiones y pericia", "ask", "Consulte disponibilidad", "Manténgase actual y en forma.", "¿Ya es piloto? Pregúntenos sobre flight reviews, vuelos de pericia y cómo sentirse cómodo en un aeropuerto de elevada elevación y sin torre.", ["Flight reviews y vuelos de pericia", "Práctica de altitud de densidad y aeropuertos de montaña", "Trabajo en el circuito sin torre en la pista 04/22"]),
    ]
    tabs = "".join(f'<button class="tab" role="tab" id="tab-{n}" aria-controls="tp-{n}" aria-selected="{"true" if i == 1 else "false"}" tabindex="{0 if i == 1 else -1}"><span class="n">{n}</span>{t}</button>' for i, (n, t, *_r) in enumerate(steps))
    panels = "".join(f'''<div class="tabpanel" role="tabpanel" id="tp-{n}" aria-labelledby="tab-{n}"{"" if i == 1 else " hidden"}>
  <div class="tp-body"><span class="status-badge {st}">{stl}</span><h3 style="font-size:clamp(1.5rem,3vw,2.1rem)">{h}</h3><p style="color:var(--muted);font-size:1.08rem">{d}</p>
    <p style="margin:1.4rem 0 0;display:flex;gap:.6rem;flex-wrap:wrap"><a class="btn btn-dark" href="{b.LP}contact.html?topic=Flight%20training">Pregunte por {t.lower()} {b.ARROW}</a><a class="btn" style="border-color:#d9c9b5;color:var(--ink)" href="{b.PHONE_HREF}">Llame al {b.PHONE}</a></p></div>
  <div class="tp-side" data-step="{n}"><h4>Cómo se ve en KOLS</h4><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>
</div>''' for i, (n, t, st, stl, h, d, li) in enumerate(steps))
    return f"""
<section class="xhero" aria-label="Instrucción de vuelo en KOLS">
  <div class="hero-media">{b.img("charter", p, eager=True, sizes="full")}</div><div class="grid-lines" aria-hidden="true"></div>
  <div class="wrap">
    <div class="xhero-inner">
      <div>
        <ul class="chips" aria-label="Estado de la instrucción">
          <li class="chip live"><i></i>FAA Part 61 · Inscripciones abiertas</li><li class="chip"><i></i>Monomotor · Activo</li>
          <li class="chip soon"><i></i>Multimotor · En breve</li><li class="chip proc"><i></i>Part 141 · En proceso</li></ul>
        <p class="eyebrow">Instrucción de vuelo · Aeropuerto Internacional de Nogales · KOLS</p>
        <h1>Aprenda a volar <span class="cu">donde el cielo se abre.</span></h1>
        <p class="lede">Instrucción de vuelo monomotor FAA Part 61 en una pista de 7,200 pies al pie del valle de Santa Cruz. Sin torre, a elevada elevación y a minutos del espacio aéreo Clase C de Tucson, para que desde la primera lección construya pericia de verdad.</p>
        <div class="actions"><a class="btn btn-primary" href="{b.LP}contact.html?topic=Flight%20training" id="start-training">Empiece su instrucción de vuelo {b.ARROW}</a>{fc}</div>
      </div>
      <aside class="livecard" aria-label="Estado en vivo del campo KOLS" data-metar-endpoint="{b.METAR_ENDPOINT}">
        <div class="top"><span class="tag">Estado en vivo del campo</span><span class="status" data-wx="status">Cargando datos en vivo de KOLS…</span></div>
        <div class="catbig"><span class="c" data-wx="cat">—</span><span class="w">Categoría de vuelo</span></div>
        <div class="pill"><span class="led"></span><span data-wx="pill">KOLS · ASOS 121.125</span></div>
        <div class="mini"><div><span>Viento</span><b data-wx="wind">—</b></div><div><span>Visibilidad</span><b><span data-wx="vis">—</span> SM</b></div><div><span>Altitud de densidad</span><b data-wx="da">—</b></div></div>
        <a class="more" href="{b.LP}weather.html">Panel completo del ASOS {b.ARROW}</a>
      </aside>
    </div>
    <div class="qstrip">
      <div><span>Elevación del campo</span><b>3,955 ft</b><small>MSL, levantada</small></div>
      <div><span>Pista 04/22</span><b>7,200 × 100</b><small>ft · asfalto · MIRL</small></div>
      <div><span>CTAF / UNICOM</span><b>122.8</b><small>Aeródromo sin torre</small></div>
      <div><span>ASOS</span><b>121.125</b><small>520-287-9332</small></div>
      <div><span>Nogales VOR/DME</span><b>114.65</b><small>Ident OLS, en el campo</small></div>
      <div><span>Tucson Approach</span><b>118.75</b><small>App / Dep</small></div>
    </div>
  </div>
</section>

<section aria-label="Clima en KOLS"><div class="wrap">
  <p>El clima en vivo de KOLS, el radar y la climatología VFR están en la página de <a href="{b.LP}weather.html">Clima</a>.</p>
</div></section>

<section class="mapsec" id="map" aria-label="Mapa del área de instrucción"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Carta seccional VFR de la FAA · Corredor de instrucción</p><h2>Su aula es el sur de Arizona.</h2><p>Cartas vigentes de la FAA centradas en el Aeropuerto Internacional de Nogales. Alterne entre la seccional VFR, la IFR Enroute Low, el satélite y el terreno, y toque un destino para ver el tramo de travesía.</p></div>
  <div class="mapwrap">
    <div><div id="kols-map" role="region" aria-label="Mapa interactivo de la carta seccional de la FAA, centrado en KOLS"></div>
      <div class="legend"><span><i style="background:var(--copper)"></i>KOLS · base</span><span><i style="background:#1d4ed8"></i>Con torre (Clase C/D)</span><span><i style="background:#7c3aed"></i>Sin torre</span><span><i class="ring"></i>Anillos de 25 / 50 NM</span></div>
      <div class="disclaimer">⚠ <span>Solo para conciencia situacional y vista previa de planificación. No usar para navegación. Use las cartas vigentes de la FAA y un briefing oficial de meteorología para planificar el vuelo.</span></div>
    </div>
    <div class="xc-list" aria-label="Destinos de travesía">
      <button class="xc" type="button" data-goto="KOLS"><span class="id">KOLS</span><span class="nm">Nogales International · base</span><span class="d">0 NM<small>3,955 ft</small></span><span class="as">Sin torre · CTAF 122.8 · ASOS 121.125</span></button>
      {xc_btns}
      <p class="wx-foot" style="margin:0">Distancia en línea recta y rumbo magnético desde KOLS (variación 9° E). Espacio aéreo y horarios de torre según el FAA Chart Supplement.</p>
    </div>
  </div>
</div>
<script type="application/json" id="xc-data">{xc_json}</script>
</section>

<section aria-label="Ruta de instrucción del piloto"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Su ruta</p><h2>Del primer vuelo al asiento derecho.</h2><p>Elija dónde está hoy. La instrucción monomotor Part 61 ya está disponible; toque un paso para ver cómo se ve en KOLS.</p></div>
  <div class="tabs" role="tablist" aria-label="Pasos de la instrucción">{tabs}</div>
  {panels}
  <div class="road" aria-hidden="true"><div><b>Prueba</b>Primera lección</div><div><b>Privado</b>Part 61 · ahora</div><div><b>IFR</b>Consúltenos</div><div><b>Comercial</b>Consúltenos</div><div class="soon"><b>Multimotor</b>En breve</div><div><b>Pericia</b>Consúltenos</div></div>
  <div class="matrix">
    <div class="mx now"><span class="st">● Disponible ahora</span><h3>FAA Part 61 monomotor</h3><p>Instrucción de vuelo en el campo del Aeropuerto Internacional de Nogales (KOLS).</p></div>
    <div class="mx soon"><span class="st">● En breve</span><h3>Instrucción multimotor</h3><p>Únase a la lista de interés y le avisaremos cuando abra.</p></div>
    <div class="mx proc"><span class="st">● En proceso</span><h3>Escuela FAA Part 141</h3><p>La certificación Part 141 está actualmente en proceso.</p></div>
  </div>
</div></section>

<section class="dark" aria-label="Por qué entrenar en KOLS"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">¿Por qué Nogales?</p><h2>Por qué entrenar en KOLS.</h2><p>Vuelo real desde el primer día, sin la congestión de un aeropuerto de gran ciudad.</p></div>
  <div class="why reveal">
    <div><span class="ic">{b.ico("runway")}</span><h3>Una pista de 7,200 ft, sin filas en torre</h3><p>Sin torre, con <b>7,200 × 100 ft</b> de asfalto, para que más de su lección se vaya en volar y menos en esperar para despegar.</p></div>
    <div><span class="ic">{b.ico("mountain")}</span><h3>Pericia a elevada elevación</h3><p>A <b>3,955 ft</b> de elevación del campo, con montañas alrededor, aprende altitud de densidad y vuelo en montaña de verdad, no solo en el libro.</p></div>
    <div><span class="ic">{b.ico("tower")}</span><h3>Espacio aéreo controlado al lado</h3><p>Sierra Vista (Clase D) está a <b>{xc[0]["dist"]} NM</b> y Tucson International (Clase C) a <b>{tus["dist"]} NM</b>, un salto sencillo para practicar radio y operaciones con torre.</p></div>
    <div><span class="ic">{b.ico("compass")}</span><h3>Campo listo para IFR</h3><p>Un <b>VOR/DME en el campo</b>, aproximaciones publicadas RNAV (GPS)-A y VOR-B, y Tucson Approach en la zona.</p></div>
    <div><span class="ic">{b.ico("sun")}</span><h3>Clima de vuelo en el desierto</h3><p>El clima seco del sur de Arizona permite volar gran parte del año. Vea las <a href="{b.LP}weather.html">condiciones en vivo y la climatología VFR</a> de hoy y del año.</p></div>
    <div><span class="ic">{b.ico("fuel")}</span><h3>FBO de servicio completo en el campo</h3><p>Phillips 66 Jet A y 100LL, sala de pilotos y escritorio de planificación de vuelo, todo de Copper Mountain Air en KOLS.</p></div>
  </div>
</div></section>

<figure class="photo-band">{b.img("kols-guide", p, sizes="full")}<figcaption>Pista 4-22 en KOLS</figcaption></figure>

<section aria-label="Portal del estudiante"><div class="wrap">
  <div class="fcband reveal">
    <div><p class="eyebrow">Estudiantes · FlightCircle</p><h2>Programe y administre su instrucción en línea.</h2><p>Copper Mountain Air usa FlightCircle para la programación de la escuela de vuelo y las cuentas de los estudiantes. Los estudiantes actuales pueden iniciar sesión en cualquier momento. Estudiantes nuevos: llámenos o escríbanos y le abriremos su cuenta de FlightCircle.</p></div>
    <div class="btns"><a class="btn btn-primary" href="{b.FLIGHTCIRCLE}" target="_blank" rel="noopener">Iniciar sesión en FlightCircle {b.ARROW}</a><a class="btn btn-ghost" href="{b.LP}contact.html?topic=Flight%20training">¿Estudiante nuevo? Empiece aquí</a></div>
  </div>
</div></section>
{b.cta(p, "¿Listo para volar?", f'LLame al {b.PHONE_LINK} o escriba a <a href="mailto:{b.CONTACT_TO}">{b.CONTACT_TO}</a> y le ayudaremos a empezar en KOLS.')}"""

def cargo(p):
    b = B()
    q = f"{b.LP}trip-request.html?service=cargo"
    return f"""
<section class="xhero cargo-hero" aria-label="Carga desde KOLS" style="min-height:min(86vh,820px)">
  <div class="hero-media">{b.img("cargo-sign", p, eager=True, sizes="full")}</div><div class="grid-lines" aria-hidden="true"></div>
  <div class="wrap">
    <div class="xhero-inner" style="grid-template-columns:1fr">
      <div>
        <ul class="chips" aria-label="Capacidades de carga"><li class="chip live"><i></i>Despacho desde KOLS</li><li class="chip"><i></i>Camión de caja con elevador</li><li class="chip"><i></i>Van para envíos urgentes</li><li class="chip"><i></i>De la rampa al camión</li></ul>
        <p class="eyebrow">Carga · Aeropuerto Internacional de Nogales · KOLS</p>
        <h1>Flete que <span class="cu">no puede esperar.</span></h1>
        <p class="lede">Carga expedita terrestre y de aire a tierra desde el Aeropuerto Internacional de Nogales, justo en el corredor fronterizo de Nogales, Rio Rico y el condado de Santa Cruz. Movimientos de andén a andén, con elevador y de rampa a camión, despachados por nuestro propio equipo en KOLS.</p>
        <div class="actions"><a class="btn btn-primary" href="{b.PHONE_HREF}">Llame a despacho · {b.PHONE} {b.ARROW}</a><a class="btn btn-glass" href="{q}">Solicite una cotización de flete</a></div>
      </div>
    </div>
    <div class="qstrip">
      <div><span>Camión de caja</span><b>Hino 268</b><small>26 ft a altura de andén · elevador</small></div>
      <div><span>Van de carga</span><b>Ford E-150</b><small>Envíos urgentes y cargas pequeñas</small></div>
      <div><span>Con base en</span><b>KOLS</b><small>Nogales, AZ 85621</small></div>
      <div><span>Horario</span><b>7 días</b><small>Lun–sáb 7–7 · Dom 7–5</small></div>
    </div>
  </div>
</section>

<section aria-label="Capacidades de carga"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Lo que movemos</p><h2>Rampa, andén y puerta.</h2><p>Cuando un envío no puede esperar al siguiente camión programado, llámenos. Manejamos flete urgente desde Nogales por tierra y coordinamos la carga aérea en la rampa de KOLS.</p></div>
  <div class="caps">
    <article class="cap reveal"><span class="ic">{b.ico("plane")}</span><h3>De la rampa al camión en KOLS</h3><p>Coordinación de carga aérea y manejo en rampa en el campo, con el flete que pasa directo de la aeronave a nuestro camión.</p></article>
    <article class="cap reveal"><span class="ic">{b.ico("box")}</span><h3>Recolecciones en Nogales y Rio Rico</h3><p>Recolecciones en bodega, planta y andén en Nogales, Rio Rico y el condado de Santa Cruz.</p></article>
    <article class="cap reveal"><span class="ic">{b.ico("map")}</span><h3>El sur de Arizona y más allá</h3><p>Movimientos terrestres expeditos bajo demanda por el sur de Arizona y más allá.</p></article>
    <article class="cap reveal"><span class="ic">{b.ico("phone")}</span><h3>Despacho directo</h3><p>Hable directo con nuestro equipo de operaciones en KOLS. Sin centros de llamadas: las personas que mueven su flete.</p></article>
  </div>
</div></section>

<section class="dark" id="fleet" aria-label="Flota"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Flota</p><h2>Dos camiones, listos para salir.</h2><p>Desde un palé urgente hasta una carga completa a altura de andén.</p></div>
  <div class="fleet">
    <article class="truck reveal">
      <div class="art">{b.truck_svg("box")}</div>
      <div class="tb"><span class="kick">Camión de caja</span><h3>Hino 268</h3><p class="lead">Caja de 26 pies a altura de andén, con elevador (liftgate), para andenes y entregas a nivel de piso.</p>
        <span class="feature">✓ Elevador (liftgate)</span><span class="feature cu">✓ Altura de andén</span>
        <div class="specs">
          <div><span>Caja</span><b>26 ft</b><small>Altura de andén</small></div>
          <div><span>Elevador</span><b>Sí</b><small>Carga y entrega a nivel de piso</small></div>
          <div><span>GVWR</span><b>25,999 lb</b><small>16,500 lb de peso vacío</small></div>
          <div><span>Carga útil máx.</span><b>Hasta 9,499 lb</b><small>Teórica</small></div>
        </div>
        <p class="note">La carga útil real descuenta conductor, combustible, equipo y límites por eje.</p></div>
    </article>
    <article class="truck reveal">
      <div class="art">{b.truck_svg("van")}</div>
      <div class="tb"><span class="kick">Van de carga</span><h3>Ford E-150</h3><p class="lead">Ideal para envíos urgentes (hot-shot) y embarques pequeños de tiempo crítico.</p>
        <span class="feature cu">✓ Lista para envíos urgentes</span>
        <div class="specs">
          <div><span>Longitud útil de carga</span><b>108 in</b><small>9 ft</small></div>
          <div><span>Ancho de la puerta</span><b>≈ 55 in</b><small>Aprox.</small></div>
          <div><span>Altura máxima de carga</span><b>40 in</b><small>&nbsp;</small></div>
          <div><span>Carga útil máx.</span><b>≈ 1,600 lb</b><small>Aprox.</small></div>
        </div></div>
    </article>
  </div>
</div></section>

<section aria-label="Solicite una cotización"><div class="wrap split">
  <div class="frame reveal">{b.img("cargo", p)}</div>
  <div class="reveal"><p class="eyebrow">Pida una cotización</p><h2>Qué enviarnos.</h2>
    <p>Mándenos estos datos y le responderemos con una cotización.</p>
    <ul class="checks quote-list"><li>Lugares de recolección y entrega</li><li>Hora en que estará listo y hora de entrega requerida</li><li>Bultos, dimensiones y peso</li><li>Si necesita andén, elevador o manejo en rampa</li><li>Cualquier necesidad de material peligroso o manejo especial</li></ul>
    <div class="dispatch">
      <a href="{b.PHONE_HREF}"><span class="ic">{b.ico("phone")}</span><span><span class="lbl">Llame a despacho</span><b>{b.PHONE}</b></span></a>
      <a href="{b.LP}trip-request.html?service=cargo"><span class="ic">{b.ico("mail")}</span><span><span class="lbl">Solicite una cotización</span><b>Formulario de viaje</b></span></a>
    </div>
  </div>
</div></section>
{b.cta(p, "¿Flete que no puede esperar?", f'Llame a despacho al {b.PHONE_LINK} o escriba a <a href="mailto:{b.CONTACT_TO}">{b.CONTACT_TO}</a>. Horario: {b.hours_text()}.')}"""

def coming_soon_charter(p):
    b = B()
    hero = b.page_hero("Chárter", "Vuele directo desde KOLS.", "Un programa de chárter bajo demanda FAA Part 135 desde el Aeropuerto Internacional de Nogales está en desarrollo. Aún no se ofrece.", '<span class="badge soon">Próximamente</span>')
    return hero + f"""
<section><div class="wrap split">
  <div class="frame reveal">{b.img("charter", p)}</div>
  <div class="reveal"><span class="badge soon">Próximamente</span><h2>El chárter bajo demanda está en camino.</h2>
    <p>Estamos trabajando hacia un servicio de chárter bajo demanda FAA Part 135 desde el Aeropuerto Internacional de Nogales. Todavía no podemos reservar vuelos chárter. Puede enviar una solicitud de cotización o unirse a la lista de interés, y le daremos seguimiento cuando el servicio abra.</p>
    <p style="display:flex;gap:.6rem;flex-wrap:wrap"><a class="btn btn-dark" href="{b.LP}trip-request.html?service=charter">Solicite una cotización de chárter {b.ARROW}</a><a class="btn" style="border-color:#d9c9b5;color:var(--ink)" href="{b.LP}contact.html?topic=Charter%20interest">Únase a la lista de interés</a></p></div>
</div></section>{b.cta(p, "¿Tiene preguntas mientras tanto?", "Con gusto platicamos. Combustible, FBO, carga e instrucción de vuelo Part 61 ya están disponibles.")}"""

def history(p):
    b = B()
    def fig(slot, cap, cls="crop"):
        return f'<figure class="tfig {cls}">{b.img(slot, p, sizes="(min-width: 980px) 560px, 100vw")}<figcaption>{cap}</figcaption></figure>'
    items = [
      ("pro", "Prólogo", "1910–1933", "Un campamento fronterizo con campo de aviación",
       """<p>Tropas del Ejército de EE. UU. llegaron a Nogales en <b>noviembre de 1910</b>, al inicio de la Revolución Mexicana. El <b>14 de diciembre de 1915</b>, el puesto recibió el nombre de Camp Stephen D. Little, por un soldado muerto en el enfrentamiento fronterizo de noviembre de 1915. En su mayor extensión, el campamento abarcaba un acantonamiento, un polígono de tiro y un <b>campo de aviación</b>, el primer campo de vuelo documentado en Nogales. El Ejército abandonó formalmente Camp Little el <b>5 de mayo de 1933</b>.</p>
<p class="note-pro">Camp Little estaba en el borde norte del poblado de Nogales. <b>No</b> es el aeropuerto de hoy, que se encuentra a 7 u 8 millas al noreste del centro, sobre la State Route 82.</p>"""),
      ("pro", "Prólogo", "1920–1921", "DH-4 en patrulla fronteriza",
       fig("aero-1920", "Aeronaves del 12th Aero Squadron en el campo de aviación de Camp Stephen D. Little, cerca de Nogales, 1920. Foto del U.S. Air Service, dominio público. Este campo es anterior en ocho años al aeropuerto actual sobre la SR 82.", "bw") +
       """<p>Después de la Primera Guerra Mundial, el Army Air Service voló la Mexican Border Air Patrol. El <b>12th Aero Squadron</b> trasladó su cuartel a “Nogales Field” el <b>12 de abril de 1920</b> y voló patrullas Dayton-Wright DH-4 a lo largo de la línea. El cuartel se mudó a Douglas en febrero de 1921, un destacamento se quedó en Nogales, y el escuadrón se reagrupó en Texas ese septiembre.</p>
<p class="note-pro">Este era el campo militar anterior, cerca del pueblo, no el aeropuerto actual.</p>"""),
      ("", "Fundación", "1928", "La comunidad compra un campo aéreo",
       """<p>En <b>enero de 1928</b> la Cámara de Comercio del condado de Santa Cruz compró un terreno al norte de Nogales para un campo aéreo público: la misma propiedad que el aeropuerto ocupa hoy. Se inauguró en <b>marzo de 1928</b> como un rectángulo nivelado de tierra natural y pasto, de <b>1,980 por 4,180 pies</b>, donde los pilotos podían aterrizar en cualquier dirección.</p>
<p>El terreno se escrituró a favor del condado de Santa Cruz el <b>3 de octubre de 1928</b>, y el condado sigue siendo el propietario. El aeropuerto se dedicó oficialmente en <b>septiembre de 1929</b>.</p>"""),
      ("", "Época dorada", "1930s", "A un salto corto de la frontera",
       """<p>El registro de pilotos de Davis-Monthan en Tucson (1925–1936) anota decenas de vuelos hacia y desde Nogales, con pilotos basados aquí y muchos rumbo al sur. En los años de la Ley Seca, la línea internacional quedaba a minutos.</p>
<p>El Plan Maestro del aeropuerto de 2015 identifica a <b>Pickwick Airlines</b> como el primer operador regular del campo, con vuelos hacia México. Ese servicio no duró.</p>"""),
      ("", "Puerta de entrada", "1937", "Un aeropuerto internacional de entrada",
       """<p>El manual federal de aeropuertos de 1937 (Bureau of Air Commerce) ya listaba a Nogales como <b>aeropuerto internacional de entrada</b>, entonces un campo de grava. Nogales Municipal Airport aparece en la lista de aeropuertos de entrada del Código de los EE. UU. de 1946, y el Aeropuerto Internacional de Nogales sigue designado hoy bajo el <b>19 CFR § 122.13</b>, con un puerto de entrada de U.S. Customs and Border Protection en el campo.</p>"""),
      ("", "Segunda Guerra Mundial", "1942–1945", "Fondos federales pavimentan el campo",
       """<p>Los dos predios restantes se escrituraron al condado en <b>diciembre de 1942</b>. El Plan Maestro registra que el aeropuerto albergó un programa de instrucción Navy V-5 y a la Civil Air Patrol durante la guerra.</p>
<p>El <b>31 de marzo de 1944</b>, la construcción financiada por el gobierno federal dio al aeropuerto sus primeras pistas pavimentadas:</p>
<ul><li>Se pavimentó la franja original de pasto norte–sur (500 × 2,500 ft).</li><li>Se construyó una nueva pista de asfalto de <b>6,000 pies</b> de noreste a suroeste, con una calle de rodaje paralela y drenaje. Es la base de la pista 04/22 de hoy.</li></ul>
<p>Una plataforma iluminada siguió en agosto de 1944, y luces de contacto en la pista en junio de 1945.</p>"""),
      ("", "Era de aerolíneas", "1946–1953", "DC-3 en la ruta de Nogales",
       """<p><b>Arizona Airways</b>, con Douglas DC-3 desde Phoenix, incluyó a Nogales en su ruta a Bisbee y Douglas desde 1946 hasta que el servicio estatal terminó el <b>1 de marzo de 1948</b>.</p>
<p>El <b>1 de junio de 1950</b>, la recién formada <b>Frontier Airlines</b> inició servicio en DC-3 en la ruta Phoenix–Tucson–Nogales–Bisbee–Douglas. La autorización temporal de ruta no se renovó en 1953.</p>"""),
      ("", "Mediados de siglo", "1956–1981", "Combustible, un VOR y una aerolínea pequeña",
       """<ul><li><b>1956:</b> franjas de calle de rodaje y plataformas de amarre.</li><li><b>1965:</b> se resurface y se marca la pista de 6,000 pies.</li><li><b>1967:</b> abre una instalación de combustible en el campo.</li><li><b>1975:</b> se instalan una ayuda a la navegación VOR/DME, un camino de acceso y el servicio eléctrico.</li></ul>
<p><b>Copper State Airlines</b> aparece en un itinerario del <b>1 de abril de 1981</b>, volando un Piper Cherokee de Nogales a Sierra Vista/Fort Huachuca y Tucson.</p>"""),
      ("", "Campo moderno", "1984–1996", "La pista de 7,200 pies de hoy",
       fig("kols-guide", "Letrero de la pista 4-22 en el Aeropuerto Internacional de Nogales, hoy.") +
       """<p>La pista principal se recubrió en 1984 y se reforzó y repavimentó en 1989. Hacia 1988 la antigua pista de viento cruzado norte–sur dejó de usarse y desde entonces desapareció. El edificio actual de la terminal se construyó en <b>1993–94</b>.</p>
<p>En <b>1996</b> una extensión de 1,200 pies alargó la pista de 1944 a los <b>7,200 × 100 pies</b> de hoy, la pista en la que aterrizan los pilotos ahora.</p>"""),
      ("", "Modernización", "2002–2022", "Seguridad, iluminación y guía",
       fig("charter", "Luces de pista en KOLS al anochecer.") +
       """<p>De 2002 a 2011, casi <b>6 millones de dólares</b> en subvenciones del FAA Airport Improvement Program financiaron un cerco perimetral, letreros de guía, iluminación de pista y calles de rodaje, una rehabilitación de pista, una nueva plataforma y trabajos en calles de rodaje. Hay observaciones meteorológicas automatizadas del ASOS en el campo desde al menos 1999.</p>
<p>En <b>2022</b>, casi <b>2 millones de dólares</b> en subvenciones estatales financiaron un nuevo faro rotatorio LED, luces de identificación de extremo de pista, luces de borde de pista, letreros de guía y un nuevo sistema visual de guía de aproximación.</p>"""),
      ("now", "Hoy", "2024–presente", "Copper Mountain Air en KOLS",
       fig("cargo", "El letrero de CARGO en el campo de KOLS, hoy.") +
       f"""<p>En <b>2024</b>, Copper Mountain Air sucedió a Tiffin Aviation como el FBO de servicio completo en el Aeropuerto Internacional de Nogales, reuniendo combustible Phillips 66, instrucción de vuelo y carga expedita bajo un techo de dirección local, en el campo.</p>
<p>Con la inversión del condado de Santa Cruz en una nueva granja de combustible del aeropuerto y mejoras continuas al campo, KOLS entra en su segundo siglo listo para la siguiente generación de la aviación del sur de Arizona.</p>
<p style="margin-top:1rem"><a class="btn btn-primary" href="{b.LP}flight-training.html">Vuele con nosotros {b.ARROW}</a></p>"""),
    ]
    lis = "".join(f'<li class="{cls} reveal"><article class="tcard"><span class="era">{era}</span><span class="tyear">{yr}</span><h3>{h}</h3>{body}</article></li>' for cls, era, yr, h, body in items)
    srcs = "".join(f'<li>{t}. <a href="{u}" target="_blank" rel="noopener">Fuente</a></li>' for t, u in b.HISTORY_SOURCES)
    return f"""
<section class="heritage" id="history" aria-label="Historia del Aeropuerto Internacional de Nogales"><div class="wrap">
  <div class="lead-in">
    <div class="section-head reveal" style="margin:0"><p class="eyebrow">Historia de KOLS</p><h2>Casi un siglo de aviación fronteriza.</h2></div>
    <p class="big reveal">El Aeropuerto Internacional de Nogales nació en 1928 como un campo de pasto que la comunidad compró para sí. Se convirtió en aeropuerto federal de entrada, se pavimentó en tiempos de guerra, vio por un tiempo los DC-3 de aerolínea y creció hasta ser la puerta de entrada fronteriza de 7,200 pies que los pilotos usan hoy. Y Nogales ya volaba incluso antes de eso.</p>
  </div>
  <div class="hstats reveal">
    <div><b>1928</b><span>Se inauguró el campo actual, marzo de 1928</span></div>
    <div><b>1937</b><span>Listado como aeropuerto internacional de entrada</span></div>
    <div><b>1944</b><span>Primeras pistas pavimentadas, 31 de marzo</span></div>
    <div><b>7,200 ft</b><span>Pista 04/22 de hoy, tras la extensión de 1996</span></div>
  </div>
  <ol class="tl">{lis}</ol>
  <div class="sources"><h3>Fuentes</h3><ol>{srcs}</ol>
    <p style="margin-top:.8rem">Las fechas siguen el registro primario más sólido. Donde las fuentes discrepan (por ejemplo, la primera pista pavimentada), usamos la tabla de proyectos del Plan Maestro de 2015. La pista 04/22 se numeró 3/21 durante la mayor parte de su historia.</p></div>
</div></section>"""

def about(p):
    b = B()
    hero = f"""
<section class="xhero about-hero" aria-label="Acerca de Copper Mountain Air" style="min-height:min(80vh,760px)">
  <div class="hero-media">{b.img("airfield", p, eager=True, sizes="full")}</div><div class="grid-lines" aria-hidden="true"></div>
  <div class="wrap">
    <div class="xhero-inner" style="grid-template-columns:1fr">
      <div>
        <ul class="chips" aria-label="De un vistazo"><li class="chip"><i></i>Aeropuerto del condado de Santa Cruz desde 1928</li><li class="chip"><i></i>Aeropuerto internacional de entrada</li><li class="chip"><i></i>FBO de servicio completo desde 2024</li></ul>
        <p class="eyebrow">Nosotros · Aeropuerto Internacional de Nogales · KOLS</p>
        <h1>El equipo de casa <span class="cu">del sur de Arizona.</span></h1>
        <p class="lede">Copper Mountain Air, LLC es el FBO de servicio completo en el Aeropuerto Internacional de Nogales (KOLS), un aeropuerto del condado de Santa Cruz que ha servido a esta comunidad fronteriza desde 1928.</p>
        <div class="actions"><a class="btn btn-primary" href="#history">Casi un siglo de historia de KOLS {b.ARROW}</a><a class="btn btn-glass" href="{b.LP}contact.html">Contáctenos</a></div>
      </div>
    </div>
  </div>
</section>"""
    return hero + f"""
<section><div class="wrap split">
  <figure class="frame reveal">{b.img("training", p)}</figure>
  <div class="reveal"><p class="eyebrow">Nuestra historia</p><h2>Arraigados en KOLS.</h2>
    <p>Desde 2024, Copper Mountain Air es el operador de base fija en el Aeropuerto Internacional de Nogales (KOLS), en el condado de Santa Cruz, Arizona, justo al norte de la frontera entre Estados Unidos y México.</p>
    <p>Ofrecemos combustible Jet A y 100LL de servicio completo, apoyo de FBO en el campo, instrucción de vuelo monomotor FAA Part 61 y carga expedita bajo demanda por tierra. La instrucción multimotor llegará en breve, y la certificación como escuela FAA Part 141 está en proceso. El chárter bajo demanda está en desarrollo y aún no se ofrece.</p>
    <p><a class="btn btn-dark" href="#history">Lea la historia del aeropuerto {b.ARROW}</a></p></div>
</div></section>
{history(p)}
<section class="sand"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Equipo</p><h2>Servicio directo y de primera mano en KOLS.</h2><p>Una operación de dirección local a la que puede llegar por teléfono o correo cuando necesite combustible, un lugar en rampa, un hangar o un movimiento de flete.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="body"><h3>Seth Miller</h3><p>Principal</p><p>Dirige Copper Mountain Air en el Aeropuerto Internacional de Nogales, con un enfoque en combustible confiable, servicio de FBO, instrucción de vuelo y carga bajo demanda para los pilotos y embarcadores que usan KOLS.</p></div></article>
    <article class="card reveal"><div class="body"><h3>Operaciones en KOLS</h3><p>En el campo todos los días</p><p>Nuestro equipo de operaciones atiende el combustible, las necesidades de rampa y hangar, y la coordinación de flete. Llame al {b.PHONE_LINK} o escriba a <a href="mailto:{b.CONTACT_TO}">{b.CONTACT_TO}</a>.</p></div></article>
  </div>
</div></section>
<section class="dark"><div class="wrap"><div class="section-head reveal"><p class="eyebrow">Dónde estamos</p><h2>Aeropuerto Internacional de Nogales (KOLS)</h2><p>A unas 7 millas al noreste de Nogales, en el condado de Santa Cruz, Arizona. Dirección: {b.STREET}, Nogales, AZ 85621.</p></div>{b.airport_facts()}</div></section>
{b.cta(p)}"""


def trip_request(p):
    b = B()
    return b.page_hero("Solicite una cotización", "Cuéntenos del viaje.", "Envíe una solicitud de cotización de flete, o una de chárter para cuando ese servicio esté disponible. Nuestro equipo de operaciones en KOLS le dará seguimiento.") + f"""
<section><div class="wrap split" style="align-items:start">
  <form class="form reveal" id="trip-form" data-to="{b.CONTACT_TO}" data-endpoint="{b.TRIP_ENDPOINT}" action="{b.TRIP_ENDPOINT}" method="POST">
    <div class="row"><div class="field"><label for="name">Nombre</label><input id="name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="company">Empresa <span class="hint">Opcional</span></label><input id="company" name="company" autocomplete="organization"></div></div>
    <div class="row"><div class="field"><label for="phone">Teléfono</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
    <div class="field"><label for="email">Correo electrónico</label><input id="email" name="email" type="email" autocomplete="email" required></div></div>
    <fieldset class="field">
      <legend>Servicio</legend>
      <div class="service-choices">
        <label class="choice"><input type="radio" name="serviceType" id="service-cargo" value="cargo" required> Carga / flete</label>
        <label class="choice"><input type="radio" name="serviceType" id="service-charter" value="charter"> Solicitud de cotización de chárter</label>
      </div>
      <p class="note charter-caveat">El chárter bajo demanda está en desarrollo y aún no se ofrece. Una solicitud de cotización de chárter es solo una manifestación de interés: Copper Mountain Air no puede reservar vuelos chárter hoy.</p>
    </fieldset>
    <div class="row"><div class="field"><label for="pickup">Lugar de recolección</label><input id="pickup" name="pickup" required placeholder="Ciudad, aeropuerto o dirección"></div>
    <div class="field"><label for="dropoff">Lugar de entrega</label><input id="dropoff" name="dropoff" required placeholder="Ciudad, aeropuerto o dirección"></div></div>
    <div class="row"><div class="field"><label for="weight">Peso y dimensiones <span class="hint">Opcional</span></label><input id="weight" name="weight" placeholder="p. ej. 4,000 lb, 4 palés de 48×40×48 in"></div>
    <div class="field"><label for="pieces">Bultos o pasajeros <span class="hint">Opcional</span></label><input id="pieces" name="pieces" placeholder="p. ej. 6 bultos, o 3 pasajeros"></div></div>
    <div class="field"><label for="dates">Fechas preferidas <span class="hint">Opcional</span></label><input id="dates" name="dates" placeholder="Fecha en que estará listo y fecha de entrega requerida"></div>
    <div class="field"><label for="notes">Notas <span class="hint">Opcional</span></label><textarea id="notes" name="notes" placeholder="Necesidades de andén o elevador, material peligroso, manejo especial u otra información que debamos saber"></textarea></div>
    <input type="text" name="_honey" id="form-honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
    <div><button class="btn btn-primary" type="submit" id="trip-submit">Solicitar una cotización {b.ARROW}</button></div>
    <p class="note" id="form-status" role="status" aria-live="polite"></p>
    <p class="note">Las solicitudes se envían directamente a <a href="mailto:{b.CONTACT_TO}">{b.CONTACT_TO}</a>. Para despacho inmediato, llame al {b.PHONE_LINK}.</p>
  </form>
  <div class="contact-cards reveal">
    <div class="contact-card"><h3>Flota terrestre de carga</h3><p>Una van Ford E-150 para envíos urgentes (hot-shot) y cargas pequeñas, y un camión de caja Hino 268 de 26 ft con elevador para flete a altura de andén.</p></div>
    <div class="contact-card"><h3>Chárter</h3><p>El chárter bajo demanda FAA Part 135 está en desarrollo y aún no se ofrece. Envíe una solicitud de cotización y le daremos seguimiento cuando el servicio abra.</p></div>
    <div class="contact-card"><h3>Teléfono</h3><p>{b.PHONE_LINK}</p></div>
    <div class="contact-card"><h3>Horario</h3><p>{b.HOURS_HTML}</p></div>
  </div>
</div></section>"""

def contact(p):
    b = B()
    opts = [
        ("Fuel", "Combustible"),
        ("FBO / ramp / hangar", "FBO / rampa / hangar"),
        ("Cargo / freight", "Carga / flete"),
        ("Flight training", "Instrucción de vuelo"),
        ("Charter interest", "Interés en chárter"),
        ("Billing / payment", "Facturación / pago"),
        ("Other", "Otro"),
    ]
    options = "".join(f'<option value="{html.escape(v, quote=True)}">{html.escape(lab)}</option>' for v, lab in opts)
    return b.page_hero("Contacto", "Hablemos.", "Combustible, un lugar en rampa, una cotización de flete o una pregunta: mándenos un mensaje.") + f"""
<section><div class="wrap split" style="align-items:start">
  <form class="form reveal" id="contact-form" data-to="{b.CONTACT_TO}" data-endpoint="{b.CONTACT_ENDPOINT}" action="{b.CONTACT_ENDPOINT}" method="POST">
    <div class="row"><div class="field"><label for="name">Nombre</label><input id="name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="email">Correo electrónico</label><input id="email" name="email" type="email" autocomplete="email" required></div></div>
    <div class="row"><div class="field"><label for="phone">Teléfono <span class="hint">Opcional</span></label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="company">Empresa <span class="hint">Opcional</span></label><input id="company" name="company" autocomplete="organization"></div></div>
    <div class="field"><label for="topic">¿En qué podemos ayudarle?</label><select id="topic" name="topic" required>{options}</select></div>
    <div class="field"><label for="message">Mensaje</label><textarea id="message" name="message" required placeholder="Matrícula y ETA, necesidades de combustible, o datos del envío (recolección, entrega, bultos, peso)"></textarea></div>
    <input type="text" name="_honey" id="form-honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
    <input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_subject" value="Website inquiry — Copper Mountain Air">
    <div><button class="btn btn-primary" type="submit" id="contact-submit">Enviar mensaje {b.ARROW}</button></div>
    <p class="note" id="form-status" role="status" aria-live="polite"></p>
    <p class="note">Los mensajes llegan directo a <a href="mailto:{b.CONTACT_TO}">{b.CONTACT_TO}</a>. Para necesidades inmediatas de rampa o combustible, llame al {b.PHONE_LINK}.</p>
  </form>
  <div class="contact-cards reveal">
    <div class="contact-card"><h3>Teléfono</h3><p>{b.PHONE_LINK}</p></div>
    <div class="contact-card"><h3>Correo</h3><p><a href="mailto:{b.CONTACT_TO}">{b.CONTACT_TO}</a></p></div>
    <div class="contact-card"><h3>Horario</h3><p>{b.hours_html()}</p></div>
    <div class="contact-card"><h3>Ubicación</h3><p>Aeropuerto Internacional de Nogales (KOLS)<br>{b.STREET}<br>Nogales, AZ 85621</p></div>
    <div class="contact-card"><h3>Síganos</h3>{b.social_links()}</div>
  </div>
</div></section>"""

def privacy(p):
    b = B()
    return b.page_hero("Privacidad", "Cómo usamos este sitio.", "Una nota breve sobre cookies, analítica y cómo contactarnos.") + f"""
<section><div class="wrap" style="max-width:42rem">
  <p>Copper Mountain Air usa Google Analytics 4 para entender cómo los visitantes usan coppermountainair.com — por ejemplo, qué páginas se leen con más frecuencia. Las cookies de analítica no se colocan hasta que usted acepta el aviso de cookies, y no usamos cookies de publicidad ni anuncios en este sitio.</p>
  <p>Si lo rechaza, el sitio sigue funcionando; simplemente no mediremos su visita con Google Analytics. Puede cambiar su elección en cualquier momento con los botones de abajo, o al borrar los datos almacenados de este sitio en su navegador.</p>
  <p>Las preguntas sobre este aviso pueden enviarse a <a href="mailto:{b.CONTACT_TO}">{b.CONTACT_TO}</a>.</p>
  <p class="cookie-prefs">
    <button type="button" class="btn btn-primary" data-cookie="accept">Aceptar analítica</button>
    <button type="button" class="btn btn-ghost" data-cookie="decline">Rechazar analítica</button>
    <span class="cookie-pref-status" data-cookie="status"></span>
  </p>
</div></section>
"""

def page_404(p):
    b = B()
    return b.page_hero("404", "Fuera de carta.", "Esa página no está aquí.") + f'<section><div class="wrap"><a class="btn btn-dark" href="{b.SITE_URL}es/">Volver al inicio</a></div></section>'

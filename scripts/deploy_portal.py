import html
import json
import re
import shutil
import sqlite3
from pathlib import Path

from common import DB_PATH, DOCS_DIR, SITE_DIR, ensure_dirs


CSS = """
:root{--bg:#10100e;--panel:#181915;--panel2:#202118;--ink:#eee8d7;--muted:#b8ad94;--line:#4b442e;--gold:#d0a94f;--green:#7aa36b;--red:#b96b5f;--blue:#7296a8;--font:Georgia,'Times New Roman',serif;--ui:Inter,Segoe UI,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--ui);line-height:1.65}.nav{position:sticky;top:0;z-index:3;background:rgba(16,16,14,.94);border-bottom:1px solid var(--line);backdrop-filter:blur(10px)}.nav-inner{max-width:1180px;margin:0 auto;padding:14px 20px;display:flex;gap:18px;align-items:center;justify-content:space-between}.brand{font-family:var(--font);font-size:24px;color:var(--gold);text-decoration:none}.links{display:flex;gap:14px;flex-wrap:wrap}.links a{color:var(--ink);text-decoration:none;font-size:14px}.links a:hover{color:var(--gold)}.links a.active{color:var(--gold);border-bottom:1px solid var(--gold)}main{max-width:1180px;margin:0 auto;padding:42px 20px}.hero{min-height:360px;display:grid;align-content:end;padding:48px 20px;background:linear-gradient(rgba(16,16,14,.25),rgba(16,16,14,.92)),url('assets/manuscript-field.svg');background-size:cover;background-position:center;border-bottom:1px solid var(--line)}.hero-inner{max-width:1180px;margin:0 auto;width:100%}h1{font-family:var(--font);font-size:clamp(42px,7vw,82px);line-height:1;margin:0 0 14px;color:#f5d982;letter-spacing:0}h2{font-family:var(--font);font-size:30px;color:var(--gold);margin:34px 0 14px}.subtitle{font-size:19px;color:var(--muted);max-width:760px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;text-decoration:none;color:var(--ink);min-height:180px}.card:hover{border-color:var(--gold);background:var(--panel2)}.card-title{font-family:var(--font);font-size:23px;color:#f1d17c;line-height:1.15;margin-bottom:8px}.meta{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--gold);margin-bottom:10px}.desc{font-size:14px;color:var(--muted)}.prose{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:26px;font-family:var(--font);font-size:19px}.prose p{margin:0 0 18px}.toolbar{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 22px}.toolbar input,.toolbar select{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:10px 12px}.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:3px 9px;color:var(--muted);font-size:12px;margin-right:6px}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:30px 0}.stat{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px}.stat strong{display:block;font-family:var(--font);font-size:34px;color:var(--gold)}footer{border-top:1px solid var(--line);padding:36px 20px;text-align:center;color:var(--muted)}.map-container{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px;margin:28px 0;overflow:hidden}.map-container svg{width:100%;height:auto;display:block}.map-dot{cursor:pointer}.map-dot:hover circle{fill:var(--gold)!important}.map-tooltip{position:absolute;background:var(--panel2);border:1px solid var(--line);border-radius:6px;padding:10px 14px;font-size:13px;max-width:280px;pointer-events:none;display:none;z-index:10}.timeline-entry{border-left:2px solid var(--line);padding:0 0 28px 20px;position:relative}.timeline-entry::before{content:'';position:absolute;left:-5px;top:4px;width:8px;height:8px;border-radius:50%;background:var(--gold)}.timeline-year{font-family:var(--font);color:var(--gold);font-size:22px;margin:0 0 6px}.timeline-title{font-weight:600;margin:0 0 4px}.timeline-desc{font-size:14px;color:var(--muted)}.period-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;text-transform:uppercase;letter-spacing:.07em;margin-left:8px}.badge-renaissance{background:#2a3820;color:#7aa36b}.badge-early_modern{background:#1e2a38;color:#7296a8}.badge-modern{background:#2a2018;color:#d0a94f}
"""

ASSET = """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="700" viewBox="0 0 1600 700"><rect width="1600" height="700" fill="#17160f"/><g opacity=".18" fill="none" stroke="#d0a94f" stroke-width="2"><path d="M120 120c170 90 320 90 490 0s320-90 490 0 320 90 430 10"/><path d="M90 250h1420M90 330h1420M90 410h1420M90 490h1420"/><circle cx="340" cy="348" r="82"/><circle cx="340" cy="348" r="47"/><path d="M820 190l95 250 95-250M780 440h270"/><path d="M1170 240c80-58 170-58 250 0-80 58-170 58-250 0z"/><path d="M1295 170v150M1220 245h150"/></g><g opacity=".22" fill="#efe0b4" font-family="Georgia" font-size="38"><text x="130" y="610">ars notoria</text><text x="560" y="95">nigromantia</text><text x="1040" y="600">scientia imaginum</text></g></svg>"""


def clean(value):
    return html.escape(value or "")


def page(title, content, prefix="", active=""):
    active_class = lambda name: " class='active'" if active == name else ""
    nav = """
    <nav class="nav"><div class="nav-inner"><a class="brand" href="{0}index.html">MedievalMagicDB</a><div class="links">
    <a href="{0}texts.html"{1}>Texts</a><a href="{0}persons.html"{2}>Persons</a><a href="{0}concepts.html"{3}>Concepts</a><a href="{0}reception.html"{4}>Reception</a><a href="{0}bibliography.html"{5}>Bibliography</a><a href="{0}timeline.html"{6}>Timeline</a><a href="{0}about.html"{7}>Methodology</a>
    </div></div></nav>
    """.format(
        prefix,
        active_class("texts"), active_class("persons"), active_class("concepts"),
        active_class("reception"), active_class("bibliography"), active_class("timeline"),
        active_class("about"),
    )
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{clean(title)} - MedievalMagicDB</title><style>{CSS}</style></head><body>{nav}{content}<footer>MedievalMagicDB - scholarly reference portal generated from SQLite.</footer></body></html>"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def cards(rows, kind):
    out = ["<div class='grid'>"]
    for row in rows:
        if kind == "texts":
            href = f"texts/{row['text_id']}.html"
            meta = " / ".join(x for x in [row["text_type"], row["period"], row["language"]] if x)
            title = row["title"]
            desc = row["description"]
        elif kind == "persons":
            href = f"persons/{row['person_id']}.html"
            meta = " / ".join(x for x in [row["role_primary"], row["era"]] if x)
            title = row["name"]
            desc = row["description"]
        elif kind == "concepts":
            href = f"concepts/{row['slug']}.html"
            meta = " / ".join(x for x in [row["category_type"], row["category"]] if x)
            title = row["label"]
            desc = row["definition_short"] or row["significance"]
        else:
            href = "bibliography.html"
            meta = " / ".join(str(x) for x in [row["pub_type"], row["year"]] if x)
            title = row["title"]
            desc = f"{row['author']}. Extraction: {row['extraction_status'] or 'not converted'}."
        out.append(f"<a class='card' href='{href}'><div class='card-title'>{clean(title)}</div><div class='meta'>{clean(meta)}</div><div class='desc'>{clean(desc)}</div></a>")
    out.append("</div>")
    return "\n".join(out)


def list_page(title, subtitle, rows, kind):
    return page(title, f"<main><h1>{clean(title)}</h1><p class='subtitle'>{clean(subtitle)}</p><div class='toolbar'><input id='q' placeholder='Search'><select id='filter'><option value=''>All categories</option></select></div>{cards(rows, kind)}</main><script>{FILTER_JS}</script>", active=kind)


FILTER_JS = """
const q=document.querySelector('#q');const cards=[...document.querySelectorAll('.card')];if(q){q.addEventListener('input',()=>{const v=q.value.toLowerCase();cards.forEach(c=>{c.style.display=c.textContent.toLowerCase().includes(v)?'block':'none'})})}
"""


def detail_page(kind, title, meta, body, related=""):
    content = f"<main><a class='pill' href='../{kind}.html'>Back to {kind}</a><h1>{clean(title)}</h1><p class='subtitle'>{clean(meta)}</p><section class='prose'>{body}</section>{related}</main>"
    return page(title, content, "../")


def related_block(title, items):
    if not items:
        return ""
    parts = [f"<h2>{clean(title)}</h2><div class='grid'>"]
    for item_title, meta, href in items:
        parts.append(
            f"<a class='card' href='{href}'><div class='card-title'>{clean(item_title)}</div>"
            f"<div class='meta'>{clean(meta)}</div><div class='desc'>Related database entry.</div></a>"
        )
    parts.append("</div>")
    return "".join(parts)


EUROPE_MAP_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" style="background:#12120f;border-radius:6px">
<defs>
  <filter id="glow"><feGaussianBlur stdDeviation="2.5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<!-- Simplified Europe coastline and borders (schematic) -->
<g opacity=".35" fill="none" stroke="#4b442e" stroke-width="1">
  <!-- British Isles -->
  <path d="M205 140 Q220 120 215 100 Q225 80 210 70 Q195 60 190 80 Q185 95 195 110 Q188 125 195 140 Z"/>
  <path d="M190 150 Q200 145 205 140 Q215 155 210 170 Q200 185 188 175 Q182 163 190 150 Z"/>
  <!-- Iberian Peninsula -->
  <path d="M200 310 Q230 280 260 275 Q290 270 310 285 Q330 300 325 330 Q315 355 290 365 Q260 375 235 360 Q210 345 200 310 Z"/>
  <!-- France -->
  <path d="M260 275 Q295 240 330 230 Q360 225 370 245 Q380 265 370 285 Q355 305 330 310 Q310 315 290 305 Q270 295 260 275 Z"/>
  <!-- Low Countries / Belgium / Netherlands -->
  <path d="M330 210 Q355 195 375 200 Q385 210 380 225 Q370 235 355 230 Q340 225 330 210 Z"/>
  <!-- German lands -->
  <path d="M370 200 Q420 185 460 190 Q495 195 510 215 Q520 235 505 255 Q490 270 465 268 Q440 265 420 250 Q400 235 380 225 Q365 215 370 200 Z"/>
  <!-- Scandinavia (schematic) -->
  <path d="M400 100 Q425 70 440 60 Q455 55 460 75 Q455 95 445 115 Q435 130 420 135 Q408 130 400 115 Z"/>
  <path d="M440 60 Q465 40 480 55 Q490 75 475 95 Q460 110 445 115 Q440 95 440 75 Z"/>
  <!-- Italy -->
  <path d="M390 300 Q410 285 435 285 Q455 290 465 310 Q470 330 460 355 Q448 380 430 395 Q415 405 405 390 Q395 370 395 345 Q390 320 390 300 Z"/>
  <!-- Sicily -->
  <path d="M430 410 Q445 405 455 415 Q458 425 448 430 Q435 432 428 422 Z"/>
  <!-- Greece / Aegean area -->
  <path d="M510 340 Q530 325 555 330 Q570 340 565 360 Q555 375 540 375 Q522 372 515 358 Z"/>
  <!-- Baltic states schematic -->
  <path d="M460 155 Q490 140 520 145 Q545 155 550 175 Q545 190 525 195 Q500 198 480 188 Q462 178 460 155 Z"/>
</g>
<!-- Latitude/longitude grid (schematic) -->
<g opacity=".1" fill="none" stroke="#d0a94f" stroke-width=".5">
  <line x1="0" y1="130" x2="800" y2="130"/>
  <line x1="0" y1="260" x2="800" y2="260"/>
  <line x1="0" y1="390" x2="800" y2="390"/>
  <line x1="160" y1="0" x2="160" y2="520"/>
  <line x1="320" y1="0" x2="320" y2="520"/>
  <line x1="480" y1="0" x2="480" y2="520"/>
  <line x1="640" y1="0" x2="640" y2="520"/>
</g>
<!-- LOCATION DOTS - plotted at approximate lat/lon for the map projection -->
<!-- Projection: lon -12 to 26 → x 80 to 720; lat 62 to 37 → y 40 to 480 -->
<!-- Florence 43.77N 11.26E → x=460 y=305 -->
<g class="map-dot" data-city="Florence" data-events="Ficino translates Corpus Hermeticum (1463); Pico's 900 Theses context (1486); De Vita Coelitus Comparanda (1489); Council of Florence / Plethon (1438)">
  <circle cx="460" cy="305" r="8" fill="#d0a94f" opacity=".85" filter="url(#glow)"/>
  <text x="470" y="302" fill="#eee8d7" font-size="10" font-family="Georgia">Florence</text>
</g>
<!-- Rome 41.9N 12.5E → x=474 y=345 -->
<g class="map-dot" data-city="Rome" data-events="Pico's 900 Theses published (1486); Bruno burned (1600)">
  <circle cx="474" cy="345" r="7" fill="#b96b5f" opacity=".85" filter="url(#glow)"/>
  <text x="484" y="342" fill="#eee8d7" font-size="10" font-family="Georgia">Rome</text>
</g>
<!-- Cologne 50.93N 6.95E → x=388 y=204 -->
<g class="map-dot" data-city="Cologne" data-events="Agrippa born (1486); De Occulta Philosophia published (1531)">
  <circle cx="388" cy="204" r="7" fill="#d0a94f" opacity=".85" filter="url(#glow)"/>
  <text x="398" y="201" fill="#eee8d7" font-size="10" font-family="Georgia">Cologne</text>
</g>
<!-- Sponheim 49.84N 7.91E → x=398 y=218 -->
<g class="map-dot" data-city="Sponheim" data-events="Trithemius abbot (1483–1505); Steganographia composed (c.1499)">
  <circle cx="398" cy="220" r="6" fill="#7aa36b" opacity=".85" filter="url(#glow)"/>
  <text x="408" y="217" fill="#eee8d7" font-size="10" font-family="Georgia">Sponheim</text>
</g>
<!-- Würzburg 49.79N 9.93E → x=416 y=220 -->
<g class="map-dot" data-city="Würzburg" data-events="Trithemius final abbot post; died 1516/1519; library inventory">
  <circle cx="418" cy="222" r="5" fill="#7aa36b" opacity=".75"/>
  <text x="428" y="219" fill="#eee8d7" font-size="10" font-family="Georgia">Würzburg</text>
</g>
<!-- Frankfurt 50.11N 8.68E → x=408 y=210 -->
<g class="map-dot" data-city="Frankfurt" data-events="Steganographia printed (1606)">
  <circle cx="410" cy="212" r="5" fill="#7296a8" opacity=".75"/>
  <text x="420" y="209" fill="#eee8d7" font-size="10" font-family="Georgia">Frankfurt</text>
</g>
<!-- Basel 47.56N 7.59E → x=395 y=242 -->
<g class="map-dot" data-city="Basel" data-events="Weyer publishes De Praestigiis (1563); Arbatel printed (1575)">
  <circle cx="395" cy="242" r="6" fill="#d0a94f" opacity=".85" filter="url(#glow)"/>
  <text x="405" y="239" fill="#eee8d7" font-size="10" font-family="Georgia">Basel</text>
</g>
<!-- Marburg 50.80N 8.77E → x=410 y=208 -->
<g class="map-dot" data-city="Marburg" data-events="Fourth Book of Occult Philosophy printed (1559)">
  <circle cx="411" cy="209" r="5" fill="#7296a8" opacity=".75"/>
</g>
<!-- Naples 40.85N 14.27E → x=488 y=358 -->
<g class="map-dot" data-city="Naples" data-events="Della Porta's Magia Naturalis (1558); Accademia dei Segreti founded">
  <circle cx="488" cy="358" r="6" fill="#d0a94f" opacity=".85"/>
  <text x="498" y="355" fill="#eee8d7" font-size="10" font-family="Georgia">Naples</text>
</g>
<!-- Antwerp 51.22N 4.40E → x=374 y=197 -->
<g class="map-dot" data-city="Antwerp" data-events="Dee publishes Monas Hieroglyphica (1564)">
  <circle cx="374" cy="197" r="5" fill="#7296a8" opacity=".75"/>
  <text x="384" y="194" fill="#eee8d7" font-size="10" font-family="Georgia">Antwerp</text>
</g>
<!-- London 51.51N -0.13E → x=314 y=196 -->
<g class="map-dot" data-city="London" data-events="Dee's library at Mortlake; Scot's Discoverie (1584); Mathers Key of Solomon (1888); Barrett The Magus (1801); Walker Spiritual Magic (1958); Yates Bruno (1964)">
  <circle cx="314" cy="196" r="9" fill="#d0a94f" opacity=".9" filter="url(#glow)"/>
  <text x="324" y="193" fill="#eee8d7" font-size="10" font-family="Georgia">London</text>
</g>
<!-- Mortlake 51.47N -0.27E → x=312 y=198 -->
<g class="map-dot" data-city="Mortlake" data-events="Dee and Kelley angelic conferences begin (1582)">
  <circle cx="311" cy="200" r="5" fill="#7aa36b" opacity=".75"/>
</g>
<!-- Kassel 51.31N 9.48E → x=416 y=199 -->
<g class="map-dot" data-city="Kassel" data-events="Rosicrucian Fama Fraternitatis published (1614)">
  <circle cx="416" cy="201" r="6" fill="#7aa36b" opacity=".75"/>
  <text x="426" y="198" fill="#eee8d7" font-size="10" font-family="Georgia">Kassel</text>
</g>
<!-- Lyon 45.76N 4.84E → x=378 y=274 -->
<g class="map-dot" data-city="Lyon" data-events="French popular grimoire printing (Grand Albert, Dragon Rouge, c.1750–1800)">
  <circle cx="378" cy="274" r="6" fill="#7296a8" opacity=".8"/>
  <text x="388" y="271" fill="#eee8d7" font-size="10" font-family="Georgia">Lyon</text>
</g>
<!-- Treviso 45.67N 12.24E → x=471 y=276 -->
<g class="map-dot" data-city="Treviso" data-events="Ficino's Pimander (Corpus Hermeticum) first printed (1471)">
  <circle cx="471" cy="277" r="5" fill="#d0a94f" opacity=".75"/>
  <text x="481" y="274" fill="#eee8d7" font-size="10" font-family="Georgia">Treviso</text>
</g>
<!-- Oxford 51.75N -1.26E → x=311 y=192 -->
<g class="map-dot" data-city="Oxford" data-events="Owen Davies Grimoires published (2009)">
  <circle cx="311" cy="193" r="5" fill="#7296a8" opacity=".7"/>
  <text x="321" y="190" fill="#eee8d7" font-size="10" font-family="Georgia">Oxford</text>
</g>
<!-- Legend -->
<g transform="translate(20,420)">
  <rect x="0" y="0" width="180" height="95" rx="5" fill="#181915" opacity=".92" stroke="#4b442e"/>
  <text x="10" y="18" fill="#d0a94f" font-size="11" font-family="Georgia" font-weight="bold">Events by period</text>
  <circle cx="18" cy="35" r="5" fill="#d0a94f"/>
  <text x="28" y="39" fill="#b8ad94" font-size="10" font-family="Georgia">Renaissance (c.1400–1600)</text>
  <circle cx="18" cy="55" r="5" fill="#7296a8"/>
  <text x="28" y="59" fill="#b8ad94" font-size="10" font-family="Georgia">Early Modern (1600–1800)</text>
  <circle cx="18" cy="75" r="5" fill="#7aa36b"/>
  <text x="28" y="79" fill="#b8ad94" font-size="10" font-family="Georgia">Modern scholarship</text>
</g>
</svg>"""


MAP_TOOLTIP_JS = """
(function(){
  var dots = document.querySelectorAll('.map-dot');
  var tip = document.createElement('div');
  tip.className = 'map-tooltip';
  document.body.appendChild(tip);
  dots.forEach(function(dot){
    dot.addEventListener('mouseenter', function(e){
      var city = dot.getAttribute('data-city');
      var evs = dot.getAttribute('data-events');
      tip.innerHTML = '<strong>' + city + '</strong><br>' + (evs||'').split(';').map(function(s){return s.trim()}).filter(Boolean).join('<br>');
      tip.style.display='block';
    });
    dot.addEventListener('mousemove', function(e){
      tip.style.left = (e.pageX+14)+'px';
      tip.style.top = (e.pageY-10)+'px';
    });
    dot.addEventListener('mouseleave', function(){
      tip.style.display='none';
    });
  });
})();
"""


RECEPTION_PERIODS = ("RENAISSANCE", "EARLY_MODERN")
RECEPTION_SCHOLARSHIP_IDS = {
    "spiritual_demonic_magic_walker", "giordano_bruno_hermetic_yates",
    "occult_philosophy_elizabethan_yates", "grimoires_history_davies",
    "book_of_oberon_edition", "making_magic_elizabethan", "magic_of_rogues",
    "the_magus_barrett",
}
RECEPTION_CONCEPT_SLUGS = {
    "renaissance_magic", "hermeticism", "prisca_theologia", "magia_naturalis_concept",
    "yates_thesis", "occult_philosophy", "grimoire_printing_history",
    "vernacular_grimoire_tradition", "neoplatonism_and_magic", "enochian_system",
    "print_culture_and_magic", "kabbalism_renaissance_magic", "spiritual_magic_walker",
    "reformation_and_magic", "rosicrucian_movement",
}


def period_badge(period):
    if not period:
        return ""
    p = period.upper()
    css = {"RENAISSANCE": "badge-renaissance", "EARLY_MODERN": "badge-early_modern", "MODERN": "badge-modern"}.get(p, "")
    label = period.replace("_", " ").title()
    return f"<span class='period-badge {css}'>{label}</span>"


def generate_reception(target, conn):
    """Generate the Grimoires in Reception section page."""
    texts = conn.execute(
        "SELECT * FROM texts WHERE period IN ('RENAISSANCE','EARLY_MODERN') OR text_id IN ("
        + ",".join(f"'{x}'" for x in RECEPTION_SCHOLARSHIP_IDS)
        + ") ORDER BY period, title"
    ).fetchall()
    persons = conn.execute(
        "SELECT * FROM persons WHERE era IN ('RENAISSANCE','EARLY_MODERN') ORDER BY era, name"
    ).fetchall()
    modern_scholars = conn.execute(
        """SELECT DISTINCT p.* FROM persons p
           JOIN person_text_roles r ON r.person_id = p.id
           JOIN texts t ON t.id = r.text_id
           WHERE p.era = 'MODERN'
           AND (t.text_id IN ("""
        + ",".join(f"'{x}'" for x in RECEPTION_SCHOLARSHIP_IDS)
        + """) OR t.period IN ('RENAISSANCE','EARLY_MODERN'))
           ORDER BY p.name"""
    ).fetchall()
    concepts = conn.execute(
        "SELECT * FROM concepts WHERE slug IN ("
        + ",".join(f"'{x}'" for x in RECEPTION_CONCEPT_SLUGS)
        + ") ORDER BY label"
    ).fetchall()
    events = conn.execute(
        "SELECT * FROM timeline_events WHERE year >= 1438 ORDER BY year"
    ).fetchall()

    def rec_cards_texts(rows):
        out = ["<div class='grid'>"]
        for row in rows:
            href = f"texts/{row['text_id']}.html"
            meta = " / ".join(x for x in [row["text_type"], row["period"], row["language"]] if x)
            badge = period_badge(row["period"])
            out.append(
                f"<a class='card' href='{href}'>"
                f"<div class='card-title'>{clean(row['title'])}{badge}</div>"
                f"<div class='meta'>{clean(meta)}</div>"
                f"<div class='desc'>{clean(row['description'])}</div></a>"
            )
        out.append("</div>")
        return "\n".join(out)

    def rec_cards_persons(rows):
        out = ["<div class='grid'>"]
        for row in rows:
            href = f"persons/{row['person_id']}.html"
            meta = " / ".join(x for x in [row["role_primary"], row["era"]] if x)
            badge = period_badge(row["era"])
            out.append(
                f"<a class='card' href='{href}'>"
                f"<div class='card-title'>{clean(row['name'])}{badge}</div>"
                f"<div class='meta'>{clean(meta)}</div>"
                f"<div class='desc'>{clean(row['description'])}</div></a>"
            )
        out.append("</div>")
        return "\n".join(out)

    def rec_cards_concepts(rows):
        out = ["<div class='grid'>"]
        for row in rows:
            href = f"concepts/{row['slug']}.html"
            meta = " / ".join(x for x in [row["category_type"], row["category"]] if x)
            out.append(
                f"<a class='card' href='{href}'>"
                f"<div class='card-title'>{clean(row['label'])}</div>"
                f"<div class='meta'>{clean(meta)}</div>"
                f"<div class='desc'>{clean(row['definition_short'] or row['significance'])}</div></a>"
            )
        out.append("</div>")
        return "\n".join(out)

    def timeline_entries(rows):
        out = []
        for ev in rows:
            year_str = str(ev["year"])
            if ev["year_end"]:
                year_str += f"–{ev['year_end']}"
            loc = f" &middot; {clean(ev['location'])}" if ev["location"] else ""
            out.append(
                f"<div class='timeline-entry'>"
                f"<div class='timeline-year'>{year_str}{loc}</div>"
                f"<div class='timeline-title'>{clean(ev['title'])}</div>"
                f"<div class='timeline-desc'>{clean((ev['description'] or '')[:300]) + ('...' if len(ev['description'] or '') > 300 else '')}</div>"
                f"</div>"
            )
        return "\n".join(out)

    total_persons = len(persons) + len(modern_scholars)
    stats_html = (
        f"<div class='stats'>"
        f"<div class='stat'><strong>{len(texts)}</strong>Texts &amp; Editions</div>"
        f"<div class='stat'><strong>{total_persons}</strong>Persons</div>"
        f"<div class='stat'><strong>{len(concepts)}</strong>Concepts</div>"
        f"<div class='stat'><strong>{len(events)}</strong>Timeline Events</div>"
        f"</div>"
    )

    content = f"""
<section class='hero'>
<div class='hero-inner'>
<h1>Grimoires in Reception</h1>
<p class='subtitle'>How medieval magical texts were transmitted, transformed, and reinvented in the Renaissance and early modern period — from Ficino and Pico to Agrippa, Trithemius, Dee, and the print tradition through Mathers, Peterson, and Owen Davies.</p>
</div>
</section>
<main>
{stats_html}

<section class='prose' style='margin-bottom:28px'>
<p>The reception of medieval grimoires in the Renaissance and early modern period is one of the most contested questions in the historiography of Western magic. Frances Yates argued in <i>Giordano Bruno and the Hermetic Tradition</i> (1964) that Marsilio Ficino and Giovanni Pico della Mirandola inaugurated a distinctly new, philosophically sophisticated magical tradition — a sanitized Hermetic-natural magic that broke cleanly from what she saw as the cruder demonic operations of medieval learned practice. Frank Klaassen's manuscript evidence in <i>The Transformations of Magic</i> (2013) challenges this narrative directly: the overwhelming bulk of practical magic manuscripts from the sixteenth century is continuous with medieval ritual traditions, and the great Renaissance occultists — Agrippa, Trithemius, Dee — worked squarely within those traditions rather than against them. D.P. Walker's <i>Spiritual and Demonic Magic</i> (1958) provided the nuanced framework between these positions, showing that Ficino's natural magic was genuinely magical (not merely metaphorical) while attempting to operate below the demonic threshold. This section traces the textual, biographical, and conceptual lineages of grimoire reception from the Florentine Platonic Academy to the modern editorial tradition of Joseph Peterson and Dan Harms.</p>
</section>

<h2>Scholarly Map: Key Sites of Reception</h2>
<div class='map-container' style='position:relative'>
{EUROPE_MAP_SVG}
</div>
<p style='color:var(--muted);font-size:13px;margin-top:8px'>Hover over dots to see key events at each location. Dot size indicates relative density of events.</p>

<h2>Figures of the Renaissance and Early Modern Reception ({len(persons)} entries)</h2>
{rec_cards_persons(persons)}

<h2>Modern Scholars of the Reception ({len(modern_scholars)} entries)</h2>
{rec_cards_persons(modern_scholars)}

<h2>Primary Sources and Scholarship ({len(texts)} entries)</h2>
{rec_cards_texts(texts)}

<h2>Concepts and Historiographical Categories ({len(concepts)} entries)</h2>
{rec_cards_concepts(concepts)}

<h2>Timeline: From Plethon to Peterson</h2>
<div style='border-left:2px solid var(--line);padding-left:4px;margin:20px 0'>
{timeline_entries(events)}
</div>

</main>
<script>{MAP_TOOLTIP_JS}</script>
"""
    write(target / "reception.html", page("Grimoires in Reception", content, active="reception"))
    total_cards = len(texts) + len(persons) + len(modern_scholars) + len(concepts)
    print(f"Generated reception.html ({len(texts)} texts, {len(persons)+len(modern_scholars)} persons, {len(concepts)} concepts, {len(events)} timeline events, {total_cards} total cards)")


def generate(target):
    if target.exists():
        shutil.rmtree(target)
    (target / "assets").mkdir(parents=True, exist_ok=True)
    write(target / "assets" / "manuscript-field.svg", ASSET)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ["texts", "persons", "concepts", "bibliography", "timeline_events"]}
    reception_count = conn.execute(
        "SELECT COUNT(*) FROM texts WHERE period IN ('RENAISSANCE','EARLY_MODERN')"
    ).fetchone()[0]
    hero = f"""
    <section class='hero'><div class='hero-inner'><h1>MedievalMagicDB</h1><p class='subtitle'>A scholarly portal for medieval magic, learned ritual texts, astral image theory, necromancy, manuscript culture, and modern historiography.</p></div></section>
    <main><div class='stats'>{''.join(f"<div class='stat'><strong>{v}</strong>{k.replace('_',' ').title()}</div>" for k,v in counts.items())}</div>
    <h2>Research Gateways</h2><div class='grid'>
    <a class='card' href='concepts.html'><div class='card-title'>Concepts</div><div class='desc'>Actor terms and analyst categories, kept deliberately distinct.</div></a>
    <a class='card' href='texts.html'><div class='card-title'>Texts</div><div class='desc'>Primary sources, editions, scholarship, and manuscript-centered studies.</div></a>
    <a class='card' href='reception.html'><div class='card-title'>Grimoires in Reception</div><div class='meta'>New section</div><div class='desc'>Renaissance and early modern reception of medieval grimoires: Ficino, Agrippa, Trithemius, Dee, the Yates thesis, the printing press, and the modern editorial tradition (Peterson, Harms, Davies). Includes mapped timeline.</div></a>
    <a class='card' href='bibliography.html'><div class='card-title'>Converted Corpus</div><div class='desc'>PDF-derived Markdown sources with extraction metadata.</div></a>
    <a class='card' href='timeline.html'><div class='card-title'>Timeline</div><div class='desc'>Dated events in textual transmission, publication, condemnation, and historiography from the 9th century to the present.</div></a>
    </div></main>
    """
    write(target / "index.html", page("Home", hero))

    generate_reception(target, conn)

    rows = conn.execute("SELECT * FROM texts ORDER BY title").fetchall()
    write(target / "texts.html", list_page("Texts", "Primary sources, editions, translations, and scholarship.", rows, "texts"))
    for row in rows:
        body = row["analysis_html"] or f"<p>{clean(row['description'])}</p><h2>Research Status</h2><p>This entry has been seeded and awaits encyclopedia-length expansion from the Markdown corpus and bibliography.</p>"
        people = conn.execute("""
            SELECT p.name, r.role, p.person_id
            FROM person_text_roles r JOIN persons p ON p.id = r.person_id
            WHERE r.text_id = ? ORDER BY p.name
        """, (row["id"],)).fetchall()
        concepts = conn.execute("""
            SELECT c.label, c.category_type, c.slug
            FROM concept_text_refs r JOIN concepts c ON c.id = r.concept_id
            WHERE r.text_id = ? ORDER BY c.label
        """, (row["id"],)).fetchall()
        related = related_block("Related People", [(p["name"], p["role"], f"../persons/{p['person_id']}.html") for p in people])
        related += related_block("Related Concepts", [(c["label"], c["category_type"], f"../concepts/{c['slug']}.html") for c in concepts])
        write(target / "texts" / f"{row['text_id']}.html", detail_page("texts", row["title"], f"{row['text_type']} / {row['period']} / {row['language']}", body, related))

    rows = conn.execute("SELECT * FROM persons ORDER BY name").fetchall()
    write(target / "persons.html", list_page("Persons", "Historical actors, attributed authorities, translators, editors, and modern scholars.", rows, "persons"))
    for row in rows:
        body = row["bio_html"] or f"<p>{clean(row['description'])}</p><h2>Research Status</h2><p>This person record is seeded for future biography enrichment.</p>"
        texts = conn.execute("""
            SELECT t.title, r.role, t.text_id
            FROM person_text_roles r JOIN texts t ON t.id = r.text_id
            WHERE r.person_id = ? ORDER BY t.title
        """, (row["id"],)).fetchall()
        related = related_block("Related Texts", [(t["title"], t["role"], f"../texts/{t['text_id']}.html") for t in texts])
        write(target / "persons" / f"{row['person_id']}.html", detail_page("persons", row["name"], f"{row['role_primary']} / {row['era']}", body, related))

    rows = conn.execute("SELECT * FROM concepts ORDER BY label").fetchall()
    write(target / "concepts.html", list_page("Concepts", "Actor terms, analyst terms, and hybrid categories in medieval magic scholarship.", rows, "concepts"))
    for row in rows:
        body = row["definition_long"] or f"<p>{clean(row['definition_short'] or row['significance'])}</p><h2>Research Status</h2><p>This concept record is seeded for future DGWE-style expansion.</p>"
        texts = conn.execute("""
            SELECT t.title, t.text_type, t.text_id
            FROM concept_text_refs r JOIN texts t ON t.id = r.text_id
            WHERE r.concept_id = ? ORDER BY t.title
        """, (row["id"],)).fetchall()
        linked = conn.execute("""
            SELECT c.label, l.relationship, c.slug
            FROM concept_links l JOIN concepts c ON c.id = l.to_concept_id
            WHERE l.from_concept_id = ?
            UNION
            SELECT c.label, l.relationship, c.slug
            FROM concept_links l JOIN concepts c ON c.id = l.from_concept_id
            WHERE l.to_concept_id = ?
            ORDER BY label
        """, (row["id"], row["id"])).fetchall()
        related = related_block("Related Texts", [(t["title"], t["text_type"], f"../texts/{t['text_id']}.html") for t in texts])
        related += related_block("Related Concepts", [(c["label"], c["relationship"], f"../concepts/{c['slug']}.html") for c in linked])
        write(target / "concepts" / f"{row['slug']}.html", detail_page("concepts", row["label"], f"{row['category_type']} / {row['category']}", body, related))

    rows = conn.execute("SELECT * FROM bibliography ORDER BY author, year, title").fetchall()
    write(target / "bibliography.html", list_page("Bibliography", "Local PDF corpus and Markdown extraction metadata.", rows, "bibliography"))

    events = conn.execute("SELECT * FROM timeline_events ORDER BY year, title").fetchall()
    timeline = "<main><h1>Timeline</h1><p class='subtitle'>Granular events in textual transmission and modern scholarship.</p><section class='prose'>"
    for event in events:
        years = str(event["year"]) if not event["year_end"] else f"{event['year']}-{event['year_end']}"
        loc = f" &middot; {clean(event['location'])}" if event["location"] else ""
        timeline += f"<h2>{clean(years)}: {clean(event['title'])}</h2><p style='font-size:14px;color:var(--muted);margin-bottom:4px'>{event['event_type'] or ''}{loc}</p><p>{clean(event['description'] or '')}</p>"
    timeline += "</section></main>"
    write(target / "timeline.html", page("Timeline", timeline, active="timeline"))

    about = "<main><h1>Methodology</h1><section class='prose'><p>MedievalMagicDB treats medieval magic as a historiographical problem rather than a stable object. The site distinguishes actor terms from analyst terms, separates primary sources from modern scholarship, and keeps extraction metadata visible so database prose can remain source-aware.</p><p>The architecture is inherited from EmeraldTablet: SQLite is the source of truth, ingestion scripts are idempotent, agent drafts belong in staging, and generated pages are static HTML.</p><p>The Grimoires in Reception section (added May 2026) covers the Renaissance and early modern reception of medieval grimoires: the Ficinian Neoplatonist synthesis, Agrippa's <i>De Occulta Philosophia</i>, Trithemius's library and <i>Steganographia</i>, John Dee's angel conversations, the impact of the printing press on grimoire circulation, Frances Yates's Hermetic thesis and its revision by D.P. Walker and Frank Klaassen, and the modern editorial tradition of Joseph Peterson, Dan Harms, and Owen Davies. Timeline events are geo-coded for map display. Style requirements for reception entries follow STYLEGUIDE.md section 8 (Grimoire and Ritual-Text Entries) with additional guidance in STYLEGUIDE.md section 9 (Reception Section).</p></section></main>"
    write(target / "about.html", page("Methodology", about, active="about"))
    data = {name: [dict(r) for r in conn.execute(f"SELECT * FROM {name}").fetchall()] for name in ["texts", "persons", "concepts", "bibliography", "timeline_events"]}
    write(target / "data.json", json.dumps(data, indent=2, ensure_ascii=False))
    conn.close()


def main():
    ensure_dirs()
    generate(DOCS_DIR)
    generate(SITE_DIR)
    print(f"Generated {DOCS_DIR}")
    print(f"Generated {SITE_DIR}")


if __name__ == "__main__":
    main()

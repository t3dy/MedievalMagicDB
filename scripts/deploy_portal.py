import html
import json
import re
import shutil
import sqlite3
from pathlib import Path

from common import DB_PATH, DOCS_DIR, SITE_DIR, ensure_dirs


CSS = """
:root{--bg:#10100e;--panel:#181915;--panel2:#202118;--ink:#eee8d7;--muted:#b8ad94;--line:#4b442e;--gold:#d0a94f;--green:#7aa36b;--red:#b96b5f;--blue:#7296a8;--font:Georgia,'Times New Roman',serif;--ui:Inter,Segoe UI,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--ui);line-height:1.65}.nav{position:sticky;top:0;z-index:3;background:rgba(16,16,14,.94);border-bottom:1px solid var(--line);backdrop-filter:blur(10px)}.nav-inner{max-width:1180px;margin:0 auto;padding:14px 20px;display:flex;gap:18px;align-items:center;justify-content:space-between}.brand{font-family:var(--font);font-size:24px;color:var(--gold);text-decoration:none}.links{display:flex;gap:14px;flex-wrap:wrap}.links a{color:var(--ink);text-decoration:none;font-size:14px}.links a:hover{color:var(--gold)}.links a.active{color:var(--gold);border-bottom:1px solid var(--gold)}main{max-width:1180px;margin:0 auto;padding:42px 20px}.hero{min-height:360px;display:grid;align-content:end;padding:48px 20px;background:linear-gradient(rgba(16,16,14,.25),rgba(16,16,14,.92)),url('assets/manuscript-field.svg');background-size:cover;background-position:center;border-bottom:1px solid var(--line)}.hero-inner{max-width:1180px;margin:0 auto;width:100%}h1{font-family:var(--font);font-size:clamp(42px,7vw,82px);line-height:1;margin:0 0 14px;color:#f5d982;letter-spacing:0}h2{font-family:var(--font);font-size:30px;color:var(--gold);margin:34px 0 14px}.subtitle{font-size:19px;color:var(--muted);max-width:760px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;text-decoration:none;color:var(--ink);min-height:180px}.card:hover{border-color:var(--gold);background:var(--panel2)}.card-title{font-family:var(--font);font-size:23px;color:#f1d17c;line-height:1.15;margin-bottom:8px}.meta{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--gold);margin-bottom:10px}.desc{font-size:14px;color:var(--muted)}.prose{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:26px;font-family:var(--font);font-size:19px}.prose p{margin:0 0 18px}.toolbar{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 22px}.toolbar input,.toolbar select{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:10px 12px}.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:3px 9px;color:var(--muted);font-size:12px;margin-right:6px}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:30px 0}.stat{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px}.stat strong{display:block;font-family:var(--font);font-size:34px;color:var(--gold)}footer{border-top:1px solid var(--line);padding:36px 20px;text-align:center;color:var(--muted)}.map-container{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px;margin:28px 0;overflow:hidden}.map-container svg{width:100%;height:auto;display:block}.map-dot{cursor:pointer}.map-dot:hover circle{fill:var(--gold)!important}.map-tooltip{position:absolute;background:var(--panel2);border:1px solid var(--line);border-radius:6px;padding:10px 14px;font-size:13px;max-width:280px;pointer-events:none;display:none;z-index:10}.timeline-entry{border-left:2px solid var(--line);padding:0 0 28px 20px;position:relative}.timeline-entry::before{content:'';position:absolute;left:-5px;top:4px;width:8px;height:8px;border-radius:50%;background:var(--gold)}.timeline-year{font-family:var(--font);color:var(--gold);font-size:22px;margin:0 0 6px}.timeline-title{font-weight:600;margin:0 0 4px}.timeline-desc{font-size:14px;color:var(--muted)}.period-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;text-transform:uppercase;letter-spacing:.07em;margin-left:8px}.badge-renaissance{background:#2a3820;color:#7aa36b}.badge-early_modern{background:#1e2a38;color:#7296a8}.badge-modern{background:#2a2018;color:#d0a94f}.map-controls{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}.map-btn{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:8px 14px;color:var(--muted);cursor:pointer;font-size:13px;font-family:var(--ui);transition:border-color .15s,color .15s}.map-btn:hover{border-color:var(--gold);color:var(--ink)}.map-btn.active{background:var(--panel2);border-color:var(--gold);color:var(--gold)}.section-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;text-transform:uppercase;letter-spacing:.07em;margin-left:6px}.badge-solomonic{background:#241830;color:#9b7ec8}.badge-scholasticism{background:#1a2418;color:#6a9b6a}
"""

ASSET = """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="700" viewBox="0 0 1600 700"><rect width="1600" height="700" fill="#17160f"/><g opacity=".18" fill="none" stroke="#d0a94f" stroke-width="2"><path d="M120 120c170 90 320 90 490 0s320-90 490 0 320 90 430 10"/><path d="M90 250h1420M90 330h1420M90 410h1420M90 490h1420"/><circle cx="340" cy="348" r="82"/><circle cx="340" cy="348" r="47"/><path d="M820 190l95 250 95-250M780 440h270"/><path d="M1170 240c80-58 170-58 250 0-80 58-170 58-250 0z"/><path d="M1295 170v150M1220 245h150"/></g><g opacity=".22" fill="#efe0b4" font-family="Georgia" font-size="38"><text x="130" y="610">ars notoria</text><text x="560" y="95">nigromantia</text><text x="1040" y="600">scientia imaginum</text></g></svg>"""


def clean(value):
    return html.escape(value or "")


def page(title, content, prefix="", active=""):
    active_class = lambda name: " class='active'" if active == name else ""
    nav = """
    <nav class="nav"><div class="nav-inner"><a class="brand" href="{0}index.html">MedievalMagicDB</a><div class="links">
    <a href="{0}texts.html"{1}>Texts</a><a href="{0}persons.html"{2}>Persons</a><a href="{0}concepts.html"{3}>Concepts</a><a href="{0}reception.html"{4}>Reception</a><a href="{0}solomonic.html"{5}>Solomonic</a><a href="{0}scholasticism.html"{6}>Scholasticism</a><a href="{0}bibliography.html"{7}>Bibliography</a><a href="{0}timeline.html"{8}>Timeline</a><a href="{0}about.html"{9}>Methodology</a>
    </div></div></nav>
    """.format(
        prefix,
        active_class("texts"), active_class("persons"), active_class("concepts"),
        active_class("reception"), active_class("solomonic"), active_class("scholasticism"),
        active_class("bibliography"), active_class("timeline"), active_class("about"),
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


# Projection: x=(lon+15)/75*1000  y=(65-lat)/55*600  (lon -15→60, lat 65→10, svg 1000x600)
WIDE_MAP_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" id="wide-map" style="background:#0d1520;border-radius:6px">
<defs><filter id="glow2"><feGaussianBlur stdDeviation="2" result="cb"/><feMerge><feMergeNode in="cb"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g opacity=".32" fill="none" stroke="#4b442e" stroke-width="1">
  <!-- Ireland -->
  <path d="M80,147 Q88,130 100,115 Q112,106 120,118 Q124,133 118,148 Q112,163 100,170 Q88,163 80,147 Z"/>
  <!-- England / Scotland schematic -->
  <path d="M124,164 Q138,156 150,148 Q168,141 192,144 Q220,148 222,156 Q215,165 200,162 Q185,158 170,160 Q152,162 138,168 Z"/>
  <path d="M178,144 Q176,125 174,106 Q172,92 176,80 Q182,75 184,88 Q182,106 180,125 Q178,136 178,144 Z"/>
  <!-- Iberian Peninsula -->
  <path d="M80,305 Q86,276 92,250 Q96,234 106,225 Q120,218 142,217 Q165,217 190,227 Q212,237 238,246 Q242,264 235,283 Q224,305 206,318 Q184,330 160,330 Q135,326 114,315 Q92,305 80,305 Z"/>
  <!-- France -->
  <path d="M136,183 Q156,174 188,172 Q213,170 232,177 Q254,185 270,193 Q295,200 315,212 Q320,228 312,243 Q297,252 276,252 Q256,250 238,246 Q220,240 204,230 Q185,220 165,210 Q148,200 136,183 Z"/>
  <!-- Low Countries -->
  <path d="M264,150 Q282,144 302,146 Q314,154 308,164 Q294,170 275,166 Q263,160 264,150 Z"/>
  <!-- German lands -->
  <path d="M312,164 Q346,150 380,148 Q408,148 430,159 Q450,172 448,190 Q440,208 422,216 Q402,222 380,218 Q358,212 338,202 Q318,190 312,164 Z"/>
  <!-- Scandinavia S -->
  <path d="M296,142 Q312,124 326,110 Q334,100 332,88 Q324,82 316,92 Q308,106 300,120 Q294,132 290,142 Z"/>
  <path d="M332,88 Q348,76 362,70 Q374,65 375,78 Q368,92 354,102 Q340,110 332,100 Z"/>
  <!-- Italy -->
  <path d="M318,224 Q340,218 364,218 Q386,226 396,242 Q402,260 394,280 Q380,304 365,330 Q352,352 342,362 Q330,354 328,334 Q325,312 328,290 Q325,260 318,224 Z"/>
  <!-- Sicily -->
  <path d="M368,364 Q384,358 400,366 Q404,378 390,384 Q374,382 368,368 Z"/>
  <!-- Balkans / Greece -->
  <path d="M486,290 Q508,278 530,280 Q550,286 554,302 Q546,318 528,320 Q510,318 500,307 Z"/>
  <!-- Anatolia / Turkey -->
  <path d="M558,262 Q602,250 645,248 Q688,251 718,262 Q740,274 737,287 Q722,298 696,300 Q665,298 636,290 Q604,280 575,272 Q557,268 558,262 Z"/>
  <!-- North Africa coast -->
  <path d="M122,318 Q178,355 244,362 Q315,368 385,364 Q455,358 515,350 Q558,343 598,342"/>
  <!-- Eastern Med / Levant coast -->
  <path d="M598,342 Q626,354 650,364 Q668,370 680,358 Q684,344 680,328 Q676,314 682,305"/>
  <!-- Turkey S coast + Aegean -->
  <path d="M486,292 Q528,314 558,324 Q582,328 612,312 Q636,300 682,305"/>
  <!-- Mesopotamia / Iraq schematic -->
  <path d="M682,305 Q720,314 752,322 Q785,330 812,344 Q828,355 820,365 Q800,370 778,362 Q752,352 732,340"/>
</g>
<!-- Lat/lon grid -->
<g opacity=".08" fill="none" stroke="#d0a94f" stroke-width=".5">
  <line x1="0" y1="55" x2="1000" y2="55"/><line x1="0" y1="109" x2="1000" y2="109"/>
  <line x1="0" y1="164" x2="1000" y2="164"/><line x1="0" y1="218" x2="1000" y2="218"/>
  <line x1="0" y1="273" x2="1000" y2="273"/><line x1="0" y1="327" x2="1000" y2="327"/>
  <line x1="0" y1="382" x2="1000" y2="382"/>
  <line x1="200" y1="0" x2="200" y2="600"/><line x1="333" y1="0" x2="333" y2="600"/>
  <line x1="467" y1="0" x2="467" y2="600"/><line x1="600" y1="0" x2="600" y2="600"/>
  <line x1="733" y1="0" x2="733" y2="600"/><line x1="867" y1="0" x2="867" y2="600"/>
</g>
<!-- Grid labels -->
<g fill="#4b442e" font-size="9" font-family="Georgia" opacity=".6">
  <text x="202" y="11">0°E</text><text x="335" y="11">10°E</text><text x="469" y="11">20°E</text>
  <text x="602" y="11">30°E</text><text x="735" y="11">40°E</text><text x="869" y="11">50°E</text>
  <text x="975" y="57">60°N</text><text x="975" y="111">55°N</text><text x="975" y="166">50°N</text>
  <text x="975" y="275">40°N</text><text x="975" y="329">35°N</text><text x="975" y="384">30°N</text>
</g>
<!-- DOTS — Projection: x=(lon+15)/75*1000  y=(65-lat)/55*600
     Colours: gold=#d0a94f multi-hub  blue=#7296a8 reception  green=#7aa36b solomonic  red=#b96b5f scholasticism -->
<!-- London 51.51N -0.13E x=198 y=147 -->
<g class="map-dot" data-section="reception solomonic" data-city="London"
   data-events="Dee at Mortlake; Scot Discoverie (1584); Mathers Key of Solomon (1888); Gollancz Hebrew Key (1914); Barrett The Magus (1801); Walker Spiritual Magic (1958); Yates Bruno (1964)">
  <circle cx="198" cy="147" r="9" fill="#d0a94f" opacity=".9" filter="url(#glow2)"/>
  <text x="208" y="144" fill="#eee8d7" font-size="10" font-family="Georgia">London</text>
</g>
<!-- Oxford 51.75N -1.26E x=183 y=145 -->
<g class="map-dot" data-section="reception solomonic scholasticism" data-city="Oxford"
   data-events="Bacon's experimental philosophy (c.1260s); Ashmole collects Solomonic MSS (1641–92); Davies Grimoires (2009)">
  <circle cx="183" cy="145" r="7" fill="#d0a94f" opacity=".85" filter="url(#glow2)"/>
  <text x="155" y="142" fill="#eee8d7" font-size="10" font-family="Georgia">Oxford</text>
</g>
<!-- Cambridge UK 52.21N 0.12E x=202 y=140 -->
<g class="map-dot" data-section="solomonic" data-city="Cambridge (UK)"
   data-events="Bohak Ancient Jewish Magic (Cambridge UP, 2008); Duling OTP translation (1983)">
  <circle cx="202" cy="140" r="5" fill="#7aa36b" opacity=".8"/>
</g>
<!-- Leiden 52.16N 4.49E x=260 y=141 -->
<g class="map-dot" data-section="solomonic" data-city="Leiden"
   data-events="Torijano Solomon the Esoteric King (Brill, 2002)">
  <circle cx="260" cy="141" r="5" fill="#7aa36b" opacity=".8"/>
  <text x="265" y="138" fill="#eee8d7" font-size="10" font-family="Georgia">Leiden</text>
</g>
<!-- Antwerp 51.22N 4.40E x=259 y=150 -->
<g class="map-dot" data-section="reception" data-city="Antwerp"
   data-events="Dee publishes Monas Hieroglyphica (1564)">
  <circle cx="259" cy="150" r="5" fill="#7296a8" opacity=".78"/>
</g>
<!-- Paris 48.85N 2.35E x=231 y=176 -->
<g class="map-dot" data-section="reception solomonic scholasticism" data-city="Paris"
   data-events="French popular grimoire tradition (c.1750); Clavicula Salomonis circulates (c.1250–1320); William of Auvergne condemns Solomonic arts (1230s); Aquinas Summa theologiae (1265–74); Tempier condemnations 1270 and 1277; Oresme critiques astrology (1360s)">
  <circle cx="231" cy="176" r="9" fill="#d0a94f" opacity=".9" filter="url(#glow2)"/>
  <text x="238" y="173" fill="#eee8d7" font-size="10" font-family="Georgia">Paris</text>
</g>
<!-- Cologne 50.93N 6.95E x=293 y=153 -->
<g class="map-dot" data-section="reception scholasticism" data-city="Cologne"
   data-events="Agrippa De Occulta Philosophia published (1531); Albertus Magnus natural philosophy (1248–64)">
  <circle cx="293" cy="153" r="7" fill="#d0a94f" opacity=".85" filter="url(#glow2)"/>
  <text x="300" y="150" fill="#eee8d7" font-size="10" font-family="Georgia">Cologne</text>
</g>
<!-- Sponheim 49.84N 7.91E x=305 y=166 -->
<g class="map-dot" data-section="reception" data-city="Sponheim"
   data-events="Trithemius abbot (1483–1505); Steganographia composed (c.1499)">
  <circle cx="305" cy="166" r="6" fill="#7aa36b" opacity=".8" filter="url(#glow2)"/>
  <text x="312" y="163" fill="#eee8d7" font-size="10" font-family="Georgia">Sponheim</text>
</g>
<!-- Frankfurt 50.11N 8.68E x=315 y=162 -->
<g class="map-dot" data-section="reception" data-city="Frankfurt"
   data-events="Steganographia first printed (1606)">
  <circle cx="315" cy="162" r="5" fill="#7296a8" opacity=".75"/>
  <text x="322" y="159" fill="#eee8d7" font-size="10" font-family="Georgia">Frankfurt</text>
</g>
<!-- Speyer 49.32N 8.44E x=312 y=173 -->
<g class="map-dot" data-section="scholasticism" data-city="Speyer"
   data-events="Malleus Maleficarum first printed (1487)">
  <circle cx="312" cy="173" r="5" fill="#b96b5f" opacity=".8"/>
</g>
<!-- Kassel 51.31N 9.48E x=326 y=149 -->
<g class="map-dot" data-section="reception" data-city="Kassel"
   data-events="Rosicrucian Fama Fraternitatis published (1614)">
  <circle cx="326" cy="149" r="5" fill="#7aa36b" opacity=".78"/>
  <text x="332" y="146" fill="#eee8d7" font-size="10" font-family="Georgia">Kassel</text>
</g>
<!-- Würzburg 49.79N 9.93E x=332 y=167 -->
<g class="map-dot" data-section="reception" data-city="Würzburg"
   data-events="Trithemius: St James Abbey; died 1516; library inventory survives">
  <circle cx="332" cy="167" r="5" fill="#7aa36b" opacity=".75"/>
</g>
<!-- Marburg 50.80N 8.77E x=317 y=153 -->
<g class="map-dot" data-section="reception" data-city="Marburg"
   data-events="Fourth Book of Occult Philosophy printed (1559)">
  <circle cx="317" cy="153" r="4" fill="#7296a8" opacity=".72"/>
</g>
<!-- Munich 48.14N 11.58E x=355 y=185 -->
<g class="map-dot" data-section="solomonic" data-city="Munich"
   data-events="Hartlieb classifies Solomonic arts for Duke Albrecht of Bavaria (1456)">
  <circle cx="355" cy="185" r="5" fill="#7aa36b" opacity=".8"/>
  <text x="362" y="182" fill="#eee8d7" font-size="10" font-family="Georgia">Munich</text>
</g>
<!-- Basel 47.56N 7.59E x=301 y=190 -->
<g class="map-dot" data-section="reception" data-city="Basel"
   data-events="Weyer De Praestigiis Daemonum (1563); Arbatel de Magia Veterum printed (1575)">
  <circle cx="301" cy="190" r="6" fill="#7296a8" opacity=".82" filter="url(#glow2)"/>
  <text x="308" y="187" fill="#eee8d7" font-size="10" font-family="Georgia">Basel</text>
</g>
<!-- Treviso 45.67N 12.24E x=363 y=210 -->
<g class="map-dot" data-section="reception" data-city="Treviso"
   data-events="Ficino's Pimander (Corpus Hermeticum) first printed (1471)">
  <circle cx="363" cy="210" r="5" fill="#d0a94f" opacity=".75"/>
  <text x="370" y="207" fill="#eee8d7" font-size="10" font-family="Georgia">Treviso</text>
</g>
<!-- Padua 45.41N 11.88E x=359 y=213 -->
<g class="map-dot" data-section="scholasticism" data-city="Padua"
   data-events="Pietro d'Abano's Conciliator (c.1310); Pietro d'Abano tried by Inquisition (1315–17)">
  <circle cx="359" cy="213" r="6" fill="#b96b5f" opacity=".82" filter="url(#glow2)"/>
  <text x="366" y="223" fill="#eee8d7" font-size="10" font-family="Georgia">Padua</text>
</g>
<!-- Florence 43.77N 11.26E x=350 y=231 -->
<g class="map-dot" data-section="reception scholasticism" data-city="Florence"
   data-events="Council of Florence / Plethon (1438); Ficino translates Corpus Hermeticum (1463); Pico's context (1486); De Vita Coelitus Comparanda (1489); Cecco d'Ascoli burned (1327)">
  <circle cx="350" cy="231" r="8" fill="#d0a94f" opacity=".88" filter="url(#glow2)"/>
  <text x="358" y="228" fill="#eee8d7" font-size="10" font-family="Georgia">Florence</text>
</g>
<!-- Rome 41.9N 12.5E x=367 y=252 -->
<g class="map-dot" data-section="reception" data-city="Rome"
   data-events="Pico's 900 Theses published (1486); Giordano Bruno burned (1600)">
  <circle cx="367" cy="252" r="6" fill="#b96b5f" opacity=".82" filter="url(#glow2)"/>
  <text x="374" y="249" fill="#eee8d7" font-size="10" font-family="Georgia">Rome</text>
</g>
<!-- Lyon 45.76N 4.84E x=265 y=209 -->
<g class="map-dot" data-section="reception" data-city="Lyon"
   data-events="French popular grimoire printing: Grand Albert, Dragon Rouge (c.1750–1800)">
  <circle cx="265" cy="209" r="5" fill="#7296a8" opacity=".78"/>
  <text x="272" y="206" fill="#eee8d7" font-size="10" font-family="Georgia">Lyon</text>
</g>
<!-- Naples 40.85N 14.27E x=390 y=264 -->
<g class="map-dot" data-section="reception solomonic" data-city="Naples"
   data-events="Della Porta's Magia Naturalis (1558); Liber Razielis at Aragonese court (c.1300–50)">
  <circle cx="390" cy="264" r="6" fill="#d0a94f" opacity=".82" filter="url(#glow2)"/>
  <text x="397" y="261" fill="#eee8d7" font-size="10" font-family="Georgia">Naples</text>
</g>
<!-- Seville 37.39N -5.99E x=120 y=301 -->
<g class="map-dot" data-section="scholasticism" data-city="Seville"
   data-events="Isidore of Seville: Etymologiae classifies the magical arts (c.623–636)">
  <circle cx="120" cy="301" r="6" fill="#b96b5f" opacity=".82" filter="url(#glow2)"/>
  <text x="127" y="298" fill="#eee8d7" font-size="10" font-family="Georgia">Seville</text>
</g>
<!-- Toledo 39.86N -4.03E x=146 y=274 -->
<g class="map-dot" data-section="solomonic" data-city="Toledo"
   data-events="Arabic and Hebrew Solomonic texts translated into Latin (c.1150–1220); Translators include Gerard of Cremona, Michael Scot">
  <circle cx="146" cy="274" r="6" fill="#7aa36b" opacity=".82" filter="url(#glow2)"/>
  <text x="153" y="271" fill="#eee8d7" font-size="10" font-family="Georgia">Toledo</text>
</g>
<!-- Hippo / Annaba 36.9N 7.77E x=307 y=306 -->
<g class="map-dot" data-section="scholasticism" data-city="Hippo Regius (Annaba)"
   data-events="Augustine of Hippo: City of God — foundational Christian demonology (c.415–426)">
  <circle cx="307" cy="306" r="6" fill="#b96b5f" opacity=".82" filter="url(#glow2)"/>
  <text x="314" y="303" fill="#eee8d7" font-size="10" font-family="Georgia">Hippo</text>
</g>
<!-- Constantinople 41.01N 28.98E x=586 y=262 -->
<g class="map-dot" data-section="solomonic" data-city="Constantinople"
   data-events="Byzantine Hygromanteia compiled (c.1000–1100); Solomonic tradition in Greek learned culture">
  <circle cx="586" cy="262" r="7" fill="#7aa36b" opacity=".85" filter="url(#glow2)"/>
  <text x="594" y="259" fill="#eee8d7" font-size="10" font-family="Georgia">Constantinople</text>
</g>
<!-- Jerusalem 31.78N 35.22E x=670 y=362 -->
<g class="map-dot" data-section="solomonic" data-city="Jerusalem"
   data-events="Legendary site of Solomon's Temple; Sepher ha-Razim compiled (c.700–900); origin of all Solomonic pseudepigraphic authority">
  <circle cx="670" cy="362" r="8" fill="#d0a94f" opacity=".9" filter="url(#glow2)"/>
  <text x="678" y="359" fill="#eee8d7" font-size="10" font-family="Georgia">Jerusalem</text>
</g>
<!-- Alexandria 31.2N 29.95E x=599 y=369 -->
<g class="map-dot" data-section="solomonic" data-city="Alexandria (Egypt)"
   data-events="Testament of Solomon compiled (c.200–500 CE); Christian demonological milieu">
  <circle cx="599" cy="369" r="6" fill="#7aa36b" opacity=".82" filter="url(#glow2)"/>
  <text x="607" y="366" fill="#eee8d7" font-size="10" font-family="Georgia">Alexandria</text>
</g>
<!-- Baghdad 33.34N 44.44E x=793 y=345 -->
<g class="map-dot" data-section="solomonic" data-city="Baghdad"
   data-events="Solomonic traditions in Islamic literature (c.850–1000); Ring of Sulayman in Arabic texts; Abbasid learned culture and Solomonic magic">
  <circle cx="793" cy="345" r="7" fill="#7aa36b" opacity=".85" filter="url(#glow2)"/>
  <text x="800" y="342" fill="#eee8d7" font-size="10" font-family="Georgia">Baghdad</text>
</g>
<!-- Sea labels -->
<g fill="#2a3545" font-size="11" font-family="Georgia" font-style="italic" opacity=".7">
  <text x="355" y="345">Mediterranean Sea</text>
  <text x="620" y="240">Black Sea</text>
</g>
</svg>"""


SECTION_MAP_JS = """
(function(){
  var VIEWS = {
    all:           {vb:'0 0 1000 600',   show:null},
    solomonic:     {vb:'0 50 1000 540',  show:'solomonic'},
    reception:     {vb:'80 80 420 250',  show:'reception'},
    scholasticism: {vb:'40 70 580 320',  show:'scholasticism'}
  };
  var svg = document.getElementById('wide-map');
  if(!svg) return;
  var dots = document.querySelectorAll('.map-dot');
  var btns = document.querySelectorAll('.map-btn');
  function setView(key){
    var v = VIEWS[key] || VIEWS.all;
    svg.setAttribute('viewBox', v.vb);
    dots.forEach(function(d){
      if(!v.show){ d.style.display=''; return; }
      var secs = (d.getAttribute('data-section')||'').split(' ');
      d.style.display = secs.indexOf(v.show)>-1 ? '' : 'none';
    });
    btns.forEach(function(b){ b.classList.toggle('active', b.getAttribute('data-view')===key); });
  }
  btns.forEach(function(b){ b.addEventListener('click', function(){ setView(b.getAttribute('data-view')); }); });
  var tip = document.createElement('div');
  tip.className = 'map-tooltip';
  document.body.appendChild(tip);
  dots.forEach(function(dot){
    dot.addEventListener('mouseenter', function(e){
      var city = dot.getAttribute('data-city');
      var evs = (dot.getAttribute('data-events')||'');
      tip.innerHTML = '<strong>'+city+'</strong><br>'+evs.split(';').map(function(s){return s.trim();}).filter(Boolean).join('<br>');
      tip.style.display='block';
    });
    dot.addEventListener('mousemove', function(e){ tip.style.left=(e.pageX+14)+'px'; tip.style.top=(e.pageY-10)+'px'; });
    dot.addEventListener('mouseleave', function(){ tip.style.display='none'; });
  });
  var active = document.querySelector('.map-btn.active');
  setView(active ? active.getAttribute('data-view') : 'all');
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


def map_controls_html(active_section="all"):
    sections = [("all", "All Events"), ("solomonic", "Solomonic"), ("reception", "Reception"), ("scholasticism", "Scholasticism")]
    btns = []
    for k, label in sections:
        cls = "map-btn active" if k == active_section else "map-btn"
        btns.append(f"<button class='{cls}' data-view='{k}'>{label}</button>")
    return "<div class='map-controls'>" + "".join(btns) + "</div>"


def map_block_html(active_section="all", title="Key Sites on the Map"):
    legend = (
        "<div style='display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:8px'>"
        "<span><span style='color:#d0a94f'>&#9679;</span> Major hub</span>"
        "<span><span style='color:#7296a8'>&#9679;</span> Reception</span>"
        "<span><span style='color:#7aa36b'>&#9679;</span> Solomonic</span>"
        "<span><span style='color:#b96b5f'>&#9679;</span> Scholasticism</span>"
        "</div>"
    )
    hint = "<p style='color:var(--muted);font-size:13px;margin-top:6px'>Hover dots for events. Toggle buttons zoom the map to each section's geographic region.</p>"
    return (
        f"<h2>{title}</h2>"
        f"<div class='map-container' style='position:relative'>"
        f"{map_controls_html(active_section)}"
        f"{WIDE_MAP_SVG}"
        f"</div>"
        f"{legend}{hint}"
    )


def _timeline_entries_html(rows):
    out = []
    for ev in rows:
        year_str = str(ev["year"])
        if ev["year_end"]:
            year_str += f"–{ev['year_end']}"
        loc = f" &middot; {clean(ev['location'])}" if ev["location"] else ""
        desc = ev["description"] or ""
        out.append(
            f"<div class='timeline-entry'>"
            f"<div class='timeline-year'>{year_str}{loc}</div>"
            f"<div class='timeline-title'>{clean(ev['title'])}</div>"
            f"<div class='timeline-desc'>{clean(desc[:300]) + ('...' if len(desc) > 300 else '')}</div>"
            f"</div>"
        )
    return "\n".join(out)


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

    def _cards(rows, kind):
        out = ["<div class='grid'>"]
        for row in rows:
            if kind == "texts":
                href = f"texts/{row['text_id']}.html"
                meta = " / ".join(x for x in [row["text_type"], row["period"], row["language"]] if x)
                title_html = f"{clean(row['title'])}{period_badge(row['period'])}"
                desc = row["description"]
            elif kind == "concepts":
                href = f"concepts/{row['slug']}.html"
                meta = " / ".join(x for x in [row["category_type"], row["category"]] if x)
                title_html = clean(row["label"])
                desc = row["definition_short"] or row["significance"]
            else:
                href = f"persons/{row['person_id']}.html"
                meta = " / ".join(x for x in [row["role_primary"], row["era"]] if x)
                title_html = f"{clean(row['name'])}{period_badge(row['era'])}"
                desc = row["description"]
            out.append(
                f"<a class='card' href='{href}'>"
                f"<div class='card-title'>{title_html}</div>"
                f"<div class='meta'>{clean(meta)}</div>"
                f"<div class='desc'>{clean(desc)}</div></a>"
            )
        out.append("</div>")
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

{map_block_html("reception", "Scholarly Map: Key Sites of Reception")}

<h2>Figures of the Renaissance and Early Modern Reception ({len(persons)} entries)</h2>
{_cards(persons, "persons")}

<h2>Modern Scholars of the Reception ({len(modern_scholars)} entries)</h2>
{_cards(modern_scholars, "persons")}

<h2>Primary Sources and Scholarship ({len(texts)} entries)</h2>
{_cards(texts, "texts")}

<h2>Concepts and Historiographical Categories ({len(concepts)} entries)</h2>
{_cards(concepts, "concepts")}

<h2>Timeline: From Plethon to Peterson</h2>
<div style='border-left:2px solid var(--line);padding-left:4px;margin:20px 0'>
{_timeline_entries_html(events)}
</div>

</main>
<script>{SECTION_MAP_JS}</script>
"""
    write(target / "reception.html", page("Grimoires in Reception", content, active="reception"))
    total_cards = len(texts) + len(persons) + len(modern_scholars) + len(concepts)
    print(f"Generated reception.html ({len(texts)} texts, {len(persons)+len(modern_scholars)} persons, {len(concepts)} concepts, {len(events)} timeline events, {total_cards} total cards)")


SOLOMONIC_TEXT_IDS = {
    "testament_of_solomon", "clavicula_salomonis", "hygromanteia", "liber_razielis",
    "ars_notoria", "liber_juratus_honorii", "lemegeton", "ars_goetia", "ars_almadel",
    "sepher_ha_razim", "mafteah_shelomoh", "solomon_esoteric_king",
    "ancient_jewish_magic", "ot_pseudepigrapha_vol1",
}
SOLOMONIC_PERSON_IDS = {
    "solomon", "raziel", "elias_ashmole", "pablo_torijano", "gideon_bohak",
    "dennis_duling", "herman_gollancz", "michael_morgan", "samuel_liddell_mathers",
    "joseph_peterson", "richard_kieckhefer", "frank_klaassen", "david_pingree",
    "don_c_skemer", "dan_harms",
}
SOLOMONIC_CONCEPT_SLUGS = {
    "solomonic_magic", "ring_of_solomon", "adjuration", "solomonic_authority",
    "spirit_catalogue", "pentacle_magic", "characters_and_seals", "pseudepigraphy",
    "angelic_invocation", "demonic_pact", "learned_magic", "grimoire",
}

SCHOLASTICISM_PERSON_IDS = {
    "augustine_of_hippo", "isidore_of_seville", "albertus_magnus", "roger_bacon",
    "thomas_aquinas", "william_of_auvergne", "nicole_oresme", "peter_abano",
    "cecco_d_ascoli", "michael_scot", "etienne_tempier", "john_of_salisbury",
    "hugh_of_saint_victor", "arnald_of_villanova", "thabit_ibn_qurra",
    "abu_mashar", "al_kindi",
}
SCHOLASTICISM_TEXT_IDS = {
    "summa_theologiae", "de_universo_william_auvergne", "speculum_astronomiae",
    "opus_majus", "de_mineralibus", "de_occultis_operibus_naturae",
    "etymologiae", "de_radiis", "de_imaginibus", "picatrix", "secretum_secretorum",
    "history_magic_experimental_science",
}
SCHOLASTICISM_CONCEPT_SLUGS = {
    "scholastic_classification", "university_condemnation", "demonology",
    "astral_image_magic", "divination", "superstitio", "natural_powers",
    "condemned_arts", "experimental_science", "learned_magic",
    "celestial_influence", "occult_properties", "prohibited_arts",
}


def _section_cards(rows, kind):
    out = ["<div class='grid'>"]
    for row in rows:
        if kind == "texts":
            href = f"texts/{row['text_id']}.html"
            meta = " / ".join(x for x in [row["text_type"], row["period"], row["language"]] if x)
            title_html = f"{clean(row['title'])}{period_badge(row['period'])}"
            desc = row["description"]
        elif kind == "concepts":
            href = f"concepts/{row['slug']}.html"
            meta = " / ".join(x for x in [row["category_type"], row["category"]] if x)
            title_html = clean(row["label"])
            desc = row["definition_short"] or row["significance"]
        else:
            href = f"persons/{row['person_id']}.html"
            meta = " / ".join(x for x in [row["role_primary"], row["era"]] if x)
            title_html = f"{clean(row['name'])}{period_badge(row['era'])}"
            desc = row["description"]
        out.append(
            f"<a class='card' href='{href}'>"
            f"<div class='card-title'>{title_html}</div>"
            f"<div class='meta'>{clean(meta)}</div>"
            f"<div class='desc'>{clean(desc)}</div></a>"
        )
    out.append("</div>")
    return "\n".join(out)


def generate_solomonic(target, conn):
    texts = conn.execute(
        "SELECT * FROM texts WHERE text_id IN ("
        + ",".join(f"'{x}'" for x in SOLOMONIC_TEXT_IDS)
        + ") ORDER BY period, title"
    ).fetchall()
    persons = conn.execute(
        "SELECT * FROM persons WHERE person_id IN ("
        + ",".join(f"'{x}'" for x in SOLOMONIC_PERSON_IDS)
        + ") ORDER BY era, name"
    ).fetchall()
    concepts = conn.execute(
        "SELECT * FROM concepts WHERE slug IN ("
        + ",".join(f"'{x}'" for x in SOLOMONIC_CONCEPT_SLUGS)
        + ") ORDER BY label"
    ).fetchall()
    events = conn.execute(
        "SELECT * FROM timeline_events WHERE section_tag='solomonic' ORDER BY year"
    ).fetchall()

    stats_html = (
        f"<div class='stats'>"
        f"<div class='stat'><strong>{len(texts)}</strong>Texts</div>"
        f"<div class='stat'><strong>{len(persons)}</strong>Persons</div>"
        f"<div class='stat'><strong>{len(concepts)}</strong>Concepts</div>"
        f"<div class='stat'><strong>{len(events)}</strong>Timeline Events</div>"
        f"</div>"
    )

    content = f"""
<section class='hero'>
<div class='hero-inner'>
<h1>Solomonic Magic</h1>
<p class='subtitle'>The grimoire tradition centered on the authority of Solomon: from the Testament of Solomon and Sepher ha-Razim through the Clavicula Salomonis manuscript families, Solomonic adjuration, spirit catalogues, and the Ring of Solomon — traced across Jewish, Christian, and Islamic textual cultures from late antiquity to the modern critical edition.</p>
</div>
</section>
<main>
{stats_html}

<section class='prose' style='margin-bottom:28px'>
<p>Solomonic magic is the largest and most historically consequential tradition in the Western magical grimoire corpus. Its authority derives from the biblical Solomon — king, builder of the Temple, master of wisdom — whose legendary powers over demons, spirits, and the natural world were elaborated in Jewish pseudepigraphic literature, Christian demonological writing, and Islamic Qur'anic tradition from the second century CE onward. The Testament of Solomon, compiled in the eastern Mediterranean between the second and fifth centuries CE, catalogues seventy-two demons bound by Solomon's divinely-given ring and establishes the genre of the Solomonic spirit catalogue. The Clavicula Salomonis (Key of Solomon), the Hygromanteia, the Liber Razielis, the Sepher ha-Razim, and the entire Lemegeton complex all operate under Solomonic pseudepigraphic authority. Pablo Torijano's <i>Solomon the Esoteric King</i> (Brill, 2002) provides the fullest account of how the biblical king was transformed into a magus across religious traditions; Gideon Bohak's <i>Ancient Jewish Magic</i> (Cambridge UP, 2008) grounds the Solomonic corpus in its late antique Jewish context. The map below shows the geographic span of the tradition from Jerusalem and Baghdad to the manuscript libraries of Paris, Florence, and London.</p>
</section>

{map_block_html("solomonic", "Map: Solomonic Tradition from Jerusalem to London")}

<h2>Key Figures ({len(persons)} entries)</h2>
{_section_cards(persons, "persons")}

<h2>Primary Sources and Scholarship ({len(texts)} entries)</h2>
{_section_cards(texts, "texts")}

<h2>Concepts and Categories ({len(concepts)} entries)</h2>
{_section_cards(concepts, "concepts")}

<h2>Timeline of the Solomonic Tradition</h2>
<div style='border-left:2px solid var(--line);padding-left:4px;margin:20px 0'>
{_timeline_entries_html(events)}
</div>

</main>
<script>{SECTION_MAP_JS}</script>
"""
    write(target / "solomonic.html", page("Solomonic Magic", content, active="solomonic"))
    print(f"Generated solomonic.html ({len(texts)} texts, {len(persons)} persons, {len(concepts)} concepts, {len(events)} events)")


def generate_scholasticism(target, conn):
    texts = conn.execute(
        "SELECT * FROM texts WHERE text_id IN ("
        + ",".join(f"'{x}'" for x in SCHOLASTICISM_TEXT_IDS)
        + ") ORDER BY period, title"
    ).fetchall()
    persons = conn.execute(
        "SELECT * FROM persons WHERE person_id IN ("
        + ",".join(f"'{x}'" for x in SCHOLASTICISM_PERSON_IDS)
        + ") ORDER BY era, name"
    ).fetchall()
    concepts = conn.execute(
        "SELECT * FROM concepts WHERE slug IN ("
        + ",".join(f"'{x}'" for x in SCHOLASTICISM_CONCEPT_SLUGS)
        + ") ORDER BY label"
    ).fetchall()
    events = conn.execute(
        "SELECT * FROM timeline_events WHERE section_tag='scholasticism' ORDER BY year"
    ).fetchall()

    stats_html = (
        f"<div class='stats'>"
        f"<div class='stat'><strong>{len(texts)}</strong>Texts</div>"
        f"<div class='stat'><strong>{len(persons)}</strong>Persons</div>"
        f"<div class='stat'><strong>{len(concepts)}</strong>Concepts</div>"
        f"<div class='stat'><strong>{len(events)}</strong>Timeline Events</div>"
        f"</div>"
    )

    content = f"""
<section class='hero'>
<div class='hero-inner'>
<h1>Scholasticism and Magic</h1>
<p class='subtitle'>How medieval universities and theologians classified, condemned, naturalized, and debated magic: from Augustine's demonology and Isidore's taxonomy through Albertus Magnus, Roger Bacon, Thomas Aquinas, Pietro d'Abano, and Nicole Oresme — the scholastic frameworks that shaped every subsequent discussion of learned magic.</p>
</div>
</section>
<main>
{stats_html}

<section class='prose' style='margin-bottom:28px'>
<p>The scholastic treatment of magic is inseparable from the broader project of medieval natural philosophy and theology. From Augustine's demonological framework in <i>De civitate Dei</i> (c.426) through Isidore's encyclopedic classification of divination arts in the <i>Etymologiae</i> (c.636), through the great thirteenth-century syntheses of William of Auvergne, Albertus Magnus, and Thomas Aquinas, and into the contested naturalism of Pietro d'Abano, Cecco d'Ascoli, and Nicole Oresme, scholastic thinkers debated a fundamental question: which operations attributed to magic were genuinely natural (products of occult natural properties, celestial influences, or human art), and which required demonic cooperation? The answer to this question determined whether a practitioner was a natural philosopher or a heretic — a life-and-death distinction illustrated by the burning of Cecco d'Ascoli in Florence in 1327. Bishop Étienne Tempier's condemnations of 1270 and 1277 defined the institutional boundaries within which all subsequent scholastic discussion of magic, astrology, and image magic had to navigate. Lynn Thorndike's eight-volume <i>A History of Magic and Experimental Science</i> (1923–1958) remains the indispensable documentary guide to this tradition.</p>
</section>

{map_block_html("scholasticism", "Map: Scholasticism and Magic — Key Sites")}

<h2>Key Thinkers ({len(persons)} entries)</h2>
{_section_cards(persons, "persons")}

<h2>Primary Sources and Scholarship ({len(texts)} entries)</h2>
{_section_cards(texts, "texts")}

<h2>Concepts and Categories ({len(concepts)} entries)</h2>
{_section_cards(concepts, "concepts")}

<h2>Timeline of Scholastic Engagements with Magic</h2>
<div style='border-left:2px solid var(--line);padding-left:4px;margin:20px 0'>
{_timeline_entries_html(events)}
</div>

</main>
<script>{SECTION_MAP_JS}</script>
"""
    write(target / "scholasticism.html", page("Scholasticism and Magic", content, active="scholasticism"))
    print(f"Generated scholasticism.html ({len(texts)} texts, {len(persons)} persons, {len(concepts)} concepts, {len(events)} events)")


def generate(target):
    if target.exists():
        shutil.rmtree(target)
    (target / "assets").mkdir(parents=True, exist_ok=True)
    write(target / "assets" / "manuscript-field.svg", ASSET)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ["texts", "persons", "concepts", "bibliography", "timeline_events"]}
    hero = f"""
    <section class='hero'><div class='hero-inner'><h1>MedievalMagicDB</h1><p class='subtitle'>A scholarly portal for medieval magic, learned ritual texts, astral image theory, necromancy, manuscript culture, and modern historiography.</p></div></section>
    <main><div class='stats'>{''.join(f"<div class='stat'><strong>{v}</strong>{k.replace('_',' ').title()}</div>" for k,v in counts.items())}</div>
    <h2>Thematic Sections</h2><div class='grid'>
    <a class='card' href='reception.html'><div class='card-title'>Grimoires in Reception</div><div class='meta'>Renaissance &amp; Early Modern</div><div class='desc'>How medieval grimoires were transmitted and transformed from Ficino and Pico to Agrippa, Trithemius, Dee, the printing press, and the modern editorial tradition.</div></a>
    <a class='card' href='solomonic.html'><div class='card-title'>Solomonic Magic</div><div class='meta'>Late Antique to Modern</div><div class='desc'>The grimoire tradition centered on Solomon's authority: Testament of Solomon, Clavicula Salomonis, Sepher ha-Razim, and spirit catalogues across Jewish, Christian, and Islamic sources.</div></a>
    <a class='card' href='scholasticism.html'><div class='card-title'>Scholasticism and Magic</div><div class='meta'>Medieval University Culture</div><div class='desc'>How Aquinas, Albertus Magnus, Bacon, Oresme, and Pietro d'Abano classified, condemned, and naturalized magic — and how condemnations shaped the field.</div></a>
    </div>
    <h2>Reference Gateways</h2><div class='grid'>
    <a class='card' href='concepts.html'><div class='card-title'>Concepts</div><div class='desc'>Actor terms and analyst categories, kept deliberately distinct.</div></a>
    <a class='card' href='texts.html'><div class='card-title'>Texts</div><div class='desc'>Primary sources, editions, scholarship, and manuscript-centered studies.</div></a>
    <a class='card' href='persons.html'><div class='card-title'>Persons</div><div class='desc'>Historical figures, attributed authorities, and modern scholars.</div></a>
    <a class='card' href='bibliography.html'><div class='card-title'>Converted Corpus</div><div class='desc'>PDF-derived Markdown sources with extraction metadata.</div></a>
    <a class='card' href='timeline.html'><div class='card-title'>Timeline</div><div class='desc'>Dated events from the 9th century to the present — now with interactive map.</div></a>
    </div></main>
    """
    write(target / "index.html", page("Home", hero))

    generate_reception(target, conn)
    generate_solomonic(target, conn)
    generate_scholasticism(target, conn)

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

import html
import json
import re
import shutil
import sqlite3
from pathlib import Path

from common import DB_PATH, DOCS_DIR, SITE_DIR, ensure_dirs


CSS = """
:root{--bg:#10100e;--panel:#181915;--panel2:#202118;--ink:#eee8d7;--muted:#b8ad94;--line:#4b442e;--gold:#d0a94f;--green:#7aa36b;--red:#b96b5f;--blue:#7296a8;--font:Georgia,'Times New Roman',serif;--ui:Inter,Segoe UI,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--ui);line-height:1.65}.nav{position:sticky;top:0;z-index:3;background:rgba(16,16,14,.94);border-bottom:1px solid var(--line);backdrop-filter:blur(10px)}.nav-inner{max-width:1180px;margin:0 auto;padding:14px 20px;display:flex;gap:18px;align-items:center;justify-content:space-between}.brand{font-family:var(--font);font-size:24px;color:var(--gold);text-decoration:none}.links{display:flex;gap:14px;flex-wrap:wrap}.links a{color:var(--ink);text-decoration:none;font-size:14px}.links a:hover{color:var(--gold)}main{max-width:1180px;margin:0 auto;padding:42px 20px}.hero{min-height:360px;display:grid;align-content:end;padding:48px 20px;background:linear-gradient(rgba(16,16,14,.25),rgba(16,16,14,.92)),url('assets/manuscript-field.svg');background-size:cover;background-position:center;border-bottom:1px solid var(--line)}.hero-inner{max-width:1180px;margin:0 auto;width:100%}h1{font-family:var(--font);font-size:clamp(42px,7vw,82px);line-height:1;margin:0 0 14px;color:#f5d982;letter-spacing:0}h2{font-family:var(--font);font-size:30px;color:var(--gold);margin:34px 0 14px}.subtitle{font-size:19px;color:var(--muted);max-width:760px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px;text-decoration:none;color:var(--ink);min-height:180px}.card:hover{border-color:var(--gold);background:var(--panel2)}.card-title{font-family:var(--font);font-size:23px;color:#f1d17c;line-height:1.15;margin-bottom:8px}.meta{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--gold);margin-bottom:10px}.desc{font-size:14px;color:var(--muted)}.prose{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:26px;font-family:var(--font);font-size:19px}.prose p{margin:0 0 18px}.toolbar{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 22px}.toolbar input,.toolbar select{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:10px 12px}.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:3px 9px;color:var(--muted);font-size:12px;margin-right:6px}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:30px 0}.stat{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px}.stat strong{display:block;font-family:var(--font);font-size:34px;color:var(--gold)}footer{border-top:1px solid var(--line);padding:36px 20px;text-align:center;color:var(--muted)}
"""

ASSET = """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="700" viewBox="0 0 1600 700"><rect width="1600" height="700" fill="#17160f"/><g opacity=".18" fill="none" stroke="#d0a94f" stroke-width="2"><path d="M120 120c170 90 320 90 490 0s320-90 490 0 320 90 430 10"/><path d="M90 250h1420M90 330h1420M90 410h1420M90 490h1420"/><circle cx="340" cy="348" r="82"/><circle cx="340" cy="348" r="47"/><path d="M820 190l95 250 95-250M780 440h270"/><path d="M1170 240c80-58 170-58 250 0-80 58-170 58-250 0z"/><path d="M1295 170v150M1220 245h150"/></g><g opacity=".22" fill="#efe0b4" font-family="Georgia" font-size="38"><text x="130" y="610">ars notoria</text><text x="560" y="95">nigromantia</text><text x="1040" y="600">scientia imaginum</text></g></svg>"""


def clean(value):
    return html.escape(value or "")


def page(title, content, prefix=""):
    nav = """
    <nav class="nav"><div class="nav-inner"><a class="brand" href="{0}index.html">MedievalMagicDB</a><div class="links">
    <a href="{0}texts.html">Texts</a><a href="{0}persons.html">Persons</a><a href="{0}concepts.html">Concepts</a><a href="{0}bibliography.html">Bibliography</a><a href="{0}timeline.html">Timeline</a><a href="{0}about.html">Methodology</a>
    </div></div></nav>
    """.format(prefix)
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
    return page(title, f"<main><h1>{clean(title)}</h1><p class='subtitle'>{clean(subtitle)}</p><div class='toolbar'><input id='q' placeholder='Search'><select id='filter'><option value=''>All categories</option></select></div>{cards(rows, kind)}</main><script>{FILTER_JS}</script>")


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
    <h2>Research Gateways</h2><div class='grid'>
    <a class='card' href='concepts.html'><div class='card-title'>Concepts</div><div class='desc'>Actor terms and analyst categories, kept deliberately distinct.</div></a>
    <a class='card' href='texts.html'><div class='card-title'>Texts</div><div class='desc'>Primary sources, editions, scholarship, and manuscript-centered studies.</div></a>
    <a class='card' href='bibliography.html'><div class='card-title'>Converted Corpus</div><div class='desc'>PDF-derived Markdown sources with extraction metadata.</div></a>
    </div></main>
    """
    write(target / "index.html", page("Home", hero))

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
        timeline += f"<h2>{clean(years)}: {clean(event['title'])}</h2><p>{clean(event['description'])}</p>"
    timeline += "</section></main>"
    write(target / "timeline.html", page("Timeline", timeline))

    about = "<main><h1>Methodology</h1><section class='prose'><p>MedievalMagicDB treats medieval magic as a historiographical problem rather than a stable object. The site distinguishes actor terms from analyst terms, separates primary sources from modern scholarship, and keeps extraction metadata visible so database prose can remain source-aware.</p><p>The architecture is inherited from EmeraldTablet: SQLite is the source of truth, ingestion scripts are idempotent, agent drafts belong in staging, and generated pages are static HTML.</p></section></main>"
    write(target / "about.html", page("Methodology", about))
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

import json
import re
import sqlite3
import argparse
from pathlib import Path

from common import DB_PATH, MANIFEST_PATH, ensure_dirs


def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value[:80] or "entry"


def upsert(conn, table, key, row):
    columns = list(row.keys())
    placeholders = ", ".join("?" for _ in columns)
    update_cols = [c for c in columns if c != key]
    updates = ", ".join(f"{c}=excluded.{c}" for c in update_cols)
    sql = f"""
        INSERT INTO {table} ({", ".join(columns)})
        VALUES ({placeholders})
        ON CONFLICT({key}) DO UPDATE SET {updates}
    """
    conn.execute(sql, [row[c] for c in columns])


def pub_type_for(title):
    lower = title.lower()
    if "speculum" in lower or "journal" in lower or "american historical review" in lower:
        return "ARTICLE"
    if "review" in lower or "10.2307_2864593" in lower:
        return "REVIEW"
    if "edition" in lower or "picatrix" in lower or "ars notoria" in lower or "sworn book" in lower:
        return "EDITION"
    if "routledge history" in lower or "studies in" in lower:
        return "COLLECTION"
    return "MONOGRAPH"


def infer_author(title):
    if "Kieckhefer" in title:
        return "Kieckhefer, Richard"
    if "Benedek Lang" in title or "Lang" in title:
        return "Lang, Benedek"
    if "Thorndike" in title:
        return "Thorndike, Lynn"
    if "Hartlieb" in title:
        return "Hartlieb, Johannes; Kieckhefer, Richard"
    if "Fanger" in title:
        return "Fanger, Claire"
    if "Klaassen" in title:
        return "Klaassen, Frank"
    if "Sophie Page" in title or "Page" in title:
        return "Page, Sophie"
    if "Bailey" in title:
        return "Bailey, Michael D.; Bain, Kristi Woodward; Callan, Maeve Brigid"
    if "Picatrix" in title or "Porreca" in title or "Attrell" in title:
        return "Attrell, Dan; Porreca, David"
    if "Peterson" in title:
        return "Peterson, Joseph H."
    if "Skinner" in title:
        return "Skinner, Stephen; Rankine, David"
    if "Greer" in title:
        return "Greer, John Michael"
    if "Harms" in title:
        return "Harms, Daniel"
    if "Rider" in title or "Routledge History" in title:
        return "Page, Sophie; Rider, Catherine"
    return "Unknown"


def infer_year(title):
    match = re.search(r"(19|20)\d{2}", title)
    return int(match.group(0)) if match else None


def seed_bibliography(conn, manifest_path=MANIFEST_PATH):
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest: {manifest_path}. Run convert_pdfs_to_md.py first.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest:
        title = item.get("title_guess") or Path(item["pdf_path"]).stem
        source_id = slugify(title)
        upsert(
            conn,
            "bibliography",
            "source_id",
            {
                "source_id": source_id,
                "author": infer_author(title),
                "title": title,
                "year": infer_year(title),
                "publisher": None,
                "journal": None,
                "pub_type": pub_type_for(title),
                "relevance": "DIRECT",
                "pdf_path": item.get("pdf_path"),
                "markdown_path": item.get("markdown_path"),
                "pages": item.get("pages"),
                "text_pages": item.get("text_pages"),
                "extraction_status": item.get("status"),
                "notes": f"Seeded from local corpus manifest: {manifest_path.name}.",
            },
        )


PERSONS = [
    ("richard_kieckhefer", "Richard Kieckhefer", "SCHOLAR", "MODERN", "Learned magic, necromancy, and the social history of medieval ritual texts."),
    ("claire_fanger", "Claire Fanger", "SCHOLAR", "MODERN", "Medieval ritual magic, angelic theurgy, and visionary autobiographical writing."),
    ("frank_klaassen", "Frank Klaassen", "SCHOLAR", "MODERN", "Manuscript culture and transformations of learned magic in late medieval and early modern England."),
    ("sophie_page", "Sophie Page", "SCHOLAR", "MODERN", "Monastic, clerical, and manuscript contexts for medieval occult learning."),
    ("michael_d_bailey", "Michael D. Bailey", "SCHOLAR", "MODERN", "Medieval religion, superstition, witchcraft, and magic as contested categories."),
    ("catherine_rider", "Catherine Rider", "SCHOLAR", "MODERN", "Medieval magic, medicine, fertility, charms, and pastoral contexts."),
    ("dan_attrell", "Dan Attrell", "TRANSLATOR", "MODERN", "Translator and scholar of the Latin Picatrix and astral magic."),
    ("david_porreca", "David Porreca", "SCHOLAR", "MODERN", "Medieval Latin Hermetica, Picatrix studies, and transmission of Arabic astral magic."),
    ("apollonius_of_tyana", "Apollonius of Tyana", "ATTRIBUTED_AUTHORITY", "LATE_ANTIQUE", "Ancient sage whose name became attached to medieval ritual and talismanic traditions."),
    ("thabit_ibn_qurra", "Thabit ibn Qurra", "PHILOSOPHER", "MEDIEVAL", "Ninth-century Sabian scholar associated in Latin reception with astral image theory."),
]

CONCEPTS = [
    ("medieval_magic", "Medieval Magic", "HISTORIOGRAPHICAL", "ANALYST_TERM", "Medieval magic is an Analyst Term for practices, accusations, texts, and learned theories that modern scholars group under magic while medieval actors used more specific categories such as nigromantia, superstitio, experimentum, and scientia imaginum."),
    ("ars_notoria", "Ars Notoria", "RITUAL", "ACTOR_TERM", "Ars Notoria is an Actor Term for a medieval ritual art of learning that joined prayers, notae, angelic invocation, and claims of accelerated intellectual acquisition."),
    ("nigromantia", "Nigromantia", "DEMONOLOGICAL", "ACTOR_TERM", "Nigromantia is a medieval Latin Actor Term often used for illicit ritual operations involving spirits, frequently blurred by clerical writers with necromancy and demonic magic."),
    ("astral_image_magic", "Astral Image Magic", "ASTRAL", "ANALYST_TERM", "Astral image magic is an Analyst Term for learned practices that connect images, planetary timing, materials, and celestial influence in Arabic and Latin scholastic settings."),
    ("picatrix_tradition", "Picatrix Tradition", "ASTRAL", "HYBRID", "The Picatrix tradition denotes the Arabic-to-Latin transmission of the Ghayat al-hakim and its reception as a major source for medieval and Renaissance astral magic."),
    ("grimoire", "Grimoire", "MANUSCRIPT", "ANALYST_TERM", "Grimoire is primarily an Analyst Term for manuscript or printed collections of ritual instructions, spirit lists, conjurations, prayers, and experiments."),
    ("superstitio", "Superstitio", "THEOLOGICAL", "ACTOR_TERM", "Superstitio is a Latin Actor Term used by theologians and pastoral writers to classify improper religious practice, divination, charms, and illicit ritual dependence."),
    ("learned_magic", "Learned Magic", "HISTORIOGRAPHICAL", "ANALYST_TERM", "Learned magic is an Analyst Term for textually transmitted practices cultivated by literate clerical, university, monastic, or courtly actors."),
]

TEXTS = [
    ("picatrix", "Picatrix", "LATIN", "PRIMARY_SOURCE", "MEDIEVAL", "The Latin Picatrix is the principal medieval Latin witness to the Arabic Ghayat al-hakim and a central source for astral image magic."),
    ("ars_notoria", "Ars Notoria", "LATIN", "PRIMARY_SOURCE", "MEDIEVAL", "The Ars Notoria is a ritual art of memory and learning transmitted in medieval Latin manuscripts."),
    ("sworn_book_of_honorius", "Sworn Book of Honorius", "LATIN", "PRIMARY_SOURCE", "MEDIEVAL", "The Sworn Book of Honorius is a major medieval ritual magic text concerned with divine vision, angelic hierarchy, and ritual discipline."),
    ("forbidden_rites", "Forbidden Rites", "ENGLISH", "EDITION", "MODERN", "Richard Kieckhefer's Forbidden Rites edits and studies a fifteenth-century necromantic manual."),
    ("transformations_of_magic", "The Transformations of Magic", "ENGLISH", "SCHOLARSHIP", "MODERN", "Frank Klaassen's study examines illicit learned magic in the later Middle Ages and Renaissance."),
    ("magic_in_the_cloister", "Magic in the Cloister", "ENGLISH", "SCHOLARSHIP", "MODERN", "Sophie Page's monograph examines monastic and clerical engagements with occult approaches to the medieval universe."),
    ("invoking_angels", "Invoking Angels", "ENGLISH", "COLLECTION", "MODERN", "Claire Fanger's edited collection studies theurgic ideas and practices from the thirteenth to sixteenth centuries."),
]

TIMELINE = [
    (875, None, "COMPOSITION", "Thabit ibn Qurra and the Sabian milieu", "c. 875, Harran and Baghdad: Thabit ibn Qurra works within Arabic scientific and philosophical networks later associated in Latin reception with astral image theory. The connection matters for medieval magic scholarship because Latin attributions to Thabit helped frame image magic as learned natural philosophy rather than merely illicit ritual."),
    (1250, 1300, "TRANSLATION", "Latin Picatrix enters western learned culture", "c. 1250-1300, Iberia and the Latin West: The Arabic Ghayat al-hakim circulates in Latin as the Picatrix, transmitting a large body of astral image theory, ritual timing, planetary correspondences, and philosophical justification. Modern scholars treat this translation history as central to the Arabic-Latin formation of learned magic."),
    (1300, 1400, "MANUSCRIPT", "Ars Notoria and angelic learning circulate in manuscripts", "c. 1300-1400, western Europe: Ars Notoria manuscripts transmit prayers, diagrams, and ritual schedules promising divinely assisted learning. The tradition complicates simple oppositions between piety and magic because its procedures often present themselves through Christian prayer while attracting suspicion from theologians and ecclesiastical authorities."),
    (1998, None, "EDITION", "Forbidden Rites published", "1998, University Park, Pennsylvania: Richard Kieckhefer publishes Forbidden Rites, an edition and study of a fifteenth-century necromancer's manual. The book becomes a landmark for studying medieval ritual magic as manuscript practice, learned clerical culture, and historically specific textual compilation."),
]


def seed_entities(conn):
    for pid, name, role, era, desc in PERSONS:
        upsert(conn, "persons", "person_id", {
            "person_id": pid, "name": name, "role_primary": role, "era": era,
            "scholar_group": "Medieval Magic and Manuscript Studies" if role == "SCHOLAR" else None,
            "description": desc, "source_method": "CURATED_SEED", "review_status": "DRAFT", "confidence": "MEDIUM",
        })
    for slug, label, category, category_type, definition in CONCEPTS:
        upsert(conn, "concepts", "slug", {
            "slug": slug, "label": label, "category": category, "category_type": category_type,
            "definition_short": definition, "significance": definition,
            "source_method": "CURATED_SEED", "review_status": "DRAFT", "confidence": "MEDIUM",
        })
    for tid, title, language, text_type, period, desc in TEXTS:
        upsert(conn, "texts", "text_id", {
            "text_id": tid, "title": title, "language": language, "text_type": text_type,
            "period": period, "description": desc, "source_method": "CURATED_SEED",
            "review_status": "DRAFT", "confidence": "MEDIUM",
        })
    for year, year_end, event_type, title, desc in TIMELINE:
        conn.execute(
            """INSERT OR IGNORE INTO timeline_events
               (year, year_end, event_type, title, description, confidence)
               VALUES (?, ?, ?, ?, ?, 'MEDIUM')""",
            (year, year_end, event_type, title, desc),
        )


def link_seed_data(conn):
    def id_for(table, key_col, value):
        return conn.execute(f"SELECT id FROM {table} WHERE {key_col}=?", (value,)).fetchone()[0]

    concept_texts = {
        "astral_image_magic": ["picatrix"],
        "picatrix_tradition": ["picatrix"],
        "ars_notoria": ["ars_notoria"],
        "nigromantia": ["forbidden_rites"],
        "learned_magic": ["forbidden_rites", "transformations_of_magic", "magic_in_the_cloister", "invoking_angels"],
        "grimoire": ["sworn_book_of_honorius", "ars_notoria"],
    }
    for concept, texts in concept_texts.items():
        concept_id = id_for("concepts", "slug", concept)
        for text in texts:
            text_id = id_for("texts", "text_id", text)
            conn.execute(
                "INSERT OR IGNORE INTO concept_text_refs (concept_id, text_id, notes) VALUES (?, ?, ?)",
                (concept_id, text_id, "Initial curated relationship."),
            )

    concept_links = [
        ("learned_magic", "medieval_magic", "PART_OF"),
        ("nigromantia", "superstitio", "RELATED"),
        ("astral_image_magic", "picatrix_tradition", "RELATED"),
        ("ars_notoria", "learned_magic", "PART_OF"),
        ("grimoire", "learned_magic", "RELATED"),
    ]
    for a, b, rel in concept_links:
        conn.execute(
            "INSERT OR IGNORE INTO concept_links (from_concept_id, to_concept_id, relationship, notes) VALUES (?, ?, ?, ?)",
            (id_for("concepts", "slug", a), id_for("concepts", "slug", b), rel, "Initial curated concept graph."),
        )


def main():
    parser = argparse.ArgumentParser(description="Seed MedievalMagicDB from a conversion manifest.")
    parser.add_argument("--manifest", default=str(MANIFEST_PATH), help="Manifest JSON to ingest.")
    parser.add_argument("--bibliography-only", action="store_true", help="Only ingest bibliography rows from the manifest.")
    args = parser.parse_args()
    manifest_path = Path(args.manifest)

    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    seed_bibliography(conn, manifest_path)
    if not args.bibliography_only:
        seed_entities(conn)
        link_seed_data(conn)
    conn.commit()
    for table in ["bibliography", "persons", "texts", "concepts", "timeline_events"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count}")
    conn.close()


if __name__ == "__main__":
    main()

import sqlite3

from common import DB_PATH, ensure_dirs


def upsert(conn, table, key, row):
    columns = list(row.keys())
    placeholders = ", ".join("?" for _ in columns)
    updates = ", ".join(f"{c}=excluded.{c}" for c in columns if c != key)
    conn.execute(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) "
        f"ON CONFLICT({key}) DO UPDATE SET {updates}",
        [row[c] for c in columns],
    )


def id_for(conn, table, key_col, value):
    row = conn.execute(f"SELECT id FROM {table} WHERE {key_col}=?", (value,)).fetchone()
    return row[0] if row else None


TEXTS = [
    ("liber_experimentorum", "Liber experimentorum", "LATIN", "MANUSCRIPT_COMPILATION", "MEDIEVAL", "Liber experimentorum names a family or genre of experiment-books in medieval learned magic, where recipes, trials, secrets, and operations circulate as textual experiments rather than stable authored treatises."),
    ("buch_aller_verbotenen_kunst", "Buch aller verbotenen Kunst", "GERMAN", "TREATISE", "MEDIEVAL", "Johannes Hartlieb's Buch aller verbotenen Kunst, or Book of All Forbidden Arts, is a fifteenth-century German treatment of prohibited arts, witchcraft, and magical practices for princely and moral instruction."),
]

CONCEPTS = [
    ("witchcraft", "Witchcraft", "DEMONOLOGICAL", "ANALYST_TERM", "Witchcraft is an Analyst Term for accusations, learned demonological categories, and late medieval constructions of harmful magic; it must be distinguished from ritual manuscripts and from broader categories of learned magic."),
    ("exorcism", "Exorcism", "RITUAL", "HYBRID", "Exorcism names authorized Christian rites and adjacent ritual practices for expelling or commanding spirits, making it a boundary category between liturgy, pastoral care, and ritual magic."),
    ("hydromancy", "Hydromancy", "DIVINATORY", "ACTOR_TERM", "Hydromancy is an Actor Term for divination by water, frequently named in medieval taxonomies of forbidden divination and often treated as suspect because of its association with spirit mediation."),
    ("pyromancy", "Pyromancy", "DIVINATORY", "ACTOR_TERM", "Pyromancy is an Actor Term for divination by fire, appearing in medieval lists of mantic arts and classifications of illicit knowledge."),
    ("sortilege", "Sortilege", "DIVINATORY", "ACTOR_TERM", "Sortilege is an Actor Term for divination by lots, books, or chance procedures, treated variously as superstition, clerical misuse, or illicit inquiry into hidden things."),
    ("notae", "Notae", "MANUSCRIPT", "ACTOR_TERM", "Notae are the visual signs or figures central to Ars Notoria traditions of ritual learning, requiring attention to diagrammatic transmission as well as verbal prayer."),
    ("confession", "Confession", "THEOLOGICAL", "ACTOR_TERM", "Confession is a sacramental and pastoral context in which medieval clergy identified charms, divination, superstition, and illicit ritual practices as matters of correction."),
    ("secret_of_secrets", "Secret of Secrets", "HISTORIOGRAPHICAL", "HYBRID", "Secret of Secrets refers to the Secretum Secretorum tradition and its reception as a pseudo-Aristotelian vehicle for princely counsel, occult knowledge, physiognomy, astrology, and medicine."),
    ("experimenta", "Experimenta", "NATURAL_PHILOSOPHY", "ACTOR_TERM", "Experimenta is an Actor Term for trials, recipes, or procedures transmitted as experiential knowledge; in medieval magic studies it marks the overlap between practical experiment, secrets literature, medicine, and ritual operation."),
]

CONCEPT_TEXTS = [
    ("experimenta", "liber_experimentorum"),
    ("experimental_science", "liber_experimentorum"),
    ("prohibited_arts", "buch_aller_verbotenen_kunst"),
    ("witchcraft", "buch_aller_verbotenen_kunst"),
    ("hydromancy", "hazards_of_the_dark_arts"),
    ("pyromancy", "hazards_of_the_dark_arts"),
    ("sortilege", "hazards_of_the_dark_arts"),
    ("exorcism", "liber_de_angelis"),
    ("notae", "ars_notoria"),
    ("secret_of_secrets", "secretum_secretorum"),
]

CONCEPT_LINKS = [
    ("witchcraft", "demonology", "RELATED"),
    ("exorcism", "demonology", "RELATED"),
    ("hydromancy", "divination", "PART_OF"),
    ("pyromancy", "divination", "PART_OF"),
    ("sortilege", "divination", "PART_OF"),
    ("notae", "ritual_diagrams", "PART_OF"),
    ("confession", "pastoral_care_and_magic", "PART_OF"),
    ("secret_of_secrets", "licit_and_illicit_knowledge", "RELATED"),
    ("experimenta", "experimental_science", "RELATED"),
]

PERSON_TEXTS = [
    ("johannes_hartlieb", "buch_aller_verbotenen_kunst", "AUTHOR"),
]

TIMELINE = [
    (1140, 1160, "TRANSLATION", "Secretum Secretorum enters Latin learned culture", "c. 1140-1160, Iberia and the Latin West: The pseudo-Aristotelian Secretum Secretorum circulates in Latin as a flexible vehicle for princely counsel, physiognomy, medicine, astrology, and hidden knowledge. Its importance for medieval magic lies not in being a grimoire, but in showing how political advice, natural philosophy, and occultized secrets could travel under Aristotelian authority."),
    (1250, 1270, "COMPOSITION", "Albertus Magnus treats minerals and occult natural powers", "c. 1250-1270, Cologne and the Dominican schools: Albertus Magnus discusses stones, minerals, and hidden natural powers in works such as De mineralibus. The episode matters because scholastic natural philosophy offered categories for unusual effects that could be treated as natural rather than demonic, shaping later debates over natural magic and occult properties."),
    (1456, None, "COMPOSITION", "Hartlieb writes the Book of All Forbidden Arts", "1456, Bavaria: Johannes Hartlieb writes the Buch aller verbotenen Kunst for a princely milieu, classifying and warning against prohibited arts, witchcraft, divination, and magical practices. The text matters because it joins vernacular advice, moral instruction, and late medieval concern with illicit knowledge before the full consolidation of early modern witchcraft theory."),
]


def main():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    for text_id, title, language, text_type, period, desc in TEXTS:
        upsert(conn, "texts", "text_id", {
            "text_id": text_id, "title": title, "language": language,
            "text_type": text_type, "period": period, "description": desc,
            "source_method": "DISCOVERY_HIGH_SIGNAL", "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for slug, label, category, category_type, desc in CONCEPTS:
        upsert(conn, "concepts", "slug", {
            "slug": slug, "label": label, "category": category,
            "category_type": category_type, "definition_short": desc, "significance": desc,
            "source_method": "DISCOVERY_HIGH_SIGNAL", "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for concept, text in CONCEPT_TEXTS:
        concept_id = id_for(conn, "concepts", "slug", concept)
        text_id = id_for(conn, "texts", "text_id", text)
        if concept_id and text_id:
            conn.execute(
                "INSERT OR IGNORE INTO concept_text_refs (concept_id, text_id, notes) VALUES (?, ?, ?)",
                (concept_id, text_id, "Seeded from high-signal corpus discovery."),
            )

    for source, target, relationship in CONCEPT_LINKS:
        source_id = id_for(conn, "concepts", "slug", source)
        target_id = id_for(conn, "concepts", "slug", target)
        if source_id and target_id:
            conn.execute(
                "INSERT OR IGNORE INTO concept_links (from_concept_id, to_concept_id, relationship, notes) VALUES (?, ?, ?, ?)",
                (source_id, target_id, relationship, "Seeded from high-signal corpus discovery."),
            )

    for person, text, role in PERSON_TEXTS:
        person_id = id_for(conn, "persons", "person_id", person)
        text_id = id_for(conn, "texts", "text_id", text)
        if person_id and text_id:
            conn.execute(
                "INSERT OR IGNORE INTO person_text_roles (person_id, text_id, role, notes, confidence) VALUES (?, ?, ?, ?, 'MEDIUM')",
                (person_id, text_id, role, "Seeded from high-signal corpus discovery."),
            )

    for year, year_end, event_type, title, description in TIMELINE:
        conn.execute(
            "INSERT OR IGNORE INTO timeline_events (year, year_end, event_type, title, description, confidence) VALUES (?, ?, ?, ?, ?, 'MEDIUM')",
            (year, year_end, event_type, title, description),
        )

    conn.commit()
    for table in ("texts", "concepts", "person_text_roles", "concept_text_refs", "concept_links", "timeline_events"):
        print(f"{table}: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()

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


PERSONS = [
    ("adelard_of_bath", "Adelard of Bath", "PHILOSOPHER", "MEDIEVAL", "Twelfth-century translator and natural philosopher whose Arabic-Latin learning helped shape Latin debates about astrology, natural causality, and experiment."),
    ("hugh_of_saint_victor", "Hugh of Saint-Victor", "THEOLOGIAN", "MEDIEVAL", "Twelfth-century theologian whose classifications of arts, knowledge, and illicit curiosity form part of the scholastic background for later treatments of magic."),
    ("bernard_silvester", "Bernard Silvester", "PHILOSOPHER", "MEDIEVAL", "Twelfth-century intellectual associated with cosmological and astrological learning in the Latin schools, important for the learned background of celestial influence."),
    ("peter_abelard", "Peter Abelard", "THEOLOGIAN", "MEDIEVAL", "Twelfth-century theologian whose discussions of divination and astrology belong to earlier scholastic attempts to delimit illicit knowledge."),
    ("cecco_d_ascoli", "Cecco d'Ascoli", "ASTROLOGER", "MEDIEVAL", "Fourteenth-century astrologer and poet whose condemnation and execution made him a key figure in debates over astrology, determinism, and forbidden knowledge."),
    ("michael_scot", "Michael Scot", "TRANSLATOR", "MEDIEVAL", "Thirteenth-century translator, astrologer, and court intellectual associated with Arabic-Latin science and later magical reputation."),
]

TEXTS = [
    ("secretum_secretorum", "Secretum Secretorum", "LATIN", "TREATISE", "MEDIEVAL", "The Secretum Secretorum is a pseudo-Aristotelian mirror-for-princes and knowledge compendium whose medieval reception intersects with astrology, physiognomy, medicine, and occult counsel."),
    ("opus_majus", "Opus Majus", "LATIN", "TREATISE", "MEDIEVAL", "Roger Bacon's Opus Majus is central to medieval discussions of experiment, language, optics, astrology, and the status of knowledge later associated with magic and science."),
    ("de_universo_william_auvergne", "De universo", "LATIN", "TREATISE", "MEDIEVAL", "William of Auvergne's De universo is central to theological discussion of spirits, demons, image magic, and the created order."),
    ("etymologiae", "Etymologiae", "LATIN", "TREATISE", "MEDIEVAL", "Isidore of Seville's Etymologiae transmitted influential classifications of magic, divination, and pagan learning to medieval encyclopedic culture."),
    ("de_mineralibus", "De mineralibus", "LATIN", "TREATISE", "MEDIEVAL", "Albertus Magnus's De mineralibus is important for scholastic discussion of stones, occult properties, natural powers, and lapidary traditions."),
    ("de_divinatione_daemonum", "De divinatione daemonum", "LATIN", "TREATISE", "LATE_ANTIQUE", "Augustine's De divinatione daemonum helped shape Christian explanations of divination, demons, signs, and illicit curiosity."),
]

CONCEPTS = [
    ("experimental_science", "Experimental Science", "HISTORIOGRAPHICAL", "ANALYST_TERM", "Experimental science is an Analyst Term especially associated with older histories such as Thorndike's, where magic and experiment are studied as intertwined medieval attempts to test, command, or explain nature."),
    ("natural_powers", "Natural Powers", "NATURAL_PHILOSOPHY", "HYBRID", "Natural powers names medieval attempts to explain unusual effects through created nature rather than demonic pact, a key boundary zone between natural philosophy and magic."),
    ("prohibited_arts", "Prohibited Arts", "LEGAL", "HYBRID", "Prohibited arts is a hybrid category for practices forbidden by theological, legal, university, or pastoral authorities, including forms of divination, image magic, spirit invocation, and suspect astrology."),
    ("mathematical_arts", "Mathematical Arts", "NATURAL_PHILOSOPHY", "HYBRID", "Mathematical arts refers to quadrivial and astral disciplines, especially astrology, whose learned status made their relation to divination and magic especially contested."),
    ("licit_and_illicit_knowledge", "Licit and Illicit Knowledge", "THEOLOGICAL", "ANALYST_TERM", "Licit and illicit knowledge is an Analyst Term for medieval debates over what could be known through nature, revelation, experiment, stars, demons, or ritual practice."),
    ("demonology", "Demonology", "DEMONOLOGICAL", "ANALYST_TERM", "Demonology is an Analyst Term for systematic learned discussion of demons, their powers, limitations, deception, and relation to divination, magic, superstition, and witchcraft."),
]

PERSON_TEXTS = [
    ("roger_bacon", "opus_majus", "AUTHOR"),
    ("william_of_auvergne", "de_universo_william_auvergne", "AUTHOR"),
    ("isidore_of_seville", "etymologiae", "AUTHOR"),
    ("albertus_magnus", "de_mineralibus", "AUTHOR"),
    ("augustine_of_hippo", "de_divinatione_daemonum", "AUTHOR"),
    ("michael_scot", "secretum_secretorum", "SCHOLAR_OF"),
    ("adelard_of_bath", "de_radiis", "SCHOLAR_OF"),
    ("bernard_silvester", "speculum_astronomiae", "SCHOLAR_OF"),
    ("hugh_of_saint_victor", "hazards_of_the_dark_arts", "SCHOLAR_OF"),
    ("peter_abelard", "hazards_of_the_dark_arts", "SCHOLAR_OF"),
    ("cecco_d_ascoli", "speculum_astronomiae", "SCHOLAR_OF"),
]

CONCEPT_TEXTS = [
    ("experimental_science", "history_magic_experimental_science"),
    ("experimental_science", "opus_majus"),
    ("natural_powers", "de_mineralibus"),
    ("natural_powers", "de_occultis_operibus_naturae"),
    ("prohibited_arts", "hazards_of_the_dark_arts"),
    ("prohibited_arts", "de_divinatione_daemonum"),
    ("mathematical_arts", "speculum_astronomiae"),
    ("mathematical_arts", "opus_majus"),
    ("licit_and_illicit_knowledge", "de_universo_william_auvergne"),
    ("demonology", "de_divinatione_daemonum"),
    ("demonology", "de_universo_william_auvergne"),
    ("celestial_influence", "opus_majus"),
    ("scholastic_classification", "etymologiae"),
]

CONCEPT_LINKS = [
    ("experimental_science", "natural_magic", "RELATED"),
    ("natural_powers", "occult_properties", "RELATED"),
    ("prohibited_arts", "condemned_arts", "RELATED"),
    ("mathematical_arts", "celestial_influence", "RELATED"),
    ("licit_and_illicit_knowledge", "scholastic_classification", "RELATED"),
    ("demonology", "demonic_pact", "RELATED"),
]


def main():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    for person_id, name, role, era, desc in PERSONS:
        upsert(conn, "persons", "person_id", {
            "person_id": person_id, "name": name, "role_primary": role, "era": era,
            "description": desc, "source_method": "THORNDIKE_EXPANSION",
            "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for text_id, title, language, text_type, period, desc in TEXTS:
        upsert(conn, "texts", "text_id", {
            "text_id": text_id, "title": title, "language": language, "text_type": text_type,
            "period": period, "description": desc, "source_method": "THORNDIKE_EXPANSION",
            "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for slug, label, category, category_type, desc in CONCEPTS:
        upsert(conn, "concepts", "slug", {
            "slug": slug, "label": label, "category": category,
            "category_type": category_type, "definition_short": desc, "significance": desc,
            "source_method": "THORNDIKE_EXPANSION", "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for person, text, role in PERSON_TEXTS:
        person_id = id_for(conn, "persons", "person_id", person)
        text_id = id_for(conn, "texts", "text_id", text)
        if person_id and text_id:
            conn.execute(
                "INSERT OR IGNORE INTO person_text_roles (person_id, text_id, role, notes, confidence) VALUES (?, ?, ?, ?, 'MEDIUM')",
                (person_id, text_id, role, "Seeded from Thorndike expansion."),
            )

    for concept, text in CONCEPT_TEXTS:
        concept_id = id_for(conn, "concepts", "slug", concept)
        text_id = id_for(conn, "texts", "text_id", text)
        if concept_id and text_id:
            conn.execute(
                "INSERT OR IGNORE INTO concept_text_refs (concept_id, text_id, notes) VALUES (?, ?, ?)",
                (concept_id, text_id, "Seeded from Thorndike expansion."),
            )

    for source, target, relationship in CONCEPT_LINKS:
        source_id = id_for(conn, "concepts", "slug", source)
        target_id = id_for(conn, "concepts", "slug", target)
        if source_id and target_id:
            conn.execute(
                "INSERT OR IGNORE INTO concept_links (from_concept_id, to_concept_id, relationship, notes) VALUES (?, ?, ?, ?)",
                (source_id, target_id, relationship, "Seeded from Thorndike expansion."),
            )

    conn.commit()
    for table in ("persons", "texts", "concepts", "person_text_roles", "concept_text_refs", "concept_links"):
        print(f"{table}: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()

import sqlite3

from common import BASE_DIR, DB_PATH, ensure_dirs


def id_for(conn, table, key_col, value):
    row = conn.execute(f"SELECT id FROM {table} WHERE {key_col}=?", (value,)).fetchone()
    return row[0] if row else None


def link_person_text(conn, person, text, role, notes):
    person_id = id_for(conn, "persons", "person_id", person)
    text_id = id_for(conn, "texts", "text_id", text)
    if person_id and text_id:
        conn.execute(
            "INSERT OR IGNORE INTO person_text_roles (person_id, text_id, role, notes, confidence) VALUES (?, ?, ?, ?, 'MEDIUM')",
            (person_id, text_id, role, notes),
        )


def link_concept_text(conn, concept, text, notes):
    concept_id = id_for(conn, "concepts", "slug", concept)
    text_id = id_for(conn, "texts", "text_id", text)
    if concept_id and text_id:
        conn.execute(
            "INSERT OR IGNORE INTO concept_text_refs (concept_id, text_id, notes) VALUES (?, ?, ?)",
            (concept_id, text_id, notes),
        )


def link_concepts(conn, source, target, relationship, notes):
    source_id = id_for(conn, "concepts", "slug", source)
    target_id = id_for(conn, "concepts", "slug", target)
    if source_id and target_id:
        conn.execute(
            "INSERT OR IGNORE INTO concept_links (from_concept_id, to_concept_id, relationship, notes) VALUES (?, ?, ?, ?)",
            (source_id, target_id, relationship, notes),
        )


PERSON_TEXT_LINKS = [
    ("solomon", "testament_of_solomon", "ATTRIBUTED_AUTHOR", "Solomon functions as the attributed authority of this demonological tradition."),
    ("solomon", "clavicula_salomonis", "ATTRIBUTED_AUTHOR", "Solomonic attribution authorizes the Key of Solomon tradition."),
    ("solomon", "hygromanteia", "ATTRIBUTED_AUTHOR", "Byzantine Solomonic ritual tradition."),
    ("solomon", "ars_goetia", "ATTRIBUTED_AUTHOR", "Solomonic authority structures the Goetia's reception."),
    ("solomon", "lemegeton", "ATTRIBUTED_AUTHOR", "The Lemegeton is transmitted under Solomonic authority."),
    ("honorius_of_thebes", "liber_juratus_honorii", "ATTRIBUTED_AUTHOR", "Honorius is the attributed authority of the sworn-book tradition."),
    ("honorius_of_thebes", "sworn_book_of_honorius", "ATTRIBUTED_AUTHOR", "Honorius is the attributed authority of the Sworn Book."),
    ("raziel", "liber_razielis", "ATTRIBUTED_AUTHOR", "Raziel is the angelic authority attached to the Liber Razielis."),
    ("john_of_morigny", "liber_visionum", "AUTHOR", "John of Morigny is the historical actor associated with this visionary ritual project."),
    ("john_of_morigny", "flowers_of_heavenly_teaching", "AUTHOR", "The Flowers tradition belongs to John's revision of Ars Notoria materials."),
    ("johannes_hartlieb", "hazards_of_the_dark_arts", "AUTHOR", "Hartlieb authored the fifteenth-century advice text translated in Hazards of the Dark Arts."),
    ("richard_kieckhefer", "forbidden_rites", "EDITOR", "Kieckhefer edited and analyzed the necromantic manual."),
    ("richard_kieckhefer", "munich_manual", "SCHOLAR_OF", "The Munich Manual is the manuscript basis of Forbidden Rites."),
    ("sophie_page", "magic_in_medieval_manuscripts", "AUTHOR", "Page authored the monograph."),
    ("benedek_lang", "unlocked_books", "AUTHOR", "Lang authored the Central European manuscript study."),
    ("lynn_thorndike", "history_magic_experimental_science", "AUTHOR", "Thorndike authored the multi-volume history."),
    ("dan_attrell", "picatrix", "TRANSLATOR", "Attrell translated the Latin Picatrix with Porreca."),
    ("david_porreca", "picatrix", "TRANSLATOR", "Porreca translated the Latin Picatrix with Attrell."),
    ("al_kindi", "de_radiis", "ATTRIBUTED_AUTHOR", "The Latin tradition associates De radiis with al-Kindi."),
    ("thabit_ibn_qurra", "de_imaginibus", "ATTRIBUTED_AUTHOR", "The Latin image-magic tradition attributes De imaginibus to Thabit."),
    ("peter_abano", "heptameron", "ATTRIBUTED_AUTHOR", "The print tradition attributes the Heptameron to Pietro d'Abano."),
    ("abu_mashar", "picatrix", "SCHOLAR_OF", "Abu Ma'shar belongs to the Arabic astrological background for Latin astral magic."),
    ("agostino_paravicini_bagliani", "speculum_astronomiae", "SCHOLAR_OF", "Paravicini Bagliani's work helps contextualize courtly, astrological, and learned culture."),
    ("albertus_magnus", "speculum_astronomiae", "SCHOLAR_OF", "Albertus Magnus is central to the scholastic background of astrology and image-magic classification."),
    ("apollonius_of_tyana", "ars_notoria", "ATTRIBUTED_AUTHOR", "Apollonius functions as an ancient authority in Ars Notoria reception."),
    ("arnald_of_villanova", "de_occultis_operibus_naturae", "SCHOLAR_OF", "Arnald's reception participates in the medical and natural-philosophical edges of occult knowledge."),
    ("augustine_of_hippo", "hazards_of_the_dark_arts", "SCHOLAR_OF", "Augustinian demonology shapes later classifications of forbidden arts."),
    ("beatice_delaurenti", "de_occultis_operibus_naturae", "SCHOLAR_OF", "Delaurenti's work helps frame marvels, nature, and occult causality."),
    ("catherine_rider", "magic_in_the_cloister", "SCHOLAR_OF", "Rider's work provides pastoral and social context for medieval magic."),
    ("charles_burnett", "de_radiis", "SCHOLAR_OF", "Burnett's Arabic-Latin transmission work contextualizes De radiis."),
    ("claire_fanger", "ars_notoria", "SCHOLAR_OF", "Fanger's work is central to Ars Notoria and ritual magic."),
    ("david_pingree", "picatrix", "SCHOLAR_OF", "Pingree's work is fundamental for astral magic and transmission history."),
    ("don_c_skemer", "liber_razielis", "SCHOLAR_OF", "Skemer's work on written amulets and textual protection contextualizes Raziel materials."),
    ("florence_chave_mahir", "liber_de_angelis", "SCHOLAR_OF", "Chave-Mahir's work on exorcism and ritual authority contextualizes angelic ritual texts."),
    ("frank_klaassen", "transformations_of_magic", "AUTHOR", "Klaassen authored The Transformations of Magic."),
    ("isidore_of_seville", "hazards_of_the_dark_arts", "SCHOLAR_OF", "Isidore's classifications fed later encyclopedic and moral treatments of magic."),
    ("jan_veenstra", "speculum_astronomiae", "SCHOLAR_OF", "Veenstra's intellectual history work connects medieval classification to later learned magic."),
    ("jean_patrice_boudet", "speculum_astronomiae", "SCHOLAR_OF", "Boudet's scholarship is central for astrology, divination, and learned magic."),
    ("john_of_salisbury", "hazards_of_the_dark_arts", "SCHOLAR_OF", "John of Salisbury's critique of divination supplies an earlier moral framework."),
    ("julien_veronese", "ars_notoria", "SCHOLAR_OF", "Veronese is a major scholar of Ars Notoria and ritual magic manuscripts."),
    ("katelyn_mesler", "liber_razielis", "SCHOLAR_OF", "Mesler's work contextualizes Jewish and Christian ritual-magic transmission."),
    ("lea_olsan", "magic_in_medieval_manuscripts", "SCHOLAR_OF", "Olsan's work on charms contextualizes manuscript evidence for practical ritual texts."),
    ("michael_d_bailey", "hazards_of_the_dark_arts", "SCHOLAR_OF", "Bailey's work contextualizes superstition, religion, and demonology."),
    ("nicolas_weill_parot", "de_imaginibus", "SCHOLAR_OF", "Weill-Parot's work is central for astral image theory."),
    ("nicole_oresme", "speculum_astronomiae", "SCHOLAR_OF", "Oresme belongs to late medieval criticism of astrology and divination."),
    ("paola_zambelli", "speculum_astronomiae", "SCHOLAR_OF", "Zambelli's work is central to the Speculum astronomiae and astrological debates."),
    ("robert_mathiesen", "ars_notoria", "SCHOLAR_OF", "Mathiesen's work is important for Ars Notoria and ritual manuscript traditions."),
    ("roger_bacon", "de_radiis", "SCHOLAR_OF", "Bacon belongs to debates over experiment, language, and natural powers relevant to De radiis."),
    ("theysolius", "liber_theysolius", "ATTRIBUTED_AUTHOR", "Theysolius is the attributed authority of the Liber Theysolius."),
    ("thomas_aquinas", "hazards_of_the_dark_arts", "SCHOLAR_OF", "Aquinas's treatments of superstition and demons shape later forbidden-arts classifications."),
    ("ulrich_molitor", "hazards_of_the_dark_arts", "SCHOLAR_OF", "Molitor belongs to late medieval witchcraft and demonological discussion."),
    ("valerie_flint", "magic_in_medieval_manuscripts", "SCHOLAR_OF", "Flint's work gives early medieval context for religion and magic."),
    ("william_of_auvergne", "speculum_astronomiae", "SCHOLAR_OF", "William of Auvergne is central to theological debate over image magic and demons."),
]

CONCEPT_TEXT_LINKS = [
    ("grimoire_corpus", "clavicula_salomonis"), ("grimoire_corpus", "hygromanteia"),
    ("grimoire_corpus", "liber_juratus_honorii"), ("grimoire_corpus", "liber_razielis"),
    ("grimoire_corpus", "book_of_oberon"), ("grimoire_corpus", "book_of_soyga"),
    ("grimoire_corpus", "heptameron"), ("grimoire_corpus", "lemegeton"),
    ("grimoire_corpus", "grimorium_verum"), ("solomonic_magic", "clavicula_salomonis"),
    ("solomonic_magic", "hygromanteia"), ("solomonic_magic", "testament_of_solomon"),
    ("solomonic_magic", "ars_goetia"), ("solomonic_magic", "lemegeton"),
    ("angelic_invocation", "ars_almadel"), ("angelic_invocation", "ars_paulina"),
    ("angelic_invocation", "liber_de_angelis"), ("angelic_invocation", "book_of_soyga"),
    ("ritual_diagrams", "ars_notoria"), ("ritual_diagrams", "book_of_soyga"),
    ("ritual_diagrams", "liber_razielis"), ("magical_alphabets", "book_of_soyga"),
    ("secret_names", "liber_razielis"), ("secret_names", "clavicula_salomonis"),
    ("pseudepigraphy", "clavicula_salomonis"), ("pseudepigraphy", "heptameron"),
    ("pseudepigraphy", "liber_juratus_honorii"), ("planetary_spirits", "ars_paulina"),
    ("planetary_spirits", "heptameron"), ("planetary_spirits", "picatrix"),
    ("scholastic_classification", "speculum_astronomiae"), ("occult_properties", "de_occultis_operibus_naturae"),
    ("celestial_influence", "de_radiis"), ("celestial_influence", "de_imaginibus"),
    ("university_condemnation", "speculum_astronomiae"), ("pastoral_care_and_magic", "hazards_of_the_dark_arts"),
    ("astral_image_magic", "liber_lunae"), ("celestial_influence", "liber_lunae"),
    ("solomonic_magic", "sixth_and_seventh_books_of_moses"), ("grimoire_corpus", "sixth_and_seventh_books_of_moses"),
    ("amulets", "magic_in_medieval_manuscripts"), ("charms", "magic_in_medieval_manuscripts"),
    ("geomancy", "hazards_of_the_dark_arts"), ("chiromancy", "hazards_of_the_dark_arts"),
]

CONCEPT_LINKS = [
    ("solomonic_magic", "grimoire_corpus", "PART_OF"),
    ("pseudepigraphy", "grimoire_corpus", "RELATED"),
    ("ritual_diagrams", "characters_and_seals", "RELATED"),
    ("magical_alphabets", "characters_and_seals", "PART_OF"),
    ("secret_names", "voces_magicae", "RELATED"),
    ("planetary_spirits", "astral_image_magic", "RELATED"),
    ("celestial_influence", "astral_image_magic", "RELATED"),
    ("occult_properties", "natural_magic", "RELATED"),
    ("scholastic_classification", "superstitio", "RELATED"),
    ("pastoral_care_and_magic", "superstitio", "RELATED"),
    ("university_condemnation", "condemned_arts", "RELATED"),
    ("amulets", "charms", "RELATED"),
    ("geomancy", "divination", "PART_OF"),
    ("chiromancy", "divination", "PART_OF"),
]


def coverage_report(conn):
    rows = []
    for table, label_col, key_col in [
        ("persons", "name", "person_id"),
        ("texts", "title", "text_id"),
        ("concepts", "label", "slug"),
    ]:
        total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        rows.append(f"- {table}: {total} seeded entries")

    isolated_texts = conn.execute(
        """
        SELECT t.title FROM texts t
        WHERE t.id NOT IN (SELECT text_id FROM concept_text_refs)
          AND t.id NOT IN (SELECT text_id FROM person_text_roles)
        ORDER BY t.title
        """
    ).fetchall()
    isolated_persons = conn.execute(
        """
        SELECT p.name FROM persons p
        WHERE p.id NOT IN (SELECT person_id FROM person_text_roles)
        ORDER BY p.name
        """
    ).fetchall()
    isolated_concepts = conn.execute(
        """
        SELECT c.label FROM concepts c
        WHERE c.id NOT IN (SELECT concept_id FROM concept_text_refs)
          AND c.id NOT IN (SELECT from_concept_id FROM concept_links)
          AND c.id NOT IN (SELECT to_concept_id FROM concept_links)
        ORDER BY c.label
        """
    ).fetchall()

    lines = [
        "# Coverage Audit",
        "",
        "Generated by `scripts/seed_relationships_and_coverage_audit.py`. This report tracks the portal's progress toward comprehensive coverage and highlights isolated draft entries that need relational work.",
        "",
        "## Counts",
        "",
        *rows,
        "",
        "## Remaining Isolated Texts",
        "",
        *(f"- {row[0]}" for row in isolated_texts),
        "",
        "## Remaining Isolated Persons",
        "",
        *(f"- {row[0]}" for row in isolated_persons),
        "",
        "## Remaining Isolated Concepts",
        "",
        *(f"- {row[0]}" for row in isolated_concepts),
        "",
    ]
    (BASE_DIR / "COVERAGE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    for person, text, role, notes in PERSON_TEXT_LINKS:
        link_person_text(conn, person, text, role, notes)
    for concept, text in CONCEPT_TEXT_LINKS:
        link_concept_text(conn, concept, text, "Seeded comprehensive relationship.")
    for source, target, relationship in CONCEPT_LINKS:
        link_concepts(conn, source, target, relationship, "Seeded comprehensive concept relationship.")
    conn.commit()
    coverage_report(conn)
    for table in ("person_text_roles", "concept_text_refs", "concept_links"):
        print(f"{table}: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
    print(f"Wrote {BASE_DIR / 'COVERAGE_AUDIT.md'}")
    conn.close()


if __name__ == "__main__":
    main()

import re
import sqlite3

from common import DB_PATH, ensure_dirs


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
    conn.execute(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) "
        f"ON CONFLICT({key}) DO UPDATE SET {updates}",
        [row[c] for c in columns],
    )


SCHOLARS = [
    ("david_pingree", "David Pingree", "Historian of exact sciences, astrology, and astral magic whose work is essential for Arabic, Greek, Sanskrit, and Latin transmission histories."),
    ("valerie_flint", "Valerie Flint", "Historian of early medieval religion and magic whose work shaped debates about Christianization, pastoral care, and magical survivals."),
    ("robert_mathiesen", "Robert Mathiesen", "Scholar of ritual magic manuscripts and Solomonic textual traditions, especially relevant to Ars Notoria and grimoire transmission."),
    ("jan_veenstra", "Jan R. Veenstra", "Historian of magic, learned culture, and intellectual history whose work connects medieval classifications to Renaissance magic."),
    ("charles_burnett", "Charles Burnett", "Historian of Arabic-Latin transmission, astrology, natural philosophy, and occult sciences in the medieval Latin West."),
    ("paola_zambelli", "Paola Zambelli", "Historian of astrology, magic, scholastic debates, and the Speculum astronomiae tradition."),
    ("agostino_paravicini_bagliani", "Agostino Paravicini Bagliani", "Historian of medieval learned culture, astrology, medicine, and courtly/scientific contexts relevant to occult knowledge."),
    ("don_c_skemer", "Don C. Skemer", "Manuscript scholar whose work on textual amulets and written protection is central for charms and apotropaic writing."),
    ("lea_olsan", "Lea T. Olsan", "Scholar of charms, healing prayers, and vernacular ritual language in medieval manuscript contexts."),
    ("katelyn_mesler", "Katelyn Mesler", "Scholar of Jewish, Christian, and ritual magic traditions, including Solomonic and angelological transmission."),
    ("florence_chave_mahir", "Florence Chave-Mahir", "Scholar of exorcism, liturgy, ritual authority, and the borderlands of religious and magical practice."),
    ("beatice_delaurenti", "Béatrice Delaurenti", "Historian of medieval knowledge, marvels, nature, and the conceptual edges of natural and occult causality."),
]

FIGURES = [
    ("roger_bacon", "Roger Bacon", "PHILOSOPHER", "MEDIEVAL", "Thirteenth-century Franciscan philosopher whose discussions of experiment, language, optics, astrology, and natural powers are central to medieval debates over knowledge and magic."),
    ("albertus_magnus", "Albertus Magnus", "PHILOSOPHER", "MEDIEVAL", "Thirteenth-century Dominican philosopher whose authority shaped scholastic natural philosophy, astrology, minerals, animals, and debates over occult properties."),
    ("thomas_aquinas", "Thomas Aquinas", "THEOLOGIAN", "MEDIEVAL", "Thirteenth-century Dominican theologian whose discussions of demons, superstition, divination, and illicit pact shaped later scholastic classifications of magic."),
    ("william_of_auvergne", "William of Auvergne", "THEOLOGIAN", "MEDIEVAL", "Thirteenth-century bishop and theologian whose treatment of demons, image magic, and illicit ritual is central to medieval demonological classification."),
    ("peter_abano", "Pietro d'Abano", "PHILOSOPHER", "MEDIEVAL", "Italian physician and philosopher associated with astrology, astral causality, and later magical attributions."),
    ("arnald_of_villanova", "Arnald of Villanova", "PHYSICIAN", "MEDIEVAL", "Physician and religious writer whose attributed corpus became entangled with medical, alchemical, and astrological materials."),
    ("john_of_salisbury", "John of Salisbury", "CLERIC", "MEDIEVAL", "Twelfth-century cleric whose critique of courtly divination and occult practices is important for earlier medieval moral classification."),
    ("nicole_oresme", "Nicole Oresme", "PHILOSOPHER", "MEDIEVAL", "Fourteenth-century philosopher and bishop whose criticism of astrology and divination belongs to late medieval debates over celestial influence."),
    ("augustine_of_hippo", "Augustine of Hippo", "THEOLOGIAN", "LATE_ANTIQUE", "Late antique Christian theologian whose account of demons, signs, superstition, and illicit curiosity shaped medieval classifications of magic."),
    ("isidore_of_seville", "Isidore of Seville", "THEOLOGIAN", "MEDIEVAL", "Early medieval encyclopedist whose etymological classifications of magic, divination, and pagan learning shaped later reference traditions."),
    ("al_kindi", "al-Kindi", "PHILOSOPHER", "MEDIEVAL", "Arabic philosopher associated in Latin reception with De radiis and theories of rays, causality, words, and celestial influence."),
    ("abu_mashar", "Abu Ma'shar", "ASTROLOGER", "MEDIEVAL", "Ninth-century astrologer whose works shaped Latin astrology and the learned background for astral magic and image theory."),
]

GRIMOIRES_AND_TEXTS = [
    ("clavicula_salomonis", "Clavicula Salomonis", "LATIN", "GRIMOIRE", "MEDIEVAL", "The Key of Solomon is a major Solomonic grimoire tradition transmitted in late medieval and early modern manuscripts, important for ritual purity, seals, conjurations, and textual instability."),
    ("hygromanteia", "Hygromanteia", "GREEK", "GRIMOIRE", "MEDIEVAL", "The Hygromanteia is a Byzantine Greek Solomonic ritual tradition that stands behind later Key of Solomon materials and complicates Latin-centered grimoire histories."),
    ("testament_of_solomon", "Testament of Solomon", "GREEK", "PRIMARY_SOURCE", "LATE_ANTIQUE", "The Testament of Solomon is a late antique demonological text that made Solomon a paradigmatic commander of spirits in later magical and literary traditions."),
    ("liber_de_angelis", "Liber de angelis", "LATIN", "GRIMOIRE", "MEDIEVAL", "The Liber de angelis names a family of Latin ritual texts concerned with angelic knowledge, invocation, and the textual authority of revealed ritual."),
    ("liber_visionum", "Liber visionum", "LATIN", "PRIMARY_SOURCE", "MEDIEVAL", "The Liber visionum is associated with John of Morigny's visionary and ritual reworking of Ars Notoria materials."),
    ("flowers_of_heavenly_teaching", "Flowers of Heavenly Teaching", "LATIN", "PRIMARY_SOURCE", "MEDIEVAL", "The Flowers of Heavenly Teaching names John of Morigny's revised ritual and visionary project for divinely assisted knowledge."),
    ("munich_manual", "Munich Manual", "LATIN", "MANUSCRIPT_COMPILATION", "MEDIEVAL", "The Munich Manual is the fifteenth-century necromantic manuscript edited and analyzed by Richard Kieckhefer in Forbidden Rites."),
    ("book_of_oberon", "Book of Oberon", "ENGLISH", "GRIMOIRE", "EARLY_MODERN", "The Book of Oberon is an early modern English ritual magic compilation that preserves and transforms medieval Solomonic and spirit-conjuring materials."),
    ("book_of_soyga", "Book of Soyga", "LATIN", "GRIMOIRE", "EARLY_MODERN", "The Book of Soyga is an early modern angelological and cryptographic ritual text associated with John Dee and earlier learned magical traditions."),
    ("heptameron", "Heptameron", "LATIN", "GRIMOIRE", "EARLY_MODERN", "The Heptameron is a ritual magic text attributed to Pietro d'Abano in print tradition and central to early modern angelic and planetary conjuration."),
    ("ars_almadel", "Ars Almadel", "LATIN", "GRIMOIRE", "EARLY_MODERN", "The Ars Almadel is a Solomonic angelic ritual text transmitted in early modern grimoire compilations and linked to older angelic invocation traditions."),
    ("ars_paulina", "Ars Paulina", "LATIN", "GRIMOIRE", "EARLY_MODERN", "The Ars Paulina is a Solomonic text of planetary and zodiacal angelic invocation preserved in early modern Lemegeton traditions."),
    ("ars_goetia", "Ars Goetia", "LATIN", "GRIMOIRE", "EARLY_MODERN", "The Ars Goetia is an early modern Solomonic demon catalogue and conjuring text whose roots and reception belong to the wider grimoire tradition."),
    ("lemegeton", "Lemegeton", "ENGLISH", "GRIMOIRE", "EARLY_MODERN", "The Lemegeton or Lesser Key of Solomon is an early modern Solomonic compilation whose parts preserve angelic, demonic, and planetary ritual traditions."),
    ("grimorium_verum", "Grimorium Verum", "FRENCH", "GRIMOIRE", "EARLY_MODERN", "Grimorium Verum is an early modern printed grimoire important for the post-medieval reception and reorganization of spirit conjuration traditions."),
    ("sixth_and_seventh_books_of_moses", "Sixth and Seventh Books of Moses", "GERMAN", "GRIMOIRE", "EARLY_MODERN", "The Sixth and Seventh Books of Moses are early modern/modern grimoire traditions relevant to the long reception of biblical magical authority."),
    ("liber_lunae", "Liber Lunae", "LATIN", "GRIMOIRE", "MEDIEVAL", "The Liber Lunae is a Latin lunar and astral ritual text associated with image magic, timing, and the broader learned magical manuscript corpus."),
    ("de_occultis_operibus_naturae", "De occultis operibus naturae", "LATIN", "TREATISE", "MEDIEVAL", "De occultis operibus naturae names a scholastic problem field concerning hidden natural powers, occult properties, and the boundary between nature and magic."),
]

CONCEPTS = [
    ("grimoire_corpus", "Grimoire Corpus", "HISTORIOGRAPHICAL", "ANALYST_TERM", "Grimoire corpus is an Analyst Term for the unstable family of manuscript and printed ritual books attributed to Solomon, Honorius, Raziel, angels, or ancient sages; the portal must track each text individually rather than treating grimoires as interchangeable."),
    ("solomonic_magic", "Solomonic Magic", "HISTORIOGRAPHICAL", "HYBRID", "Solomonic magic names traditions that invoke Solomon's authority for spirit command, seals, ritual purity, and secret knowledge; it is both an actor strategy of attribution and a modern scholarly category."),
    ("scholastic_classification", "Scholastic Classification of Magic", "HISTORIOGRAPHICAL", "ANALYST_TERM", "Scholastic classification of magic denotes the theological and philosophical sorting of practices into natural, demonic, superstitious, divinatory, or licit forms by medieval intellectuals."),
    ("occult_properties", "Occult Properties", "NATURAL_PHILOSOPHY", "HYBRID", "Occult properties are hidden natural powers invoked in scholastic natural philosophy to explain effects not reducible to manifest qualities, creating a crucial boundary zone with natural magic."),
    ("celestial_influence", "Celestial Influence", "NATURAL_PHILOSOPHY", "HYBRID", "Celestial influence names medieval theories of astral causation that support astrology, image magic, medicine, and debates over determinism."),
    ("university_condemnation", "University Condemnation", "LEGAL", "ANALYST_TERM", "University condemnation is an Analyst Term for institutional acts that classified, restricted, or prohibited suspect doctrines and practices, including astrology, image magic, and demonic arts."),
    ("pastoral_care_and_magic", "Pastoral Care and Magic", "THEOLOGICAL", "ANALYST_TERM", "Pastoral care and magic names the confessional, preaching, and catechetical settings in which clergy identified charms, divination, and superstition as problems of Christian discipline."),
    ("pseudepigraphy", "Pseudepigraphy", "MANUSCRIPT", "ANALYST_TERM", "Pseudepigraphy is an Analyst Term for attribution to authoritative figures such as Solomon, Honorius, Raziel, Aristotle, or Hermes; in grimoire studies it is a central mechanism of textual authority."),
    ("ritual_diagrams", "Ritual Diagrams", "MANUSCRIPT", "ANALYST_TERM", "Ritual diagrams are visual structures such as circles, notae, seals, tables, and figures that organize ritual knowledge and require attention to manuscript layout and copying."),
    ("magical_alphabets", "Magical Alphabets", "MANUSCRIPT", "ANALYST_TERM", "Magical alphabets are nonordinary scripts and character systems used in ritual texts, amulets, and seals; they are visual technologies of secrecy, authority, and transmission."),
    ("planetary_spirits", "Planetary Spirits", "ASTRAL", "HYBRID", "Planetary spirits are named intelligences, angels, or demons associated with planets in ritual and astral texts, linking astrology to invocation and image practice."),
    ("secret_names", "Secret Names", "RITUAL", "HYBRID", "Secret names are divine, angelic, demonic, or voces magicae names whose ritual force is tied to secrecy, antiquity, revelation, or exact textual transmission."),
]


def main():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    for slug, name, desc in SCHOLARS:
        upsert(conn, "persons", "person_id", {
            "person_id": slug, "name": name, "era": "MODERN", "role_primary": "SCHOLAR",
            "scholar_group": "Medieval Magic and Manuscript Studies", "description": desc,
            "source_method": "COMPREHENSIVE_COVERAGE", "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for slug, name, role, era, desc in FIGURES:
        upsert(conn, "persons", "person_id", {
            "person_id": slug, "name": name, "era": era, "role_primary": role,
            "description": desc, "source_method": "COMPREHENSIVE_COVERAGE",
            "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for text_id, title, language, text_type, period, desc in GRIMOIRES_AND_TEXTS:
        upsert(conn, "texts", "text_id", {
            "text_id": text_id, "title": title, "language": language, "text_type": text_type,
            "period": period, "description": desc, "source_method": "COMPREHENSIVE_COVERAGE",
            "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for slug, label, category, category_type, desc in CONCEPTS:
        upsert(conn, "concepts", "slug", {
            "slug": slug, "label": label, "category": category, "category_type": category_type,
            "definition_short": desc, "significance": desc,
            "source_method": "COMPREHENSIVE_COVERAGE", "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    conn.commit()
    for table in ("persons", "texts", "concepts"):
        print(f"{table}: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()

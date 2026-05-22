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
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) ON CONFLICT({key}) DO UPDATE SET {updates}"
    conn.execute(sql, [row[c] for c in columns])


PERSONS = [
    ("benedek_lang", "Benedek Lang", "SCHOLAR", "MODERN", "Central European manuscript libraries, learned magic, and the codicological history of ritual texts."),
    ("lynn_thorndike", "Lynn Thorndike", "SCHOLAR", "MODERN", "Early twentieth-century historian whose multi-volume history made magic and experimental science a continuous object of medieval intellectual history."),
    ("nicolas_weill_parot", "Nicolas Weill-Parot", "SCHOLAR", "MODERN", "Historian of astral image theory, scholastic natural philosophy, and the boundary between licit and illicit image practices."),
    ("jean_patrice_boudet", "Jean-Patrice Boudet", "SCHOLAR", "MODERN", "Historian of medieval astrology, divination, learned magic, and manuscript transmission in the Latin West."),
    ("julien_veronese", "Julien Veronese", "SCHOLAR", "MODERN", "Scholar of ritual magic, the Ars Notoria, and manuscript traditions of angelic and learned ritual practice."),
    ("johannes_hartlieb", "Johannes Hartlieb", "AUTHOR", "MEDIEVAL", "Fifteenth-century Bavarian physician and author of advice literature on forbidden arts, witchcraft, and princely governance."),
    ("ulrich_molitor", "Ulrich Molitor", "AUTHOR", "MEDIEVAL", "Late medieval jurist and author associated with learned discussion of witchcraft and demonic magic."),
    ("john_of_morigny", "John of Morigny", "MONK", "MEDIEVAL", "Fourteenth-century Benedictine monk whose visionary autobiography and ritual book reworked the Ars Notoria in Marian and monastic terms."),
    ("honorius_of_thebes", "Honorius of Thebes", "ATTRIBUTED_AUTHORITY", "MEDIEVAL", "Attributed authorial figure attached to the Sworn Book of Honorius and traditions of angelic ritual magic."),
    ("raziel", "Raziel", "ATTRIBUTED_AUTHORITY", "MEDIEVAL", "Angelic authority associated with the Liber Razielis and related Jewish and Latin traditions of revealed esoteric knowledge."),
    ("solomon", "Solomon", "ATTRIBUTED_AUTHORITY", "MEDIEVAL", "Biblical king whose attributed authority structures major medieval and early modern traditions of spirit command, talismanic lore, and ritual experiment."),
    ("theysolius", "Theysolius", "ATTRIBUTED_AUTHORITY", "MEDIEVAL", "Attributed or textual authority associated with the Liber Theysolius and traditions concerning familiar spirits and wisdom."),
]

CONCEPTS = [
    ("familiar_spirit", "Familiar Spirit", "RITUAL", "ACTOR_TERM", "Familiar spirit is an Actor Term in many late medieval and early modern contexts for a spirit bound to, assisting, or repeatedly contacted by a practitioner; modern scholars use the category cautiously because legal, literary, and ritual sources describe such spirits in different registers."),
    ("magic_and_cognition", "Magic and Cognition", "HISTORIOGRAPHICAL", "ANALYST_TERM", "Magic and cognition is an Analyst Term for scholarship that studies medieval magical practice through memory, perception, learning, ritual attention, and the mental operations implied by diagrams, prayers, images, and repeated procedures."),
    ("manuscript_miscellany", "Manuscript Miscellany", "MANUSCRIPT", "ANALYST_TERM", "Manuscript miscellany is an Analyst Term for codices that collect heterogeneous texts; in medieval magic scholarship it matters because ritual, medical, devotional, astrological, and divinatory materials often survive together rather than in isolated genre books."),
    ("clerical_underworld", "Clerical Underworld", "HISTORIOGRAPHICAL", "ANALYST_TERM", "Clerical underworld is an Analyst Term associated especially with Richard Kieckhefer's account of literate clerics who copied, adapted, and used illicit ritual texts while remaining within ecclesiastical culture."),
    ("angelic_invocation", "Angelic Invocation", "RITUAL", "HYBRID", "Angelic invocation names ritual address to angels in medieval texts; it may function as an actor practice in prayer-based ritual books and as an analyst category for the study of theurgic or devotional magic."),
    ("demonic_pact", "Demonic Pact", "DEMONOLOGICAL", "HYBRID", "Demonic pact is a theological and legal category used to explain illicit magic as explicit or implicit agreement with demons, while modern historians analyze it as a polemical and juridical tool rather than a transparent description of practice."),
    ("necromancy", "Necromancy", "DEMONOLOGICAL", "ANALYST_TERM", "Necromancy is an Analyst Term in much modern scholarship for learned spirit-conjuring practices, although medieval Latin nigromantia often carried broader associations with illicit demonic magic rather than the literal raising of the dead."),
    ("divination", "Divination", "RITUAL", "HYBRID", "Divination covers practices for obtaining hidden knowledge, from geomancy and sortilege to astrological judgment; medieval sources classify it variously as natural, superstitious, demonic, or licit depending on method and authority."),
    ("geomancy", "Geomancy", "RITUAL", "ACTOR_TERM", "Geomancy is an Actor Term for a learned divinatory art based on figures generated by points or marks and interpreted through structured houses, often circulating with astrology and other clerical arts."),
    ("chiromancy", "Chiromancy", "RITUAL", "ACTOR_TERM", "Chiromancy is an Actor Term for palmistry or hand-reading, a divinatory practice treated in medieval manuals and often debated within broader classifications of natural signs and illicit prediction."),
    ("charms", "Charms", "RITUAL", "ANALYST_TERM", "Charms is an Analyst Term for spoken, written, or performed formulae used for healing, protection, coercion, or divination; the category requires care because medieval sources may frame the same materials as prayer, medicine, superstition, or magic."),
    ("amulets", "Amulets", "RITUAL", "ANALYST_TERM", "Amulets are objects worn or carried for protection, healing, or influence, frequently combining inscriptions, images, materials, and ritual timing in ways that cross medical, devotional, and magical classifications."),
    ("talismans", "Talismans", "ASTRAL", "ANALYST_TERM", "Talismans are crafted objects intended to mediate celestial, spiritual, or symbolic power; in medieval scholarship the term often overlaps with image magic, astral magic, and Arabic-Latin theories of celestial influence."),
    ("suffumigation", "Suffumigation", "RITUAL", "ACTOR_TERM", "Suffumigation is an Actor Term for ritual fumigation with incense, herbs, or other substances, often coordinated with planetary timing, spirit address, purification, or image consecration."),
    ("characters_and_seals", "Characters and Seals", "MANUSCRIPT", "HYBRID", "Characters and seals are graphic signs used in ritual, talismanic, and angelic materials; they matter as manuscript phenomena because their transmission depends on visual copying as much as verbal text."),
    ("voces_magicae", "Voces Magicae", "RITUAL", "ANALYST_TERM", "Voces magicae is an Analyst Term for nonordinary ritual words, names, and syllables whose efficacy is attached to sound, secrecy, antiquity, or divine and angelic names."),
    ("ritual_purity", "Ritual Purity", "RITUAL", "HYBRID", "Ritual purity names requirements of confession, fasting, abstinence, cleanliness, prayer, or moral preparation that structure many medieval ritual magic texts and blur devotional and magical categories."),
    ("condemned_arts", "Condemned Arts", "LEGAL", "HYBRID", "Condemned arts is a hybrid category for practices classified as illicit by theologians, jurists, pastoral writers, or university authorities, including divination, demonic invocation, image magic, and suspect ritual learning."),
]

TEXTS = [
    ("unlocked_books", "Unlocked Books", "ENGLISH", "SCHOLARSHIP", "MODERN", "Benedek Lang's study of manuscripts of learned magic in Central European libraries foregrounds codicology, ownership, and library context as evidence for learned magical transmission."),
    ("magic_in_medieval_manuscripts", "Magic in Medieval Manuscripts", "ENGLISH", "SCHOLARSHIP", "MODERN", "Sophie Page's study examines medieval manuscript evidence for magical texts and the codicological contexts in which occult, devotional, and scientific materials circulated."),
    ("hazards_of_the_dark_arts", "Hazards of the Dark Arts", "ENGLISH", "EDITION", "MODERN", "Richard Kieckhefer's translation and study of Johannes Hartlieb's advice for princes places witchcraft, magic, and prohibited arts within fifteenth-century political and moral counsel."),
    ("liber_theysolius", "Liber Theysolius", "LATIN", "PRIMARY_SOURCE", "MEDIEVAL", "The Liber Theysolius is a medieval text associated in recent scholarship with wisdom, familiar spirits, and the pursuit of knowledge through ritualized contact."),
    ("liber_juratus_honorii", "Liber Juratus Honorii", "LATIN", "PRIMARY_SOURCE", "MEDIEVAL", "The Liber Juratus Honorii, or Sworn Book of Honorius, is a major Latin ritual text concerning divine vision, angelic hierarchy, and sworn secrecy."),
    ("liber_razielis", "Liber Razielis", "LATIN", "PRIMARY_SOURCE", "MEDIEVAL", "The Liber Razielis is a Latin textual complex associated with angelic revelation, astral knowledge, and the figure of Raziel."),
    ("de_radiis", "De radiis", "LATIN", "TREATISE", "MEDIEVAL", "De radiis, associated with al-Kindi in Latin tradition, theorizes rays, celestial causality, and the efficacy of words and images in medieval natural philosophy."),
    ("de_imaginibus", "De imaginibus", "LATIN", "TREATISE", "MEDIEVAL", "De imaginibus is a Latin astral-image text attributed to Thabit ibn Qurra and important for theories of talismanic images and celestial timing."),
    ("speculum_astronomiae", "Speculum astronomiae", "LATIN", "TREATISE", "MEDIEVAL", "The Speculum astronomiae classifies astrological and image-making texts and became a crucial witness for scholastic attempts to distinguish licit astronomy from illicit image magic."),
    ("history_magic_experimental_science", "A History of Magic and Experimental Science", "ENGLISH", "SCHOLARSHIP", "MODERN", "Lynn Thorndike's multi-volume history framed magic and experimental science as intertwined parts of medieval intellectual history, even where later scholarship has revised its assumptions."),
]

TIMELINE = [
    (1350, None, "COMPOSITION", "John of Morigny reworks the Ars Notoria", "c. 1350, northern France: John of Morigny composes and revises a visionary and ritual work that transforms Ars Notoria materials through Marian devotion, monastic autobiography, and claims of correction. Claire Fanger's work has made this case central for understanding how medieval ritual learning could be simultaneously devotional, visionary, and suspect."),
    (1456, None, "COMPOSITION", "Johannes Hartlieb writes on prohibited arts", "1456, Bavaria: Johannes Hartlieb composes advice literature for princely readers on forbidden arts, witchcraft, and magic. The work is significant because it joins courtly counsel, medical learning, and moral warning at a moment when late medieval categories of witchcraft and ritual magic were being systematized."),
    (1923, None, "SCHOLARSHIP", "Thorndike publishes the first volumes of A History of Magic and Experimental Science", "1923, New York: Lynn Thorndike publishes early volumes of A History of Magic and Experimental Science, establishing a vast documentary frame for the entanglement of magic, natural philosophy, astrology, and experimental inquiry. Later scholars have revised Thorndike's evolutionary assumptions while continuing to rely on the scope of his evidence."),
    (2008, None, "SCHOLARSHIP", "Benedek Lang publishes Unlocked Books", "2008, University Park, Pennsylvania: Benedek Lang publishes Unlocked Books, shifting attention toward Central European manuscript libraries, ownership, and codicological evidence. The study broadens medieval magic scholarship beyond famous Latin treatises toward the practical survival of learned magic in library collections."),
]

CONCEPT_LINKS = [
    ("necromancy", "nigromantia", "RELATED"),
    ("clerical_underworld", "learned_magic", "RELATED"),
    ("manuscript_miscellany", "grimoire", "CONTRASTED"),
    ("angelic_invocation", "ars_notoria", "RELATED"),
    ("demonic_pact", "superstitio", "RELATED"),
    ("talismans", "astral_image_magic", "RELATED"),
    ("suffumigation", "astral_image_magic", "PART_OF"),
    ("characters_and_seals", "grimoire", "PART_OF"),
    ("voces_magicae", "angelic_invocation", "RELATED"),
    ("ritual_purity", "angelic_invocation", "PART_OF"),
    ("condemned_arts", "superstitio", "RELATED"),
]

CONCEPT_TEXTS = {
    "familiar_spirit": ["liber_theysolius"],
    "magic_and_cognition": ["invoking_angels"],
    "manuscript_miscellany": ["unlocked_books", "magic_in_medieval_manuscripts"],
    "clerical_underworld": ["forbidden_rites"],
    "angelic_invocation": ["ars_notoria", "liber_juratus_honorii"],
    "demonic_pact": ["hazards_of_the_dark_arts"],
    "necromancy": ["forbidden_rites"],
    "divination": ["hazards_of_the_dark_arts"],
    "talismans": ["de_imaginibus", "picatrix"],
    "suffumigation": ["picatrix", "de_imaginibus"],
    "characters_and_seals": ["liber_razielis", "ars_notoria"],
    "ritual_purity": ["liber_juratus_honorii", "ars_notoria"],
    "condemned_arts": ["hazards_of_the_dark_arts", "speculum_astronomiae"],
}


def id_for(conn, table, key_col, value):
    row = conn.execute(f"SELECT id FROM {table} WHERE {key_col}=?", (value,)).fetchone()
    return row[0] if row else None


def main():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    for pid, name, role, era, desc in PERSONS:
        upsert(conn, "persons", "person_id", {
            "person_id": pid, "name": name, "role_primary": role, "era": era,
            "scholar_group": "Medieval Magic and Manuscript Studies" if role == "SCHOLAR" else None,
            "description": desc, "source_method": "CORPUS_DISCOVERY", "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for slug, label, category, category_type, desc in CONCEPTS:
        upsert(conn, "concepts", "slug", {
            "slug": slug, "label": label, "category": category, "category_type": category_type,
            "definition_short": desc, "significance": desc,
            "source_method": "CORPUS_DISCOVERY", "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for tid, title, language, text_type, period, desc in TEXTS:
        upsert(conn, "texts", "text_id", {
            "text_id": tid, "title": title, "language": language, "text_type": text_type, "period": period,
            "description": desc, "source_method": "CORPUS_DISCOVERY", "review_status": "DRAFT", "confidence": "MEDIUM",
        })

    for year, year_end, event_type, title, desc in TIMELINE:
        conn.execute(
            "INSERT OR IGNORE INTO timeline_events (year, year_end, event_type, title, description, confidence) VALUES (?, ?, ?, ?, ?, 'MEDIUM')",
            (year, year_end, event_type, title, desc),
        )

    for concept, texts in CONCEPT_TEXTS.items():
        concept_id = id_for(conn, "concepts", "slug", concept)
        for text in texts:
            text_id = id_for(conn, "texts", "text_id", text)
            if concept_id and text_id:
                conn.execute(
                    "INSERT OR IGNORE INTO concept_text_refs (concept_id, text_id, notes) VALUES (?, ?, ?)",
                    (concept_id, text_id, "Seeded from corpus discovery expansion."),
                )

    for source, target, relationship in CONCEPT_LINKS:
        source_id = id_for(conn, "concepts", "slug", source)
        target_id = id_for(conn, "concepts", "slug", target)
        if source_id and target_id:
            conn.execute(
                "INSERT OR IGNORE INTO concept_links (from_concept_id, to_concept_id, relationship, notes) VALUES (?, ?, ?, ?)",
                (source_id, target_id, relationship, "Seeded from corpus discovery expansion."),
            )

    conn.commit()
    for table in ["persons", "texts", "concepts", "concept_links", "concept_text_refs", "timeline_events"]:
        print(f"{table}: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()

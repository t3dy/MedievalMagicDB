"""
Seed the Solomonic Magic section.

Adds section_tag TEXT column to timeline_events, backfills reception tags,
seeds Solomonic persons, texts, concepts, timeline events, and relationships.
Run this script after seed_reception_section.py.
"""
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DB_PATH


def migrate_schema(conn):
    cols = {r[1] for r in conn.execute("PRAGMA table_info(timeline_events)").fetchall()}
    if "section_tag" not in cols:
        conn.execute("ALTER TABLE timeline_events ADD COLUMN section_tag TEXT")
        print("Added section_tag column to timeline_events")


def backfill_reception_tags(conn):
    conn.execute(
        "UPDATE timeline_events SET section_tag='reception' WHERE year >= 1438 AND section_tag IS NULL"
    )
    n = conn.execute("SELECT changes()").fetchone()[0]
    print(f"Backfilled {n} reception timeline events")


def seed_persons(conn):
    persons = [
        {
            "person_id": "pablo_torijano",
            "name": "Pablo Torijano",
            "era": "MODERN",
            "role_primary": "SCHOLAR",
            "description": (
                "Specialist in the esoteric traditions associated with Solomon in late antique "
                "and medieval Jewish, Christian, and Islamic sources. His Solomon the Esoteric "
                "King (2002) traces how the biblical king became a master of angels, demons, "
                "and occult knowledge, fundamentally reshaping scholarly understanding of "
                "Solomonic textual authority across religious boundaries."
            ),
        },
        {
            "person_id": "gideon_bohak",
            "name": "Gideon Bohak",
            "era": "MODERN",
            "role_primary": "SCHOLAR",
            "description": (
                "Professor of Jewish philosophy at Tel Aviv University and leading authority "
                "on ancient Jewish magic. His Ancient Jewish Magic: A History (Cambridge, 2008) "
                "provides the most comprehensive account of Jewish magical practice from "
                "antiquity through the rabbinic period, treating amulets, adjurations, "
                "Solomonic traditions, and the multilingual magical papyri that document "
                "a shared Mediterranean magical culture."
            ),
        },
        {
            "person_id": "dennis_duling",
            "name": "Dennis C. Duling",
            "era": "MODERN",
            "role_primary": "SCHOLAR",
            "description": (
                "New Testament scholar and translator of the Testament of Solomon in "
                "James Charlesworth's Old Testament Pseudepigrapha (Doubleday, 1983). "
                "Duling's annotated translation made the Testament accessible to "
                "mainstream biblical scholarship and remains the standard English edition, "
                "contextualizing the text within first-century Jewish and Christian "
                "demonological thought and Solomonic legend."
            ),
        },
        {
            "person_id": "elias_ashmole",
            "name": "Elias Ashmole",
            "era": "EARLY_MODERN",
            "role_primary": "COLLECTOR",
            "description": (
                "English antiquary, astrologer, and founding collector (1617–1692) whose "
                "manuscript collection at the Bodleian Library (Ashmole MSS) became one "
                "of the principal repositories of English magical manuscripts. Ashmole "
                "studied, copied, and preserved Solomonic and astrological texts including "
                "the Ars Notoria, Key of Solomon variants, and alchemical manuscripts, "
                "linking the learned magical tradition to early modern antiquarianism and "
                "the emerging scientific culture of the Royal Society."
            ),
        },
        {
            "person_id": "herman_gollancz",
            "name": "Herman Gollancz",
            "era": "MODERN",
            "role_primary": "EDITOR",
            "description": (
                "British rabbi and orientalist (1852–1930) who edited the Hebrew Mafteah "
                "Shelomoh (Key of Solomon) from the British Museum manuscript (Oriental "
                "MS 14759) for the Oriental Translation Fund (1914). Gollancz's edition "
                "was the first critical edition of a Hebrew recension of the Clavicula "
                "Salomonis, establishing that Hebrew versions of the Key of Solomon "
                "circulated independently of the Latin tradition and preserving Solomonic "
                "ritual formulas in their original linguistic setting."
            ),
        },
        {
            "person_id": "michael_morgan",
            "name": "Michael A. Morgan",
            "era": "MODERN",
            "role_primary": "EDITOR",
            "description": (
                "Scholar who produced the first English translation of Sepher ha-Razim "
                "(The Book of Mysteries) published by the Society of Biblical Literature "
                "in 1983. Morgan's translation of Mordecai Margalioth's 1966 critical "
                "Hebrew edition made this foundational Jewish magical text available to "
                "English-language scholars of late antique and medieval magic, enabling "
                "comparative study of its angel hierarchies and Solomonic framework with "
                "Latin and Greek magical traditions."
            ),
        },
        {
            "person_id": "etienne_tempier",
            "name": "Étienne Tempier",
            "era": "MEDIEVAL",
            "role_primary": "THEOLOGIAN",
            "description": (
                "Bishop of Paris (d. 1279) whose condemnations of 1270 (13 theses) and "
                "1277 (219 theses) defined the institutional limits of scholastic natural "
                "philosophy, including the condemnation of astrological determinism, "
                "the claim that celestial bodies determine terrestrial events, and related "
                "propositions that bore on learned magic. The 1277 condemnations reshaped "
                "the intellectual context for all subsequent medieval treatments of "
                "divination, image magic, and natural magical theory."
            ),
        },
    ]
    for p in persons:
        conn.execute(
            """INSERT OR IGNORE INTO persons
               (person_id, name, era, role_primary, description)
               VALUES (:person_id,:name,:era,:role_primary,:description)""",
            p,
        )
    print(f"Seeded {len(persons)} Solomonic/scholasticism persons")


def seed_texts(conn):
    texts = [
        {
            "text_id": "sepher_ha_razim",
            "title": "Sepher ha-Razim",
            "text_type": "PRIMARY_SOURCE",
            "period": "LATE_ANTIQUE",
            "language": "HEBREW",
            "description": (
                "The Book of Mysteries (Sepher ha-Razim) is a Hebrew magical handbook "
                "whose compilation is usually dated to the 7th–10th century CE, though "
                "it draws on much older traditions of angel magic. Attributed to Noah "
                "and transmitted through Shem, the text organizes the seven heavens "
                "and their angelic inhabitants, providing adjurations, incantations, "
                "and ritual procedures keyed to each heavenly realm. Its framework "
                "of named angels ordered by celestial sphere connects to both the "
                "Solomonic grimoire tradition and broader Jewish mystical cosmology. "
                "The standard critical edition is Mordecai Margalioth's 1966 Hebrew "
                "text; Morgan's English translation appeared in 1983."
            ),
        },
        {
            "text_id": "solomon_esoteric_king",
            "title": "Solomon the Esoteric King",
            "text_type": "SCHOLARSHIP",
            "period": "MODERN",
            "language": "ENGLISH",
            "description": (
                "Pablo Torijano's Solomon the Esoteric King: From King to Magus, "
                "Development of a Tradition (Brill, 2002) traces the transformation "
                "of the biblical Solomon into a master of demons, occult knowledge, "
                "and magical authority across Jewish, Christian, and Islamic sources "
                "from the Second Temple period through the medieval era. Torijano "
                "analyzes the Testament of Solomon, Solomonic adjurations, and the "
                "pseudepigraphic authority of the Solomonic corpus as a cross-cultural "
                "phenomenon. Reviewed by Frank Klaassen and others as foundational "
                "for understanding Solomonic attribution as a legitimating strategy."
            ),
        },
        {
            "text_id": "ancient_jewish_magic",
            "title": "Ancient Jewish Magic: A History",
            "text_type": "SCHOLARSHIP",
            "period": "MODERN",
            "language": "ENGLISH",
            "description": (
                "Gideon Bohak's Ancient Jewish Magic: A History (Cambridge University "
                "Press, 2008) surveys Jewish magical practice from the biblical period "
                "through the end of antiquity, drawing on amulets, magical papyri, "
                "incantation bowls, genizah fragments, and rabbinic literature. "
                "The book argues that Jewish magic was a coherent and distinctive "
                "tradition with identifiable practices, texts, and practitioners, "
                "and that it contributed substantially to the broader Mediterranean "
                "magical culture from which Christian and Islamic magical traditions "
                "emerged. Essential for the pre-history of the Solomonic grimoire corpus."
            ),
        },
        {
            "text_id": "ot_pseudepigrapha_vol1",
            "title": "Old Testament Pseudepigrapha, Volume 1",
            "text_type": "EDITION",
            "period": "MODERN",
            "language": "ENGLISH",
            "description": (
                "James H. Charlesworth's Old Testament Pseudepigrapha, Volume 1 "
                "(Doubleday, 1983) contains Dennis Duling's annotated English "
                "translation of the Testament of Solomon, with introduction covering "
                "date, provenance, original language (Greek), manuscript tradition, "
                "and theological significance. The volume remains the standard "
                "reference collection for pseudepigraphic literature adjacent to the "
                "Hebrew Bible and New Testament, placing Solomonic demonology within "
                "the context of Jewish apocalyptic and early Christian writing."
            ),
        },
        {
            "text_id": "mafteah_shelomoh",
            "title": "Mafteah Shelomoh",
            "text_type": "PRIMARY_SOURCE",
            "period": "MEDIEVAL",
            "language": "HEBREW",
            "description": (
                "The Mafteah Shelomoh (Key of Solomon in Hebrew) survives in several "
                "medieval and early modern manuscripts, of which the most significant "
                "for scholarship is British Museum MS Oriental 14759, edited by "
                "Herman Gollancz in 1914. The Hebrew recension of the Clavicula "
                "Salomonis tradition shows independence from the Latin manuscript "
                "families while sharing ritual categories including conjurations, "
                "pentacles, and spirit hierarchies attributed to Solomon. Its "
                "relationship to the Latin Clavicula Salomonis remains debated: "
                "whether the Hebrew text preceded or derived from Latin versions "
                "is a key question in Solomonic textual scholarship."
            ),
        },
        {
            "text_id": "summa_theologiae",
            "title": "Summa theologiae",
            "text_type": "PRIMARY_SOURCE",
            "period": "MEDIEVAL",
            "language": "LATIN",
            "description": (
                "Thomas Aquinas's Summa theologiae (c. 1265–1274), composed at Paris, "
                "Naples, and Rome, contains the most systematic scholastic treatment "
                "of divination, astrology, demonic magic, and the limits of natural "
                "philosophy in medieval Latin thought. Questions in the Secunda "
                "secundae (ST II-II, qq. 92–96) address superstition, divination, "
                "and the pact with demons; earlier sections treat angels and demons "
                "as rational creatures with limited but real causal powers. Aquinas's "
                "framework dominated university theology through the fifteenth century "
                "and informed every major scholastic classification of magic."
            ),
        },
    ]
    for t in texts:
        conn.execute(
            """INSERT OR IGNORE INTO texts
               (text_id, title, text_type, period, language, description)
               VALUES (:text_id,:title,:text_type,:period,:language,:description)""",
            t,
        )
    print(f"Seeded {len(texts)} Solomonic/scholasticism texts")


def seed_concepts(conn):
    concepts = [
        {
            "slug": "ring_of_solomon",
            "label": "Ring of Solomon",
            "category_type": "ACTOR_TERM",
            "category": "DEMONOLOGICAL",
            "definition_short": (
                "Actor Term. The signet ring with which Solomon was said to bind, "
                "seal, and control demons, appearing in the Testament of Solomon and "
                "pervasive in Islamic, Jewish, and Christian magical literature. The "
                "ring functions as a symbol of divine authority over the demonic "
                "hierarchy and as the architectural concept underlying seals and "
                "pentacles in the Solomonic grimoire tradition."
            ),
            "significance": "Central symbol of Solomonic magical authority and demonic binding",
        },
        {
            "slug": "adjuration",
            "label": "Adjuration",
            "category_type": "ACTOR_TERM",
            "category": "RITUAL",
            "definition_short": (
                "Actor Term (from Latin adjurare, to swear by). The ritual speech "
                "act by which a practitioner compels a spirit, demon, or angel to "
                "act, typically by invoking divine names, Solomonic authority, or "
                "binding formulas. Adjuration is the central ritual mode of the "
                "Solomonic grimoire tradition, distinguishing this literature from "
                "prayer (petitionary) and from simple invocation."
            ),
            "significance": "Primary ritual speech act of the Solomonic and demonic conjuration tradition",
        },
        {
            "slug": "solomonic_authority",
            "label": "Solomonic Authority",
            "category_type": "ANALYST_TERM",
            "category": "HISTORIOGRAPHICAL",
            "definition_short": (
                "Analyst Term. The legitimating strategy by which magical texts "
                "attribute their contents to Solomon, thereby claiming royal, "
                "divinely-granted, and pre-Christian authority for their procedures. "
                "Solomonic authority is a form of pseudepigraphy that confers "
                "prestige and apparent safety on texts that might otherwise be "
                "condemned as demonic. Torijano (2002) and Klaassen (2013) both "
                "analyze Solomonic attribution as a dynamic textual strategy."
            ),
            "significance": "Key mechanism of legitimation in the learned magical grimoire tradition",
        },
        {
            "slug": "spirit_catalogue",
            "label": "Spirit Catalogue",
            "category_type": "ANALYST_TERM",
            "category": "DEMONOLOGICAL",
            "definition_short": (
                "Analyst Term. A structured list or hierarchy of named demons, "
                "angels, or spirits with their ranks, attributes, seals, and "
                "functions, constituting a major organizational feature of the "
                "Solomonic grimoire tradition. Spirit catalogues appear in the "
                "Testament of Solomon, the Ars Goetia (Lemegeton book 1), and "
                "numerous medieval Latin and vernacular compilations. Kieckhefer "
                "(1997) treats them as evidence of a learned clerical engagement "
                "with demonological classification."
            ),
            "significance": "Structural feature distinguishing learned grimoire from popular charm tradition",
        },
        {
            "slug": "pentacle_magic",
            "label": "Pentacles and Magical Figures",
            "category_type": "HYBRID",
            "category": "RITUAL",
            "definition_short": (
                "Hybrid Term. In the Solomonic grimoire tradition, pentacles "
                "(also called lamens, sigils, or seals) are geometric or symbolic "
                "figures drawn on paper, parchment, or metal and attributed with "
                "power over specific spirits or for specific operations. The term "
                "has both actor usage (practitioners made and used pentacles) and "
                "analyst function (scholars classify them as material artefacts "
                "of ritual practice). The Clavicula Salomonis devotes major "
                "sections to pentacle construction and consecration."
            ),
            "significance": "Material ritual object central to Solomonic grimoire practice",
        },
    ]
    for c in concepts:
        conn.execute(
            """INSERT OR IGNORE INTO concepts
               (slug, label, category_type, category, definition_short, significance)
               VALUES (:slug,:label,:category_type,:category,:definition_short,:significance)""",
            c,
        )
    print(f"Seeded {len(concepts)} Solomonic concepts")


def seed_timeline_events(conn):
    # Projection formula:
    # x = (lon + 15) / 75 * 1000  (lon -15 to 60 → x 0 to 1000)
    # y = (65 - lat) / 55 * 600   (lat 65 to 10 → y 0 to 600)
    events = [
        {
            "year": 200, "year_end": 500,
            "event_type": "COMPOSITION",
            "title": "Testament of Solomon Compiled",
            "location": "Alexandria (Egypt)",
            "latitude": 31.2, "longitude": 29.95,
            "section_tag": "solomonic",
            "description": (
                "The Testament of Solomon, a Greek pseudepigraphic text presenting Solomon "
                "as a master of demons bound by his divinely-given ring, was compiled "
                "somewhere in the eastern Mediterranean — most likely Egypt or Syria — "
                "between the second and fifth centuries CE. Drawing on Jewish demonological "
                "traditions, Solomonic legend, and early Christian angelology, the text "
                "catalogues seventy-two demons, their attributes, and the angelic powers "
                "that bind them. It is the foundational document of the Solomonic magical "
                "tradition and the earliest systematic demon catalogue in western magical "
                "literature. Dennis Duling's translation (Charlesworth, Old Testament "
                "Pseudepigrapha, 1983) remains standard."
            ),
        },
        {
            "year": 700, "year_end": 900,
            "event_type": "COMPOSITION",
            "title": "Sepher ha-Razim Compiled",
            "location": "Babylonia / Palestine",
            "latitude": 32.0, "longitude": 35.0,
            "section_tag": "solomonic",
            "description": (
                "Sepher ha-Razim (The Book of Mysteries) — a Hebrew magical handbook "
                "attributed to Noah and transmitted via the patriarchs to Solomon — "
                "was compiled in its surviving form between the seventh and tenth centuries "
                "CE, likely in the Babylonian Jewish academies or Palestinian milieu. "
                "The text organizes the seven heavens with their angel hierarchies and "
                "provides ritual procedures for each celestial realm. Its framework of "
                "named angels indexed to planetary and calendrical factors directly "
                "influenced the broader Solomonic grimoire tradition. Mordecai Margalioth "
                "produced the critical Hebrew edition in 1966; Michael Morgan's English "
                "translation appeared in 1983."
            ),
        },
        {
            "year": 850, "year_end": 1000,
            "event_type": "COMPOSITION",
            "title": "Solomonic Traditions in Islamic Literature",
            "location": "Baghdad",
            "latitude": 33.34, "longitude": 44.44,
            "section_tag": "solomonic",
            "description": (
                "The Islamic tradition of Solomon (Sulayman) as a prophet with power "
                "over jinn, wind, and all creatures was elaborated in Abbasid Baghdad "
                "through Qur'anic exegesis (tafsir), collections of prophetic stories "
                "(qisas al-anbiya), and eventually folktale compilations including "
                "precursors to the Alf Layla wa Layla (Thousand and One Nights). "
                "The Ring of Sulayman — granting command over jinn — became a central "
                "motif in Arabic literature. Islamic Solomonic magic (sihr Sulaymaani) "
                "developed a parallel grimoire tradition, some of which entered "
                "European knowledge through Arabic-to-Latin translation movements "
                "in the twelfth century."
            ),
        },
        {
            "year": 1000, "year_end": 1100,
            "event_type": "COMPOSITION",
            "title": "Byzantine Hygromanteia Compiled",
            "location": "Constantinople",
            "latitude": 41.01, "longitude": 28.98,
            "section_tag": "solomonic",
            "description": (
                "The Hygromanteia — a Greek ritual handbook attributed to Solomon and "
                "known in the West as the Magical Treatise of Solomon — was compiled "
                "in Byzantine circles between the tenth and twelfth centuries, likely "
                "in Constantinople or its scholarly orbit. It systematizes astral "
                "magic, angel and demon hierarchies, and ritual procedures within "
                "a Solomonic framework, preserving elements of late antique magical "
                "tradition that had been partially suppressed in western Latin contexts. "
                "The critical edition and translation by Marathakis and Ioannis "
                "Marathakis (2011) established the text's relationship to the Latin "
                "Clavicula Salomonis as a parallel rather than derivative tradition."
            ),
        },
        {
            "year": 1150, "year_end": 1220,
            "event_type": "TRANSLATION",
            "title": "Solomonic Texts Enter Latin via Toledo and Palermo",
            "location": "Toledo",
            "latitude": 39.86, "longitude": -4.03,
            "section_tag": "solomonic",
            "description": (
                "The great translation movements centered on Toledo in Castile and "
                "Palermo in Norman Sicily brought Arabic philosophical, astrological, "
                "and magical texts into Latin between approximately 1150 and 1220. "
                "Among these were Solomonic and pseudo-Aristotelian magical works "
                "including material that would eventually crystallize as the Clavicula "
                "Salomonis, the Liber Razielis, and the Picatrix. Translators including "
                "Gerard of Cremona, Hermann the German, and Michael Scot worked in "
                "both cities, creating the Latin learned magical corpus that dominated "
                "manuscript culture through the fifteenth century."
            ),
        },
        {
            "year": 1225, "year_end": 1240,
            "event_type": "SCHOLARSHIP",
            "title": "William of Auvergne Condemns Solomonic Arts",
            "location": "Paris",
            "latitude": 48.85, "longitude": 2.35,
            "section_tag": "solomonic",
            "description": (
                "William of Auvergne, bishop of Paris from 1228, composed De universo "
                "and De legibus in the 1230s, providing the most systematic scholastic "
                "critique of Solomonic and demonic magic in the period. William "
                "distinguished carefully between operations that claimed natural "
                "causation and those that required demonic cooperation, condemning "
                "the latter as diabolical regardless of their invocation of Solomonic "
                "or biblical authority. His analysis was foundational for later "
                "scholastic treatments, anticipating Aquinas's framework and directly "
                "influencing the tradition of university-level classification of "
                "magic that culminated in the fifteenth-century witchcraft debates."
            ),
        },
        {
            "year": 1250, "year_end": 1320,
            "event_type": "COMPOSITION",
            "title": "Clavicula Salomonis Circulates in Latin Manuscripts",
            "location": "Paris",
            "latitude": 48.85, "longitude": 2.35,
            "section_tag": "solomonic",
            "description": (
                "Latin manuscripts of the Clavicula Salomonis (Key of Solomon) circulated "
                "in French and Parisian contexts from the mid-thirteenth century, alongside "
                "the Ars Notoria, Liber Juratus, and other Solomonic ritual texts. "
                "The Clavicula presents elaborate procedures for conjuring spirits, "
                "constructing pentacles, and operating within a ritual framework derived "
                "from Solomonic pseudepigraphic authority. Its manuscript families — "
                "Italian, French, and later English — show significant variance, "
                "suggesting ongoing compilation and revision rather than stable textual "
                "transmission. Richard Kieckhefer's Forbidden Rites (1997) and Frank "
                "Klaassen's Transformations of Magic (2013) analyze this circulation "
                "as evidence of a persistent clerical interest in learned ritual magic."
            ),
        },
        {
            "year": 1300, "year_end": 1350,
            "event_type": "COMPOSITION",
            "title": "Liber Razielis at the Aragonese Court",
            "location": "Naples",
            "latitude": 40.85, "longitude": 14.27,
            "section_tag": "solomonic",
            "description": (
                "The Liber Razielis — a massive compilation of Solomonic and angelic "
                "magic attributed to the angel Raziel and compiled in Latin from Hebrew "
                "and Arabic sources — circulated at the Aragonese court of Naples in "
                "the early fourteenth century. A copy was produced for King Alfonso X "
                "of Castile in the thirteenth century, and the text continued to be "
                "copied and expanded in aristocratic contexts. Its presence at the "
                "Neapolitan court reflects the patronage of learned magic by secular "
                "rulers who sought access to Solomonic angelic knowledge for "
                "astrological, protective, and practical ends."
            ),
        },
        {
            "year": 1456,
            "event_type": "SCHOLARSHIP",
            "title": "Hartlieb Classifies Solomonic Arts Among Forbidden Practices",
            "location": "Munich",
            "latitude": 48.14, "longitude": 11.58,
            "section_tag": "solomonic",
            "description": (
                "Johannes Hartlieb's Buch aller verbotenen Kunst (1456), written for "
                "Duke Albrecht III of Bavaria, includes Solomonic ceremonial magic "
                "among the eight forbidden arts alongside geomancy, chiromancy, "
                "and necromancy. Hartlieb describes the ritual framework — fasting, "
                "consecrated implements, spirit names — without providing actual "
                "procedures, and condemns the entire tradition as demonic regardless "
                "of its claimed Solomonic authority. His classification is an important "
                "vernacular index of what educated late medieval German readers "
                "understood 'Solomonic magic' to encompass, and demonstrates that "
                "the authority of Solomon's name did not protect its attributees "
                "from condemnation."
            ),
        },
        {
            "year": 1641, "year_end": 1692,
            "event_type": "SCHOLARSHIP",
            "title": "Elias Ashmole Collects Solomonic Manuscripts",
            "location": "Oxford",
            "latitude": 51.75, "longitude": -1.26,
            "section_tag": "solomonic",
            "description": (
                "Elias Ashmole (1617–1692), astrologer, antiquary, and founding "
                "benefactor of the Ashmolean Museum, assembled one of the most "
                "significant collections of English magical manuscripts, now preserved "
                "as the Ashmole manuscripts at the Bodleian Library. His collection "
                "includes copies of the Ars Notoria, Key of Solomon variants, "
                "astrological and alchemical compilations, and working magical "
                "notebooks documenting astrological and Solomonic practice. "
                "Ashmole's collecting activity shows how Solomonic manuscript "
                "culture persisted alongside the emerging natural philosophy "
                "of the mid-seventeenth century, complicating any simple narrative "
                "of magical decline after the Scientific Revolution."
            ),
        },
        {
            "year": 1888,
            "event_type": "EDITION",
            "title": "Mathers Publishes The Key of Solomon the King",
            "location": "London",
            "latitude": 51.51, "longitude": -0.13,
            "section_tag": "solomonic",
            "description": (
                "Samuel Liddell MacGregor Mathers published The Key of Solomon the King "
                "(George Redway, London, 1888), translated from five manuscripts in the "
                "British Museum and Bibliothèque nationale de France. Mathers's edition "
                "was the first widely available English translation of the Clavicula "
                "Salomonis tradition and defined how the text was understood by the "
                "Victorian occult revival, the Hermetic Order of the Golden Dawn, "
                "and twentieth-century ceremonial magic. Owen Davies (Grimoires, 2009) "
                "and Joseph Peterson's critical online edition (2004) have since "
                "documented significant divergences between Mathers's translation "
                "and the manuscript sources, showing that Mathers edited and regularized "
                "the text substantially."
            ),
        },
        {
            "year": 1914,
            "event_type": "EDITION",
            "title": "Gollancz Edits Hebrew Key of Solomon",
            "location": "London",
            "latitude": 51.51, "longitude": -0.13,
            "section_tag": "solomonic",
            "description": (
                "Herman Gollancz published Mafteah Shelomoh: A Book of the Art of "
                "Solomon (Oxford University Press for the Oriental Translation Fund, "
                "1914), a facsimile and edition of British Museum MS Oriental 14759, "
                "the most complete surviving Hebrew manuscript of the Key of Solomon. "
                "Gollancz's edition established that a Hebrew recension of the "
                "Clavicula Salomonis tradition existed independently of the Latin "
                "manuscript families, with its own distinct ritual procedures and "
                "textual organization. The relationship between Hebrew and Latin "
                "Solomonic texts remains a central question in Solomonic scholarship: "
                "whether Hebrew versions preceded or derived from Latin ones bears "
                "on the question of whether the tradition originated in Jewish or "
                "Christian clerical milieu."
            ),
        },
        {
            "year": 1983,
            "event_type": "EDITION",
            "title": "Duling Translates Testament of Solomon (OTP)",
            "location": "Cambridge, UK",
            "latitude": 52.21, "longitude": 0.12,
            "section_tag": "solomonic",
            "description": (
                "Dennis Duling's annotated English translation of the Testament of "
                "Solomon, published in James Charlesworth's Old Testament Pseudepigrapha "
                "vol. 1 (Doubleday, 1983), brought the text to the attention of "
                "mainstream biblical studies and studies of early Judaism and Christianity. "
                "Duling argued for a first-century provenance, Christian authorship "
                "with Jewish sources, and Palestinian or Syrian origin. His introduction "
                "addressed the text's complex manuscript tradition (MSS A, B, and C "
                "groups) and its demonological system. The translation enabled comparative "
                "work on Solomonic demonology across Testament of Solomon, Sepher "
                "ha-Razim, and the later Latin Clavicula Salomonis tradition."
            ),
        },
        {
            "year": 2002,
            "event_type": "SCHOLARSHIP",
            "title": "Torijano: Solomon the Esoteric King",
            "location": "Leiden",
            "latitude": 52.16, "longitude": 4.49,
            "section_tag": "solomonic",
            "description": (
                "Pablo Torijano's Solomon the Esoteric King: From King to Magus, "
                "Development of a Tradition (Brill, Leiden, 2002) provided the "
                "first comprehensive cross-cultural study of the Solomonic magical "
                "tradition from its Second Temple origins through medieval Islam. "
                "Torijano traced how the biblical Solomon became progressively "
                "invested with esoteric authority — master of demons, possessor "
                "of divine secrets, heir of Adam's occult knowledge — across Jewish "
                "pseudepigrapha, early Christian literature, Qur'anic exegesis, "
                "and Islamic magical texts. The book established that Solomonic "
                "attribution was a dynamic, multilingual strategy rather than "
                "a static medieval convention."
            ),
        },
        {
            "year": 2008,
            "event_type": "SCHOLARSHIP",
            "title": "Bohak: Ancient Jewish Magic",
            "location": "Cambridge, UK",
            "latitude": 52.21, "longitude": 0.12,
            "section_tag": "solomonic",
            "description": (
                "Gideon Bohak's Ancient Jewish Magic: A History (Cambridge University "
                "Press, 2008) provided the most comprehensive account of Jewish "
                "magical practice from the biblical period through the rabbinic era, "
                "drawing on amulets, incantation bowls, magical papyri, and textual "
                "evidence. Bohak argued that Jewish magic was a coherent and "
                "distinctively Jewish tradition — not merely a borrowing from Egyptian "
                "or Greco-Roman practice — and that it fed substantially into "
                "Christian and Islamic magical traditions. The book is essential "
                "background for understanding the pre-history of the Solomonic "
                "grimoire corpus: the angel hierarchies, divine name manipulation, "
                "and adjuration formulas of Jewish magical texts became the raw "
                "material of the medieval Clavicula Salomonis and its cognates."
            ),
        },
    ]
    for ev in events:
        conn.execute(
            """INSERT OR IGNORE INTO timeline_events
               (year, year_end, event_type, title, description, location, latitude, longitude, section_tag, confidence)
               VALUES (:year,:year_end,:event_type,:title,:description,:location,:latitude,:longitude,:section_tag,'HIGH')""",
            {**ev, "year_end": ev.get("year_end")},
        )
    print(f"Seeded {len(events)} Solomonic timeline events")


def seed_relationships(conn):
    # person_text_roles
    roles = [
        # Solomon with Solomonic texts
        ("solomon", "clavicula_salomonis", "attributed authority"),
        ("solomon", "ars_notoria", "attributed authority"),
        ("solomon", "hygromanteia", "attributed authority"),
        ("solomon", "testament_of_solomon", "subject/attributed authority"),
        ("solomon", "mafteah_shelomoh", "attributed authority"),
        ("solomon", "sepher_ha_razim", "attributed authority via pseudepigraphy"),
        # Raziel with Liber Razielis
        ("raziel", "liber_razielis", "attributed author"),
        ("raziel", "sepher_ha_razim", "attributed transmitter"),
        # Scholars
        ("pablo_torijano", "solomon_esoteric_king", "author"),
        ("pablo_torijano", "testament_of_solomon", "scholar"),
        ("gideon_bohak", "ancient_jewish_magic", "author"),
        ("gideon_bohak", "sepher_ha_razim", "scholar"),
        ("dennis_duling", "ot_pseudepigrapha_vol1", "translator/contributor"),
        ("dennis_duling", "testament_of_solomon", "translator"),
        ("elias_ashmole", "clavicula_salomonis", "collector/copyist"),
        ("elias_ashmole", "ars_notoria", "collector/copyist"),
        ("herman_gollancz", "mafteah_shelomoh", "editor"),
        ("michael_morgan", "sepher_ha_razim", "translator"),
        ("joseph_peterson", "clavicula_salomonis", "critical editor"),
        ("samuel_liddell_mathers", "clavicula_salomonis", "translator/editor"),
        ("richard_kieckhefer", "clavicula_salomonis", "scholar"),
        ("frank_klaassen", "clavicula_salomonis", "scholar"),
    ]
    for pid, tid, role in roles:
        p = conn.execute("SELECT id FROM persons WHERE person_id=?", (pid,)).fetchone()
        t = conn.execute("SELECT id FROM texts WHERE text_id=?", (tid,)).fetchone()
        if p and t:
            conn.execute(
                "INSERT OR IGNORE INTO person_text_roles (person_id, text_id, role) VALUES (?,?,?)",
                (p[0], t[0], role),
            )

    # concept_text_refs
    concept_text = [
        ("solomonic_magic", "testament_of_solomon"),
        ("solomonic_magic", "clavicula_salomonis"),
        ("solomonic_magic", "hygromanteia"),
        ("solomonic_magic", "liber_razielis"),
        ("solomonic_magic", "mafteah_shelomoh"),
        ("solomonic_magic", "sepher_ha_razim"),
        ("solomonic_magic", "ars_notoria"),
        ("solomonic_magic", "solomon_esoteric_king"),
        ("solomonic_magic", "ancient_jewish_magic"),
        ("solomonic_magic", "lemegeton"),
        ("ring_of_solomon", "testament_of_solomon"),
        ("ring_of_solomon", "hygromanteia"),
        ("ring_of_solomon", "clavicula_salomonis"),
        ("ring_of_solomon", "solomon_esoteric_king"),
        ("adjuration", "testament_of_solomon"),
        ("adjuration", "clavicula_salomonis"),
        ("adjuration", "sepher_ha_razim"),
        ("adjuration", "liber_juratus_honorii"),
        ("solomonic_authority", "clavicula_salomonis"),
        ("solomonic_authority", "ars_notoria"),
        ("solomonic_authority", "solomon_esoteric_king"),
        ("solomonic_authority", "ancient_jewish_magic"),
        ("spirit_catalogue", "testament_of_solomon"),
        ("spirit_catalogue", "lemegeton"),
        ("spirit_catalogue", "clavicula_salomonis"),
        ("spirit_catalogue", "hygromanteia"),
        ("pentacle_magic", "clavicula_salomonis"),
        ("pentacle_magic", "mafteah_shelomoh"),
        ("pentacle_magic", "lemegeton"),
        ("characters_and_seals", "clavicula_salomonis"),
        ("pseudepigraphy", "testament_of_solomon"),
        ("pseudepigraphy", "clavicula_salomonis"),
        ("pseudepigraphy", "sepher_ha_razim"),
        ("angelic_invocation", "sepher_ha_razim"),
        ("angelic_invocation", "liber_razielis"),
    ]
    for cslug, tid in concept_text:
        c = conn.execute("SELECT id FROM concepts WHERE slug=?", (cslug,)).fetchone()
        t = conn.execute("SELECT id FROM texts WHERE text_id=?", (tid,)).fetchone()
        if c and t:
            conn.execute(
                "INSERT OR IGNORE INTO concept_text_refs (concept_id, text_id) VALUES (?,?)",
                (c[0], t[0]),
            )

    # concept_links
    links = [
        ("solomonic_magic", "pseudepigraphy", "relies on"),
        ("solomonic_magic", "characters_and_seals", "includes"),
        ("solomonic_magic", "angelic_invocation", "includes"),
        ("solomonic_magic", "ring_of_solomon", "centered on"),
        ("solomonic_magic", "adjuration", "primary ritual mode"),
        ("solomonic_magic", "spirit_catalogue", "typically includes"),
        ("solomonic_magic", "solomonic_authority", "operates through"),
        ("solomonic_magic", "pentacle_magic", "uses"),
        ("solomonic_authority", "pseudepigraphy", "form of"),
        ("ring_of_solomon", "adjuration", "enables"),
        ("spirit_catalogue", "demonology", "intersects with"),
    ]
    for from_slug, to_slug, rel in links:
        f = conn.execute("SELECT id FROM concepts WHERE slug=?", (from_slug,)).fetchone()
        t = conn.execute("SELECT id FROM concepts WHERE slug=?", (to_slug,)).fetchone()
        if f and t:
            conn.execute(
                "INSERT OR IGNORE INTO concept_links (from_concept_id, to_concept_id, relationship) VALUES (?,?,?)",
                (f[0], t[0], rel),
            )

    print("Seeded Solomonic relationships")


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        migrate_schema(conn)
        backfill_reception_tags(conn)
        seed_persons(conn)
        seed_texts(conn)
        seed_concepts(conn)
        seed_timeline_events(conn)
        seed_relationships(conn)
        conn.commit()
        counts = {
            t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in ["persons", "texts", "concepts", "timeline_events"]
        }
        print(f"\nDatabase totals after Solomonic seed: {counts}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

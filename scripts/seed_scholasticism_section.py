"""
Seed the Scholasticism and Magic section.

Seeds scholasticism-tagged timeline events and any missing persons/texts/concepts
relevant to the scholastic treatment of magic (Bacon, Aquinas, Albertus, Oresme,
Pietro d'Abano, Tempier condemnations). Run after seed_solomonic_section.py.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DB_PATH


def seed_timeline_events(conn):
    events = [
        {
            "year": 415, "year_end": 426,
            "event_type": "COMPOSITION",
            "title": "Augustine Writes City of God: Foundational Demonology",
            "location": "Hippo Regius (Annaba, Algeria)",
            "latitude": 36.9, "longitude": 7.77,
            "section_tag": "scholasticism",
            "description": (
                "Augustine of Hippo composed De civitate Dei (City of God) in the years "
                "following the sack of Rome (410), completing it around 426. Books VIII "
                "through X contain the foundational Christian demonological framework "
                "that shaped all subsequent medieval scholastic engagement with magic. "
                "Augustine argued that demons are real spiritual beings capable of "
                "causing apparent wonders, that all pagan religion was effectively "
                "demonic, and that any traffic with demons — including the theurgic "
                "practices of Neoplatonism — was illicit regardless of the practitioner's "
                "intent. His distinction between true miracles (divine) and demonic "
                "wonders (trickery or limited natural power) provided scholastic "
                "thinkers from William of Auvergne to Thomas Aquinas with their "
                "basic conceptual vocabulary."
            ),
        },
        {
            "year": 623, "year_end": 636,
            "event_type": "COMPOSITION",
            "title": "Isidore of Seville's Etymologiae: Classification of the Magical Arts",
            "location": "Seville",
            "latitude": 37.39, "longitude": -5.99,
            "section_tag": "scholasticism",
            "description": (
                "Isidore of Seville completed his Etymologiae (Originum libri XX) around "
                "623–636, providing the classification of magic that dominated medieval "
                "encyclopedic thought for six centuries. Book VIII, chapter 9 treats "
                "malefici, mathematici, astrologi, haruspices, augures, pythones, "
                "magi, and necromancers as a taxonomy of forbidden arts, tracing each "
                "term etymologically and morally. Book III treats astronomy and its "
                "relation to astrology. Isidore's treatment is foundational: medieval "
                "authors from Rabanus Maurus to Thomas Aquinas drew directly on his "
                "categories. Richard Kieckhefer and Michael Bailey both identify "
                "the Etymologiae as the starting point for any history of medieval "
                "magic classification."
            ),
        },
        {
            "year": 1230, "year_end": 1240,
            "event_type": "COMPOSITION",
            "title": "William of Auvergne's De universo and De legibus",
            "location": "Paris",
            "latitude": 48.85, "longitude": 2.35,
            "section_tag": "scholasticism",
            "description": (
                "William of Auvergne, bishop of Paris from 1228, composed De universo "
                "and De legibus in the 1230s — the most systematic scholastic analysis "
                "of natural magic, astral influence, and demonic operations before "
                "Aquinas. William distinguished sharply between natural powers "
                "(admissible) and demonic cooperation (always forbidden), condemned "
                "image magic as necessarily demonic, and attacked Aristotelian and "
                "Arabic authority when it seemed to validate magical causation. "
                "His treatment of the imagination, of stellar influence on terrestrial "
                "matter, and of the psychology of enchantment introduced categories "
                "that Aquinas would refine. Nicolas Weill-Parot treats William as the "
                "key transition figure between twelfth-century natural philosophy and "
                "thirteenth-century scholastic demonology."
            ),
        },
        {
            "year": 1248, "year_end": 1264,
            "event_type": "COMPOSITION",
            "title": "Albertus Magnus on Natural Powers and Magical Images",
            "location": "Cologne",
            "latitude": 50.93, "longitude": 6.95,
            "section_tag": "scholasticism",
            "description": (
                "Albertus Magnus composed his major natural philosophical works — "
                "including De mineralibus (c.1262), De animalibus, and the Speculum "
                "astronomiae (attribution debated) — at Cologne, Paris, and in "
                "the Dominican studium generale during the 1240s–1260s. These "
                "texts treated the occult properties of stones, the influence of "
                "stars on terrestrial matter, and the conditions under which "
                "astrological image-making could be licit or illicit. The Speculum "
                "astronomiae distinguished legitimate astrological image magic "
                "(operating through natural celestial causes) from demonic necromancy "
                "(requiring demonic aid). Weill-Parot's analysis of the Speculum "
                "and Nicolas Weill-Parot's work on De mineralibus identify Albert "
                "as the crucial scholastic defender of a naturalized version of "
                "image magic."
            ),
        },
        {
            "year": 1266, "year_end": 1268,
            "event_type": "COMPOSITION",
            "title": "Roger Bacon's Opus Majus and Experimental Philosophy",
            "location": "Oxford",
            "latitude": 51.75, "longitude": -1.26,
            "section_tag": "scholasticism",
            "description": (
                "Roger Bacon composed the Opus Majus, Opus Minus, and Opus Tertium "
                "for Pope Clement IV in 1266–1268, arguing for an experimental "
                "philosophy (scientia experimentalis) that could unlock the secrets "
                "of nature including the prolongation of life, the making of burning "
                "mirrors, and the production of apparent wonders through natural means. "
                "Bacon's earlier Epistola de secretis operibus artis et naturae "
                "(c.1248) had similarly defended operations that appeared magical "
                "as products of natural science. His distinction between legitimate "
                "natural experiment and illicit demonic magic was more permissive "
                "than Aquinas's: Bacon allowed a wide range of apparently "
                "wondrous operations to fall within natural philosophy's domain."
            ),
        },
        {
            "year": 1265, "year_end": 1274,
            "event_type": "COMPOSITION",
            "title": "Aquinas's Summa theologiae: Systematic Treatment of Magic",
            "location": "Paris",
            "latitude": 48.85, "longitude": 2.35,
            "section_tag": "scholasticism",
            "description": (
                "Thomas Aquinas composed the Summa theologiae in stages at Paris, "
                "Rome, and Naples between 1265 and 1274, producing the most "
                "influential scholastic synthesis of theology and natural philosophy. "
                "The Secunda secundae (questions 92–96) provides a detailed taxonomy "
                "of superstition, idolatry, divination, and magic, grounding each "
                "category in either implicit or explicit demonic pact. Aquinas "
                "accepted that demons have real but limited causal powers, that "
                "celestial bodies genuinely influence terrestrial matter (though not "
                "the intellective soul), and that apparent wonders not explainable "
                "by natural causes necessarily involve demonic agency. His framework "
                "defined the orthodox scholastic position and was referenced by "
                "virtually every subsequent medieval treatment of magic, from "
                "university condemnations to inquisitorial manuals."
            ),
        },
        {
            "year": 1270,
            "event_type": "CONDEMNATION",
            "title": "Tempier's First Paris Condemnation (13 Theses)",
            "location": "Paris",
            "latitude": 48.85, "longitude": 2.35,
            "section_tag": "scholasticism",
            "description": (
                "Bishop Étienne Tempier of Paris issued his first condemnation in 1270, "
                "targeting thirteen Averroist theses taught at the University of Paris, "
                "including the eternity of the world, the unity of the intellect, and "
                "the necessary determination of the will by external causes. Several "
                "condemned propositions bore on magic: the claim that celestial bodies "
                "necessarily determine terrestrial events was directly relevant to "
                "astrological determinism. The condemnation targeted the logical "
                "extremes of Aristotelian natural philosophy — positions that, if "
                "accepted, would have made astrological magic a form of natural "
                "science rather than demonic art."
            ),
        },
        {
            "year": 1277,
            "event_type": "CONDEMNATION",
            "title": "Tempier's 219 Condemnations: Defining Scholastic Limits",
            "location": "Paris",
            "latitude": 48.85, "longitude": 2.35,
            "section_tag": "scholasticism",
            "description": (
                "On 7 March 1277, Bishop Étienne Tempier condemned 219 philosophical "
                "and theological propositions taught at the University of Paris, on "
                "the orders of Pope John XXI. The condemned theses included astrological "
                "determinism, the necessity of natural processes, and the power of "
                "images and words to produce natural effects. Propositions 166–171 "
                "specifically addressed magic and images: they condemned the claim "
                "that engraved images have power through the configuration of celestial "
                "bodies (the position the Speculum astronomiae tried to defend). "
                "The 1277 condemnations reshaped the intellectual landscape of "
                "natural magic for a generation and drove subsequent defenses of "
                "image magic (like Cecco d'Ascoli's and Pietro d'Abano's) into "
                "increasingly dangerous territory."
            ),
        },
        {
            "year": 1303, "year_end": 1310,
            "event_type": "COMPOSITION",
            "title": "Pietro d'Abano's Conciliator: Reconciling Medicine and Astrology",
            "location": "Padua",
            "latitude": 45.41, "longitude": 11.88,
            "section_tag": "scholasticism",
            "description": (
                "Pietro d'Abano composed the Conciliator differentiarum at Padua "
                "around 1303–1310, attempting to harmonize Aristotelian natural "
                "philosophy, Galenic medicine, and Arabic astrological medicine. "
                "The Conciliator includes extended defenses of astral determinism "
                "and of the medical efficacy of suffumigations and incantations, "
                "claiming natural rather than demonic causes for their effects. "
                "Pietro also composed the Lucidator dubitabilium astronomiae, "
                "which treats astrological image magic as a form of natural science. "
                "His naturalistic defense of magical operations put him in direct "
                "conflict with post-1277 orthodoxy: he was tried by the Inquisition "
                "at least twice, and his works were condemned posthumously."
            ),
        },
        {
            "year": 1315, "year_end": 1317,
            "event_type": "CONDEMNATION",
            "title": "Pietro d'Abano Tried by Inquisition at Padua",
            "location": "Padua",
            "latitude": 45.41, "longitude": 11.88,
            "section_tag": "scholasticism",
            "description": (
                "Pietro d'Abano was tried by the Inquisition at Padua on charges of "
                "heresy and magic, including the claim that he performed wonders through "
                "demonic arts and that his astrological determinism denied free will. "
                "He died around 1316–1318, probably before the verdict was delivered; "
                "he was subsequently condemned in absentia and his body was ordered "
                "burned (reportedly his friends had already buried him and burned an "
                "effigy). Pietro's case illustrates the institutional danger faced "
                "by scholastic naturalists who pushed the limits of licit natural "
                "magic, and the difficulty of defending astrological determinism "
                "against the 1277 condemnations."
            ),
        },
        {
            "year": 1327,
            "event_type": "CONDEMNATION",
            "title": "Cecco d'Ascoli Burned for Magical Heresy at Florence",
            "location": "Florence",
            "latitude": 43.77, "longitude": 11.26,
            "section_tag": "scholasticism",
            "description": (
                "Francesco degli Stabili, known as Cecco d'Ascoli, was burned at the "
                "stake in Florence on 16 September 1327 — one of the earliest executions "
                "of a scholastic natural philosopher for the crime of magical heresy. "
                "Cecco had taught astrology at Bologna and composed the L'Acerba, "
                "a vernacular encyclopedia defending strong astral determinism. "
                "His condemnation rested on claims that he had prophesied the horoscope "
                "of Christ as that of a criminal condemned to crucifixion and that he "
                "had taught spirits and demons as natural forces. His case shows that "
                "the post-1277 institutional climate could convert scholastic naturalism "
                "into capital heresy."
            ),
        },
        {
            "year": 1363, "year_end": 1380,
            "event_type": "COMPOSITION",
            "title": "Nicole Oresme Critiques Astrology and Divination",
            "location": "Paris",
            "latitude": 48.85, "longitude": 2.35,
            "section_tag": "scholasticism",
            "description": (
                "Nicole Oresme, master of theology at the University of Paris and "
                "later bishop of Lisieux, composed a series of works critiquing "
                "astrology and divination in French and Latin: the Livre de "
                "divinacions (c.1361), Quaestio contra divinatores, and treatises "
                "on commensurability and celestial motion. Oresme argued that "
                "astrological prediction was epistemically impossible because "
                "celestial motions are likely incommensurable with each other, "
                "making exact periodicity calculations unattainable. His mathematical "
                "critiques undercut the foundation of astrological determinism "
                "from within natural philosophy and represented the most rigorous "
                "scholastic skepticism about astrology before the sixteenth century. "
                "Michael Bailey and Lynn Thorndike both treat Oresme as the "
                "culmination of medieval scholastic rationalism applied to magic."
            ),
        },
        {
            "year": 1487,
            "event_type": "PUBLICATION",
            "title": "Malleus Maleficarum Printed at Speyer",
            "location": "Speyer",
            "latitude": 49.32, "longitude": 8.44,
            "section_tag": "scholasticism",
            "description": (
                "Heinrich Kramer (Institoris) published the Malleus Maleficarum "
                "(Hammer of Witches) at Speyer in 1487, the most influential "
                "late-medieval synthesis of scholastic demonology and inquisitorial "
                "practice. The Malleus applied Thomistic demonological principles — "
                "real demonic power, the witch's pact, and the reality of maleficium — "
                "to the prosecution of women accused of witchcraft, arguing for the "
                "reality of night-flight, the sabbath, and demonic copulation. "
                "Though not universally accepted by scholastic contemporaries (many "
                "rejected its specific claims as unorthodox), the Malleus shows "
                "how scholastic frameworks for understanding demonic causation "
                "could be weaponized in judicial contexts. Michael Bailey's "
                "Battling Demons (2003) provides the best recent analysis."
            ),
        },
        {
            "year": 1923, "year_end": 1958,
            "event_type": "SCHOLARSHIP",
            "title": "Thorndike's History of Magic and Experimental Science",
            "location": "New York",
            "latitude": 40.71, "longitude": -74.01,
            "section_tag": "scholasticism",
            "description": (
                "Lynn Thorndike published A History of Magic and Experimental Science "
                "in eight volumes between 1923 and 1958 (Columbia University Press), "
                "the most comprehensive documentary survey of scholastic magic, "
                "astrology, and natural philosophy in medieval Latin sources. "
                "Thorndike treated magic and experimental science as aspects of a "
                "single intellectual tradition, arguing against the sharp separation "
                "of rational from magical thought in medieval culture. His work made "
                "accessible thousands of manuscript texts on astrology, alchemy, "
                "divination, and natural magic, providing the empirical foundation "
                "for all later scholarship including Kieckhefer, Fanger, Klaassen, "
                "and Weill-Parot. Despite its age, HMES remains an indispensable "
                "reference for medieval scholastic magical literature."
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
    print(f"Seeded {len(events)} scholasticism timeline events")


def seed_relationships(conn):
    # person_text_roles for scholasticism
    roles = [
        ("etienne_tempier", "summa_theologiae", "contemporary / institutional context"),
        ("thomas_aquinas", "summa_theologiae", "author"),
        ("thomas_aquinas", "de_universo_william_auvergne", "intellectual successor"),
        ("william_of_auvergne", "de_universo_william_auvergne", "author"),
        ("roger_bacon", "opus_majus", "author"),
        ("roger_bacon", "de_occultis_operibus_naturae", "author"),
        ("albertus_magnus", "speculum_astronomiae", "attributed author"),
        ("albertus_magnus", "de_mineralibus", "author"),
        ("peter_abano", "summa_theologiae", "scholastic context"),
        ("nicole_oresme", "de_universo_william_auvergne", "intellectual successor"),
        ("cecco_d_ascoli", "speculum_astronomiae", "intellectual heir"),
        ("lynn_thorndike", "history_magic_experimental_science", "author"),
        ("michael_d_bailey", "summa_theologiae", "scholar"),
        ("richard_kieckhefer", "summa_theologiae", "scholar"),
        ("nicolas_weill_parot", "speculum_astronomiae", "scholar"),
        ("nicolas_weill_parot", "de_mineralibus", "scholar"),
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
        ("scholastic_classification", "summa_theologiae"),
        ("scholastic_classification", "de_universo_william_auvergne"),
        ("scholastic_classification", "speculum_astronomiae"),
        ("scholastic_classification", "opus_majus"),
        ("scholastic_classification", "etymologiae"),
        ("university_condemnation", "summa_theologiae"),
        ("demonology", "summa_theologiae"),
        ("demonology", "de_universo_william_auvergne"),
        ("astral_image_magic", "speculum_astronomiae"),
        ("astral_image_magic", "de_mineralibus"),
        ("astral_image_magic", "summa_theologiae"),
        ("divination", "summa_theologiae"),
        ("divination", "etymologiae"),
        ("natural_powers", "opus_majus"),
        ("natural_powers", "de_mineralibus"),
        ("natural_powers", "de_occultis_operibus_naturae"),
        ("superstitio", "etymologiae"),
        ("superstitio", "summa_theologiae"),
        ("condemned_arts", "summa_theologiae"),
        ("condemned_arts", "etymologiae"),
        ("learned_magic", "summa_theologiae"),
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
        ("scholastic_classification", "demonology", "produces framework for"),
        ("scholastic_classification", "university_condemnation", "leads to"),
        ("scholastic_classification", "astral_image_magic", "attempts to classify"),
        ("scholastic_classification", "superstitio", "deploys category of"),
        ("university_condemnation", "condemned_arts", "enforces"),
        ("demonology", "demonic_pact", "elaborates"),
        ("demonology", "witchcraft", "provides framework for"),
        ("astral_image_magic", "natural_powers", "claimed as"),
        ("experimental_science", "natural_powers", "investigates"),
    ]
    for from_slug, to_slug, rel in links:
        f = conn.execute("SELECT id FROM concepts WHERE slug=?", (from_slug,)).fetchone()
        t = conn.execute("SELECT id FROM concepts WHERE slug=?", (to_slug,)).fetchone()
        if f and t:
            conn.execute(
                "INSERT OR IGNORE INTO concept_links (from_concept_id, to_concept_id, relationship) VALUES (?,?,?)",
                (f[0], t[0], rel),
            )

    print("Seeded scholasticism relationships")


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        seed_timeline_events(conn)
        seed_relationships(conn)
        conn.commit()
        counts = {
            t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in ["persons", "texts", "concepts", "timeline_events"]
        }
        print(f"\nDatabase totals after Scholasticism seed: {counts}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Seed the Grimoires in Reception: Renaissance and Early Modern section.

Adds 55+ new entries covering:
- 18 persons (Ficino, Pico, Agrippa, Trithemius, Dee, Bruno, Yates, Walker,
  Davies, Peterson, Harms, Barrett, Mathers, Paracelsus, Scot, Weyer,
  della Porta, Kelley)
- 22 texts (De Occulta Philosophia, Steganographia, Corpus Hermeticum,
  De Vita Coelitus Comparanda, Oration on the Dignity of Man, Monas
  Hieroglyphica, Mysteriorum Libri, Magia Naturalis, Arbatel, The Magus,
  Abramelin, Discoverie of Witchcraft, De Praestigiis Daemonum,
  Book of Oberon edition, Fourth Book of Occult Philosophy, Polygraphia,
  Spiritual and Demonic Magic, Giordano Bruno and the Hermetic Tradition,
  The Occult Philosophy in the Elizabethan Age, Grimoires: A History,
  Making Magic in Elizabethan England, The Magic of Rogues)
- 15 concepts (Renaissance Magic, Hermeticism, Prisca Theologia, Magia
  Naturalis concept, Yates Thesis, Occult Philosophy, Grimoire Printing
  History, Vernacular Grimoire Tradition, Neoplatonism and Magic, Enochian
  System, Print Culture and Magic, Kabbalism in Renaissance Magic, Spiritual
  Magic, Reformation and Magic, Rosicrucian Movement)
- 30+ timeline events with geo-coordinates (1438-2015)

Also performs schema migration to add location/latitude/longitude to
timeline_events if not already present.
"""

import sqlite3

from common import DB_PATH


def migrate_schema(conn):
    """Add location columns to timeline_events if not present."""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(timeline_events)")}
    if "location" not in cols:
        conn.execute("ALTER TABLE timeline_events ADD COLUMN location TEXT")
    if "latitude" not in cols:
        conn.execute("ALTER TABLE timeline_events ADD COLUMN latitude REAL")
    if "longitude" not in cols:
        conn.execute("ALTER TABLE timeline_events ADD COLUMN longitude REAL")
    conn.commit()
    print("Schema migration complete (location columns present).")


def seed_persons(conn):
    persons = [
        {
            "person_id": "marsilio_ficino",
            "name": "Marsilio Ficino",
            "name_alt": "Marsilius Ficinus",
            "birth_year": 1433,
            "death_year": 1499,
            "era": "RENAISSANCE",
            "role_primary": "PHILOSOPHER",
            "description": (
                "Florentine philosopher, physician, and priest who directed Cosimo de' "
                "Medici's Platonic Academy and produced the first Latin translation of "
                "the Corpus Hermeticum (1463). Ficino's De Vita (1489), especially the "
                "third book De Vita Coelitus Comparanda, formulated an influential theory "
                "of stellar and spiritus magic drawing on Neoplatonism, astral medicine, "
                "and what he took to be ancient Hermetic wisdom. Frances Yates argued "
                "that Ficino inaugurated a distinctly Renaissance magical tradition; Frank "
                "Klaassen has argued the continuities with medieval learned magic are "
                "stronger than Yates recognized. D.P. Walker's Spiritual and Demonic "
                "Magic (1958) remains the standard treatment of Ficino's magical theory."
            ),
        },
        {
            "person_id": "pico_della_mirandola",
            "name": "Giovanni Pico della Mirandola",
            "name_alt": "Picus Mirandulanus",
            "birth_year": 1463,
            "death_year": 1494,
            "era": "RENAISSANCE",
            "role_primary": "PHILOSOPHER",
            "description": (
                "Italian Renaissance philosopher who attempted to synthesize Christian "
                "theology, Neoplatonism, Hermeticism, and Jewish Kabbalah. His 900 "
                "Theses (1486) and Oration on the Dignity of Man presented magic as a "
                "natural science capable of uniting all human knowledge. Pope Innocent "
                "VIII condemned thirteen of his theses. Pico distinguished magia "
                "naturalis from goetia and was among the first Renaissance writers to "
                "incorporate Hebrew Kabbalah into a Christian magical synthesis. His "
                "early death in 1494 left his synthesis incomplete but enormously "
                "influential on Agrippa, Trithemius, Dee, and later Renaissance occultists."
            ),
        },
        {
            "person_id": "cornelius_agrippa",
            "name": "Heinrich Cornelius Agrippa",
            "name_alt": "Agrippa von Nettesheim; Cornelius Agrippa",
            "birth_year": 1486,
            "death_year": 1535,
            "era": "RENAISSANCE",
            "role_primary": "AUTHOR",
            "description": (
                "German polymath and lawyer who produced the most comprehensive "
                "Renaissance synthesis of occult philosophy. De Occulta Philosophia "
                "circulated in manuscript from c.1510 and was published in Cologne "
                "in expanded form (1531-1533). Agrippa drew on Ficino, Pico, Trithemius, "
                "and medieval magical sources to construct a three-tiered system of "
                "natural, celestial, and ceremonial magic. Klaassen has shown that "
                "Agrippa's third book draws directly on late medieval demonic and angelic "
                "magic manuscripts, undermining the clean break often claimed between "
                "medieval and Renaissance magic. He was at various times physician, "
                "courtier, legal scholar, and itinerant lecturer across Germany, France, "
                "and Italy."
            ),
        },
        {
            "person_id": "johannes_trithemius",
            "name": "Johannes Trithemius",
            "name_alt": "Johann von Trittenheim; Trithemius of Sponheim",
            "birth_year": 1462,
            "death_year": 1516,
            "era": "RENAISSANCE",
            "role_primary": "CLERIC",
            "description": (
                "Benedictine abbot of Sponheim (1483-1505) and later Würzburg, legendary "
                "bibliophile who transformed Sponheim's library from fifty to over two "
                "thousand volumes. His Steganographia (c.1499, printed 1606) circulated "
                "in manuscript as an apparent manual of angel magic for long-distance "
                "communication; Book III was shown in 1998 to contain cryptographic "
                "ciphers beneath the magical text. His Polygraphia (1518) was the first "
                "printed cryptography manual. Trithemius was accused of necromancy and "
                "demonic magic but defended a restricted natural magic. Agrippa visited "
                "him in 1509-1510, and the meeting was formative for the composition of "
                "De Occulta Philosophia."
            ),
        },
        {
            "person_id": "john_dee",
            "name": "John Dee",
            "name_alt": "Dr John Dee",
            "birth_year": 1527,
            "death_year": 1608,
            "era": "EARLY_MODERN",
            "role_primary": "SCHOLAR",
            "description": (
                "English mathematician, astrologer, and natural philosopher who assembled "
                "one of the largest private libraries in Elizabethan England at Mortlake, "
                "Surrey, with approximately 4,000 volumes including manuscripts of medieval "
                "magical texts. Dee's angel conversations with scryers including Bartholomew "
                "Hickman and Edward Kelley (1582-1589) produced the Mysteriorum Libri "
                "Quinque and the Enochian angelic language system. Frank Klaassen has "
                "demonstrated that Dee's magical practice was firmly grounded in late "
                "medieval demonic and angelic magic traditions, contradicting interpretations "
                "that see him as a pure Hermetic or Neoplatonist. Dee also had a hand in "
                "preserving three codices of image magic."
            ),
        },
        {
            "person_id": "edward_kelley",
            "name": "Edward Kelley",
            "name_alt": "Edward Kelly; Talbot",
            "birth_year": 1555,
            "death_year": 1597,
            "era": "EARLY_MODERN",
            "role_primary": "AUTHOR",
            "description": (
                "English scryer and alchemist who served as John Dee's primary medium "
                "during the angelic conversations of 1582-1589. Kelley arrived at Dee's "
                "Mortlake home in March 1582 and served as the visionary intermediary "
                "through whose shewstone the angelic intelligences were seen and heard. "
                "The Enochian language and the associated tables of correspondences were "
                "developed through these sessions and recorded by Dee in the Mysteriorum "
                "Libri Quinque and related diaries. Kelley later separated from Dee and "
                "pursued alchemy in Bohemia under Emperor Rudolf II, where he died in "
                "prison in 1597. His claimed relationship to the angelic communications "
                "remains debated by historians."
            ),
        },
        {
            "person_id": "giordano_bruno",
            "name": "Giordano Bruno",
            "name_alt": "Filippo Bruno; Bruno of Nola",
            "birth_year": 1548,
            "death_year": 1600,
            "era": "RENAISSANCE",
            "role_primary": "PHILOSOPHER",
            "description": (
                "Italian Dominican friar, philosopher, and itinerant intellectual who "
                "synthesized Hermeticism, Neoplatonism, infinite cosmology, and mnemonic "
                "art. Frances Yates argued in Giordano Bruno and the Hermetic Tradition "
                "(1964) that Bruno was fundamentally a Hermetic Magus whose memory theater "
                "and cosmological innovations derived from Ficino's magical tradition and "
                "were central to the Scientific Revolution. Subsequent scholars have "
                "substantially revised this thesis while acknowledging Bruno's explicit "
                "engagement with astral magic sources including the Picatrix. He was "
                "burned at the stake in Rome in February 1600, condemned for heresies "
                "that may have included magical doctrines alongside his cosmological views."
            ),
        },
        {
            "person_id": "giovanni_battista_della_porta",
            "name": "Giovanni Battista della Porta",
            "name_alt": "Giambattista della Porta; J.B. Porta",
            "birth_year": 1535,
            "death_year": 1615,
            "era": "RENAISSANCE",
            "role_primary": "PHILOSOPHER",
            "description": (
                "Neapolitan natural philosopher, playwright, and polymath who compiled "
                "Magia Naturalis (first edition 1558, expanded four-book version 1589). "
                "Della Porta articulated a systematic natural philosophy of sympathies, "
                "antipathies, and occult properties, incorporating phenomena previously "
                "attributed to magical or demonic agency into natural explanation. He "
                "founded the Accademia dei Segreti (Academy of Secrets) in Naples and "
                "was investigated by the Inquisition. His work represents the interface "
                "between late Renaissance natural philosophy and the grimoire tradition, "
                "exemplifying how the concept of magia naturalis expanded to include "
                "observational, experimental, and artisanal knowledge under a single "
                "rubric derived from natural philosophy."
            ),
        },
        {
            "person_id": "frances_yates",
            "name": "Frances Yates",
            "name_alt": "Frances Amelia Yates",
            "birth_year": 1899,
            "death_year": 1981,
            "era": "MODERN",
            "role_primary": "SCHOLAR",
            "description": (
                "British historian of Renaissance culture associated with the Warburg "
                "Institute, London. Her Giordano Bruno and the Hermetic Tradition (1964) "
                "argued that Hermeticism and natural magic were central to Renaissance "
                "intellectual culture and causally linked to the Scientific Revolution. "
                "Her related studies The Art of Memory (1966), The Rosicrucian "
                "Enlightenment (1972), and The Occult Philosophy in the Elizabethan Age "
                "(1979) extended this framework. The Yates thesis held that Ficino and "
                "Pico transmitted an ancient Hermetic-magical wisdom that renewed and "
                "transformed both natural philosophy and occult practice; this argument "
                "was challenged by Vickers, Copenhaver, and Klaassen, but it transformed "
                "the historiography of Renaissance magic and remains a necessary reference point."
            ),
        },
        {
            "person_id": "dp_walker",
            "name": "D.P. Walker",
            "name_alt": "Daniel Pickering Walker",
            "birth_year": 1914,
            "death_year": 1985,
            "era": "MODERN",
            "role_primary": "SCHOLAR",
            "description": (
                "British historian at the Warburg Institute whose Spiritual and Demonic "
                "Magic: From Ficino to Campanella (1958) gave the first systematic "
                "scholarly treatment to Renaissance magic's relationship with Neoplatonism "
                "and demonology. Walker distinguished spiritual magic, which operates "
                "through the spiritus or pneuma mediating between soul and body in "
                "Ficino's sense, from demonic magic involving explicit demonic summoning. "
                "His nuanced framework preceded and shaped Frances Yates's more sweeping "
                "arguments and remains the standard scholarly account of Ficino's De Vita "
                "Coelitus Comparanda as a magical text. Walker also published on music "
                "therapy in the Renaissance and on unorthodox religious thought."
            ),
        },
        {
            "person_id": "owen_davies",
            "name": "Owen Davies",
            "birth_year": 1969,
            "era": "MODERN",
            "role_primary": "SCHOLAR",
            "description": (
                "British historian at the University of Hertfordshire specializing in "
                "the social and cultural history of magic, witchcraft, and folk religion "
                "from the early modern period to the present. His Grimoires: A History "
                "of Magic Books (Oxford University Press, 2009) provides the most "
                "comprehensive survey of grimoire transmission from late antiquity to "
                "the twenty-first century, covering the printing press, vernacular "
                "diffusion, popular magic, and contemporary usage. Davies has also "
                "published on cunning folk in early modern England, the global spread "
                "of magical texts in colonial and postcolonial contexts, and popular "
                "witchcraft beliefs. His work bridges the gap between medieval manuscript "
                "studies and the social history of popular magic."
            ),
        },
        {
            "person_id": "joseph_peterson",
            "name": "Joseph H. Peterson",
            "era": "MODERN",
            "role_primary": "EDITOR",
            "description": (
                "American editor and archivist who founded esotericarchives.com (1995), "
                "the most comprehensive online repository of transcribed historical "
                "magical texts. Peterson's critical editions include The Lesser Key of "
                "Solomon (2001), Grimorium Verum (2007), John Dee's Five Books of Mystery: "
                "Mysteriorum Libri Quinque (2003), and The Sworn Book of Honorius (2016). "
                "His editions bring rigorous philological practice to texts long circulating "
                "in corrupt printed forms, comparing manuscript witnesses to establish "
                "reliable texts with scholarly apparatus. Peterson is also co-editor of "
                "The Book of Oberon (2015, with Daniel Harms and James R. Clark), the "
                "edition of the Folger Shakespeare Library's Elizabethan manuscript of "
                "conjuring and fairy magic."
            ),
        },
        {
            "person_id": "dan_harms",
            "name": "Dan Harms",
            "name_alt": "Daniel Harms",
            "era": "MODERN",
            "role_primary": "SCHOLAR",
            "description": (
                "American librarian and scholar based in New York whose major research "
                "area is the history of magic from antiquity to the present, with "
                "particular attention to necromancy, fairy magic, and grimoire transmission. "
                "Harms is co-editor of The Book of Oberon: A Sourcebook of Elizabethan "
                "Magic (Llewellyn, 2015, with James R. Clark and Joseph H. Peterson), a "
                "transcription and annotated translation of Folger MS Vb.26, a late "
                "sixteenth-century English manuscript combining Solomonic spirit lists "
                "with vernacular fairy magic and practical conjuring. He has also edited "
                "The Long-Lost Friend (Llewellyn, 2012) and published articles in the "
                "Journal for the Academic Study of Magic, Abraxas, and Fortean Times."
            ),
        },
        {
            "person_id": "francis_barrett",
            "name": "Francis Barrett",
            "era": "EARLY_MODERN",
            "role_primary": "AUTHOR",
            "description": (
                "English occultist and author of The Magus, or Celestial Intelligencer "
                "(London, 1801), a substantial compilation drawing heavily on Agrippa's "
                "De Occulta Philosophia, Robert Turner's translations of magical texts, "
                "and related Renaissance and medieval sources. Barrett's work marks the "
                "transition from the circulation of learned magic in manuscript and early "
                "print to Romantic-era occultism and is an early example of the commercial "
                "popularization of the grimoire tradition. He is reported to have run "
                "practical classes in occult philosophy in London. The Magus served as a "
                "conduit bringing Agrippa's system and related Renaissance material to "
                "nineteenth-century audiences before the Golden Dawn produced more "
                "scholarly treatments."
            ),
        },
        {
            "person_id": "samuel_liddell_mathers",
            "name": "Samuel Liddell MacGregor Mathers",
            "name_alt": "S.L. MacGregor Mathers; Count MacGregor",
            "birth_year": 1854,
            "death_year": 1918,
            "era": "MODERN",
            "role_primary": "EDITOR",
            "description": (
                "Scottish occultist and a founder of the Hermetic Order of the Golden "
                "Dawn (1888). Mathers produced influential editions of medieval and early "
                "modern magical texts that introduced them to a wide English audience: "
                "The Key of Solomon the King (1888, translated from British Library "
                "manuscripts), The Book of the Sacred Magic of Abramelin the Mage (1898, "
                "from a French manuscript), and The Goetia: The Lesser Key of Solomon "
                "the King (1904, with Aleister Crowley). His editorial choices, invented "
                "sections, and translations significantly shaped twentieth-century "
                "reception of the grimoire tradition. Joseph Peterson's later critical "
                "editions have corrected many of Mathers's departures from manuscript "
                "sources."
            ),
        },
        {
            "person_id": "paracelsus",
            "name": "Paracelsus",
            "name_alt": "Philippus Aureolus Theophrastus Bombastus von Hohenheim",
            "birth_year": 1493,
            "death_year": 1541,
            "era": "RENAISSANCE",
            "role_primary": "PHYSICIAN",
            "description": (
                "Swiss-German physician, alchemist, and natural philosopher who rejected "
                "Galenic medicine and scholastic Aristotelianism in favor of a doctrine "
                "of correspondences, signatures, and elemental spirits. Paracelsus "
                "postulated gnomes, undines, sylphs, and salamanders as natural beings "
                "inhabiting the four elements, a framework that influenced later spirit "
                "magic traditions. His medical and philosophical works circulated widely "
                "from the later sixteenth century and contributed to an expanded magia "
                "naturalis incorporating alchemical operations. His relationship to the "
                "grimoire tradition is indirect but significant: Paracelsian natural "
                "philosophy provided intellectual resources for later vernacular magic "
                "practitioners and contributed to the Rosicrucian synthesis of the "
                "early seventeenth century."
            ),
        },
        {
            "person_id": "reginald_scot",
            "name": "Reginald Scot",
            "birth_year": 1538,
            "death_year": 1599,
            "era": "EARLY_MODERN",
            "role_primary": "AUTHOR",
            "description": (
                "English gentleman and writer who published The Discoverie of Witchcraft "
                "(London, 1584), the most important English-language skeptical critique "
                "of witch-hunting in the sixteenth century. Scot argued systematically "
                "that witchcraft accusations rested on fraud, delusion, and clerical "
                "manipulation. The Discoverie also preserved extensive descriptions of "
                "conjuring practice, spirit magic, and Solomonic procedures, making it "
                "an inadvertent sourcebook for later grimoire compilers. Klaassen notes "
                "that the book's publishers reissued it at mid-century recognizing its "
                "value to magical practitioners. King James VI of Scotland, who took "
                "witchcraft seriously, is reported to have ordered copies burned, though "
                "this is debated."
            ),
        },
        {
            "person_id": "johann_weyer",
            "name": "Johann Weyer",
            "name_alt": "Johannes Wier; Wierus",
            "birth_year": 1515,
            "death_year": 1588,
            "era": "RENAISSANCE",
            "role_primary": "PHYSICIAN",
            "description": (
                "Dutch physician and skeptic who studied under Agrippa and published "
                "De Praestigiis Daemonum et Incantationibus ac Veneficiis (Basel, 1563). "
                "Weyer argued that confessions of witchcraft reflected delusion and "
                "disease rather than real demonic pacts; accused women lacked the "
                "intellectual and spiritual capacity for genuine demonic compacts. He "
                "accepted demonic existence while denying effective human magic, a "
                "position that allowed him to challenge witch-hunting while remaining "
                "within orthodox Christian demonology. His work drew on medical and "
                "theological authorities including his teacher Agrippa. Weyer influenced "
                "Reginald Scot and represents a significant strand of Renaissance "
                "critical engagement with learned demonology."
            ),
        },
    ]

    for p in persons:
        conn.execute(
            """INSERT OR IGNORE INTO persons
               (person_id, name, name_alt, birth_year, death_year, era, role_primary, description, source_method)
               VALUES (:person_id, :name, :name_alt, :birth_year, :death_year, :era, :role_primary, :description, 'SEED_RECEPTION')""",
            {**{"name_alt": None, "birth_year": None, "death_year": None}, **p},
        )
    conn.commit()
    print(f"Seeded {len(persons)} persons.")


def seed_texts(conn):
    texts = [
        {
            "text_id": "de_occulta_philosophia",
            "title": "De Occulta Philosophia",
            "title_original": "De occulta philosophia libri tres",
            "language": "LATIN",
            "text_type": "TREATISE",
            "period": "RENAISSANCE",
            "date_start": 1510,
            "date_end": 1533,
            "description": (
                "The most comprehensive Renaissance synthesis of occult philosophy, "
                "completed in manuscript c.1510 by Cornelius Agrippa and published in "
                "Cologne 1531-1533. Three books treat natural magic (book I), celestial "
                "and mathematical magic (book II), and ceremonial magic including spirit "
                "conjuration (book III). Agrippa drew on Ficino, Pico, Trithemius, and "
                "extensively on medieval learned magic manuscripts. Frank Klaassen has "
                "shown that book III is substantially continuous with the Munich Manual, "
                "the Sworn Book of Honorius, and other late medieval necromantic texts, "
                "directly undermining the sharp medieval-Renaissance break posited by "
                "Yates. The work was enormously influential on subsequent learned magic "
                "including Dee's Elizabethan practice."
            ),
        },
        {
            "text_id": "steganographia",
            "title": "Steganographia",
            "title_original": "Steganographia hoc est ars per occultam scripturam animi sui voluntatem absentibus aperiendi certa",
            "language": "LATIN",
            "text_type": "TREATISE",
            "period": "RENAISSANCE",
            "date_start": 1499,
            "date_end": 1606,
            "description": (
                "Written c.1499 by Johannes Trithemius, abbot of Sponheim, and circulated "
                "in manuscript for over a century before print publication in Frankfurt "
                "(1606). Books I and II describe a system of angel magic for long-distance "
                "communication through angelic intermediaries, firmly within late medieval "
                "spirit magic traditions. Book III was demonstrated in 1998 by Thomas "
                "Ernst to conceal cryptographic ciphers beneath the apparent magical text. "
                "Placed on the Index Librorum Prohibitorum in 1609 and removed in 1900, "
                "the Steganographia influenced Agrippa's angelic cosmology, fascinated "
                "John Dee, and contributed to early modern debates about the boundary "
                "between natural and demonic magic."
            ),
        },
        {
            "text_id": "corpus_hermeticum_latin",
            "title": "Corpus Hermeticum (Ficino Translation)",
            "title_original": "Pimander seu de potestate et sapientia divina",
            "language": "LATIN",
            "text_type": "TRANSLATION",
            "period": "RENAISSANCE",
            "date_start": 1463,
            "date_end": 1471,
            "description": (
                "Marsilio Ficino's Latin translation of the fourteen Greek texts known "
                "as the Corpus Hermeticum, completed in 1463 at the direction of Cosimo "
                "de' Medici before Ficino had finished his Plato translations. Published "
                "as Pimander in 1471 (Treviso). The Hermetic texts, then believed to "
                "preserve ancient Egyptian wisdom older than Plato and Moses (a dating "
                "demolished by Isaac Casaubon in 1614), provided Ficino and his circle "
                "with what they took to be a prisca theologia supporting natural magic "
                "and Neoplatonist cosmology. Frances Yates's thesis that Hermeticism "
                "drove the Renaissance scientific revolution depended heavily on the "
                "influence of this translation."
            ),
        },
        {
            "text_id": "de_vita_coelitus_comparanda",
            "title": "De Vita Coelitus Comparanda",
            "title_original": "De vita libri tres, liber tertius",
            "language": "LATIN",
            "text_type": "TREATISE",
            "period": "RENAISSANCE",
            "date_start": 1489,
            "date_end": 1489,
            "description": (
                "The third book of Ficino's De Vita (1489), treating how to attract "
                "stellar influences through talismans, music, scents, foods, and "
                "sympathetic correspondence. The text draws on the Picatrix, Pseudo-"
                "Ptolemy's De imaginibus, and the pseudo-Hermetic De quindecim stellis, "
                "combining astral medicine with a Neoplatonist theory of spiritus "
                "mediation. Klaassen has argued that the text has extensive commonalities "
                "with medieval ritual magic and was used as a source by sixteenth-century "
                "ritual magic practitioners. D.P. Walker's Spiritual and Demonic Magic "
                "(1958) remains the standard scholarly treatment, arguing that Ficino "
                "attempted to limit his magic to the spiritus level, avoiding demonic "
                "invocation."
            ),
        },
        {
            "text_id": "oration_dignity_man",
            "title": "Oration on the Dignity of Man",
            "title_original": "Oratio de hominis dignitate",
            "language": "LATIN",
            "text_type": "TREATISE",
            "period": "RENAISSANCE",
            "date_start": 1486,
            "date_end": 1496,
            "description": (
                "Prefatory oration by Giovanni Pico della Mirandola, written c.1486 "
                "as an introduction to his 900 Theses (Conclusiones), a university "
                "disputation that Pope Innocent VIII ultimately condemned. Pico presents "
                "humanity as uniquely capable of ascending through all orders of being, "
                "and presents magic alongside Kabbalah as a demonstrative natural science. "
                "The Oration distinguishes magia naturalis, which operates through "
                "natural sympathies and is licit, from goetia, which employs demons and "
                "is condemned. Published posthumously. Frances Yates treated it as the "
                "founding document of a Renaissance Hermetic-magical worldview; "
                "subsequent scholars have offered more qualified readings."
            ),
        },
        {
            "text_id": "monas_hieroglyphica",
            "title": "Monas Hieroglyphica",
            "language": "LATIN",
            "text_type": "TREATISE",
            "period": "EARLY_MODERN",
            "date_start": 1564,
            "date_end": 1564,
            "description": (
                "A short cryptic treatise by John Dee, published in Antwerp in 1564 "
                "and dedicated to Holy Roman Emperor Maximilian II. Organized around "
                "an alchemical-astronomical-magical symbol Dee called the monad, the "
                "text claims to derive a unified symbolic language from planetary, "
                "elemental, zodiacal, and Kabbalistic correspondences. Dee considered "
                "it among his most important theoretical works. The Monas has been "
                "variously interpreted as alchemical treatise, Kabbalistic commentary, "
                "and purely mathematical symbolism. Nicholas Clulee's study John Dee's "
                "Natural Philosophy (1988) remains the standard scholarly treatment of "
                "Dee's mathematical and occult theories."
            ),
        },
        {
            "text_id": "mysteriorum_libri",
            "title": "Mysteriorum Libri Quinque",
            "title_original": "Five Books of Mystery",
            "language": "ENGLISH",
            "text_type": "PRIMARY_SOURCE",
            "period": "EARLY_MODERN",
            "date_start": 1583,
            "date_end": 1589,
            "description": (
                "John Dee's record of the first five of his angelic conferences with "
                "scryers including Bartholomew Hickman and primarily Edward Kelley, "
                "conducted from 1583 onward. The manuscripts, preserved in the British "
                "Library and published in critical edition by Joseph Peterson (2003), "
                "document the procedures, visions, angelic speeches, and tables of "
                "correspondences that constitute the Enochian system. Frank Klaassen "
                "has argued that the angel operations in these records are firmly within "
                "the tradition of late medieval angelic conjuration rather than a new "
                "Hermetic or Neoplatonist departure; the form of the conferences directly "
                "parallels procedures in the Sworn Book of Honorius and Ars Notoria."
            ),
        },
        {
            "text_id": "magia_naturalis",
            "title": "Magia Naturalis",
            "title_original": "Magia naturalis sive de miraculis rerum naturalium",
            "language": "LATIN",
            "text_type": "TREATISE",
            "period": "RENAISSANCE",
            "date_start": 1558,
            "date_end": 1589,
            "description": (
                "Compiled by Giovanni Battista della Porta of Naples. First edition "
                "1558, expanded from four books to twenty books in the 1589 edition. "
                "Della Porta systematized a natural philosophy of sympathies, antipathies, "
                "and occult properties, incorporating phenomena from alchemy, gardening, "
                "optics, distillation, magnetism, and cosmetics alongside traditional "
                "magical procedures. The expanded 1589 edition was widely translated "
                "and circulated throughout Europe. It represents the late Renaissance "
                "attempt to naturalize the content of medieval magic by framing it within "
                "an Aristotelian natural philosophy of hidden properties. The Accademia "
                "dei Segreti founded by della Porta was the first learned society focused "
                "on natural experiment."
            ),
        },
        {
            "text_id": "arbatel_de_magia_veterum",
            "title": "Arbatel de Magia Veterum",
            "title_original": "Arbatel: De magia veterum",
            "language": "LATIN",
            "text_type": "GRIMOIRE",
            "period": "EARLY_MODERN",
            "date_start": 1575,
            "date_end": 1575,
            "description": (
                "Latin grimoire of unknown authorship printed at Basel in 1575, purporting "
                "to be the first of nine books of Olympic spirit magic. Only one book "
                "survives in print. The Arbatel presents a system of seven Olympic spirits "
                "governing planetary spheres, accessible through prayer and ethical "
                "preparation rather than through elaborate demonic conjuration. Its tone "
                "is markedly more devotional and Protestant-inflected than most grimoires "
                "of the period. Klaassen notes that editions of the Fourth Book of Occult "
                "Philosophy, the Arbatel, and related texts were printed around the same "
                "time, suggesting a market for printed ceremonial magic. Joseph Peterson "
                "produced the standard modern critical edition."
            ),
        },
        {
            "text_id": "fourth_book_occult_philosophy",
            "title": "Fourth Book of Occult Philosophy",
            "title_original": "De occulta philosophia liber quartus",
            "language": "LATIN",
            "text_type": "GRIMOIRE",
            "period": "EARLY_MODERN",
            "date_start": 1559,
            "date_end": 1559,
            "description": (
                "A Latin grimoire of spirit conjuration printed under Agrippa's name "
                "from 1559 onward, though likely not by Agrippa. Klaassen identifies "
                "three editions in the mid-sixteenth century and notes it was bound with "
                "the Arbatel. The text concerns the conjuration of spirits using circles, "
                "pentacles, and Solomonic procedures, drawing on and extending the "
                "tradition of late medieval demonic magic rather than the philosophical "
                "natural magic of Agrippa's genuine De Occulta Philosophia. Its circulation "
                "under Agrippa's authority demonstrates the tendency of sixteenth-century "
                "grimoire compilers to attach their texts to prestigious Renaissance "
                "names, conflating the philosophical and the practical registers of "
                "occult writing."
            ),
        },
        {
            "text_id": "polygraphia_trithemius",
            "title": "Polygraphia",
            "title_original": "Polygraphiae libri sex",
            "language": "LATIN",
            "text_type": "TREATISE",
            "period": "RENAISSANCE",
            "date_start": 1518,
            "date_end": 1518,
            "description": (
                "Printed posthumously in 1518 with a full title indicating its dedication "
                "to Emperor Maximilian, Polygraphia was the first printed book on "
                "cryptography and the first of Trithemius's works to reach print. It "
                "presents a system of letter-substitution ciphers and encoded alphabets "
                "without the angelic or magical framing of Steganographia. Its publication "
                "established Trithemius's reputation as a pioneer of cryptography separate "
                "from his reputation as a magician. The relationship between Polygraphia "
                "and Steganographia has been illuminated by modern cryptographers who "
                "demonstrated that Steganographia's Book III conceals legitimate ciphers "
                "beneath magical apparatus, while Polygraphia presents the ciphers "
                "transparently."
            ),
        },
        {
            "text_id": "discoverie_of_witchcraft",
            "title": "The Discoverie of Witchcraft",
            "language": "ENGLISH",
            "text_type": "TREATISE",
            "period": "EARLY_MODERN",
            "date_start": 1584,
            "date_end": 1584,
            "description": (
                "Published in London in 1584 by Reginald Scot, a Kentish gentleman. "
                "The most systematic English-language skeptical critique of witch-hunting "
                "in the sixteenth century, arguing that witchcraft accusations rest on "
                "fraud, delusion, poverty, and clerical manipulation, and that demonic "
                "operations are physically impossible. The Discoverie also contains "
                "extensive appendices on practical magic, conjuring tricks, and Solomonic "
                "procedures, making it an inadvertent sourcebook for later grimoire "
                "compilers. Klaassen notes that Scot's book was reissued in the "
                "seventeenth century by publishers who recognized its commercial value "
                "to magical practitioners. King James I reportedly ordered copies burned, "
                "though this claim is difficult to verify."
            ),
        },
        {
            "text_id": "de_praestigiis_daemonum",
            "title": "De Praestigiis Daemonum",
            "title_original": "De praestigiis daemonum et incantationibus ac veneficiis",
            "language": "LATIN",
            "text_type": "TREATISE",
            "period": "RENAISSANCE",
            "date_start": 1563,
            "date_end": 1563,
            "description": (
                "Published at Basel in 1563 by Johann Weyer, physician to Duke William "
                "of Jülich-Cleves-Berg. Weyer argued that confessions of witchcraft "
                "reflect delusion and melancholy rather than genuine demonic pacts, and "
                "that old women accused as witches lacked the capacity for real commerce "
                "with demons. He accepted the existence of powerful demons while denying "
                "effective human magic, a position developed from his teacher Agrippa. "
                "The work underwent six Latin editions and several vernacular translations "
                "in the later sixteenth century and was a major reference for skeptical "
                "thinkers including Reginald Scot. Bodin attacked it vigorously in De "
                "la Démonomanie (1580)."
            ),
        },
        {
            "text_id": "spiritual_demonic_magic_walker",
            "title": "Spiritual and Demonic Magic: From Ficino to Campanella",
            "language": "ENGLISH",
            "text_type": "SCHOLARSHIP",
            "period": "MODERN",
            "date_start": 1958,
            "date_end": 1958,
            "description": (
                "Published by D.P. Walker at the Warburg Institute in 1958. The first "
                "systematic scholarly account of Renaissance magic's relationship to "
                "Neoplatonism, demonology, and natural philosophy. Walker distinguished "
                "spiritual magic, operating through the pneuma or spiritus mediating "
                "between soul and body, from demonic magic involving explicit summons of "
                "evil spirits. He demonstrated that Ficino's De Vita Coelitus Comparanda "
                "was genuinely a magical text, not merely philosophical metaphor, while "
                "arguing Ficino sought to remain on the natural side of the spiritual-"
                "demonic boundary. Walker's framework preceded and shaped Frances Yates's "
                "broader Hermetic thesis. The book covers Ficino, Pico, Pomponazzi, "
                "Agrippa, Cardano, della Porta, Bruno, and Campanella."
            ),
        },
        {
            "text_id": "giordano_bruno_hermetic_yates",
            "title": "Giordano Bruno and the Hermetic Tradition",
            "language": "ENGLISH",
            "text_type": "SCHOLARSHIP",
            "period": "MODERN",
            "date_start": 1964,
            "date_end": 1964,
            "description": (
                "Published by Frances Yates at the University of Chicago Press in 1964. "
                "The founding text of what scholars call the Yates thesis: that "
                "Hermeticism and natural magic were central to Renaissance culture, that "
                "Ficino and Pico inaugurated a new Hermetic-magical worldview, and that "
                "this tradition, carried by Bruno, Dee, and others, contributed to the "
                "Scientific Revolution. Yates drew on Walker and on the Warburg tradition "
                "of iconological analysis. The thesis was challenged by Brian Vickers, "
                "Brian Copenhaver, and most recently Frank Klaassen, who argued that "
                "Renaissance ritual magic was continuous with medieval practice rather "
                "than the sanitized Hermetic-natural magic Yates envisioned. The book "
                "remains a landmark of historiography despite these revisions."
            ),
        },
        {
            "text_id": "occult_philosophy_elizabethan_yates",
            "title": "The Occult Philosophy in the Elizabethan Age",
            "language": "ENGLISH",
            "text_type": "SCHOLARSHIP",
            "period": "MODERN",
            "date_start": 1979,
            "date_end": 1979,
            "description": (
                "Frances Yates's last major book, published by Routledge in 1979, extending "
                "her Hermetic thesis to Elizabethan England through the figures of John "
                "Dee, Christopher Marlowe's Doctor Faustus, Edmund Spenser, and Philip "
                "Sidney. Yates argued that a Kabbalist-Hermetic magical philosophy, "
                "transmitted through Agrippa and Dee, shaped Elizabethan literature "
                "and intellectual culture. The book's treatment of Dee as a Hermetic "
                "philosopher in the Ficino-Pico tradition was challenged by Klaassen, "
                "whose study of Dee's magical manuscripts showed his practice rooted in "
                "medieval ritual traditions rather than Hermetic natural magic. Yates's "
                "reading of Spenser and Marlowe has proved more durable than her "
                "account of Dee's specific practices."
            ),
        },
        {
            "text_id": "grimoires_history_davies",
            "title": "Grimoires: A History of Magic Books",
            "language": "ENGLISH",
            "text_type": "SCHOLARSHIP",
            "period": "MODERN",
            "date_start": 2009,
            "date_end": 2009,
            "description": (
                "Published by Owen Davies at Oxford University Press in 2009. The most "
                "comprehensive survey of grimoire history from ancient Mesopotamia and "
                "Egypt through the twenty-first century, covering medieval manuscript "
                "circulation, the impact of the printing press on grimoire diffusion, "
                "the French popular grimoire tradition (Grand Albert, Petit Albert, "
                "Dragon Rouge), nineteenth-century occultist editions (Mathers, Waite, "
                "Levi), and contemporary global usage. Davies situates the grimoire "
                "tradition in social history, examining who owned, copied, sold, and "
                "used magical books across different social strata. The book is essential "
                "reading for understanding the gap between manuscript-based learned magic "
                "and the popular print tradition that emerged after 1500."
            ),
        },
        {
            "text_id": "book_of_oberon_edition",
            "title": "The Book of Oberon",
            "title_original": "A Sourcebook of Elizabethan Magic",
            "language": "ENGLISH",
            "text_type": "EDITION",
            "period": "MODERN",
            "date_start": 2015,
            "date_end": 2015,
            "description": (
                "Critical transcription and annotated translation of Folger Shakespeare "
                "Library MS Vb.26, a late sixteenth-century English manuscript of "
                "approximately 450 pages. Edited by Daniel Harms, James R. Clark, and "
                "Joseph H. Peterson, published by Llewellyn in 2015. The manuscript "
                "combines Solomonic spirit lists drawn from Agrippa and related sources "
                "with vernacular fairy magic, conjuring for treasure and love, and "
                "practical operations in both Latin and English. The edition exemplifies "
                "how the Elizabethan period combined learned Continental magic traditions "
                "with native English vernacular practices. Klaassen's Making Magic in "
                "Elizabethan England examined related manuscripts from the same period."
            ),
        },
        {
            "text_id": "making_magic_elizabethan",
            "title": "Making Magic in Elizabethan England",
            "title_original": "Making Magic in Elizabethan England: Two Early Modern Vernacular Books of Magic",
            "language": "ENGLISH",
            "text_type": "EDITION",
            "period": "MODERN",
            "date_start": 2019,
            "date_end": 2019,
            "description": (
                "Edited volume published by Frank Klaassen at Penn State University "
                "Press (2019), providing critical editions and analysis of two Elizabethan "
                "vernacular magic manuscripts. The volume demonstrates how early modern "
                "English practitioners engaged with Continental learned magic traditions "
                "including Agrippa, Dee, and earlier Solomonic texts while producing "
                "vernacular adaptations that combined learned and popular elements. "
                "Klaassen situates these manuscripts within his broader argument about "
                "the continuity of medieval ritual magic into the early modern period, "
                "showing that sixteenth-century English practitioners drew on the same "
                "core of medieval spirit-conjuring texts as their fifteenth-century "
                "predecessors, supplemented by printed Renaissance sources."
            ),
        },
        {
            "text_id": "magic_of_rogues",
            "title": "The Magic of Rogues",
            "title_original": "Necromancers in Early Tudor England",
            "language": "ENGLISH",
            "text_type": "EDITION",
            "period": "MODERN",
            "date_start": 2021,
            "date_end": 2021,
            "description": (
                "Published by Frank Klaassen and Sharon Hubbs Wright at Penn State "
                "University Press (2021) in the Magic in History Sourcebooks series. "
                "Examines legal documents and magic texts from two early Tudor cases "
                "where English authorities confronted practicing magicians, exploring "
                "how practitioners thought about the world, where they obtained their "
                "ideas, and how their magic was supposed to work. The volume provides "
                "critical editions of the relevant manuscripts and legal records alongside "
                "analysis of the practices involved. Demonstrates the vitality of the "
                "medieval necromantic tradition in early sixteenth-century England and "
                "the social networks through which magical manuscripts circulated among "
                "clerics, practitioners, and curious laypeople."
            ),
        },
        {
            "text_id": "the_magus_barrett",
            "title": "The Magus",
            "title_original": "The Magus, or Celestial Intelligencer",
            "language": "ENGLISH",
            "text_type": "EDITION",
            "period": "EARLY_MODERN",
            "date_start": 1801,
            "date_end": 1801,
            "description": (
                "Compiled by Francis Barrett and published in London in 1801. A substantial "
                "compilation drawing heavily on Agrippa's De Occulta Philosophia, Robert "
                "Turner's seventeenth-century English translations of magical texts, and "
                "related Renaissance and medieval sources. The Magus marks the transition "
                "from manuscript and early print circulation of learned magic to Romantic-"
                "era popular occultism. Barrett organized his compilation in three parts: "
                "natural magic, magnetism and alchemy, and ritual and talismanic magic. "
                "The Magus served as a conduit bringing Agrippa's framework and associated "
                "Renaissance material to nineteenth-century English-language audiences "
                "and influenced later figures including Edward Bulwer-Lytton and "
                "Eliphas Lévi."
            ),
        },
    ]

    for t in texts:
        defaults = {
            "title_original": None,
            "date_start": None,
            "date_end": None,
        }
        conn.execute(
            """INSERT OR IGNORE INTO texts
               (text_id, title, title_original, language, text_type, period,
                date_start, date_end, description, source_method)
               VALUES (:text_id, :title, :title_original, :language, :text_type,
                       :period, :date_start, :date_end, :description, 'SEED_RECEPTION')""",
            {**defaults, **t},
        )
    conn.commit()
    print(f"Seeded {len(texts)} texts.")


def seed_concepts(conn):
    concepts = [
        {
            "slug": "renaissance_magic",
            "label": "Renaissance Magic",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "ANALYST_TERM",
            "definition_short": (
                "Analyst term for the magical traditions of fifteenth- and sixteenth-century "
                "Europe, characterized by the synthesis of Hermeticism, Neoplatonism, "
                "Kabbalah, and natural philosophy associated with figures including Ficino, "
                "Pico, Agrippa, Bruno, and Dee. The category has been contested since "
                "Frances Yates's foundational work of the 1960s-1970s: Yates argued for a "
                "sharp break from medieval magic toward a sanitized natural-Hermetic magic; "
                "Frank Klaassen's manuscript evidence shows strong continuity with medieval "
                "ritual magic traditions. The concept requires careful distinction from "
                "magia naturalis, occult philosophy, and demonic magic."
            ),
            "significance": "Central to the historiography of the transition between medieval and early modern learned magic.",
        },
        {
            "slug": "hermeticism",
            "label": "Hermeticism",
            "label_alt": "Hermetic tradition; Hermetism",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "HYBRID",
            "definition_short": (
                "Hybrid term covering both an ancient body of Greek philosophical and "
                "magical texts attributed to Hermes Trismegistus (a conflation of the "
                "Greek god Hermes and Egyptian Thoth), and the tradition of thought "
                "that drew on these texts from late antiquity through the Renaissance. "
                "As an actor term, Hermetic designated the Corpus Hermeticum and related "
                "Asclepius texts. As an analyst term, it was expanded by Frances Yates "
                "to describe a broader Renaissance synthesis including Neoplatonism, "
                "astral magic, and Kabbalah. The dating of the Hermetic texts to ancient "
                "Egypt was demolished by Isaac Casaubon's philological analysis (1614)."
            ),
            "significance": "Framework for the Yates thesis and key to debates about Renaissance magic's relationship to medieval learned traditions.",
        },
        {
            "slug": "prisca_theologia",
            "label": "Prisca Theologia",
            "label_alt": "Ancient theology; Philosophia perennis",
            "category": "THEOLOGICAL",
            "category_type": "ACTOR_TERM",
            "definition_short": (
                "Latin actor term for the doctrine, articulated primarily by Marsilio "
                "Ficino, that a single ancient theology passed from Moses and Zoroaster "
                "through Hermes Trismegistus, Orpheus, Pythagoras, and Plato to Christian "
                "truth. The term justified Ficino's engagement with pagan texts including "
                "the Corpus Hermeticum, Chaldean Oracles, and Orphic hymns as preparations "
                "for Christian revelation. Pico della Mirandola extended the chain to "
                "include the Kabbalistic tradition. The prisca theologia legitimated a "
                "speculative natural magic rooted in ancient wisdom. Its chronology was "
                "undermined when Casaubon dated the Hermetic texts to the Christian era."
            ),
            "significance": "Foundational doctrine for Ficinian magic and the Yates thesis.",
        },
        {
            "slug": "magia_naturalis_concept",
            "label": "Magia Naturalis",
            "label_alt": "Natural magic",
            "category": "NATURAL_PHILOSOPHY",
            "category_type": "ACTOR_TERM",
            "definition_short": (
                "Latin actor term for a branch of knowledge concerned with the hidden "
                "powers of natural objects and their manipulation through sympathy, "
                "antipathy, and occult correspondence. Distinguished from demonic magic "
                "(goetia) and ceremonial magic, magia naturalis claimed to operate "
                "through natural forces accessible to human knowledge rather than through "
                "demonic mediation. Elaborated by della Porta's Magia Naturalis (1558, "
                "1589) and given philosophical depth by Ficino's spiritus theory, the "
                "category proved capacious: by the seventeenth century it absorbed "
                "alchemy, magnetism, optics, medicine, and experimental observation, "
                "blurring the boundary between natural philosophy and learned magic."
            ),
            "significance": "Central category for Renaissance naturalization of magical practice.",
        },
        {
            "slug": "yates_thesis",
            "label": "The Yates Thesis",
            "label_alt": "Hermetic thesis; Yates hypothesis",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "ANALYST_TERM",
            "definition_short": (
                "Analyst term for the historiographical argument advanced by Frances "
                "Yates in Giordano Bruno and the Hermetic Tradition (1964) and related "
                "works: that Hermeticism and natural magic were central forces in "
                "Renaissance culture, that they drove a transformation of magic from "
                "medieval demonic practice to a naturalized astrological-mathematical "
                "philosophy, and that this Hermetic magic contributed causally to the "
                "Scientific Revolution. The thesis was challenged by Vickers (1979), "
                "Copenhaver, and Klaassen, whose manuscript evidence for strong continuity "
                "between medieval and Renaissance ritual magic contradicts Yates's "
                "narrative of a clean break."
            ),
            "significance": "Transformed Renaissance historiography; now substantially revised but still the organizing reference for debates about the period.",
        },
        {
            "slug": "occult_philosophy",
            "label": "Occult Philosophy",
            "label_alt": "Philosophia occulta",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "HYBRID",
            "definition_short": (
                "Hybrid term used by Agrippa as the title of his major work (De Occulta "
                "Philosophia, 1531-1533) and by later writers to denote a systematic "
                "philosophy of hidden natural powers, astral influences, and ceremonial "
                "operations. As an actor term in the sixteenth century, it designated "
                "Agrippa's three-tiered synthesis of natural, celestial, and ceremonial "
                "magic. As an analyst term, it has been applied to the broader tradition "
                "of learned magic associated with Ficino, Pico, Agrippa, Dee, and related "
                "figures, and to the study of this tradition in works from Walker and "
                "Yates to the present."
            ),
            "significance": "Links the philosophical claims of Renaissance learned magic to its manuscript and ritual practices.",
        },
        {
            "slug": "grimoire_printing_history",
            "label": "Grimoire Printing History",
            "category": "MANUSCRIPT",
            "category_type": "ANALYST_TERM",
            "definition_short": (
                "Analyst term for the history of grimoire transmission through print "
                "from the fifteenth century onward. The printing press dramatically "
                "changed the circulation of magical texts: works that had circulated "
                "in small numbers of manuscripts became available in multiple editions "
                "across Europe. Key events include the printing of Ficino's De Vita "
                "(1489), Agrippa's De Occulta Philosophia (1531), the Arbatel and "
                "Fourth Book of Occult Philosophy (c.1559), Trithemius's Steganographia "
                "(1606), and the French popular grimoire tradition (Grand Albert, Petit "
                "Albert, Grand Grimoire) in the eighteenth century. Owen Davies's "
                "Grimoires (2009) is the standard reference."
            ),
            "significance": "Key to understanding the transformation of medieval manuscript magic into modern print occultism.",
        },
        {
            "slug": "vernacular_grimoire_tradition",
            "label": "Vernacular Grimoire Tradition",
            "category": "MANUSCRIPT",
            "category_type": "ANALYST_TERM",
            "definition_short": (
                "Analyst term for the tradition of magical texts composed or transmitted "
                "in vernacular languages (English, French, German, Italian, Spanish) "
                "rather than Latin. While the high tradition of learned magic remained "
                "primarily Latin, vernacular grimoires emerged from the fifteenth century "
                "onward, often combining learned magical procedures with popular charms, "
                "medical recipes, and folk practices. Klaassen's Making Magic in "
                "Elizabethan England and The Magic of Rogues examine English vernacular "
                "magic manuscripts; Dan Harms and Joseph Peterson's Book of Oberon "
                "edition provides a major source text. The French Grand Albert and "
                "Petit Albert represent the popular side of the vernacular tradition."
            ),
            "significance": "Essential for understanding how Latin learned magic was adapted and democratized in the early modern period.",
        },
        {
            "slug": "neoplatonism_and_magic",
            "label": "Neoplatonism and Magic",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "HYBRID",
            "definition_short": (
                "Hybrid term for the relationship between Neoplatonist philosophy and "
                "magical practice from late antiquity through the Renaissance. Plotinus "
                "and Iamblichus theorized a hierarchy of being through which sympathetic "
                "operations (theurgy) could draw down divine powers. Ficino's translation "
                "of Plotinus, Porphyry, and Iamblichus alongside the Corpus Hermeticum "
                "gave Renaissance magic its philosophical framework of celestial "
                "hierarchies, spiritus mediation, and astral attraction. D.P. Walker "
                "and Frances Yates showed how Ficino's Neoplatonism provided an "
                "intellectual legitimation for astral magic operations. Klaassen has "
                "argued this legitimation was often more rhetorical than operational."
            ),
            "significance": "Defines the philosophical context of Ficinian and Agrippan magic.",
        },
        {
            "slug": "enochian_system",
            "label": "Enochian System",
            "label_alt": "Enochian magic; angelic language",
            "category": "RITUAL",
            "category_type": "HYBRID",
            "definition_short": (
                "A system of angelic language, tables, and magical operations developed "
                "by John Dee and his scryer Edward Kelley through their angelic "
                "conferences of 1582-1589 and recorded in the Mysteriorum Libri Quinque "
                "and related diaries. The system comprises a non-natural language (Enochian) "
                "transmitted by angelic dictation, extensive tables of correspondences, "
                "and operatory procedures. Frank Klaassen has shown that the conference "
                "format and angelic invocation procedures are continuous with late medieval "
                "angelic magic traditions including the Sworn Book of Honorius and the "
                "Ars Notoria, rather than being a distinctly Hermetic or Renaissance "
                "innovation."
            ),
            "significance": "Key example of Renaissance magical practice that claimed novelty while remaining within medieval ritual frameworks.",
        },
        {
            "slug": "print_culture_and_magic",
            "label": "Print Culture and Magic",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "ANALYST_TERM",
            "definition_short": (
                "Analyst term for the intersection of the history of print with the "
                "history of magical text circulation. The printing press from the "
                "1450s onward transformed how magical texts reached audiences: works "
                "that survived in a handful of manuscripts could reach hundreds of "
                "readers in printed editions. This created new markets, new censorship "
                "pressures (Index Librorum Prohibitorum entries for many magical works), "
                "and new possibilities for the corruption and standardization of texts. "
                "Owen Davies's Grimoires (2009) is the standard account; Klaassen's work "
                "on sixteenth-century manuscript collections shows that manuscript "
                "transmission persisted alongside print throughout the early modern period."
            ),
            "significance": "Explains how medieval manuscript traditions became early modern print traditions.",
        },
        {
            "slug": "kabbalism_renaissance_magic",
            "label": "Kabbalism in Renaissance Magic",
            "label_alt": "Christian Kabbalah; Cabala",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "HYBRID",
            "definition_short": (
                "Hybrid term for the incorporation of Jewish Kabbalistic methods and "
                "cosmology into Renaissance Christian philosophical and magical systems. "
                "Pico della Mirandola was the first major Christian thinker to synthesize "
                "Kabbalah with Neoplatonism and magic in his 1486 Theses. Agrippa devoted "
                "substantial sections of De Occulta Philosophia to Kabbalistic letter "
                "magic, divine names, and numerical speculation. Frances Yates argued "
                "that Christian Kabbalah was central to the Hermetic tradition she traced "
                "through Bruno and Dee. Klaassen has noted that the Kabbalistic elements "
                "in actual practical magic manuscripts of the period are present but less "
                "dominant than the philosophical literature suggests."
            ),
            "significance": "Links Renaissance philosophical magic to the Hebrew learned tradition and to debates about Yates's thesis.",
        },
        {
            "slug": "spiritual_magic_walker",
            "label": "Spiritual Magic",
            "label_alt": "Spirit magic; magia spiritalis",
            "category": "RITUAL",
            "category_type": "HYBRID",
            "definition_short": (
                "A category developed by D.P. Walker in Spiritual and Demonic Magic "
                "(1958) to describe magical operations that work through the pneuma or "
                "spiritus, the subtle material medium between soul and body in Neoplatonist "
                "physiology, rather than through explicit demonic summons. Walker argued "
                "that Ficino's De Vita Coelitus Comparanda was a spiritual magic: "
                "operations on the spiritus through music, scent, diet, and talismans "
                "drew stellar influences without violating the natural order or summoning "
                "demons. Walker's distinction between spiritual and demonic magic parallels "
                "but is not identical to the Renaissance actor-term distinction between "
                "magia naturalis and goetia or nigromantia."
            ),
            "significance": "Walker's framework for Ficinian magic remains the primary analytical tool for distinguishing categories within Renaissance occult philosophy.",
        },
        {
            "slug": "reformation_and_magic",
            "label": "Reformation and Magic",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "ANALYST_TERM",
            "definition_short": (
                "Analyst term for the relationship between the Protestant and Catholic "
                "Reformations and the history of magical practice and belief in the "
                "sixteenth and seventeenth centuries. The Reformation created new "
                "pressures on magical practice: Protestant theologians rejected Catholic "
                "sacramental and exorcistic rites as superstition while simultaneously "
                "enabling new forms of learned Protestant demonology. The Inquisition "
                "prosecuted magical practitioners in Catholic territories. The Arbatel "
                "(1575) shows Protestant inflections in its grimoire; the development "
                "of vernacular magic in England was shaped by the Reformation's "
                "disruption of monastic and clerical institutional contexts for "
                "manuscript transmission."
            ),
            "significance": "Contextualizes the social and institutional conditions of early modern magical practice.",
        },
        {
            "slug": "rosicrucian_movement",
            "label": "Rosicrucian Movement",
            "label_alt": "Rosicrucianism; Fraternitas Rosae Crucis",
            "category": "HISTORIOGRAPHICAL",
            "category_type": "ANALYST_TERM",
            "definition_short": (
                "Analyst term for the early seventeenth-century movement associated with "
                "three anonymous manifestos: the Fama Fraternitatis (1614), Confessio "
                "Fraternitatis (1615), and Chymische Hochzeit Christiani Rosenkreutz "
                "(1616). These texts claimed the existence of a secret brotherhood of "
                "Christian Rosenkreuz devoted to spiritual and magical reform of society. "
                "Frances Yates's Rosicrucian Enlightenment (1972) argued that the "
                "movement represented a political and magical program connected to the "
                "Hermetic-Kabbalist tradition. The Rosicrucian synthesis drew on "
                "Paracelsian natural philosophy, alchemy, and the occult philosophy "
                "of Agrippa and Dee to produce a distinctive early modern magical-"
                "religious worldview."
            ),
            "significance": "Marks the culmination of Renaissance magical synthesis into an early seventeenth-century reform movement.",
        },
    ]

    for c in concepts:
        defaults = {"label_alt": None, "definition_short": None, "definition_long": None}
        conn.execute(
            """INSERT OR IGNORE INTO concepts
               (slug, label, label_alt, category, category_type, definition_short, significance, source_method)
               VALUES (:slug, :label, :label_alt, :category, :category_type, :definition_short, :significance, 'SEED_RECEPTION')""",
            {**defaults, **c},
        )
    conn.commit()
    print(f"Seeded {len(concepts)} concepts.")


def seed_timeline_events(conn):
    events = [
        {
            "year": 1438,
            "year_end": 1439,
            "event_type": "SCHOLARSHIP",
            "title": "Gemistos Plethon at the Council of Florence",
            "location": "Florence, Italy",
            "latitude": 43.7696,
            "longitude": 11.2558,
            "description": (
                "The Byzantine Neoplatonist philosopher Gemistos Plethon attended the "
                "Council of Florence (1438-1445) and introduced Cosimo de' Medici and "
                "Florentine humanists to the living tradition of Greek Neoplatonism and "
                "to the Hermetic and Chaldean texts. Plethon's lectures on Platonic "
                "philosophy sparked the Platonic revival that Cosimo would support through "
                "the founding of the Platonic Academy and the patronage of Marsilio Ficino. "
                "This event initiated the chain of transmission that brought the Corpus "
                "Hermeticum to Latin Europe and made Neoplatonism the philosophical "
                "framework for Renaissance learned magic. Plethon's influence on "
                "Ficino, through the intermediary of Cardinal Bessarion, established "
                "the intellectual conditions for the Ficinian synthesis."
            ),
        },
        {
            "year": 1463,
            "event_type": "TRANSLATION",
            "title": "Ficino translates the Corpus Hermeticum",
            "location": "Florence, Italy",
            "latitude": 43.7696,
            "longitude": 11.2558,
            "description": (
                "Marsilio Ficino, acting on Cosimo de' Medici's urgent instructions, "
                "set aside his translation of Plato to complete a Latin version of the "
                "fourteen Greek texts of the Corpus Hermeticum. Ficino completed the "
                "translation—titled Pimander—in 1463, before Cosimo's death in August "
                "of that year. Published in 1471 (Treviso), the translation provided "
                "Renaissance Europe with direct access to texts then believed to represent "
                "an ancient Egyptian theology older than Plato and Moses. The documents "
                "were in fact composed in the first and second centuries CE, as Isaac "
                "Casaubon demonstrated philologically in 1614, but the earlier dating "
                "gave the Hermetic writings authority as a prisca theologia and made "
                "Ficino's natural magic appear to rest on ancient foundations."
            ),
        },
        {
            "year": 1471,
            "event_type": "PUBLICATION",
            "title": "Ficino's Pimander printed at Treviso",
            "location": "Treviso, Italy",
            "latitude": 45.6669,
            "longitude": 12.2436,
            "description": (
                "The first printing of Marsilio Ficino's Latin translation of the Corpus "
                "Hermeticum, under the title Pimander seu de potestate et sapientia "
                "divina, was issued at Treviso in 1471 by Gerardus de Lisa. This was "
                "among the earliest Italian printings of a text associated with the "
                "Hermetic tradition, and it inaugurated the wide European circulation "
                "of texts previously confined to manuscript. The print edition brought "
                "Ficino's synthesis of Hermeticism and Neoplatonism to a European "
                "scholarly audience and provided the source text for the later elaborations "
                "of the Hermetic tradition by Pico, Agrippa, Bruno, and Dee. Owen "
                "Davies and Frances Yates both note the Pimander printing as a pivotal "
                "moment in the history of learned magic in print."
            ),
        },
        {
            "year": 1486,
            "event_type": "PUBLICATION",
            "title": "Pico della Mirandola publishes 900 Theses",
            "location": "Rome, Italy",
            "latitude": 41.9028,
            "longitude": 12.4964,
            "description": (
                "Giovanni Pico della Mirandola, aged twenty-three, published his "
                "Conclusiones nongentae (900 Theses) in Rome with an invitation to "
                "public disputation. The theses synthesized scholastic philosophy, "
                "Neoplatonism, Hermeticism, and Kabbalah, and argued that magic "
                "and Kabbalah together constituted the best proof of Christ's divinity. "
                "Pope Innocent VIII condemned thirteen of the theses and prohibited "
                "the disputation. Pico's accompanying Oration on the Dignity of Man "
                "became a foundational text of Renaissance humanism and occult philosophy. "
                "His synthesis of Kabbalistic divine-name magic with the Neoplatonist "
                "hierarchy of being established a template for Agrippa and subsequent "
                "Renaissance occultists who sought to unify all forms of knowledge "
                "including natural magic within a single philosophical system."
            ),
        },
        {
            "year": 1489,
            "event_type": "PUBLICATION",
            "title": "Ficino publishes De Vita Coelitus Comparanda",
            "location": "Florence, Italy",
            "latitude": 43.7696,
            "longitude": 11.2558,
            "description": (
                "Marsilio Ficino published the third book of his De Vita, titled De Vita "
                "Coelitus Comparanda (On Obtaining Life from the Heavens), as part of "
                "the three-book De Vita collection. The text constitutes the most "
                "explicit Renaissance theory of stellar magic, drawing on the Picatrix, "
                "pseudo-Ptolemy's De imaginibus, and Hermetic star catalogues to describe "
                "how physicians and scholars may attract beneficial celestial influences "
                "through talismans, music, scents, and dietary practice. D.P. Walker "
                "identified this text as the key document for Ficino's spiritual magic. "
                "Frank Klaassen has shown that it shares significant material with "
                "medieval ritual magic texts and was used as a source by sixteenth-century "
                "magic manuscript compilers, demonstrating strong continuity with "
                "medieval learned traditions."
            ),
        },
        {
            "year": 1499,
            "event_type": "COMPOSITION",
            "title": "Trithemius composes Steganographia",
            "location": "Sponheim, Germany",
            "latitude": 49.8358,
            "longitude": 7.9139,
            "description": (
                "Johannes Trithemius, abbot of Sponheim, composed the Steganographia "
                "approximately in 1499. The work circulated in manuscript for over a "
                "century before print publication in 1606. Ostensibly a system for "
                "long-distance communication using angelic intermediaries, the text "
                "drew on the late medieval tradition of angel magic while claiming to "
                "operate through purely natural forces. When its manuscript circulation "
                "became known, Trithemius was accused of teaching demonic magic and had "
                "to defend himself in letters. The Steganographia was enormously "
                "influential: Agrippa visited Trithemius in 1509-1510 and the meeting "
                "shaped the composition of De Occulta Philosophia. John Dee acquired "
                "a manuscript copy and made extensive annotations. In 1998 Thomas Ernst "
                "demonstrated that Book III conceals a system of cryptographic ciphers "
                "beneath the magical text."
            ),
        },
        {
            "year": 1510,
            "event_type": "COMPOSITION",
            "title": "Agrippa completes manuscript De Occulta Philosophia",
            "location": "Cologne, Germany",
            "latitude": 50.9333,
            "longitude": 6.9503,
            "description": (
                "Heinrich Cornelius Agrippa completed an early version of De Occulta "
                "Philosophia approximately in 1510, following his visit to Trithemius at "
                "Sponheim in 1509-1510. The manuscript version circulated among "
                "humanist and magical circles for more than two decades before the "
                "expanded printed edition of 1531-1533. The early composition demonstrates "
                "the degree to which the major Renaissance occult synthesis was already "
                "in place by the early sixteenth century, before the printed editions "
                "of most of the works Agrippa synthesized had appeared. Frank Klaassen's "
                "analysis of the manuscript witnesses and their relationship to late "
                "medieval magic texts provides the clearest demonstration of the "
                "continuity between medieval ritual magic and Renaissance occult philosophy."
            ),
        },
        {
            "year": 1519,
            "event_type": "SCHOLARSHIP",
            "title": "Trithemius dies; library inventory survives",
            "location": "Würzburg, Germany",
            "latitude": 49.7944,
            "longitude": 9.9294,
            "description": (
                "Johannes Trithemius died at the monastery of St. James in Würzburg "
                "on 13 December 1516 (some sources give 1519). His library at Sponheim, "
                "which he had built from approximately fifty volumes to over two thousand, "
                "was one of the largest monastic libraries in Germany and included an "
                "extensive collection of magical, philosophical, and historical manuscripts. "
                "Trithemius composed a Catalogus scriptorum ecclesiasticorum (1494) and "
                "related bibliographic works that constitute important sources for the "
                "history of medieval manuscript transmission. His library inventories "
                "record the breadth of occult and magical texts available to a learned "
                "abbot in the German Rhineland in the late fifteenth and early sixteenth "
                "centuries, providing crucial evidence for the institutional contexts "
                "of Renaissance learned magic."
            ),
        },
        {
            "year": 1531,
            "event_type": "PUBLICATION",
            "title": "Agrippa publishes De Occulta Philosophia",
            "location": "Cologne, Germany",
            "latitude": 50.9333,
            "longitude": 6.9503,
            "description": (
                "Heinrich Cornelius Agrippa published the expanded three-book version "
                "of De Occulta Philosophia at Cologne in 1531-1533 with the printer "
                "Johannes Soter. The published version substantially expanded the "
                "manuscript draft of c.1510, drawing on additional sources and "
                "incorporating Kabbalistic material in greater depth. The work became "
                "the most widely circulated and influential printed text on occult "
                "philosophy in the sixteenth and seventeenth centuries and shaped "
                "generations of magical practitioners and writers. The third book, "
                "on ceremonial magic, includes material from the Munich Manual and "
                "related medieval spirit-conjuring texts, demonstrating to Klaassen "
                "that Agrippa served as a conduit transmitting medieval demonic and "
                "angelic magic traditions into print under a philosophical framework."
            ),
        },
        {
            "year": 1558,
            "event_type": "PUBLICATION",
            "title": "Della Porta publishes Magia Naturalis",
            "location": "Naples, Italy",
            "latitude": 40.8518,
            "longitude": 14.2681,
            "description": (
                "Giovanni Battista della Porta published the first edition of Magia "
                "Naturalis, in four books, in Naples in 1558. An expanded twenty-book "
                "edition followed in 1589 and was widely translated into Italian, French, "
                "English, and Dutch. The work systematized the concept of natural magic "
                "as a body of knowledge about the hidden properties of nature, framed "
                "within Aristotelian natural philosophy. By organizing phenomena of "
                "alchemy, gardening, optics, magnetism, and popular medical practice "
                "under the rubric of magia naturalis, della Porta demonstrated how "
                "the concept could absorb observational and experimental practice while "
                "retaining its magical terminology. The Accademia dei Segreti, which "
                "della Porta founded in Naples, was the first institutional expression "
                "of natural magic as a collective intellectual enterprise."
            ),
        },
        {
            "year": 1559,
            "event_type": "PUBLICATION",
            "title": "Fourth Book of Occult Philosophy first printed",
            "location": "Marburg, Germany",
            "latitude": 50.8021,
            "longitude": 8.7740,
            "description": (
                "The Latin text known as the Fourth Book of Occult Philosophy was printed "
                "for the first time in Marburg in 1559 under Agrippa's name, though "
                "almost certainly not by Agrippa. Klaassen identifies multiple editions "
                "in the mid-sixteenth century and notes the Fourth Book circulating "
                "bound with the Arbatel and related texts. The work concerns the "
                "conjuration and binding of spirits using circles, pentacles, and "
                "Solomonic procedures derived from the tradition of late medieval demonic "
                "magic. Its attribution to Agrippa guaranteed a wide audience and "
                "demonstrates the tendency of early print culture to attach practical "
                "magical manuals to prestigious learned names, conflating the "
                "philosophical and the operational dimensions of Renaissance occultism."
            ),
        },
        {
            "year": 1563,
            "event_type": "PUBLICATION",
            "title": "Weyer publishes De Praestigiis Daemonum",
            "location": "Basel, Switzerland",
            "latitude": 47.5596,
            "longitude": 7.5886,
            "description": (
                "Johann Weyer published De Praestigiis Daemonum et Incantationibus ac "
                "Veneficiis at Basel in 1563, with the printer Johannes Oporinus. The "
                "work argued that confessions of witchcraft reflected delusional disease "
                "rather than genuine demonic pacts, and challenged the legal prosecution "
                "of accused witches. Weyer drew on his teacher Agrippa's sceptical "
                "arguments about magic's effectiveness while maintaining belief in "
                "demonic existence. The book went through six Latin editions and several "
                "vernacular translations. It was violently attacked by Jean Bodin in "
                "De la Démonomanie (1580). Weyer's work represents the beginning of "
                "a critical medical tradition that would continue through Reginald Scot "
                "and into the Enlightenment critique of witchcraft prosecution."
            ),
        },
        {
            "year": 1564,
            "event_type": "PUBLICATION",
            "title": "Dee publishes Monas Hieroglyphica",
            "location": "Antwerp, Belgium",
            "latitude": 51.2194,
            "longitude": 4.4025,
            "description": (
                "John Dee published his cryptic treatise Monas Hieroglyphica in Antwerp "
                "in 1564, dedicated to Holy Roman Emperor Maximilian II. The text argues "
                "for a unified symbolic language derived from the conjunction of "
                "astronomical, alchemical, and Kabbalistic symbols in the glyph of "
                "the monad. Dee considered it among his most significant theoretical "
                "works and believed it communicated a philosophical secret about the "
                "unity of knowledge. The Monas has been interpreted variously as "
                "alchemical treatise, Kabbalistic commentary, and mathematical symbolism. "
                "Nicholas Clulee's John Dee's Natural Philosophy (1988) and Dee's own "
                "notes to the angel diaries provide the best evidence for its place "
                "within his intellectual system."
            ),
        },
        {
            "year": 1575,
            "event_type": "PUBLICATION",
            "title": "Arbatel de Magia Veterum printed at Basel",
            "location": "Basel, Switzerland",
            "latitude": 47.5596,
            "longitude": 7.5886,
            "description": (
                "The Arbatel de Magia Veterum was printed at Basel in 1575 as the first "
                "of nine supposed books of Olympic spirit magic, only the Isagoge (first "
                "book) of which survives. The text presents a system of seven Olympic "
                "spirits governing planetary spheres, to be approached through prayer "
                "and ethical preparation rather than elaborate demonic conjuration. "
                "Its tone is markedly devotional and shows Protestant-inflected concern "
                "with the practitioner's spiritual state. Klaassen notes that the Arbatel "
                "was printed around the same time as the Fourth Book of Occult Philosophy "
                "and was often bound with it, suggesting a mid-sixteenth-century market "
                "for printed ceremonial magic. Joseph Peterson's edition provides the "
                "standard critical text."
            ),
        },
        {
            "year": 1582,
            "event_type": "COMPOSITION",
            "title": "Dee and Kelley begin angelic conferences",
            "location": "Mortlake, England",
            "latitude": 51.4688,
            "longitude": -0.2687,
            "description": (
                "In March 1582 Edward Kelley arrived at John Dee's home at Mortlake, "
                "Surrey, and began serving as Dee's primary scryer in a series of "
                "angelic conferences that would continue until 1589. The conferences "
                "used a shewstone (crystal ball) and a show-stone of dark stone, through "
                "which Kelley reported visions and heard angelic speeches that Dee "
                "recorded in extensive diaries. The conferences produced the Enochian "
                "language system, tables of angelic correspondences, and numerous "
                "operations that Dee copied into the Mysteriorum Libri Quinque and "
                "related records. Klaassen's analysis demonstrates that the conference "
                "format, the angelic intermediaries, and the procedures used are "
                "continuous with the tradition of late medieval angelic magic represented "
                "by the Sworn Book of Honorius and the Ars Notoria."
            ),
        },
        {
            "year": 1584,
            "event_type": "PUBLICATION",
            "title": "Reginald Scot publishes Discoverie of Witchcraft",
            "location": "London, England",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "description": (
                "Reginald Scot published The Discoverie of Witchcraft in London in 1584. "
                "The work is the most systematic English-language skeptical critique of "
                "witch-hunting in the sixteenth century, arguing that witchcraft "
                "accusations rest on fraud, delusion, and clerical manipulation. The "
                "Discoverie also preserves, in its appendices, extensive descriptions "
                "of practical conjuring operations, Solomonic procedures, and magical "
                "experiments that make it an inadvertent sourcebook for practitioners. "
                "Klaassen notes that seventeenth-century publishers reissued the work "
                "recognizing its commercial value to magical practitioners. The book "
                "circulated widely in Elizabethan England and was read by figures in "
                "the same networks as the vernacular magic manuscript compilers studied "
                "in Klaassen's Making Magic in Elizabethan England."
            ),
        },
        {
            "year": 1600,
            "event_type": "CONDEMNATION",
            "title": "Giordano Bruno burned in Rome",
            "location": "Rome, Italy",
            "latitude": 41.9028,
            "longitude": 12.4964,
            "description": (
                "Giordano Bruno was burned at the stake in the Campo de' Fiori, Rome, "
                "on 17 February 1600, after a seven-year Inquisition trial in Venice "
                "and Rome. The charges against Bruno are not fully documented, but "
                "included denial of the Trinity, belief in an infinite universe and "
                "plurality of worlds, and possibly the practice of magic. Frances Yates "
                "argued that Bruno's death marked the end of the Hermetic-magical phase "
                "of Renaissance thought and a turning point toward the mechanical "
                "philosophy of the Scientific Revolution. This interpretation has been "
                "challenged: Bruno's cosmological heterodoxy, not his Hermeticism, "
                "appears to have been the primary cause of his condemnation. Bruno's "
                "execution became a symbol of intellectual martyrdom in later "
                "historiography and occultist reception."
            ),
        },
        {
            "year": 1606,
            "event_type": "PUBLICATION",
            "title": "Steganographia finally printed",
            "location": "Frankfurt, Germany",
            "latitude": 50.1109,
            "longitude": 8.6821,
            "description": (
                "Trithemius's Steganographia, composed c.1499 and circulated in "
                "manuscript for over a century, was finally printed at Frankfurt in "
                "1606. The printing came three years before the text was placed on the "
                "Index Librorum Prohibitorum (1609). The delay between composition and "
                "print is itself significant: Trithemius explicitly withheld the work "
                "from wide circulation due to its content, and its manuscript transmission "
                "was consequently limited to humanist and magical networks. The print "
                "publication changed the reception entirely, making the text available "
                "broadly for the first time and triggering renewed accusations of demonic "
                "content. John Dee had already acquired a manuscript copy and made "
                "extensive notes. The 1606 printing is the standard base text for modern "
                "scholars including Joseph Peterson's online edition at esotericarchives.com."
            ),
        },
        {
            "year": 1614,
            "year_end": 1616,
            "event_type": "PUBLICATION",
            "title": "Rosicrucian manifestos published",
            "location": "Kassel, Germany",
            "latitude": 51.3127,
            "longitude": 9.4797,
            "description": (
                "Three anonymous texts associated with the early Rosicrucian movement "
                "were published in Germany between 1614 and 1616: the Fama Fraternitatis "
                "(1614, Kassel), the Confessio Fraternitatis (1615, Kassel), and the "
                "Chymische Hochzeit Christiani Rosenkreutz (1616, Strasbourg). The Fama "
                "and Confessio claimed the existence of a secret learned brotherhood "
                "devoted to spiritual, medical, and magical reform; the Chymische Hochzeit "
                "is now attributed to Johann Valentin Andreae. Frances Yates's Rosicrucian "
                "Enlightenment (1972) argued that these texts represented a political "
                "and magical program connected to the Hermetic-Kabbalist tradition of "
                "Ficino, Agrippa, and Dee. The manifestos drew heavily on Paracelsian "
                "natural philosophy and alchemy alongside learned magic."
            ),
        },
        {
            "year": 1614,
            "event_type": "SCHOLARSHIP",
            "title": "Casaubon dates the Hermetic texts",
            "location": "London, England",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "description": (
                "Isaac Casaubon, in his De rebus sacris et ecclesiasticis exercitationes "
                "(1614), demonstrated through philological analysis that the Corpus "
                "Hermeticum was not of ancient Egyptian origin but was composed in the "
                "first and second centuries CE in the Greek-speaking world. This dating "
                "demolished the intellectual foundation of the prisca theologia and "
                "the authority Ficino, Pico, and Agrippa had attributed to the Hermetic "
                "texts as ancient wisdom older than Plato. The demonstration did not "
                "immediately end Hermetic influence, which continued through the "
                "seventeenth century, but it fundamentally changed the evidentiary "
                "status of the tradition. Frances Yates acknowledged Casaubon's "
                "importance but argued that Hermeticism continued to operate as an "
                "intellectual force despite the revised dating."
            ),
        },
        {
            "year": 1750,
            "year_end": 1800,
            "event_type": "PUBLICATION",
            "title": "French popular grimoire tradition flourishes",
            "location": "Lyon, France",
            "latitude": 45.7640,
            "longitude": 4.8357,
            "description": (
                "During the second half of the eighteenth century, Lyon and other French "
                "printing centers became the primary source for a vast popular grimoire "
                "literature distributed across France and its colonies. The Grand Albert "
                "(attributed to Albertus Magnus), the Petit Albert, the Dragon Rouge "
                "(Grand Grimoire), and related texts were printed in cheap editions and "
                "sold through colporteurs (traveling peddlers) and market stalls. Owen "
                "Davies's Grimoires (2009) traces how these popular texts combined "
                "remnants of learned medieval and Renaissance magic with folk remedies, "
                "agricultural charms, and popular devotional practices. The Lyon printing "
                "trade provided these texts to French-speaking populations in Europe, "
                "the Caribbean, and West Africa, establishing the vernacular grimoire "
                "tradition that would eventually influence Vodou and other Atlantic "
                "religious traditions."
            ),
        },
        {
            "year": 1801,
            "event_type": "PUBLICATION",
            "title": "Francis Barrett publishes The Magus",
            "location": "London, England",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "description": (
                "Francis Barrett published The Magus, or Celestial Intelligencer in "
                "London in 1801. The work is a substantial compilation drawn primarily "
                "from Agrippa's De Occulta Philosophia, Robert Turner's seventeenth-"
                "century English translations of magical texts, and related sources. "
                "The Magus marks a key moment in the commercial popularization of learned "
                "magic: a text previously accessible only to readers of Latin or to "
                "those with access to expensive manuscripts now appeared in English in "
                "a format aimed at a popular audience. Barrett's compilation served as "
                "a bridge between Renaissance occult philosophy and the nineteenth-century "
                "occult revival. Owen Davies traces the influence of The Magus on the "
                "generation of occultists who preceded the Golden Dawn."
            ),
        },
        {
            "year": 1888,
            "event_type": "EDITION",
            "title": "Mathers translates and publishes Key of Solomon",
            "location": "London, England",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "description": (
                "Samuel Liddell MacGregor Mathers published The Key of Solomon the King "
                "(Clavicula Salomonis) in London in 1888, translated from British Library "
                "manuscripts and other sources. The edition, the first scholarly English "
                "translation of the Clavicula Salomonis, made the most important "
                "medieval Solomonic grimoire widely available to English-language "
                "occultists and was immediately influential in Golden Dawn circles. "
                "Mathers's editorial choices—including some invented sections and "
                "departure from the best manuscripts—have been corrected in subsequent "
                "editions. Joseph Peterson's later critical editions of the Clavicula "
                "Salomonis and the Lesser Key of Solomon (2001) substantially supersede "
                "Mathers's work as scholarly editions while recognizing its historical "
                "importance in the reception history of the text."
            ),
        },
        {
            "year": 1958,
            "event_type": "SCHOLARSHIP",
            "title": "D.P. Walker publishes Spiritual and Demonic Magic",
            "location": "London, England",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "description": (
                "Danielle Pickering Walker published Spiritual and Demonic Magic: From "
                "Ficino to Campanella at the Warburg Institute in 1958. The book provided "
                "the first systematic scholarly account of Renaissance magic's relationship "
                "to Neoplatonism and demonology, with chapters on Ficino's De Vita "
                "Coelitus Comparanda, Pico, Agrippa, Cardano, della Porta, Bruno, and "
                "Campanella. Walker's distinction between spiritual magic operating through "
                "the pneuma and demonic magic involving explicit diabolical summons "
                "established the primary analytical framework for Renaissance magical "
                "theory. The book preceded and directly influenced Frances Yates's broader "
                "Hermetic thesis, and remains the standard scholarly account of Ficino's "
                "magical philosophy decades after its publication."
            ),
        },
        {
            "year": 1964,
            "event_type": "SCHOLARSHIP",
            "title": "Yates publishes Giordano Bruno and the Hermetic Tradition",
            "location": "London, England",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "description": (
                "Frances Yates published Giordano Bruno and the Hermetic Tradition at "
                "the University of Chicago Press in 1964. The book argued that Hermeticism "
                "and natural magic, transmitted from Ficino through Pico, Agrippa, Bruno, "
                "and Dee, constituted a major force in Renaissance culture and contributed "
                "to the Scientific Revolution. The Yates thesis transformed Renaissance "
                "historiography and established the study of Renaissance magic as a "
                "legitimate field of intellectual history. The thesis has since been "
                "substantially revised: Brian Vickers challenged it in 1979, Brian "
                "Copenhaver refined the understanding of Hermeticism, and Frank Klaassen's "
                "manuscript evidence for strong continuity between medieval ritual magic "
                "and Renaissance practice challenged the clean break between medieval "
                "'dirty magic' and Renaissance Hermetic philosophy that Yates assumed."
            ),
        },
        {
            "year": 1979,
            "event_type": "SCHOLARSHIP",
            "title": "Yates publishes The Occult Philosophy in the Elizabethan Age",
            "location": "London, England",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "description": (
                "Frances Yates published The Occult Philosophy in the Elizabethan Age "
                "at Routledge in 1979, her last major book. The work extended her "
                "Hermetic thesis to the Elizabethan period, reading John Dee, Christopher "
                "Marlowe's Doctor Faustus, Edmund Spenser, and Philip Sidney through "
                "the lens of Kabbalist-Hermetic magic. Yates argued that Dee's practical "
                "magic derived from Agrippa's occult philosophy and represented an attempt "
                "to realize a Hermetic reform of knowledge. This interpretation has been "
                "challenged by Klaassen and Nicholas Clulee, who demonstrated that Dee's "
                "actual magical practice drew on medieval ritual traditions rather than "
                "the natural Hermetic magic Yates described. The book helped establish "
                "the study of early modern English literature and culture in relation to "
                "the history of magic."
            ),
        },
        {
            "year": 1995,
            "event_type": "SCHOLARSHIP",
            "title": "Peterson founds Esoteric Archives",
            "location": "Tacoma, United States",
            "latitude": 47.2529,
            "longitude": -122.4443,
            "description": (
                "Joseph H. Peterson founded esotericarchives.com in 1995, providing free "
                "online access to transcriptions of historical magical texts including "
                "the Key of Solomon, Grimorium Verum, Steganographia, Arbatel, Book of "
                "Oberon, and dozens of related works. The site grew to serve over three "
                "million document requests per month and became the primary online "
                "resource for scholars and practitioners seeking access to grimoire texts. "
                "Peterson's editorial practice involved collating manuscript witnesses "
                "and printed editions to establish reliable texts with scholarly notes. "
                "His online archive, combined with his print editions from Ibis Press "
                "and Weiser Books, represents the most important contribution to making "
                "the grimoire tradition accessible to serious scholarly and popular "
                "audiences since Mathers's editions of the 1880s-1900s."
            ),
        },
        {
            "year": 2009,
            "event_type": "SCHOLARSHIP",
            "title": "Owen Davies publishes Grimoires: A History",
            "location": "Oxford, England",
            "latitude": 51.7520,
            "longitude": -1.2577,
            "description": (
                "Owen Davies published Grimoires: A History of Magic Books at Oxford "
                "University Press in 2009. The book provides the most comprehensive "
                "social and cultural history of grimoire transmission from ancient "
                "Mesopotamia and Egypt through the twenty-first century. Davies covers "
                "medieval manuscript circulation, the impact of the printing press on "
                "grimoire diffusion in the sixteenth and seventeenth centuries, the "
                "French popular grimoire tradition of the eighteenth century, "
                "nineteenth-century occultist editions (Mathers, Waite, Lévi, Barrett), "
                "and contemporary global usage in North America, West Africa, the "
                "Caribbean, and Brazil. Davies situates grimoires in social history, "
                "examining ownership, circulation, commercial networks, and the "
                "relationship between elite learned magic and popular practice across "
                "five millennia."
            ),
        },
        {
            "year": 2015,
            "event_type": "EDITION",
            "title": "Harms, Clark, and Peterson publish Book of Oberon",
            "location": "Washington, United States",
            "latitude": 38.9072,
            "longitude": -77.0369,
            "description": (
                "Daniel Harms, James R. Clark, and Joseph H. Peterson published The "
                "Book of Oberon: A Sourcebook of Elizabethan Magic at Llewellyn "
                "Worldwide in 2015. The volume provides a complete transcription and "
                "annotated translation of Folger Shakespeare Library MS Vb.26, a late "
                "sixteenth-century English manuscript of approximately 450 pages. The "
                "manuscript combines Solomonic spirit lists drawn from Agrippa and "
                "Continental sources with vernacular fairy magic, treasure-seeking, "
                "love operations, and practical conjuring in both Latin and English. "
                "The Book of Oberon edition, alongside Klaassen's Making Magic in "
                "Elizabethan England, documents how Elizabethan practitioners combined "
                "learned Continental magic traditions with native English vernacular "
                "practices and provides a primary source for the study of the vernacular "
                "grimoire tradition in Renaissance England."
            ),
        },
    ]

    for ev in events:
        conn.execute(
            """INSERT OR IGNORE INTO timeline_events
               (year, year_end, event_type, title, description, location, latitude, longitude, confidence)
               VALUES (:year, :year_end, :event_type, :title, :description, :location, :latitude, :longitude, 'MEDIUM')""",
            {
                "year_end": None,
                "location": None,
                "latitude": None,
                "longitude": None,
                **ev,
            },
        )
    conn.commit()
    print(f"Seeded {len(events)} timeline events.")


def seed_relationships(conn):
    """Link new entries together and to existing entries."""

    def pid(person_id):
        row = conn.execute("SELECT id FROM persons WHERE person_id=?", (person_id,)).fetchone()
        return row[0] if row else None

    def tid(text_id):
        row = conn.execute("SELECT id FROM texts WHERE text_id=?", (text_id,)).fetchone()
        return row[0] if row else None

    def cid(slug):
        row = conn.execute("SELECT id FROM concepts WHERE slug=?", (slug,)).fetchone()
        return row[0] if row else None

    person_text_links = [
        # Ficino
        ("marsilio_ficino", "de_vita_coelitus_comparanda", "AUTHOR"),
        ("marsilio_ficino", "corpus_hermeticum_latin", "TRANSLATOR"),
        ("marsilio_ficino", "picatrix", "SCHOLAR_OF"),
        ("marsilio_ficino", "speculum_astronomiae", "SCHOLAR_OF"),
        # Pico
        ("pico_della_mirandola", "oration_dignity_man", "AUTHOR"),
        # Agrippa
        ("cornelius_agrippa", "de_occulta_philosophia", "AUTHOR"),
        ("cornelius_agrippa", "transformations_of_magic", "SUBJECT"),
        ("cornelius_agrippa", "fourth_book_occult_philosophy", "ATTRIBUTED_AUTHOR"),
        # Trithemius
        ("johannes_trithemius", "steganographia", "AUTHOR"),
        ("johannes_trithemius", "polygraphia_trithemius", "AUTHOR"),
        # Dee
        ("john_dee", "mysteriorum_libri", "AUTHOR"),
        ("john_dee", "monas_hieroglyphica", "AUTHOR"),
        ("john_dee", "making_magic_elizabethan", "SUBJECT"),
        ("john_dee", "occult_philosophy_elizabethan_yates", "SUBJECT"),
        # Kelley
        ("edward_kelley", "mysteriorum_libri", "AUTHOR"),
        # Bruno
        ("giordano_bruno", "giordano_bruno_hermetic_yates", "SUBJECT"),
        # della Porta
        ("giovanni_battista_della_porta", "magia_naturalis", "AUTHOR"),
        # Yates
        ("frances_yates", "giordano_bruno_hermetic_yates", "AUTHOR"),
        ("frances_yates", "occult_philosophy_elizabethan_yates", "AUTHOR"),
        # Walker
        ("dp_walker", "spiritual_demonic_magic_walker", "AUTHOR"),
        # Davies
        ("owen_davies", "grimoires_history_davies", "AUTHOR"),
        # Peterson
        ("joseph_peterson", "book_of_oberon_edition", "EDITOR"),
        ("joseph_peterson", "mysteriorum_libri", "EDITOR"),
        ("joseph_peterson", "liber_juratus_honorii", "EDITOR"),
        ("joseph_peterson", "grimorium_verum", "EDITOR"),
        ("joseph_peterson", "lemegeton", "SCHOLAR_OF"),
        # Harms
        ("dan_harms", "book_of_oberon_edition", "EDITOR"),
        ("dan_harms", "book_of_oberon", "EDITOR"),
        # Mathers
        ("samuel_liddell_mathers", "clavicula_salomonis", "EDITOR"),
        ("samuel_liddell_mathers", "ars_goetia", "EDITOR"),
        # Scot
        ("reginald_scot", "discoverie_of_witchcraft", "AUTHOR"),
        # Weyer
        ("johann_weyer", "de_praestigiis_daemonum", "AUTHOR"),
        # Paracelsus
        ("paracelsus", "de_mineralibus", "SCHOLAR_OF"),
        # Barrett
        ("francis_barrett", "the_magus_barrett", "AUTHOR"),
        # Klaassen (existing) - link to new texts
        ("frank_klaassen", "making_magic_elizabethan", "EDITOR"),
        ("frank_klaassen", "magic_of_rogues", "AUTHOR"),
        ("frank_klaassen", "giordano_bruno_hermetic_yates", "SCHOLAR_OF"),
        ("frank_klaassen", "spiritual_demonic_magic_walker", "SCHOLAR_OF"),
        # Sophie Page (existing)
        ("sophie_page", "grimoires_history_davies", "SCHOLAR_OF"),
    ]

    for person_id_str, text_id_str, role in person_text_links:
        p = pid(person_id_str)
        t = tid(text_id_str)
        if p and t:
            conn.execute(
                "INSERT OR IGNORE INTO person_text_roles (person_id, text_id, role) VALUES (?,?,?)",
                (p, t, role),
            )
        else:
            print(f"  WARN: cannot link {person_id_str} -> {text_id_str} ({role}): p={p}, t={t}")

    concept_text_links = [
        # Renaissance Magic concept
        ("renaissance_magic", "de_occulta_philosophia"),
        ("renaissance_magic", "giordano_bruno_hermetic_yates"),
        ("renaissance_magic", "transformations_of_magic"),
        ("renaissance_magic", "occult_philosophy_elizabethan_yates"),
        ("renaissance_magic", "spiritual_demonic_magic_walker"),
        # Hermeticism
        ("hermeticism", "corpus_hermeticum_latin"),
        ("hermeticism", "giordano_bruno_hermetic_yates"),
        ("hermeticism", "de_vita_coelitus_comparanda"),
        # Prisca Theologia
        ("prisca_theologia", "corpus_hermeticum_latin"),
        ("prisca_theologia", "oration_dignity_man"),
        # Magia Naturalis
        ("magia_naturalis_concept", "magia_naturalis"),
        ("magia_naturalis_concept", "de_vita_coelitus_comparanda"),
        ("magia_naturalis_concept", "de_occulta_philosophia"),
        # Yates Thesis
        ("yates_thesis", "giordano_bruno_hermetic_yates"),
        ("yates_thesis", "occult_philosophy_elizabethan_yates"),
        ("yates_thesis", "transformations_of_magic"),
        ("yates_thesis", "spiritual_demonic_magic_walker"),
        # Occult Philosophy
        ("occult_philosophy", "de_occulta_philosophia"),
        ("occult_philosophy", "fourth_book_occult_philosophy"),
        ("occult_philosophy", "the_magus_barrett"),
        # Grimoire Printing History
        ("grimoire_printing_history", "grimoires_history_davies"),
        ("grimoire_printing_history", "clavicula_salomonis"),
        ("grimoire_printing_history", "fourth_book_occult_philosophy"),
        ("grimoire_printing_history", "arbatel_de_magia_veterum"),
        # Vernacular Grimoire
        ("vernacular_grimoire_tradition", "book_of_oberon_edition"),
        ("vernacular_grimoire_tradition", "making_magic_elizabethan"),
        ("vernacular_grimoire_tradition", "magic_of_rogues"),
        ("vernacular_grimoire_tradition", "discoverie_of_witchcraft"),
        # Neoplatonism and Magic
        ("neoplatonism_and_magic", "de_vita_coelitus_comparanda"),
        ("neoplatonism_and_magic", "corpus_hermeticum_latin"),
        ("neoplatonism_and_magic", "spiritual_demonic_magic_walker"),
        # Enochian
        ("enochian_system", "mysteriorum_libri"),
        ("enochian_system", "sworn_book_of_honorius"),
        ("enochian_system", "ars_notoria"),
        # Print Culture
        ("print_culture_and_magic", "grimoires_history_davies"),
        ("print_culture_and_magic", "steganographia"),
        ("print_culture_and_magic", "de_occulta_philosophia"),
        # Kabbalism
        ("kabbalism_renaissance_magic", "oration_dignity_man"),
        ("kabbalism_renaissance_magic", "de_occulta_philosophia"),
        ("kabbalism_renaissance_magic", "monas_hieroglyphica"),
        # Spiritual Magic
        ("spiritual_magic_walker", "spiritual_demonic_magic_walker"),
        ("spiritual_magic_walker", "de_vita_coelitus_comparanda"),
        ("spiritual_magic_walker", "magia_naturalis"),
        # Reformation and Magic
        ("reformation_and_magic", "discoverie_of_witchcraft"),
        ("reformation_and_magic", "de_praestigiis_daemonum"),
        ("reformation_and_magic", "arbatel_de_magia_veterum"),
        # Rosicrucian
        ("rosicrucian_movement", "de_occulta_philosophia"),
        ("rosicrucian_movement", "grimoires_history_davies"),
    ]

    for slug, text_id_str in concept_text_links:
        c = cid(slug)
        t = tid(text_id_str)
        if c and t:
            conn.execute(
                "INSERT OR IGNORE INTO concept_text_refs (concept_id, text_id) VALUES (?,?)",
                (c, t),
            )
        else:
            print(f"  WARN: cannot link concept {slug} -> text {text_id_str}: c={c}, t={t}")

    concept_concept_links = [
        # Renaissance magic relates to many
        ("renaissance_magic", "learned_magic", "RELATED"),
        ("renaissance_magic", "medieval_magic", "CONTRASTED"),
        ("renaissance_magic", "yates_thesis", "RELATED"),
        ("renaissance_magic", "hermeticism", "RELATED"),
        ("renaissance_magic", "occult_philosophy", "RELATED"),
        # Hermeticism
        ("hermeticism", "prisca_theologia", "RELATED"),
        ("hermeticism", "neoplatonism_and_magic", "RELATED"),
        ("hermeticism", "yates_thesis", "RELATED"),
        # Prisca Theologia
        ("prisca_theologia", "hermeticism", "PART_OF"),
        ("prisca_theologia", "neoplatonism_and_magic", "RELATED"),
        # Yates Thesis
        ("yates_thesis", "renaissance_magic", "RELATED"),
        ("yates_thesis", "hermeticism", "PART_OF"),
        # Magia Naturalis
        ("magia_naturalis_concept", "natural_powers", "RELATED"),
        ("magia_naturalis_concept", "occult_properties", "RELATED"),
        ("magia_naturalis_concept", "astral_image_magic", "RELATED"),
        # Occult Philosophy
        ("occult_philosophy", "renaissance_magic", "PART_OF"),
        ("occult_philosophy", "learned_magic", "RELATED"),
        # Grimoire Printing
        ("grimoire_printing_history", "grimoire_corpus", "RELATED"),
        ("grimoire_printing_history", "print_culture_and_magic", "RELATED"),
        ("grimoire_printing_history", "vernacular_grimoire_tradition", "RELATED"),
        # Print Culture
        ("print_culture_and_magic", "grimoire_printing_history", "RELATED"),
        ("print_culture_and_magic", "manuscript_miscellany", "CONTRASTED"),
        # Enochian
        ("enochian_system", "angelic_invocation", "RELATED"),
        ("enochian_system", "ars_notoria", "RELATED"),
        # Spiritual Magic
        ("spiritual_magic_walker", "astral_image_magic", "RELATED"),
        ("spiritual_magic_walker", "magia_naturalis_concept", "RELATED"),
        ("spiritual_magic_walker", "demonic_pact", "CONTRASTED"),
        # Neoplatonism
        ("neoplatonism_and_magic", "hermeticism", "RELATED"),
        ("neoplatonism_and_magic", "renaissance_magic", "RELATED"),
        # Kabbalism
        ("kabbalism_renaissance_magic", "occult_philosophy", "PART_OF"),
        ("kabbalism_renaissance_magic", "renaissance_magic", "PART_OF"),
        # Reformation
        ("reformation_and_magic", "witchcraft", "RELATED"),
        ("reformation_and_magic", "condemned_arts", "RELATED"),
        # Rosicrucian
        ("rosicrucian_movement", "hermeticism", "RELATED"),
        ("rosicrucian_movement", "renaissance_magic", "RELATED"),
        # Vernacular grimoire
        ("vernacular_grimoire_tradition", "grimoire_corpus", "RELATED"),
        ("vernacular_grimoire_tradition", "grimoire_printing_history", "RELATED"),
    ]

    for from_slug, to_slug, rel in concept_concept_links:
        f = cid(from_slug)
        t_c = cid(to_slug)
        if f and t_c:
            conn.execute(
                "INSERT OR IGNORE INTO concept_links (from_concept_id, to_concept_id, relationship) VALUES (?,?,?)",
                (f, t_c, rel),
            )
        else:
            print(f"  WARN: cannot link concept {from_slug} -> {to_slug}: f={f}, t={t_c}")

    conn.commit()
    print("Seeded relationships.")


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    print("=== Grimoires in Reception: Seeding Section ===")
    migrate_schema(conn)
    seed_persons(conn)
    seed_texts(conn)
    seed_concepts(conn)
    seed_timeline_events(conn)
    seed_relationships(conn)

    # Summary
    for tbl in ["texts", "persons", "concepts", "timeline_events"]:
        n = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  {tbl}: {n}")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()

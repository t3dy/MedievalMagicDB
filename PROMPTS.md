# MedievalMagicDB: Canonical Vision and Prompts

MedievalMagicDB adapts the EmeraldTablet knowledge-portal framework to the scholarly study of medieval magic. Its model is critical, historical, and provenance-aware, drawing on the standards of Richard Kieckhefer, Claire Fanger, Frank Klaassen, Sophie Page, Michael D. Bailey, Catherine Rider, and related historians of religion, manuscript culture, learned magic, and the occult sciences.

## What This Portal Is

MedievalMagicDB is a digital reference portal for medieval magic scholarship. It organizes persons, texts, concepts, manuscripts, bibliography, and timeline events into a relational browsing system. Its purpose is to help users move from a concept such as `ars notoria` to textual witnesses, from a text such as the `Picatrix` to modern scholarship, and from a scholar such as Richard Kieckhefer to the primary sources and debates associated with his work.

The long-term goal is exhaustive scholarly coverage. The database should not stop at the authors of the PDFs. It should include every scholar of medieval magic named in the corpus, every known grimoire and ritual-text family relevant to medieval or medieval-reception traditions, every medieval philosopher, theologian, physician, astrologer, or encyclopedist who commented on magic or adjacent categories, every attributed authority such as Solomon, Raziel, Honorius, or Theysolius, and every historiographical concept needed to make the field intelligible.

## What This Portal Is Not

It is not an instruction manual for magical practice. It is not a New Age or occult promotional site. It is not a Wikipedia mirror. It does not flatten medieval ritual, natural philosophy, divination, image magic, demonic magic, charms, prayer, and ecclesiastical polemic into one undifferentiated category.

## Core Categories

Persons include historical actors, attributed authors, compilers, translators, editors, and modern scholars.

Texts include primary sources, grimoire materials, manuscript compilations, modern editions, scholarship, articles, and reviews.

Concepts include actor terms and analyst terms. Actor terms are words used by medieval or early modern actors. Analyst terms are categories used by modern scholars.

Bibliography records preserve the PDF corpus and future source provenance.

Coverage must distinguish period and evidentiary status. Early modern grimoires that receive medieval materials belong in the portal, but they must be marked as early modern. Pseudepigraphic, biblical, angelic, and legendary authorities belong in `persons` only with clear evidentiary descriptions.

## Corpus Discovery Workflow

After each new source-folder conversion, run `scripts/discover_corpus_candidates.py`. The generated `CORPUS_DISCOVERY.md` and `staging/corpus_discovery_candidates.json` are not final scholarship; they are lexical maps of the corpus. Use them to decide which dictionary entries, biographies, text summaries, concept links, and timeline events should be expanded first.

Current corpus signals show that the project is not merely a general medieval magic portal. It is especially strong in learned ritual magic, manuscript miscellanies, angelic invocation, astral image magic, necromancy or `nigromantia`, divination, clerical and monastic contexts, and the modern historiography of manuscript-based magic.

Priority text entries include `Ars Notoria`, `Picatrix`, `Speculum astronomiae`, `Liber Razielis`, `De imaginibus`, `De radiis`, `Forbidden Rites`, `Sworn Book of Honorius`, `Liber Theysolius`, `Magic in Medieval Manuscripts`, `Unlocked Books`, and `Hazards of the Dark Arts`.

Priority biography entries include Claire Fanger, Richard Kieckhefer, Sophie Page, Frank Klaassen, Jean-Patrice Boudet, Nicolas Weill-Parot, Julien Veronese, David Pingree, Lynn Thorndike, Benedek Lang, John of Morigny, Johannes Hartlieb, Solomon, Raziel, Albertus Magnus, Roger Bacon, Michael Scot, Theysolius, and Honorius of Thebes.

Priority dictionary entries include ritual magic, image magic, learned magic, natural magic, necromancy, `nigromantia`, familiar spirit, manuscript miscellany, clerical underworld, angelic invocation, demonic pact, divination, geomancy, chiromancy, charms, amulets, talismans, suffumigation, characters and seals, `voces magicae`, ritual purity, condemned arts, witchcraft, and `maleficium`.

Comprehensive grimoire and ritual-text coverage should include, at minimum, the Ars Notoria, Liber Juratus Honorii or Sworn Book of Honorius, Liber Razielis, Picatrix, Clavicula Salomonis, Hygromanteia, Testament of Solomon, Liber de angelis, Liber visionum, Flowers of Heavenly Teaching, Munich Manual, Book of Oberon, Book of Soyga, Heptameron, Ars Almadel, Ars Paulina, Ars Goetia, Lemegeton, Grimorium Verum, Sixth and Seventh Books of Moses, Liber Lunae, De radiis, De imaginibus, and Speculum astronomiae. This list is a floor, not a ceiling.

Comprehensive philosophical and theological coverage should include Roger Bacon, Albertus Magnus, Thomas Aquinas, William of Auvergne, Augustine, Isidore of Seville, John of Salisbury, Nicole Oresme, Pietro d'Abano, Arnald of Villanova, al-Kindi, Abu Ma'shar, Michael Scot, Cecco d'Ascoli, and other thinkers whose works classify, defend, criticize, or naturalize magic and adjacent arts.

Comprehensive scholar coverage should include not only authors of local PDFs but scholars mentioned by them: David Pingree, Valerie Flint, Robert Mathiesen, Jan R. Veenstra, Charles Burnett, Paola Zambelli, Agostino Paravicini Bagliani, Don C. Skemer, Lea T. Olsan, Katelyn Mesler, Florence Chave-Mahir, Béatrice Delaurenti, Jean-Patrice Boudet, Nicolas Weill-Parot, Julien Véronèse, and future names discovered in the corpus.

## Agent Output Pattern

All substantial content drafts should be written first as JSON under `staging/`, then loaded by scripts. Agents should not write directly to the SQLite database unless they are the main session running an idempotent script.

## Minimum Entry Standards

Dictionary entries require a short index definition and a long encyclopedia entry. Biographies and text pages require sustained prose with literature sections. All claims must be traceable to named sources. No stubs, placeholders, hashtags, raw markdown, or decorative symbols belong in database prose fields.

## Entry-Type Prompts

Dictionary writers must begin by identifying the term's category as Actor Term, Analyst Term, or Hybrid. They must then explain what kind of evidence supports the term: medieval usage, modern historiography, manuscript convention, theological polemic, legal accusation, or editorial shorthand. The entry should make classification part of the argument rather than hiding it.

Historical-biography writers must distinguish documented persons from attributed, legendary, biblical, angelic, or pseudepigraphic authorities. John of Morigny, Johannes Hartlieb, Albertus Magnus, Roger Bacon, and Michael Scot require different evidentiary treatment from Solomon, Raziel, Theysolius, or Honorius of Thebes.

Scholar-biography writers must foreground method. A scholar entry should answer: What archive or corpus did this scholar make visible? What category did they revise? What earlier model did they challenge? How do their works help users understand texts, concepts, or manuscripts in the portal?

Text-summary writers must identify whether the text is a primary source, ritual book, manuscript compilation, edition, translation, monograph, article, or review. Primary-source entries must treat manuscript transmission as central. Modern-scholarship entries must explain argument, method, and field impact.

Timeline writers must avoid bare publication notices. Each event should explain why the date matters for medieval magic as a history of transmission, institutional classification, manuscript survival, polemic, or historiography.

## Exhaustiveness Rule

When a source names a grimoire, scholar, historical actor, attributed authority, manuscript family, or historiographical category, the default assumption is that the portal needs an entry. If the entry is too uncertain for full prose, create a DRAFT seed with explicit uncertainty rather than omitting it. The database is allowed to mark uncertainty; it is not allowed to hide the research trail.

## Relational Completeness Rule

An entry is not considered properly seeded until it has at least one meaningful relationship and major entries should have several. Run `scripts/seed_relationships_and_coverage_audit.py` after expansion passes. `COVERAGE_AUDIT.md` should list no isolated persons, texts, or concepts. If a newly discovered entity cannot yet be linked, write a note explaining what evidence is missing and what source should be checked next.

## Depth and Enrichment Rule

The portal distinguishes three states: seeded, relationally connected, and encyclopedia-ready. Seeded entries may have short descriptions, but encyclopedia-ready entries need the full style-guide structures and literature sections. After expansion passes, run `scripts/audit_content_depth.py` and `scripts/build_enrichment_queue.py`. The next writing work should usually begin with `ENRICHMENT_QUEUE.md`, while still allowing human judgment to raise entries of strategic importance.

## Grimoires in Reception Section

Added May 2026. The portal now includes a dedicated section — accessible at `reception.html` — covering the Renaissance and early modern reception of medieval grimoires. The section is seeded by `scripts/seed_reception_section.py` and appears in the navigation as "Reception."

### What the section covers

1. **Ficinian synthesis (c.1460-1500)**: Marsilio Ficino's Latin translation of the Corpus Hermeticum (1463), his *De Vita Coelitus Comparanda* (1489), and the Neoplatonist-Hermetic framework for Renaissance natural magic.

2. **Pico, Agrippa, Trithemius (1480-1535)**: Giovanni Pico della Mirandola's synthesis of Kabbalah and natural magic (1486); Cornelius Agrippa's *De Occulta Philosophia* (manuscript c.1510, print 1531-1533); Johannes Trithemius's library-building at Sponheim and *Steganographia* (c.1499, print 1606).

3. **Dee and Elizabethan magic (1558-1600)**: John Dee's Mortlake library, angel conversations with Kelley (1582-1589), *Mysteriorum Libri Quinque*; the Enochian system's relationship to medieval angelic magic traditions.

4. **The Yates thesis and its revision**: Frances Yates's *Giordano Bruno and the Hermetic Tradition* (1964) and related works argue for a clean break between medieval demonic magic and Renaissance Hermetic-natural magic. D.P. Walker's *Spiritual and Demonic Magic* (1958) provides the nuanced framework. Frank Klaassen's *Transformations of Magic* (2013) challenges Yates directly with manuscript evidence showing strong continuity of medieval ritual magic through the sixteenth century. Every reception entry should position itself in this debate.

5. **Printing press and grimoire circulation (1471-1800)**: The impact of print on grimoire transmission from Ficino's Pimander (1471) through Agrippa's De Occulta Philosophia (1531), the Arbatel and Fourth Book of Occult Philosophy (c.1559), Trithemius's Steganographia (1606), the French popular grimoire tradition (Grand Albert, Petit Albert, Dragon Rouge, c.1750-1800), and Francis Barrett's *The Magus* (1801).

6. **Modern editorial tradition (1888-present)**: Samuel Liddell MacGregor Mathers's editions (1888-1904), Joseph Peterson's Esoteric Archives (1995-present) and critical editions (Lesser Key 2001, Grimorium Verum 2007, Mysteriorum Libri 2003), Dan Harms and Peterson's *Book of Oberon* (2015), Owen Davies's *Grimoires: A History* (2009).

### Priority entries for expansion

The following reception entries are seeded as DRAFT and should be expanded to encyclopedia length in order of scholarly importance:

**Texts**: De Occulta Philosophia (most important), De Vita Coelitus Comparanda, Corpus Hermeticum translation, Mysteriorum Libri Quinque, Giordano Bruno and the Hermetic Tradition (Yates), Spiritual and Demonic Magic (Walker), Grimoires: A History (Davies).

**Persons**: Marsilio Ficino, John Dee, Cornelius Agrippa, Frances Yates, D.P. Walker, Joseph Peterson.

**Concepts**: Yates Thesis (most historiographically important), Renaissance Magic, Hermeticism, Grimoire Printing History.

### Key sources in the Markdown corpus

- `frank-klaassen-the-transformations-of-magic-illicit-learned-magic-in-the-later-middle-ages-and-r.md` — Chapter 7 (pp. 187-218) is the primary scholarly source for the medieval-Renaissance continuity argument.
- `frank-klaassen-making-magic-in-elizabethan-england-two-early-modern-vernacular-books-of-magic-pe.md` — critical edition of Elizabethan vernacular magic manuscripts.
- `joseph-h-peterson-dan-harms-book-of-magic-with-instructions-for-invoking-spirits-1-1-libgen-li.md` — Peterson/Harms edition with scholarly introduction.
- `joseph-h-peterson-grimorium-verum-createspace.md` — Peterson's Grimorium Verum edition.
- `joseph-h-peterson-the-lesser-key-of-solomon.md` — Peterson's Lesser Key edition.
- `the-magic-of-rogues-necromancers-in-early-tudor-england-penn-state-university-press.md` — Klaassen/Wright on early Tudor magic.

## DjVu Conversion Rule

DjVu files may contain embedded `TXTz` text chunks. Those chunks use DjVuLibre BZZ compression, which is not decodable by Python's standard library or the current PyMuPDF build. If DjVuLibre tools such as `djvutxt` become available, the converter should ingest DjVu text directly. Until then, DjVu records must remain in the bibliography with `unsupported` status and a note identifying the BZZ text-layer blocker.

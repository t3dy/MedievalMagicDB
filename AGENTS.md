# Codex Instructions - MedievalMagicDB

## Mandatory First Steps

1. Read `PROMPTS.md` in full.
2. Read `STYLEGUIDE.md` in full.
3. Preserve the EmeraldTablet architecture: SQLite, idempotent Python scripts, staged JSON enrichment, static HTML output.
4. Treat every substantive scholarly claim as provenance-bound. Name the source in prose or in the bibliography record.

## Project Mission

MedievalMagicDB is an authoritative scholarly reference portal for medieval magic and its manuscript, institutional, and historiographical contexts. It is not an occult manual, a devotional resource, or a how-to site. It is a critical history portal for scholars, students, and serious independent researchers.

The portal's coverage ambition is comprehensive. It should eventually contain entries for every known medieval and medieval-reception grimoire, every major ritual text, every medieval philosopher or theologian who commented substantively on magic, astrology, divination, demons, occult properties, or superstition, every scholar of medieval magic mentioned in the corpus, every historical or attributed figure attached to magical texts, and every historiographical concept needed to navigate the field.

## Current Phase

Corpus conversion, scholarly expansion, and Reception section development:

1. Convert the source PDFs to Markdown for token-efficient ingestion.
2. Seed the database with bibliography records for the corpus.
3. Search the Markdown corpus for recurring topics, texts, scholars, historical figures, and historiographical concepts.
4. Seed candidates as dictionary entries, biographies, text summaries, concept links, and timeline events before full encyclopedia prose is written.
5. Generate the static website viewer and validate links.
6. **Reception section (added May 2026)**: A dedicated section covering the Renaissance and early modern reception of medieval grimoires. Seeded by `scripts/seed_reception_section.py`. Navigable at `reception.html`. Contains 65 cards (30 texts, 20 persons, 15 concepts) and 34 geo-coded timeline events. Style requirements in STYLEGUIDE.md § Reception Section. Key historiographical debate: Yates thesis (clean medieval/Renaissance break) vs. Klaassen continuity argument.

### Reception Section: Key Schema Notes

`timeline_events` now has `location TEXT`, `latitude REAL`, `longitude REAL` columns added by migration in `seed_reception_section.py`. The `init_db.py` schema has been updated to include these columns in new installations. All timeline events in the reception section carry geo-coordinates for the map display on `reception.html`.

Reception page generation is handled by `generate_reception()` in `deploy_portal.py`. The function filters by `period IN ('RENAISSANCE','EARLY_MODERN')` for texts/persons, by specific text_ids for modern scholarship, and by explicit slug sets for concepts. The function also queries for modern scholars linked to reception-section texts via `person_text_roles`.

### Reception Section: Enrichment Priorities

All 65 reception section cards are currently DRAFT status. Priority expansion order:

1. **Yates Thesis** concept (definition_long: 1,500-2,500 words) — most historiographically important entry in the section
2. **Marsilio Ficino** biography (bio_html: 1,200-2,200 words) — foundational figure
3. **De Occulta Philosophia** text summary (analysis_html: 900-2,500 words)
4. **John Dee** biography — best-documented Renaissance magical practitioner
5. **Grimoire Printing History** concept — links medieval manuscript and modern print traditions
6. **Renaissance Magic** concept — anchor for the section's historiographical frame

## Architecture

SQLite -> Python scripts -> static HTML/CSS/JS -> `docs/` and `site/`.

Key paths:

`db/medieval_magic.db`
`scripts/init_db.py`
`scripts/convert_pdfs_to_md.py`
`scripts/seed_from_manifest.py`
`scripts/discover_corpus_candidates.py`
`scripts/seed_expansion_candidates.py`
`scripts/seed_comprehensive_coverage.py`
`scripts/seed_relationships_and_coverage_audit.py`
`scripts/audit_content_depth.py`
`scripts/build_enrichment_queue.py`
`scripts/deploy_portal.py`
`sources/markdown/`
`sources/metadata/pdf_manifest.json`
`CORPUS_DISCOVERY.md`
`COVERAGE_AUDIT.md`
`CONTENT_DEPTH_AUDIT.md`
`ENRICHMENT_QUEUE.md`

## Historiographical Principles

Medieval magic is an analyst category. Historical actors used terms such as `nigromantia`, `ars notoria`, `scientia imaginum`, `experimentum`, `incantatio`, `sortilegium`, `maleficium`, and `superstitio`. Do not collapse those actor terms into a single timeless thing called magic.

Clerical, legal, and scholastic sources often describe practices polemically. Distinguish prescription, accusation, confession, manuscript evidence, and later editorial reconstruction.

The boundary between religion and magic is historically variable. Avoid treating ecclesiastical condemnation as transparent description.

The learned magical corpus is manuscript-based. Transmission history, codicology, language, and compilation context matter as much as doctrine.

Primary texts and modern scholarship must be kept separate.

Comprehensive does not mean indiscriminate. Early modern grimoires such as the Lemegeton, Heptameron, Book of Oberon, Grimorium Verum, or Book of Soyga belong in the portal when they preserve, reorganize, or receive medieval ritual traditions. They must be marked as EARLY_MODERN, not silently medievalized.

## Corpus-Derived Priority Areas

The current Markdown corpus strongly foregrounds the following areas and they should guide the next enrichment passes:

Texts: `Ars Notoria`, `Picatrix`, `Speculum astronomiae`, `Liber Razielis`, `De imaginibus`, `Forbidden Rites`, `Sworn Book of Honorius`, `De radiis`, `Liber Theysolius`, `Unlocked Books`, `Magic in Medieval Manuscripts`, `Hazards of the Dark Arts`.

Scholars: Claire Fanger, Richard Kieckhefer, Sophie Page, Frank Klaassen, Jean-Patrice Boudet, David Pingree, Nicolas Weill-Parot, Julien Veronese, Lynn Thorndike, Michael D. Bailey, Catherine Rider, Benedek Lang.

Historical and attributed figures: Solomon, John of Morigny, Albertus Magnus, Raziel, Roger Bacon, Thabit ibn Qurra, Michael Scot, Theysolius, Johannes Hartlieb, Apollonius of Tyana, Cecco d'Ascoli, Honorius of Thebes, Ulrich Molitor.

Concepts: ritual magic, image magic, witchcraft, necromancy, divination, natural magic, charms, characters and seals, talismans, learned magic, `notae`, superstition, amulets, confession, astral magic, exorcism, geomancy, chiromancy, `nigromantia`, suffumigation, clerical underworld, familiar spirit, `maleficium`, ritual purity, demonic pact, `voces magicae`.

## Comprehensive Coverage Mandate

Every expansion pass should ask five questions:

1. Which grimoires or ritual texts are missing?
2. Which medieval thinkers commented on magic, astrology, demons, divination, occult properties, natural powers, or superstition?
3. Which modern scholars are mentioned in the corpus but absent from `persons`?
4. Which historical, biblical, angelic, legendary, or attributed figures authorize texts or practices?
5. Which historiographical concepts are needed to explain how scholars classify the evidence?

The answer should become database seeds or staged JSON, not merely notes. No major entry should be a dead end: connect it to at least three persons, texts, concepts, timeline events, or bibliography records whenever the evidence permits.

After any seed expansion, run `scripts/seed_relationships_and_coverage_audit.py`. `COVERAGE_AUDIT.md` must show no isolated persons, texts, or concepts unless the isolation is explicitly justified in prose.

Relational coverage is not the same thing as content depth. Run `scripts/audit_content_depth.py` and `scripts/build_enrichment_queue.py` after major corpus expansion. Use `ENRICHMENT_QUEUE.md` to choose the next encyclopedia-length entries, prioritizing high corpus frequency and field importance.

## Vocabulary Lock

Enum values are defined in `scripts/init_db.py`. Do not invent new values without changing schema, seed scripts, deploy filters, and validation together.

## Entry Authoring Contracts

Dictionary entries must declare Actor Term, Analyst Term, or Hybrid in the first paragraph. They must include historical usage, scholarly significance, related concepts, and literature. Major concepts should be 1,500-2,500 words; narrower technical entries may be shorter but must not become stubs.

Historical figure biographies must state evidentiary status. Do not treat attributed authorities, biblical figures, angels, or pseudepigraphic names as ordinary documented authors. Always distinguish authorship, attribution, reception, and textual authority.

Scholar biographies must explain method and historiographical intervention, not just list publications. Each scholar page should say how the scholar changed the study of medieval magic.

Text summaries must distinguish primary source, manuscript compilation, modern edition, translation, article, monograph, and review. For primary and ritual texts, manuscript transmission and classification are required sections. For modern scholarship, argument and method are required sections.

Timeline entries must name date, place when known, actors or texts, evidence type, and significance. They must be plain text and 100-250 words.

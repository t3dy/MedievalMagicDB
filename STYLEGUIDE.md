# MedievalMagicDB Content Style Guide

MedievalMagicDB follows the EmeraldTablet style discipline: scholarly encyclopedia prose, valid HTML in long fields, plain text in short fields, and explicit provenance. The model is the best historical scholarship on medieval magic: Richard Kieckhefer on necromantic manuals and the clerical underworld, Claire Fanger on ritual magic and visionary practice, Frank Klaassen on manuscript transmission and learned magic, Sophie Page on codicology and monastic/clerical contexts, Michael D. Bailey on religion, superstition, and demonology, Benedek Lang on Central European manuscript libraries, Nicolas Weill-Parot and Jean-Patrice Boudet on astral image theory and learned divination, and Lynn Thorndike as an older but still indispensable documentary map.

The style mandate serves a comprehensive portal, not a selective essay collection. Entries should be created for canonical grimoires, obscure manuscript families, philosophical commentators, scholastic critics, modern scholars, legendary authorities, and historiographical concepts whenever they are relevant to medieval magic or its reception.

## Prose Fields

`bio_html`, `analysis_html`, and `definition_long` use valid HTML with `<p>`, `<h2>`, and `<i>` tags. Do not use Markdown bullets, hashtags, placeholder text, raw square-bracket citation artifacts, or decorative symbols.

`description` and `definition_short` are plain text only. They should be compact encyclopedia prose, not teaser copy.

## Scholarly Values

Write as a critical historian. Distinguish actor terms from analyst terms. Never write as if "magic" were a timeless object with fixed content. Identify whether a claim comes from a manuscript, a clerical polemic, a legal record, an edition, or modern scholarship.

For medieval magic specifically, never let modern umbrella terms erase medieval classifications. Define `nigromantia`, `superstitio`, `experimentum`, `ars`, `scientia`, `notae`, `voces magicae`, `maleficium`, and related actor terms in their own settings before comparing them with analyst terms such as learned magic, ritual magic, grimoire, clerical underworld, image magic, or manuscript miscellany.

When writing about texts, distinguish the surviving manuscript or edition from the ritual procedures described inside it. A manuscript may preserve prayers, diagrams, characters, seals, suffumigations, spirit names, and timings without proving that every procedure was performed exactly as copied.

When writing about accusations, trial records, demonology, or anti-magical advice literature, mark the evidentiary register clearly. Confession, polemic, pastoral warning, princely advice, university condemnation, and ritual manuscript are different kinds of evidence.

## Absolute Prohibitions

Do not include ritual instructions in a performative, operational, or how-to register. It is acceptable to describe a text's contents historically, but do not convert scholarly description into practical guidance.

Do not write confessional or promotional prose. Avoid phrases such as "powerful ritual," "effective spell," "real magic," or "ancient secrets" unless quoting or analyzing a source's rhetoric.

Do not collapse Christian prayer, angelic invocation, astral image practice, demonic conjuration, charms, medicine, divination, and witchcraft into a single undifferentiated "magic" category.

Do not treat manuscript titles as stable modern books without noting compilation, attribution, recension, and manuscript variance.

Do not omit uncertainty. If authorship, date, title, manuscript family, or textual boundary is debated, say so clearly.

## Dictionary Entries

Dictionary entries have two levels.

`definition_short` is 70-130 words of plain text. It must identify whether the term is an Actor Term, Analyst Term, or Hybrid; give the linguistic or historiographical setting; and state why the term matters for medieval magic scholarship.

`definition_long` is 1,500-2,500 words of HTML prose for major entries and 900-1,400 words for narrow technical entries. Use this structure:

`<p>` Opening definition. Begin with the term itself. State actor/analyst status explicitly and give the term's language, earliest secure context, or modern scholarly origin.

`<h2>Historical Usage</h2>` Explain how the term or practice appears in medieval sources. Name specific texts, manuscripts, genres, authorities, or institutional settings. For actor terms, privilege medieval usage before modern interpretation.

`<h2>Scholarly Significance</h2>` Name the scholars who have shaped the category. Explain specific arguments and disagreements, especially Kieckhefer on clerical ritual magic, Fanger on ritual and visionary practice, Klaassen on manuscript transformation, Page on codicology, Bailey on superstition and demonology, Boudet and Weill-Parot on astrology and image magic, and Lang on library contexts when relevant.

`<h2>Transmission and Variant Forms</h2>` Use for terms with Latin, vernacular, Arabic, Hebrew, Greek, or modern scholarly variants. Explain shifts such as necromancy/nigromantia, image/talisman, ars/scientia, grimoire/manuscript miscellany.

`<h2>Related Concepts</h2>` Write prose that links to 3-5 related concepts. Do not make a bare list.

`<h2>Literature</h2>` Include 8-15 bibliographic entries for major concepts and at least 5 for narrow concepts.

Dictionary entries should make classification itself part of the story. For example, an entry on necromancy should explain the mismatch between modern "necromancy," medieval `nigromantia`, and clerical/demonological classification.

## Biographies: Historical Figures

Historical figure biographies use `bio_html` and should be 1,200-2,200 words for major figures and 700-1,100 words for minor or attributed figures.

Opening paragraph: identify dates or floruit, region, role, and evidentiary status. State whether the figure is historical, attributed, legendary, biblical, angelic, or textually constructed. Do not write Solomon, Raziel, Honorius of Thebes, or Theysolius as though their portal role were identical to a documented medieval author.

Required sections:

`<h2>Sources and Historical Setting</h2>` Explain the evidence: manuscripts, printed editions, legal records, theological references, or scholarly reconstruction.

`<h2>Texts and Attributions</h2>` Name works associated with the figure and distinguish authorship from attribution, reception, compilation, or pseudepigraphy.

`<h2>Significance for Medieval Magic</h2>` Explain why the figure matters for ritual authority, manuscript transmission, astral theory, demonology, divination, learned practice, or historiography.

`<h2>Reception and Scholarly Debate</h2>` Use for major figures. Identify how modern scholars interpret the figure and where uncertainty remains.

`<h2>Literature</h2>` Include primary editions and modern scholarship.

## Biographies: Modern Scholars

Scholar biographies use `bio_html` and should be 1,200-2,000 words for major scholars and 700-1,100 words for narrower figures.

Opening paragraph: identify the scholar's field, institutional or disciplinary setting when known, and their central contribution to medieval magic studies. Do not turn the biography into a CV.

Required sections:

`<h2>Central Contribution</h2>` State the scholar's distinctive intervention. For example, Kieckhefer's clerical underworld, Fanger's ritual and visionary framing, Klaassen's manuscript transformations, Page's codicological contexts, Bailey's religion/superstition framework, Lang's Central European library evidence, Weill-Parot's image-magic distinctions, or Thorndike's long history of magic and science.

`<h2>Key Works</h2>` Discuss 2-5 works by title and date. Explain what each contributes to the portal's ontology.

`<h2>Method and Historiographical Position</h2>` Explain whether the scholar works through manuscript studies, intellectual history, religious history, codicology, philology, legal history, demonology, or history of science.

`<h2>Influence and Debate</h2>` Situate the scholar among related scholars and disagreements. Avoid vague praise.

`<h2>Literature</h2>` Include their major works and significant responses or related scholarship.

## Text Summaries

Text entries use `analysis_html`. Primary source, manuscript compilation, edition, and scholarship entries have different emphases.

Opening paragraph: title in `<i>` tags, date or date range, language, text type, and evidentiary status. State whether the entry covers a medieval text, a manuscript compilation, a modern edition, or a modern scholarly monograph.

For primary sources and ritual/manuscript texts:

`<h2>Content and Structure</h2>` Describe the text's contents historically without providing operational instructions. Name prayers, diagrams, spirits, images, seals, suffumigations, celestial timings, or divisions only as evidence of genre and doctrine.

`<h2>Transmission and Manuscript Context</h2>` Identify manuscripts, recensions, languages, attributions, compilations, or editorial histories when known. Codicological context is central, not decorative.

`<h2>Classification and Controversy</h2>` Explain how the text was classified: natural, astral, demonic, devotional, superstitious, experimental, or learned.

`<h2>Modern Scholarship</h2>` Name editors, translators, and major interpreters.

`<h2>Literature</h2>` Include editions, translations, and scholarship.

For modern scholarship:

`<h2>Argument</h2>` State the book or article's main thesis.

`<h2>Sources and Method</h2>` Explain the evidentiary base: manuscripts, trials, catalogues, scholastic texts, editions, or historiographical synthesis.

`<h2>Impact on the Field</h2>` Explain what database categories, entries, or debates the work supports.

`<h2>Literature</h2>` Include the work itself and related works.

## Grimoire and Ritual-Text Entries

Every known grimoire or ritual-text family should eventually have an entry, including medieval texts and early modern receptions of medieval material. A grimoire entry must not become a ritual recipe. It should explain title instability, attribution, manuscript families, language, relation to other grimoires, ritual genre, scholarly editions, and reception.

Required grimoire sections:

`<h2>Textual Identity and Attribution</h2>` Explain names, pseudepigraphy, attributed authorities, language, and date range.

`<h2>Contents and Ritual Genres</h2>` Describe the types of material historically: angelic invocation, spirit catalogues, seals, notae, suffumigations, planetary timing, prayers, or exorcistic formulae. Do not provide instructions.

`<h2>Manuscripts and Reception</h2>` Identify known manuscript or print contexts and whether the text is medieval, early modern, or a reception of medieval material.

`<h2>Scholarly Significance</h2>` Explain how scholars use the text to understand learned magic, Solomonic authority, ritual secrecy, codicology, demonology, astral magic, or vernacular transmission.

## Timeline Events

Timeline `description` fields are 100-250 words, plain text only. Each event must include date or date range, place when known, named actors or texts, evidentiary basis, and historiographical significance.

A good timeline event does not merely say a book was written. It explains why that event changes transmission, classification, manuscript circulation, institutional condemnation, or modern scholarship.

Use approximate dates honestly: `c. 1250-1300`, `late fifteenth century`, or `before 1456` are better than false precision.

## Literature Sections

Use full bibliography in prose fields. Author surname first. Book titles in `<i>` tags. Article titles in quotation marks. Include place, publisher, year, and page ranges when available.

Never use "ibid." Do not use naked URLs as substitutes for bibliographic data.

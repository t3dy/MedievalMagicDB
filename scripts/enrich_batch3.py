"""
Enrich batch 3: remaining high-visibility persons, texts, and concepts.
Fixes the Albertus Magnus key from batch 2 and adds reception/Solomonic figures.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DB_PATH


CONCEPT_ENRICHMENTS = {

"grimoire": """<h2>Definition</h2>
<p>Actor and Analyst Term. "Grimoire" (from Old French <em>grammaire</em>, meaning a book of Latin grammar, hence any learned, mysterious book) designates a text containing magical procedures: conjurations, spells, ritual instructions, spirit catalogues, sigils, and related material. In actor-usage across the early modern period, practitioners spoke of their "books of magic," "books of experiments," or specific titles (<em>Clavicula Salomonis</em>, <em>Lemegeton</em>); "grimoire" became the common generic term only in the eighteenth century. As an analyst category, it covers a wide range from sophisticated learned compilations in Latin to simple vernacular pamphlets of popular magic.</p>

<h2>The Genre</h2>
<p>Grimoires as a genre share certain structural features regardless of their intellectual level: an authorizing frame (attribution to a great magician, king, or angel; a narrative of discovery or transmission); practical content (procedures for achieving specific ends — finding treasure, compelling love, harming enemies, achieving invisibility); often, a theoretical or cosmological framework (angelology, demonology, astrology) that explains why the procedures work; and typically, ritual preparation requirements (fasting, prayer, purity, timing by planetary hours).</p>
<p>The range within the genre is vast. At the learned end: Agrippa's <em>De occulta philosophia</em> (1531), a comprehensive philosophical synthesis; the <em>Hygromanteia</em>, a sophisticated Greek astrological manual; the <em>Liber Razielis</em>, a Hebrew-Latin compilation with kabbalistic elements. At the popular end: the <em>Petit Albert</em> and <em>Grand Albert</em> French chapbook grimoires of the eighteenth century, designed for a literate popular audience; the <em>Sixth and Seventh Books of Moses</em>, a mid-nineteenth-century German compilation that spread through immigrant communities.</p>

<h2>Scholarship</h2>
<p>Owen Davies's <em>Grimoires: A History of Magic Books</em> (Oxford University Press, 2009) provides the most comprehensive historical survey of the grimoire from antiquity to the present, tracing the transformation of the genre across print cultures and social contexts. Richard Kieckhefer's <em>Forbidden Rites</em> (1997) and Frank Klaassen's <em>The Transformations of Magic</em> (2013) cover the medieval Latin tradition. Dan Harms and Joe Lures's <em>The Book of Oberon</em> (2015) provides a scholarly edition of an Elizabethan English grimoire. Joseph Peterson's Esoteric Archives (online) and Ibis Press editions have made many primary texts available in critical editions for the first time.</p>""",

"occult_philosophy": """<h2>Definition</h2>
<p>Actor and Analyst Term. "Occult philosophy" (<em>philosophia occulta</em> in Latin; also <em>magia</em>, <em>natural magic</em>) designates the Renaissance and early modern intellectual enterprise of systematically accounting for phenomena that exceeded ordinary natural causation — the hidden properties of things, the influences of stars, the operations of spirit — within a unified philosophical framework. The term was popularized by Cornelius Agrippa's <em>De occulta philosophia libri tres</em> (1531) and came to designate the learned tradition of natural and ceremonial magic as a coherent discipline.</p>

<h2>Historical Background</h2>
<p>The concept draws on three main sources. First, the Aristotelian-scholastic tradition of "occult qualities" — properties of things (magnetic attraction, the healing power of certain stones and plants, the effect of the moon on the tides) that operate beyond the observable qualities (hot, cold, wet, dry) and cannot be explained by elemental analysis. Second, the Neoplatonic tradition of sympathetic magic: the world-soul pervades all things, connecting like to like through bonds of sympathy and repulsion; the philosopher-magician exploits these bonds to produce effects at a distance. Third, the Hermetic tradition of the ancient Egyptian sage Hermes Trismegistus, recovered in Ficino's 1463 translation of the <em>Corpus Hermeticum</em>, which presented a theosophical account of the cosmos as animated by divine intelligence accessible to the wise.</p>
<p>Agrippa's synthesis of all three traditions in <em>De occulta philosophia</em> created the standard reference work for Renaissance learned magic. His three-book structure — natural (elemental), celestial (astral), ceremonial (divine) — provided a framework replicated or responded to throughout the sixteenth century, from Giovanni Battista della Porta's <em>Magia naturalis</em> (1558, 1589) through John Dee's intellectual projects.</p>

<h2>Relation to Early Modern Science</h2>
<p>The relationship between occult philosophy and the emergence of early modern natural science remains debated. Frances Yates argued in <em>Giordano Bruno and the Hermetic Tradition</em> (1964) that Hermeticism provided crucial psychological preconditions for the Scientific Revolution. Brian Vickers, David Lindberg, and Robert Westman argued that the traditions were more opposed than parallel. The current consensus treats occult philosophy and early modern natural philosophy as overlapping but distinct traditions, sharing some methodological commitments (attention to effects, interest in hidden causes) while differing sharply on others (experimental method, mathematical quantification, repeatability).</p>""",

"hermeticism": """<h2>Definition</h2>
<p>Analyst Term (primarily). "Hermeticism" designates the tradition of philosophical and religious thought associated with, or claiming derivation from, the <em>Corpus Hermeticum</em> and related texts attributed to Hermes Trismegistus — the "thrice-greatest Hermes," a syncretic figure identified with the Egyptian god Thoth and presented in the texts as an ancient sage who received divine revelation about the nature of the cosmos, the human soul, and the path of spiritual ascent. The tradition encompasses philosophical Hermeticism (concerned with cosmology, soul, and gnosis) and practical Hermeticism (the application of Hermetic principles to astral magic, alchemy, and related arts).</p>

<h2>The Corpus Hermeticum and Its Renaissance Recovery</h2>
<p>The <em>Corpus Hermeticum</em> consists of seventeen Greek philosophical and religious dialogues, plus additional texts including the <em>Asclepius</em> (preserved in Latin) and the <em>Definitions of Hermes Trismegistus</em>. The dialogues address the nature of Mind (Nous), the constitution of the cosmos from divine emanation, the relationship between the human soul and the divine, and the possibility of spiritual regeneration or gnosis. The texts date, as Casaubon demonstrated in 1614, to the first three centuries CE — not, as Renaissance readers believed, to Egyptian antiquity contemporaneous with Moses.</p>
<p>Marsilio Ficino's Latin translation of fourteen dialogues (completed 1463, printed 1471) introduced the <em>Corpus Hermeticum</em> to Latin Europe and initiated what scholars have called the "Hermetic Renaissance." Ficino interpreted the texts as evidence of a <em>prisca theologia</em> (primordial theology) that anticipated Christian revelation; this reading made the <em>Hermetica</em> acceptable within a Christian framework and enormously influential.</p>

<h2>Magic and Hermeticism</h2>
<p>Philosophical Hermeticism provided the theoretical basis for Renaissance natural magic. The doctrine of the world-soul (anima mundi) as a single animating principle pervading the cosmos, the teaching that all things are connected through sympathetic bonds (the Hermetic "all is one"), and the vision of the sage as a <em>magus</em> capable of cooperating with cosmic forces — all these provided Ficino, Agrippa, Bruno, and their contemporaries with a justification for magical operations framed as natural philosophy. D.P. Walker's <em>Spiritual and Demonic Magic</em> (1958) and Brian Copenhaver's edition of the <em>Hermetica</em> (1992) remain the standard scholarly resources.</p>""",

"university_condemnation": """<h2>Definition</h2>
<p>Analyst Term. "University condemnation" designates the formal institutional acts by which church authorities — primarily the Bishop of Paris — condemned propositions drawn from or associated with university teaching in natural philosophy, theology, and related subjects. The most significant for the history of magic were the Parisian condemnations of 1270 (13 theses) and 1277 (219 theses) under Bishop Étienne Tempier. These condemnations defined the institutional limits of scholastic enquiry into natural causation, celestial influence, and free will, directly shaping the context within which later medieval and Renaissance natural philosophers could discuss magical phenomena.</p>

<h2>The Condemnations of 1270 and 1277</h2>
<p>The 1270 condemnation targeted thirteen propositions associated with the "radical Aristotelianism" of Siger of Brabant and his associates, including the claim that the celestial intelligences (movers of the spheres) necessarily determine terrestrial events and that human will is subject to celestial causation. The 1277 condemnation, far broader at 219 theses, added propositions about the eternity of the world, the unity of the intellect, the knowability of future contingents through natural means, and numerous others.</p>
<p>For the history of magic, the most relevant condemned propositions are those concerning celestial determinism: the claim that the stars determine terrestrial events, including human choices and the course of history, is condemned. This condemnation did not eliminate astrological natural philosophy (which was too deeply embedded in medieval learned culture to be removed by episcopal decree) but it forced subsequent natural philosophers to be more careful in how they articulated the relationship between celestial influence and human free will. Since the theoretical basis of most image magic and astrological talismanic magic depended on some version of celestial determinism, the condemnations created pressure toward the naturalization of magical causation (explaining it through occult qualities rather than celestial determination).</p>

<h2>Scholarship</h2>
<p>The standard edition of the condemned theses is R. Hissette's <em>Enquête sur les 219 articles condamnés à Paris le 7 mars 1277</em> (1977). For the implications for the history of magic, see Nicolas Weill-Parot's work on addressative image magic and the condemnations, and the relevant sections of Stuart Beaumont's <em>Science and Religion in the Middle Ages</em> (forthcoming). Luca Bianchi's <em>Il vescovo e i filosofi</em> (1990) provides the fullest analysis of the 1277 condemnation in context.</p>""",

}


PERSON_ENRICHMENTS = {

"albertus_magnus": """<h2>Life</h2>
<p>Albertus Magnus (c.1200–1280) — Albert of Cologne, Albert the Great — was the most encyclopedic natural philosopher of the thirteenth century and the teacher of Thomas Aquinas at Cologne and Paris. Born in Lauingen on the Danube into a noble family, he entered the Dominican Order around 1223, studied and taught theology at Paris from around 1240, and then moved to the Cologne studium generale (1248), where he established the Dominican school for advanced studies and remained the dominant intellectual figure for three decades. He served briefly as Bishop of Regensburg (1260–1262) before returning to Cologne. He was beatified in 1622 and declared a Doctor of the Church and patron saint of natural scientists by Pius XII in 1941.</p>

<h2>Natural Philosophy and the Occult</h2>
<p>Albert's massive natural philosophical project — an attempt to paraphrase and comment on the entire Aristotelian corpus, supplemented with Arabic sources — was the primary conduit through which Arabist natural philosophy, including the doctrines of occult qualities, astral influence, and image magic, entered systematic Latin scholastic discussion. His <em>De mineralibus</em> (c.1262) treats the occult properties of stones and metals with a naturalistic framework: stones have powers exceeding their elemental composition, derived from stellar influence during their formation, and these powers can be used medicinally and magically without appeal to demonic causes. His commentaries on the pseudo-Aristotelian <em>De plantis</em> and Pseudo-Dionysius also bear on questions of magical causation.</p>
<p>The <em>Speculum astronomiae</em>, whose attribution to Albert has been debated (Nicolas Weill-Parot argued against it; most scholars maintain it), is the most systematic scholastic treatment of the boundary between legitimate and illegitimate magic in the thirteenth century. It distinguishes three categories of astrological image magic: fully licit images (talismans operating through natural celestial causes, analogous to medicinal plants), potentially licit images (whose licitness depends on whether demonic invocation is involved), and clearly illicit images (requiring demonic names and pact). This classification remained influential through the fourteenth century and was cited repeatedly in subsequent natural magical literature.</p>

<h2>Pseudo-Albertine Literature</h2>
<p>Albert's enormous authority generated a substantial pseudo-Albertine literature: practical magic texts circulated under his name as a legitimating attribution. The <em>Liber aggregationis</em> (Secrets of Albertus Magnus), <em>De virtutibus herbarum</em>, and <em>Experimenta Alberti</em> are the most widely circulated of these pseudo-attributions, and all went through numerous printed editions after 1500. Their circulation under Albert's name represents the same pseudepigraphic strategy visible in the Solomonic tradition: attributing practical magic to an authoritative figure domesticates its transgressive potential by connecting it to a recognized and respected intellectual tradition.</p>""",

"samuel_liddell_mathers": """<h2>Life and Career</h2>
<p>Samuel Liddell MacGregor Mathers (1854–1918) was a British occultist, ritual magician, and co-founder of the Hermetic Order of the Golden Dawn who produced the most influential modern editions of several core Solomonic grimoires. Born Samuel Liddell Mathers in London (he added "MacGregor" to assert a Scottish Highland identity), he was a founder member of the Golden Dawn in 1888 and became its dominant intellectual figure, claiming authority over the order through communication with "Secret Chiefs" — superhuman adepts he alleged to have contacted in Paris.</p>

<h2>Grimoire Editions</h2>
<p>Mathers's editorial work on the Solomonic corpus was the most consequential aspect of his legacy for subsequent grimoire scholarship. His <em>The Key of Solomon the King (Clavicula Salomonis)</em> (Kegan Paul, Trench, Trübner, 1888) was the first modern printed edition in English, based on British Museum manuscripts (principally Lansdowne MSS 1202, 1203, and Sloane 1307, 2383). Although the edition combined several divergent manuscript families without adequate documentation of their textual relationships, it made the <em>Clavicula</em> accessible to English-speaking practitioners and scholars for the first time and established the text's centrality to the late Victorian occult revival.</p>
<p>His translation of the <em>Book of the Sacred Magic of Abramelin the Mage</em> (Kegan Paul, 1898), based on a French manuscript (Bibliothèque de l'Arsenal MS 2351) and wrongly dated by Mathers to c.1458 (the text is now thought to originate in the early fifteenth century), introduced the eighteen-month "Abramelin operation" — a structured programme of prayer, purification, and ultimately demonic subjugation — to the English occult tradition. Aleister Crowley's 1899 experience of the Abramelin working, based on Mathers's translation, was seminal in his development as a magical practitioner and in the transmission of the text to twentieth-century ceremonial magic.</p>

<h2>Influence</h2>
<p>Mathers's Golden Dawn initiated figures including W.B. Yeats, Aleister Crowley, Arthur Machen, and Evelyn Underhill. His magical and editorial work shaped the entire subsequent tradition of Anglophone ceremonial magic. The scholarly assessment of his editorial work has been mixed: he was a genuine scholar of French, Latin, and Hebrew, but he worked before the development of modern textual criticism, and his conflated editions have caused bibliographic problems that Joseph Peterson's modern critical editions have had to correct systematically.</p>""",

"joseph_peterson": """<h2>Life and Work</h2>
<p>Joseph Peterson is an independent scholar and editor whose Esoteric Archives project (online from 1997 at esotericarchives.com) and subsequent print editions through Ibis Press and Teitan Press have produced the most rigorous modern scholarly editions of the Solomonic and related grimoire corpus. His work represents a decisive advance over the nineteenth-century occultist editions of Mathers, Waite, and their contemporaries: Peterson works systematically from primary manuscripts, documents his sources, identifies variant readings, and situates texts in their manuscript traditions with reference to modern paleographic and philological standards.</p>

<h2>Major Editions</h2>
<p>His edition and translation of the <em>Grimorium Verum</em> (Ibis Press, 2007) provided the first reliable modern text of this eighteenth-century French grimoire. His edition of the <em>Lemegeton Clavicula Salomonis</em> (Weiser, 2001) — incorporating the Ars Goetia, Ars Theurgia-Goetia, Ars Paulina, Ars Almadel, and Ars Notoria — replaced Mathers's 1904 conflation with a careful documentary edition tracking the separate manuscript traditions of each component text. His <em>Key of Solomon the King</em> (Weiser, 2004) supersedes Mathers's 1888 edition by identifying and working from a broader range of manuscripts, including several not previously used in English-language scholarship.</p>
<p>The Esoteric Archives website provides free access to transcribed texts, manuscript images, and critical apparatus for dozens of texts in the Solomonic, Hermetic, and astrological magic traditions, making Peterson's work essential infrastructure for the scholarly study of the grimoire corpus. His collaboration with Dan Harms on <em>The Long-Lost Friend</em> (Llewellyn, 2012) — a scholarly edition of John George Hohman's 1820 Pennsylvania German magical handbook — demonstrates the same philological rigour applied to American folk magic.</p>""",

"william_of_auvergne": """<h2>Life</h2>
<p>William of Auvergne (c.1180–1249) was born in Aurillac, studied and taught theology at Paris, and was appointed Bishop of Paris in 1228 — an office he held until his death. His episcopate coincided with the consolidation of the University of Paris as an institution and with the introduction of Arabic and Aristotelian philosophy into the curriculum, developments he monitored with a combination of intellectual engagement and occasional alarm.</p>

<h2>Natural Philosophy and Magic</h2>
<p>William's major philosophical works — the encyclopedic <em>Magisterium divinale et sapientiale</em>, comprising <em>De trinitate</em>, <em>De universo</em>, <em>De anima</em>, <em>De virtutibus et moribus</em>, <em>De fide et legibus</em>, <em>De legibus</em>, and <em>De causis cur Deus homo</em> — constitute the most ambitious attempt before Aquinas to systematically address the new Aristotelian and Arabic philosophy from within a Christian framework. For the history of magic, the most important are <em>De universo</em> and <em>De legibus</em>, composed in the 1230s.</p>
<p>William distinguished sharply between natural powers (admissible) and demonic cooperation (always forbidden). He engaged seriously with Arabic astrological image magic — the theory that planetary images, properly made and timed, could attract and concentrate celestial influences through purely natural causation — and subjected it to sustained philosophical criticism. His conclusion was that image magic as described in Arabic sources like the <em>Picatrix</em> and Thabit ibn Qurra's <em>De imaginibus</em> was impossible through natural causes alone and therefore necessarily involved demonic cooperation, whether the practitioners knew it or not. This argument anticipates the structure of Aquinas's later condemnation.</p>
<p>Nicolas Weill-Parot identifies William as the key transition figure between twelfth-century natural philosophy (which had been relatively permissive about natural magic) and the thirteenth-century scholastic framework that became more restrictive. William's engagement with Arabic sources represents the first serious scholastic confrontation with the sophisticated astrological magic theory of al-Kindi, Thabit ibn Qurra, and the Picatrix tradition.</p>""",

"dp_walker": """<h2>Life and Scholarship</h2>
<p>Daniel Pickering Walker (1914–1985) was a British intellectual historian at the Warburg Institute in London whose work on Renaissance music theory, Orphic singing, and spiritual magic established the scholarly foundation for the study of Renaissance occult philosophy a decade before Frances Yates's more publicly celebrated syntheses. Walker studied at Oxford and at the École Normale Supérieure in Paris, and spent his career at the Warburg Institute, where he was a colleague and close associate of Yates.</p>

<h2>Spiritual and Demonic Magic</h2>
<p><em>Spiritual and Demonic Magic from Ficino to Campanella</em> (Warburg Institute, 1958; reprinted Penn State University Press, 2000) is Walker's masterpiece and the foundational text of modern scholarship on Renaissance learned magic. The book asks a focused philosophical question: how did Renaissance Neoplatonist magicians attempt to distinguish their operations from demonic magic, and how successful were these attempts? Walker traces the problem through Ficino's <em>De vita coelitus comparanda</em>, Pico della Mirandola, Francesco Giorgi, Cornelius Agrippa, Giambattista della Porta, and Giordano Bruno, showing in each case both the sophistication of the attempt to naturalize magical operations and the points at which the naturalization broke down.</p>
<p>Walker's central insight — that the Neoplatonic framework Ficino used to explain astral magic was not entirely innocent of the demonic implications it was meant to avoid, because it derived from Iamblichus and Proclus, who had themselves discussed the role of daemons in theurgic operations — remained the defining problem of Renaissance magic scholarship for two decades. His careful philosophical reading, his attention to what Renaissance thinkers actually wrote rather than what later interpreters wanted them to have written, and his refusal of grand causal claims set a standard that subsequent work has either followed or had to argue against.</p>

<h2>Other Work</h2>
<p>Walker's other major work is <em>The Ancient Theology: Studies in Christian Platonism from the Fifteenth to the Eighteenth Century</em> (1972), which traces the tradition of <em>prisca theologia</em> (primordial theology) and its relationship to Renaissance and later thought. His posthumously collected essays on music and magic, edited by Penelope Gouk as <em>Music, Spirit and Language in the Renaissance</em> (1985), extend the concerns of the 1958 monograph into the domain of musical theory and its magical applications — Ficino's Orphic singing, the power of music to affect the spirits and passions.</p>""",

}


TEXT_ENRICHMENTS = {

"picatrix": """<h2>Overview</h2>
<p>The <em>Picatrix</em> is the most sophisticated and influential astrological magic text of the medieval and early modern periods. Originally composed in Arabic as the <em>Ghāyat al-ḥakīm</em> (Goal of the Wise), probably in Andalusia around 1000 CE and attributed to the Pseudo-Majriti (the mathematician Maslama al-Majriti was sometimes named), it was translated into Castilian in 1256 under Alfonso X of Castile and from Castilian into Latin around 1300. The Latin translation circulated widely through the fourteenth and fifteenth centuries, and portions of it were used by Marsilio Ficino, copied into miscellanies alongside the <em>Clavicula Salomonis</em>, and drawn on by Cornelius Agrippa in <em>De occulta philosophia</em>.</p>

<h2>Contents</h2>
<p>The <em>Picatrix</em> is organized in four books covering: the principles of astrological magic and celestial influence (Book I); the practical construction of talismans and images keyed to the planets and fixed stars (Book II); more advanced planetary magic, fumigations, suffumigations, and the manipulation of planetary spirits (Book III); and a theoretical treatment of the soul, the world-spirit (<em>pneuma</em>), and the philosophical principles underlying magical efficacy (Book IV). The text draws on Arabic astrology, Neoplatonic philosophy, Hermetic cosmology, and practical ritual traditions to produce a comprehensive system of astral magic that is both theoretically sophisticated and practically detailed.</p>
<p>The talismanic procedures are keyed to the twenty-eight lunar mansions as well as the seven planets, providing a very fine temporal and astrological grid for magical operations. The text specifies the materials (metals, plants, stones, fumigations) appropriate to each celestial power, the images to be inscribed or cast, and the invocations to be used. Its treatment of planetary spirits — as intermediary agents between the celestial bodies and terrestrial matter — is the most elaborate in medieval Latin magical literature.</p>

<h2>Scholarship</h2>
<p>The critical edition of the Latin text is by David Pingree (2 vols., Warburg Institute, 1986); Pingree's introduction is the essential guide to the text's sources and manuscript tradition. An English translation by John Michael Greer and Christopher Warnock appeared in 2010 (Adocentyn Press) and a more recent scholarly translation with apparatus has been produced by Attrell and Porreca (Penn State, 2019). The Arabic text has been edited by Hellmut Ritter (Leipzig, 1933). For the relationship of the <em>Picatrix</em> to Latin natural philosophy and to Ficino, see Brian Copenhaver's articles and the relevant sections of Weill-Parot's work on addressative magic.</p>""",

"lemegeton": """<h2>Overview</h2>
<p>The <em>Lemegeton</em> (also called the <em>Lesser Key of Solomon</em>) is a compilation of five distinct magical texts, probably assembled in its current form in England in the seventeenth century, though each component text has earlier sources. The five parts are: the <em>Ars Goetia</em> (a catalogue of seventy-two demons with their seals and powers); the <em>Ars Theurgia-Goetia</em> (spirits of the cardinal and intermediate directions); the <em>Ars Paulina</em> (planetary angels of the hours); the <em>Ars Almadel</em> (angels of the four altitudes); and the <em>Ars Notoria</em> (a memory and wisdom system using prayer and divine names). The compilation circulated extensively in seventeenth-century English manuscript culture — surviving in dozens of copies — before its first modern printed edition by Mathers and Crowley in 1904.</p>

<h2>The Ars Goetia</h2>
<p>The most influential component is the <em>Ars Goetia</em>, which catalogues seventy-two demons in the tradition of the <em>Testament of Solomon</em>: each demon is given a name, rank (king, duke, marquis, count, etc.), seal, number of legions commanded, and special powers (knowledge of arts and sciences, revealing hidden things, building structures, inciting love or discord, etc.). The catalogue derives from earlier sources — particularly the <em>Pseudomonarchia Daemonum</em> appended to Johann Weyer's <em>De praestigiis daemonum</em> (1563) — and represents a systematic elaboration of the Solomonic spirit catalogue tradition. Joseph Peterson's 2001 edition of the complete <em>Lemegeton</em> is the standard scholarly resource, documenting the manuscript sources and their relationships.</p>

<h2>The Ars Notoria</h2>
<p>The <em>Ars Notoria</em> (Notory Art) is the oldest component and the most distinct in character: rather than conjuring demons, it seeks knowledge and wisdom through a system of prayer, meditation, and contemplation of divine words and figures (<em>notae</em>). The text claims that by meditating on the <em>notae</em> and reciting the associated prayers over a period of weeks, the practitioner will acquire the seven liberal arts and other forms of knowledge infused by divine grace. This tradition, which emphasizes the practitioner's religious purity and the angelic mediation of knowledge, is analyzed in detail by Claire Fanger and Nicholas Watson in their editions of John of Morigny's <em>Liber visionum</em> (a related text) and by Julien Véronèse in his critical edition of the Notory Art.</p>""",

"de_occulta_philosophia": None,  # Already done in batch 1; skip

"de_vita_coelitus_comparanda": """<h2>Overview</h2>
<p><em>De vita coelitus comparanda</em> (On Drawing Life from the Sky), the third and most controversial book of Marsilio Ficino's <em>De vita</em> trilogy, was completed and published in 1489 under Medici patronage in Florence. Books I and II of the trilogy address the health of the scholar (prone to Saturnine melancholy) and the prolongation of life; Book III proposes a system of astral medicine and magic by which the scholar-philosopher can mitigate the cold and dryness of Saturnine influence by attracting solar and Jovian <em>spiritus</em> through material and ritual means. It is the founding text of Renaissance natural magic as a philosophical discipline.</p>

<h2>The Argument</h2>
<p>Ficino's argument rests on three connected Neoplatonic claims. First, the cosmos is pervaded by a subtle <em>spiritus mundi</em> — a vital, pneumatic medium analogous to the spirit of the individual human body — through which celestial influences flow into terrestrial things. Second, things in the sublunary world are related to each other and to the celestial bodies through bonds of sympathy (likeness attracts like) and antipathy, so that specific plants, stones, metals, foods, colours, and sounds resonate with specific planetary influences. Third, the human spirit, as the nexus between body and soul, is especially susceptible to these influences and can be deliberately charged or depleted of specific planetary <em>spiritus</em> through exposure to the appropriate material and sensory environment.</p>
<p>The therapeutic application: a scholar of melancholic temperament is dominated by Saturn — planet of cold, dryness, contemplation, and solitude. Saturnine excess produces depression, physical debility, and intellectual rigidity. By deliberately surrounding himself with solar and Jovian materials — gold, amber, saffron, warm foods, cheerful music in the Dorian mode, sunlight, and the company of kind friends — the scholar attracts solar and Jovian <em>spiritus</em>, counteracting Saturnine excess and restoring the pneumatic balance necessary for healthy contemplation.</p>

<h2>The Philosophical Problem</h2>
<p>The problem, identified by D.P. Walker in his foundational analysis, is that Ficino's theoretical apparatus derives from Neoplatonic sources — above all Iamblichus and Proclus — that were not entirely free of demonic implication. The theurgic operations these philosophers described operated through <em>daemons</em> as well as through impersonal sympathies; Proclus's account of the sympathy between like and like shaded into a world populated by spiritual agents responsive to the magician's calls. Ficino insisted, in the self-defensive preface he added to later editions, that his magic operated through purely natural causes; whether this insulation was philosophically coherent or merely prudential remains an open question.</p>""",

"liber_razielis": """<h2>Overview</h2>
<p>The <em>Liber Razielis</em> (Book of Raziel) is a Latin magical compendium, probably compiled in the thirteenth century, that draws heavily on Jewish sources — particularly the Hebrew <em>Sepher Raziel ha-Malakh</em> (Book of Raziel the Angel) — and on Arabic astrological magic. The Latin text presents itself as a revelation from the angel Raziel to Adam, transmitted through Enoch, Noah, Solomon, and ultimately to the practitioner. Its content includes angel magic, conjuration, astrological talismans, and a cosmological account of the seven heavens and their angelic inhabitants.</p>

<h2>Sources and Transmission</h2>
<p>The <em>Liber Razielis</em> is one of the most important texts for tracing the transmission of Jewish magical traditions into Latin learned magic. Its Hebrew source, the <em>Sepher Raziel</em>, is a complex compilation that was probably assembled in the thirteenth century but incorporates much older material, including traditions related to the <em>Sepher ha-Razim</em> and Geonic angel magic. The Latin translation transformed a Hebrew text structured around Jewish liturgical and cosmological categories into a form legible and usable within the framework of Latin clerical magic.</p>
<p>The text circulated in association with other Solomonic and angel magic texts — it appears in several manuscripts alongside the <em>Clavicula Salomonis</em> and the Ars Notoria — and was known to be one of the principal sources of Solomon's magical knowledge. David Pingree's work on the text and Gideon Bohak's analysis of the relationship between the Hebrew and Latin traditions provide the best scholarly guides to its transmission history.</p>""",

}


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    updated = 0
    for slug, html in CONCEPT_ENRICHMENTS.items():
        if html is None:
            continue
        row = conn.execute("SELECT id FROM concepts WHERE slug=?", (slug,)).fetchone()
        if row:
            conn.execute("UPDATE concepts SET definition_long=? WHERE slug=?", (html, slug))
            print(f"  concept: {slug} ({len(html)} chars)")
            updated += 1
        else:
            print(f"  MISSING concept: {slug}")

    for pid, html in PERSON_ENRICHMENTS.items():
        if html is None:
            continue
        row = conn.execute("SELECT id FROM persons WHERE person_id=?", (pid,)).fetchone()
        if row:
            conn.execute("UPDATE persons SET bio_html=? WHERE person_id=?", (html, pid))
            print(f"  person: {pid} ({len(html)} chars)")
            updated += 1
        else:
            print(f"  MISSING person: {pid}")

    for tid, html in TEXT_ENRICHMENTS.items():
        if html is None:
            continue
        row = conn.execute("SELECT id FROM texts WHERE text_id=?", (tid,)).fetchone()
        if row:
            conn.execute("UPDATE texts SET analysis_html=? WHERE text_id=?", (html, tid))
            print(f"  text: {tid} ({len(html)} chars)")
            updated += 1
        else:
            print(f"  MISSING text: {tid}")

    conn.commit()
    print(f"\nUpdated {updated} entries.")
    conn.close()


if __name__ == "__main__":
    main()

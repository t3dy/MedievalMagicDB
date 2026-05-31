"""
Enrich batch 4: remaining persons, texts, and concepts for all three sections.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DB_PATH


CONCEPT_ENRICHMENTS = {

"demonic_pact": """<h2>Definition</h2>
<p>Actor and Analyst Term. The demonic pact (<em>pactum cum daemone</em> in Latin; <em>pacte diabolique</em> in French) designates an explicit or implicit agreement between a human being and a demon or the Devil, by which the demon provides services (knowledge, power, material goods, protection) in exchange for the human's submission, worship, or soul. The concept was a cornerstone of medieval and early modern demonological theory, and its application — identifying whether a given magical practice constituted implicit pact — was the central analytical tool through which theologians and inquisitors assessed the moral status of magic.</p>

<h2>Theological Development</h2>
<p>Augustine of Hippo provided the earliest systematic account of the demonic pact: demons, he argued in <em>De civitate Dei</em> and <em>De divinatione daemonum</em>, respond to human invocation not because they are compelled by magical art but because they desire the worship of human beings diverted from God to themselves. Any consultation of demons — even when framed as a purely technical operation (astrological, divinatory, healing) — involves an implicit compact with beings hostile to human salvation. This framework made the question of pact structural rather than simply intentional: even if the practitioner did not intend to worship a demon, the operation of demonic magic presupposed demonic cooperation that was itself a form of forbidden commerce.</p>
<p>Thomas Aquinas refined this analysis in <em>Summa theologiae</em> II-II, qq. 92–96, developing the distinction between explicit pact (in which the practitioner consciously invokes a demon and requests its service) and implicit pact (in which the practitioner uses means that cannot work through natural causes and therefore presuppose demonic assistance, whether or not the practitioner recognizes this). The concept of implicit pact enormously extended the domain of potentially illicit magic: it meant that any operation using non-natural means (special words, characters, names, images without naturalistic causal explanation) was potentially pactual.</p>

<h2>Witch Trials and the Sabbath</h2>
<p>The fifteenth-century elaboration of the witches' sabbath added a new dimension: the explicit collective demonic pact, renewed at nocturnal assemblies, through which the witch renounced Christianity and submitted body and soul to the Devil. The <em>Malleus Maleficarum</em> (1486) provided the standard account: the witch makes an explicit pact with the devil, submitting to sexual intercourse with him and receiving in return the power to harm neighbours through maleficia. This version of the pact is a judicial-theological construct rather than simply a theological category, built up through confession (often under torture) and codified in the witch-trial literature of the fifteenth and sixteenth centuries.</p>

<h2>Scholarship</h2>
<p>Richard Kieckhefer's <em>Magic in the Middle Ages</em> (1989) provides the clearest account of the pact concept in medieval learned discourse. Stuart Clark's <em>Thinking with Demons</em> (1997) analyses it within the broader system of early modern demonological thought. Michael Bailey's <em>Battling Demons</em> (2003) traces the emergence of the sabbath construct in the fifteenth century.</p>""",

"astral_image_magic": """<h2>Definition</h2>
<p>Analyst Term. Astral image magic designates procedures in which an image — typically a figure sculpted in metal, wax, or another material — is created and consecrated under specific astrological conditions (appropriate planetary hour, sign, and configuration) in order to attract and concentrate the influence of a celestial body and direct it toward a practical end. The image functions as a material focal point for stellar power: its form, material, timing, and associated ritual (fumigation, prayer, inscription of divine or stellar names) constitute a complete technology of celestial mediation.</p>

<h2>Sources</h2>
<p>Astral image magic in medieval Latin culture derived primarily from Arabic sources translated in the twelfth century: al-Kindi's <em>De radiis</em> (On Rays), Thabit ibn Qurra's <em>De imaginibus</em> (On Images), and the <em>Picatrix</em> (Arabic <em>Ghāyat al-ḥakīm</em>). These texts provided the theoretical apparatus (stellar rays as the medium of celestial influence) and the practical instructions (which planets govern which operations, which materials and images are appropriate, which prayers and fumigations attract planetary spiritus). The <em>Picatrix</em> in particular — a vast compilation organized around the twenty-eight lunar mansions and seven planets — became the most comprehensive resource for astral image magic in the Latin learned tradition.</p>

<h2>The Scholastic Problem</h2>
<p>Astral image magic posed a specific and persistent problem for scholastic natural philosophy. If the images worked through purely natural celestial causes — attracting and concentrating stellar influence in the way a lens concentrates light — they were potentially licit: natural philosophy could study and even use natural forces without moral hazard. But if they required the invocation of planetary spirits as personal, rational agents — or if the inscribed names and characters had no natural basis but presupposed demonic assistance — they were operations of demonic magic condemned by Aquinas and canon law.</p>
<p>Nicolas Weill-Parot's concept of "addressative magic" (<em>magie addressative</em>), developed in his <em>Les "images astrologiques" au Moyen Âge et à la Renaissance</em> (2002), captures this distinction: magic is addressative when it explicitly addresses (speaks to, invokes, commands) spiritual agents as personal beings, rather than simply exploiting impersonal natural forces. Weill-Parot's argument is that the scholastic condemnation of image magic targeted specifically the addressative dimension, and that the naturalization strategies of Albertus Magnus and others were attempts to preserve image magic by removing or minimizing its addressative character.</p>""",

"necromancy": """<h2>Definition</h2>
<p>Actor Term (historical) and Analyst Term. In its ancient Greek and Roman usage, necromancy (<em>nekromanteia</em>, divination through the dead) designated rituals for consulting the ghosts of the dead, either at their tombs or by summoning them to appear. In medieval Latin usage, <em>nigromantia</em> (often etymologized as "black art" rather than "death-divination") designated demonic conjuration more broadly — the ritual summoning and commanding of demons — regardless of whether the dead were involved. This semantic shift is itself historically significant: medieval learned magicians who practised demonic conjuration called themselves and were called <em>nigromancers</em>.</p>

<h2>Medieval Nigromancy</h2>
<p>Richard Kieckhefer's analysis of the Munich Manual of demonic magic (<em>Forbidden Rites</em>, 1997) provides the most detailed account of what medieval Latin nigromancy actually involved. The Munich Manual (Clm 849, copied c.1440s) is a practical handbook containing illusionist tricks, love magic, and demonic conjuration proper. The conjuration procedures involve: ritual preparation (fasting, prayer, inscribing a circle), the conjuration formula (invoking divine names and the demon's name to compel appearance), interrogation of the demon, and dismissal. The spirits summoned are not ghosts of the dead but demons — fallen angels — whose hierarchy mirrors the celestial hierarchy of the Solomonic tradition.</p>
<p>The social world of medieval nigromancy, as Kieckhefer analyzes it, was what he calls the "clerical underworld": learned clergymen and university graduates who possessed the Latin literacy necessary to use the manuscripts but whose social position (often minor clergy without secure benefices) left them in economic and social vulnerability that made magical services attractive. Frank Klaassen's systematic survey of English magical manuscripts confirms and refines this picture.</p>

<h2>Later Survival</h2>
<p>Necromantic procedure — in the older, specifically dead-summoning sense — enjoyed a revival in the Spiritualist movement of the nineteenth century and its derivatives. The late antique <em>Necyomantia</em> tradition, which involved summoning the spirits of the dead at tombs or crossroads, persisted in folk practice and in literary imagination (the Witch of Endor, Lucan's Erictho) long after it ceased to be a living learned practice. Owen Davies's <em>The Haunted: A Social History of Ghosts</em> (2007) provides context for the persistence of ghost-consultation in popular magical practice.</p>""",

"divination": """<h2>Definition</h2>
<p>Actor and Analyst Term. Divination (from Latin <em>divinare</em>, to foresee, from <em>divinus</em>, divine) designates the attempt to obtain knowledge of hidden, remote, or future events through means other than ordinary sensory experience or rational inference. The category encompasses an enormous range of practices — astrology, geomancy, chiromancy, oneiromancy (dream interpretation), pyromancy, hydromancy, sortilege (casting lots), augury, and consultation of spirits — united by the claim to access knowledge unavailable to ordinary human faculties.</p>

<h2>Theological Status</h2>
<p>Christian theology took a consistently negative view of divination, on grounds established by Augustine and systematized by Thomas Aquinas. The argument proceeded through several steps: hidden knowledge belongs ultimately to God; creatures (stars, lots, demons) can at best provide signs, not genuine foreknowledge; any appeal to creatures for knowledge that only God possesses constitutes idolatry or demonic pact; ergo all divinatory practices are illicit. This condemnation was nuanced by allowances for natural prognostication through legitimate causal reasoning (the physician who predicts the patient's death from natural signs, the meteorologist who forecasts storms from atmospheric conditions) but these allowances were carefully limited to what natural causes could genuinely produce.</p>
<p>Astrology was the most contested case. Medieval astrologers and their scholastic supporters argued that celestial bodies were genuine natural causes of terrestrial events and that reading their configurations was legitimate natural philosophy, not divination. The Parisian condemnation of 1277 targeted astrological determinism specifically, and the subsequent literature on astrology is largely a negotiation of where natural astrological prediction ends and illicit divination begins.</p>

<h2>Geomancy and Related Arts</h2>
<p>Geomancy (divination from earth-figures, produced by random marks on sand or dots on paper, combined into sixteen possible figures) was the most widely used learned divinatory system of the medieval period after astrology. Its Arabic origins (translated as <em>ars geomantiae</em> in the twelfth century) gave it the same intellectual prestige as Arabic astrology; it circulated in university and court contexts alongside astrological texts. Don Skemer's <em>Binding Words: Textual Amulets in the Middle Ages</em> (2006) and Sophie Page's work document its manuscript circulation in England and continental Europe.</p>""",

"magia_naturalis_concept": """<h2>Definition</h2>
<p>Actor Term. <em>Magia naturalis</em> (natural magic) designates, in Renaissance and early modern usage, the study and application of the hidden powers of nature — the occult properties of things, the influences of the stars, the sympathies and antipathies linking all things through the world-soul — that produce marvellous effects without supernatural or demonic intervention. The term was used by Renaissance natural philosophers as a positive category distinguishing their enterprise from the condemned demonic magic of the grimoire tradition, and as a claim to scientific respectability: natural magic was, its proponents argued, simply the highest branch of natural philosophy, concerned with the hidden causes that superficial investigation missed.</p>

<h2>Major Formulations</h2>
<p>The classical Renaissance formulation of <em>magia naturalis</em> as a positive programme appears in Giovanni Battista della Porta's <em>Magia naturalis</em> (Naples, 1558; expanded to twenty books, 1589), which became one of the best-selling books of the sixteenth century. Della Porta defined natural magic as the practical application of natural philosophy, concerned with producing remarkable effects through knowledge of hidden natural causes. The work's range is characteristic: it covers sympathies and antipathies, the virtues of plants and animals, pyrotechnics, optical tricks (including early descriptions of the camera obscura), magnets, and alchemy, all framed as natural phenomena accessible to systematic investigation.</p>
<p>Earlier formulations include Ficino's <em>De vita coelitus comparanda</em> (1489), which frames astral medicine and talismanic magic as natural operations through the spiritus mundi; Agrippa's Book I of <em>De occulta philosophia</em> (1531), on the elemental world's occult properties; and Roger Bacon's concept of <em>scientia experimentalis</em> as the crown of natural philosophy, producing marvellous effects through knowledge of hidden causes.</p>

<h2>Relationship to Science</h2>
<p>The relationship between Renaissance <em>magia naturalis</em> and the emergence of early modern natural science is the central problem of the "Yates thesis" debate. Yates and her followers argued that the emphasis on operative, experimental knowledge in natural magic prepared the psychological ground for Baconian experimental science. Critics argued that the traditions were more opposed than convergent: Bacon himself rejected occult sympathies as unfit objects of natural philosophical enquiry. The current consensus treats <em>magia naturalis</em> and emerging experimental science as partially overlapping but ultimately divergent traditions, sharing a commitment to the investigation of hidden causes while differing on method and metaphysics.</p>""",

"nigromantia": """<h2>Definition</h2>
<p>Actor Term. <em>Nigromantia</em> is the medieval Latin term for demonic conjuration — the ritual summoning and commanding of demons. Although etymologically from Greek <em>nekromanteia</em> (divination through the dead), medieval Latin writers consistently glossed the term as "black art" (<em>nigra ars</em>), connecting the first element to Latin <em>niger</em> (black) rather than Greek <em>nekros</em> (dead). This folk etymology — which Isidore of Seville had already offered — transformed the meaning of the term: <em>nigromantia</em> in medieval learned usage designated not ghost-consultation but the entire complex of demonic conjuration, illusion, and operation through demonic power.</p>

<h2>The Nigromancer in Medieval Culture</h2>
<p>The figure of the <em>nigromancer</em> in medieval learned culture was typically imagined as a learned cleric: a man with Latin literacy who had access to the manuscripts containing conjuration procedures, knowledge of the ritual requirements (magic circles, fumigations, special garments, complex formulae), and the ability to perform the rites. This is the "clerical underworld" identified by Richard Kieckhefer: a penumbra of educated clergymen and university graduates whose social position and economic vulnerability made the practice of magic — offering services of divination, love magic, healing, or harm — attractive as a supplementary livelihood.</p>
<p>The Munich Manual (<em>Clm 849</em>), the principal surviving medieval Latin handbook of demonic conjuration, is addressed to exactly this figure: a literate clergyman with access to appropriate ritual materials, willing to perform procedures involving demonic pact in exchange for practical results. Kieckhefer's edition (<em>Forbidden Rites</em>, 1997) remains the essential analysis.</p>

<h2>Condemnation and Persistence</h2>
<p>Despite consistent ecclesiastical condemnation — from Isidore's taxonomy of forbidden arts through the inquisitorial manuals of the fifteenth century — nigromantic practice persisted in manuscript culture throughout the medieval period. The social conditions that sustained it (literate but economically marginal clergy, demand for magical services from laypeople, relative difficulty of detection when practices were performed privately) were not abolished by theological condemnation. The transition to print, documented by Owen Davies (<em>Grimoires</em>, 2009), transformed rather than ended the tradition.</p>""",

}


PERSON_ENRICHMENTS = {

"johannes_trithemius": """<h2>Life</h2>
<p>Johannes Trithemius (1462–1516), born Johann Heidenberg in Trittenheim on the Moselle, was a Benedictine abbot, humanist scholar, encyclopedist, and occultist whose works bridged the learned worlds of humanism, monastic reform, and Renaissance magic. Elected abbot of Sponheim at the age of twenty-one, he transformed the monastery into a major intellectual centre with a library of over 2,000 volumes — remarkable by contemporary standards. He later served as abbot of Würzburg's St. James's. His correspondents included Agrippa, Erasmus, Conrad Celtis, and the Emperor Maximilian I.</p>

<h2>Works</h2>
<p>Trithemius produced an enormous range of writing. His <em>Polygraphia</em> (1518, posthumous) and <em>Steganographia</em> (written c.1499, not printed until 1606) are the most important for the history of magic and cryptography. The <em>Steganographia</em> presents itself as a system for communicating through spirits; its three books contain what appeared to be instructions for demonic conjuration, causing it to be placed on the Index of Prohibited Books. Modern scholars (Thomas Ernst and others) have demonstrated that the first two books contain a sophisticated polyalphabetic cipher hidden within the apparently magical instructions — a pioneering work in the history of cryptography — though Book III may contain genuine magical content.</p>
<p>The <em>Polygraphia</em> is an openly acknowledged treatise on steganography and substitution ciphers, the first printed book on cryptography. Trithemius's historical works, including the <em>Annales Hirsaugienses</em> and the <em>Compendium sive Breviarium</em>, are important for the history of German monasticism, though they are notorious for containing fabricated documents — Trithemius was willing to invent sources when genuine ones were unavailable, a practice that complicates his use as a historical authority.</p>

<h2>Significance for Magic</h2>
<p>Trithemius's early response to Cornelius Agrippa's manuscript of <em>De occulta philosophia</em> (1510) — cautious approval coupled with a warning about public disclosure — captures the ambivalence of the learned magical milieu: genuine intellectual engagement with magical philosophy alongside awareness of the risks of making it public. His own <em>Steganographia</em> exemplifies this: a text that circulated in manuscript for a century before print, widely known in magical circles, apparently revealing demonic secrets while concealing a purely technical cryptographic system.</p>""",

"owen_davies": """<h2>Life and Scholarship</h2>
<p>Owen Davies is Professor of Social History at the University of Hertfordshire and the leading historian of popular and print magic in modern Britain and the English-speaking world. His scholarship spans the history of witchcraft, cunning folk, ghosts, and magical books in Britain and America, with particular attention to the intersection of print culture, popular belief, and learned tradition in the eighteenth and nineteenth centuries.</p>

<h2>Major Works</h2>
<p><em>Grimoires: A History of Magic Books</em> (Oxford University Press, 2009) is Davies's most synthetic work and the essential scholarly history of the grimoire as a genre from antiquity to the present. The book traces the transformation of learned magical manuscripts into commercial print publications, from the early modern chapbook grimoires of France (<em>Grand Albert</em>, <em>Petit Albert</em>) through the nineteenth-century occult revival editions (Mathers, Waite) and the twentieth-century paperback grimoire market, showing how each phase of print technology and each social context produced grimoires adapted to its conditions.</p>
<p><em>Popular Magic: Cunning-folk in English History</em> (Hambledon Continuum, 2003) documents the world of English cunning folk — the village-level magical practitioners who provided healing, divination, and counter-magic services — from the sixteenth through the nineteenth centuries. The book demonstrates, against the long-standing assumption that learned magic and popular magic were entirely separate spheres, that cunning folk regularly used printed and manuscript magical texts, including grimoires, as resources for their practice.</p>
<p><em>America Bewitched: The Story of Witchcraft after Salem</em> (Oxford, 2013) extends this analysis to North America, tracing the persistence of witchcraft belief and practice through the nineteenth century and into the twentieth. Earlier works include <em>Witchcraft, Magic and Culture 1736–1951</em> (Manchester, 1999) and <em>The Haunted: A Social History of Ghosts</em> (Palgrave, 2007).</p>""",

"john_of_morigny": """<h2>Life</h2>
<p>John of Morigny (active c.1301–1315) was a Benedictine monk, probably from the monastery of Morigny near Étampes in the Île-de-France, who composed the <em>Liber visionum</em> (Book of Visions) — a visionary mystical work that began as an adaptation of the Ars Notoria tradition and was progressively transformed into an original form of contemplative angel magic through direct visionary experience. His career is unusually well documented for a medieval magical author because the <em>Liber visionum</em> is itself autobiographical: it narrates John's encounter with the Ars Notoria, his initial use of it, his visions of the Virgin Mary and angels, and the progressive revision of his practice under visionary guidance.</p>

<h2>The Liber visionum</h2>
<p>John began using the Ars Notoria — a widely circulated prayer-based system for acquiring knowledge of the arts and sciences through divine infusion — and experienced visions in which the Virgin Mary and Christ appeared to him, apparently validating but also transforming the practice. Over a period of years, he composed a new version of the Notory Art that replaced the original Latin prayers and <em>notae</em> (geometric figures) with new formulas revealed in his visions, insisting that his version was purified of the diabolical contamination he had come to detect in the original Ars Notoria.</p>
<p>Claire Fanger and Nicholas Watson's edition and translation (<em>Liber florum celestis doctrine / The Flowers of Heavenly Teaching</em>, Penn State University Press, 2015) is the critical edition of this remarkable text. John of Morigny is significant as an example of a medieval practitioner who engaged critically with the learned magical tradition from within, revising its texts in response to visionary experience rather than simply transmitting or condemning them.</p>""",

"giordano_bruno": """<h2>Life</h2>
<p>Giordano Bruno (1548–1600) was born in Nola near Naples, entered the Dominican Order, and spent his career as a wandering philosopher, teacher, and controversial public figure in Toulouse, Geneva, Paris, London, Wittenberg, Prague, and Venice before his arrest by the Venetian Inquisition in 1592. He was transferred to Rome, held for seven years, and burned at the stake at the Campo de' Fiori on 17 February 1600. The specific charges on which he was condemned are not all known, but they included denying the Trinity, denying the Incarnation, denying transubstantiation, believing in the plurality of worlds and the eternity of matter, practising magic, and denying the divinity of Christ.</p>

<h2>Hermetic Philosophy and Magic</h2>
<p>Bruno's philosophy is, as Frances Yates argued in <em>Giordano Bruno and the Hermetic Tradition</em> (1964), fundamentally Hermetic: his panpsychic universe, in which the world-soul animates all things and matter is itself infused with intelligence, derives from the <em>Corpus Hermeticum</em> and from Ficino's reading of it. His works of the 1580s — the Italian philosophical dialogues (<em>La cena de le ceneri</em>, <em>De la causa, principio et uno</em>, <em>De l'infinito, universo et mondi</em>), the Latin treatises on magic (<em>De magia</em>, <em>De vinculis in genere</em>, <em>Theses de magia</em>), and the Latin memory treatises (<em>De umbris idearum</em>, <em>Cantus Circaeus</em>) — constitute the most philosophically ambitious engagement with Hermetic magic in the Renaissance.</p>
<p>Bruno's theory of magic in <em>De magia</em> and <em>De vinculis</em> moves beyond Ficinian natural magic toward a theory of what he calls "bonds" — the connections through which the magician operates on other minds and souls. The magician does not merely manipulate physical forces; he understands and exploits the passions, desires, and imaginative susceptibilities of others. This psychological theory of magic anticipates modern theories of rhetoric, persuasion, and charisma.</p>

<h2>Legacy</h2>
<p>Bruno became a martyr figure for Italian nationalism in the nineteenth century (a statue stands at the Campo de' Fiori) and for subsequent freethinkers. His philosophical legacy has been disputed: Yates argued that his Hermeticism was central to the Scientific Revolution; others have argued that his specific cosmological claims (infinite universe, plurality of worlds) were reached by philosophical reasoning rather than magic. Ioan Couliano's <em>Eros and Magic in the Renaissance</em> (1987) provides the most ambitious recent interpretation of his theory of magic.</p>""",

"claire_fanger": """<h2>Life and Scholarship</h2>
<p>Claire Fanger is a scholar of medieval religion and ritual magic at Rice University whose editorial and interpretive work has been central to establishing the study of medieval ritual magic as a rigorous historical subdiscipline. Her work focuses on the intersection of magic, mysticism, and religious experience in the later Middle Ages, with particular attention to texts that blur the boundaries between legitimate contemplative practice and condemned magical operation.</p>

<h2>Editorial Work</h2>
<p>Fanger edited the landmark volume <em>Conjuring Spirits: Texts and Traditions of Medieval Ritual Magic</em> (Penn State University Press, 1998), which brought together essays on the Ars Notoria, the Munich Manual, the <em>Liber visionum</em> of John of Morigny, and other key texts, establishing the field's scope and methods. A follow-up volume, <em>Invoking Angels: Theurgic Ideas and Practices, Thirteenth to Sixteenth Centuries</em> (Penn State, 2012), extended the analysis to the relationship between angel magic and mysticism across three centuries.</p>
<p>Her edition (with Nicholas Watson) of John of Morigny's <em>Liber florum celestis doctrine</em> (<em>The Flowers of Heavenly Teaching</em>, Penn State, 2015) is the critical scholarly edition of this extraordinary visionary text, providing Latin text, English translation, and extensive introduction. The edition demonstrates the kind of careful textual and contextual analysis that distinguishes modern grimoire scholarship from earlier occultist editions.</p>

<h2>Interpretive Contributions</h2>
<p>Fanger's interpretive work addresses the relationship between magical and mystical traditions in medieval Christianity, arguing against sharp categorical distinctions between "magic" (condemned) and "mysticism" (approved). Her analysis of John of Morigny shows how a practitioner could engage with the Ars Notoria tradition, receive visionary critique of it, and produce a revised system that was itself neither purely magical nor purely contemplative. This blurring of categories is characteristic of the learned magical milieu and important for understanding how magical practice was experienced by its practitioners.</p>""",

"lynn_thorndike": """<h2>Life and Scholarship</h2>
<p>Lynn Thorndike (1882–1965) was an American historian at Columbia University whose monumental <em>A History of Magic and Experimental Science</em> (8 volumes, Columbia University Press, 1923–1958) remains the most extensive survey of the relationship between magic and science in European intellectual history. The project covered the Roman Empire through the seventeenth century and drew on an extraordinary range of primary sources, many of which Thorndike was the first modern scholar to examine systematically.</p>

<h2>A History of Magic and Experimental Science</h2>
<p>The eight-volume work is organized chronologically, with each chapter or section treating a specific author, text, or topic. Thorndike's thesis — stated in the title — is that magic and experimental science developed in parallel, sharing an empirical orientation toward the investigation of nature's hidden properties; that medieval magic was not mere superstition but represented a serious attempt to understand and manipulate natural forces; and that the history of science cannot be properly understood without attention to the magical and astrological context within which early scientific observation and experiment took place.</p>
<p>The work's strengths are its scope and its primary-source depth: Thorndike read vast quantities of manuscript material and provides the first systematic accounts of dozens of texts previously unknown to scholarship. Its weaknesses, identified by subsequent scholars, include a tendency toward uncritical summary (Thorndike often paraphrases his sources at length without sustained analysis), an outdated historiographical framework that treats the relationship between magic and science as straightforwardly progressive, and significant factual errors in the earlier volumes that have been corrected by subsequent specialized work.</p>

<h2>Legacy</h2>
<p>Despite its limitations, <em>A History of Magic and Experimental Science</em> remains an indispensable research tool for anyone working on medieval and early modern natural philosophy and magic. The index volumes provide access to an enormous range of authors and texts; the primary-source descriptions, where later scholarship has not superseded them, remain valuable. Thorndike's work is the principal example of the encyclopedic historical approach to the subject that was standard before the development of more theoretically sophisticated methods in the 1980s and 1990s.</p>""",

}


TEXT_ENRICHMENTS = {

"grimoires_history_davies": """<h2>Overview</h2>
<p>Owen Davies's <em>Grimoires: A History of Magic Books</em> (Oxford University Press, 2009) is the most comprehensive historical survey of the grimoire as a genre from antiquity to the present and the essential starting point for any study of the magical book as a cultural artefact. The book traces the transformation of learned magical manuscripts into commercial publications, following the grimoire through the hand-press era, the chapbook revolution of the eighteenth century, the Victorian occult revival, the twentieth-century paperback market, and finally the digital age.</p>

<h2>Argument and Structure</h2>
<p>Davies's central argument is that the grimoire is not a timeless repository of esoteric knowledge but a historically conditioned object that changes with its means of production, its social context, and its intended audience. The ancient and medieval manuscript grimoire (expensive, restricted, circulating among literate elites) differs fundamentally from the eighteenth-century French chapbook grimoire (<em>Grand Albert</em>, <em>Petit Albert</em>, Dragon Rouge), which was designed for a literate popular market. The nineteenth-century occult revival editions of Mathers and Waite imposed scholarly apparatus and ritual significance on texts that had long circulated as practical handbooks. The twentieth-century paperback grimoire (Llewellyn, Weiser) addresses a self-identified magical community with different needs and assumptions.</p>
<p>The book's chapters proceed chronologically and by geography: ancient Mesopotamian and Egyptian magical books; Jewish and Christian late antique texts; medieval European manuscripts; the Arabic and Mediterranean traditions; the early modern print era; the French chapbook tradition; American popular magic (hoodoo, Pennsylvania Dutch hex); the Victorian occult revival; and twentieth-century print and digital magic. Each chapter combines primary-source analysis with attention to the social history of production, circulation, and use.</p>

<h2>Significance</h2>
<p>Davies's book is particularly important for two contributions. First, it documents the role of popular print culture — the chapbook, the pamphlet, the cheap pamphlet grimoire — in transmitting magical tradition to social strata far below the learned clerical elite that had been the focus of most previous grimoire scholarship. Second, it demonstrates the global reach of the grimoire tradition, including its transmission to colonial and post-colonial contexts in Africa, the Caribbean, and North America, where texts like the <em>Sixth and Seventh Books of Moses</em> entered African-American hoodoo practice.</p>""",

"forbidden_rites": """<h2>Overview</h2>
<p>Richard Kieckhefer's <em>Forbidden Rites: A Necromancer's Manual of the Fifteenth Century</em> (Penn State University Press, 1997) is both a critical edition and translation of the Munich Manual of demonic magic (Bayerische Staatsbibliothek, Clm 849) and a sustained scholarly analysis of what the text reveals about medieval learned magic and the social world in which it circulated. The Munich Manual is a Latin miscellany copied around the 1440s containing illusionist tricks, love magic using spirits, and full demonic conjuration rituals — the most complete surviving medieval Latin handbook of its kind.</p>

<h2>The Text and Its Contents</h2>
<p>Clm 849 contains three distinct types of material. The first section comprises "illusionist" experiments — procedures for creating apparent wonders (making a horse seem to have no head, making a banquet appear where none exists) that exploit psychological suggestion and natural properties rather than demonic power. The second section covers experiments involving spirit assistance for practical ends: finding hidden treasure, compelling love, causing discord, revealing thieves. The third section contains formal demonic conjuration: complete ritual procedures for summoning, binding, interrogating, and dismissing named demons.</p>
<p>Kieckhefer's edition provides the Latin text with facing English translation and extensive annotation identifying the demons named, the ritual sources, and the parallels in other magical manuscripts. His introductory chapters situate the text within the broader tradition of medieval Latin magic, discuss the question of how such a text was used (by whom, in what circumstances, with what expectations), and address the relationship between demonic conjuration and the theological concept of demonic pact.</p>

<h2>Significance</h2>
<p>The Munich Manual is significant as a primary document for the "clerical underworld" that Kieckhefer theorized in <em>Magic in the Middle Ages</em>: a text clearly designed for a literate, Latinately educated practitioner who expected to perform its rituals, not merely read about them. Its survival is partly accidental (it was bound with more respectable medical and astrological texts), and its content is more explicitly demonic than most surviving magical manuscripts — raising the question of what was destroyed that no longer survives. <em>Forbidden Rites</em> remains the model for how to approach a practical magic manuscript with scholarly rigour.</p>""",

"hygromanteia": """<h2>Overview</h2>
<p>The <em>Hygromanteia</em> (Greek: divination from water) is a Byzantine Greek astrological magic text, attributed to Solomon and surviving in several Greek manuscripts from the thirteenth century onward, though its compilation likely predates the surviving witnesses. The text is one of the principal Greek Solomonic texts and was a source for, or parallel development to, the Latin <em>Clavicula Salomonis</em> tradition. It combines astrological procedures, planetary images and talismans, and conjuration formulae within a Solomonic attribution framework.</p>

<h2>Contents and Structure</h2>
<p>The <em>Hygromanteia</em> addresses a wide range of practical magical procedures organized around the planets and their governing periods. Its contents include: procedures for using water, fire, and other substances for divination; instructions for making and using planetary images and talismans; formulas for conjuring planetary spirits; and procedures for a range of practical operations (finding hidden things, causing love, defeating enemies, obtaining favour from authorities). The attribution to Solomon and the invocation of divine and angelic names as authorizing forces situate it firmly within the Solomonic tradition.</p>

<h2>Scholarship</h2>
<p>Ioannis Marathakis's critical edition and English translation (<em>The Magical Treatise of Solomon or Hygromanteia</em>, Golden Hoard Press, 2011) made the text accessible to scholars working in the Latin and vernacular magical tradition. The edition establishes the manuscript tradition, provides the Greek text with English translation, and discusses the relationship of the <em>Hygromanteia</em> to the Latin <em>Clavicula Salomonis</em> — a relationship of partial correspondence and partial independence that suggests a shared tradition of Solomonic magic rather than simple textual derivation.</p>""",

"sworn_book_of_honorius": """<h2>Overview</h2>
<p>The <em>Sworn Book of Honorius</em> (<em>Liber juratus Honorii</em>) is a Latin magical text, probably composed in the thirteenth century, that presents itself as the surviving essence of a great magical library compiled by Honorius of Thebes and preserved only because ninety masters of magic swore to keep it secret and to pass it on to no more than three persons each. The framing narrative — the masters of magic assembling against papal persecution to preserve their knowledge — is itself significant as an early articulation of the magician's self-understanding as a persecuted keeper of ancient wisdom.</p>

<h2>Contents</h2>
<p>The <em>Sworn Book</em> is organized around a programme for achieving the beatific vision — the direct sight of God — through a course of prayer, fasting, and ritual practice extending over several months. The operative core is a set of prayers and conjurations for summoning the angel Hochmel (associated with divine wisdom), other celestial spirits, and eventually God himself. The text also includes procedures for more conventional magical ends: spirit conjuration for practical purposes, the construction of the Seal of God (a complex diagram combining divine names, astrological symbols, and angelic seals), and instructions for achieving invisibility.</p>
<p>Gösta Hedegård's critical edition (<em>Liber iuratus Honorii: A Critical Edition of the Latin Version of the Sworn Book of Honorius</em>, Almqvist and Wiksell, 2002) provides the scholarly text. Joseph Peterson's edition (Ibis Press, 2016) makes it available with English translation. The text occupies an interesting position between the Ars Notoria tradition (angelic infusion of knowledge through prayer and contemplation) and the demonic conjuration tradition (explicit spirit-binding for practical ends), and has been analysed by Kieckhefer, Klaassen, and Sophie Page in terms of this generic ambiguity.</p>""",

"ars_notoria": """<h2>Overview</h2>
<p>The <em>Ars Notoria</em> (Notory Art) is a Latin magical text, probably compiled in the twelfth or thirteenth century, that provides a system for acquiring knowledge of the seven liberal arts and other forms of learning through a programme of prayer, fasting, and contemplation of the <em>notae</em> — elaborate geometric and symbolic figures accompanied by sequences of divine names, Greek voces magicae, and Hebrew words, arranged into extended series of prayers (<em>orationes</em>). The practitioner is promised that diligent use of the system will result in divine infusion of the knowledge of grammar, rhetoric, dialectic, arithmetic, geometry, music, and astronomy, without the ordinary labour of study.</p>

<h2>Structure and Use</h2>
<p>The text exists in two main recensions: a shorter version and a longer version incorporating additional <em>notae</em> and prayers. The cycle of use for the complete system takes several months; intermediate cycles of shorter duration are also prescribed. The practitioner must observe strict conditions of ritual purity, undertake fasting and prayer at specified times, and contemplate the <em>notae</em> while reciting the associated prayers. The result is claimed to be not only the acquisition of encyclopedic knowledge but also prophetic dreams, visions of angels, and ultimately the direct perception of God.</p>
<p>Julien Véronèse's critical edition (<em>L'Ars notoria au Moyen Âge: Introduction et édition critique</em>, Sismel, 2007) is the scholarly standard. John of Morigny's <em>Liber visionum</em> (early fourteenth century), edited by Claire Fanger and Nicholas Watson (Penn State, 2015), is the most important medieval response to the Ars Notoria — a visionary revision of the system undertaken after Marian apparitions. Frank Klaassen's work situates the text within the broader manuscript tradition of English learned magic.</p>

<h2>Theological Status</h2>
<p>The <em>Ars Notoria</em> occupied an unusual theological position: it claimed to work through divine grace rather than demonic pact, making it arguably licit. Thomas Aquinas condemned it in the <em>Summa theologiae</em> (II-II, q. 96, a. 1) as vain (the system cannot achieve what it claims) and as implicitly involving demonic assistance (the voces magicae and geometric figures have no natural relationship to the knowledge they are supposed to infuse). Nevertheless, the text circulated widely in monastic and university contexts, and its practitioners evidently found the theological condemnation less than conclusive.</p>""",

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

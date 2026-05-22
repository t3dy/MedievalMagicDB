import sqlite3

from common import DB_PATH, ensure_dirs


def upsert(conn, table, key, row):
    columns = list(row.keys())
    placeholders = ", ".join("?" for _ in columns)
    updates = ", ".join(f"{c}=excluded.{c}" for c in columns if c != key)
    conn.execute(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) "
        f"ON CONFLICT({key}) DO UPDATE SET {updates}",
        [row[c] for c in columns],
    )


def concept_ars_notoria():
    return """
    <p><i>Ars Notoria</i> is an <b>Actor Term</b> for a medieval ritual art of learning, memory, and intellectual preparation that emerged in Latin manuscript culture and became one of the most influential and controversial ritual texts of the later Middle Ages. Its earliest secure form belongs to the thirteenth-century Latin tradition, where prayers, notae, angelic names, and structured sequences of recitation are presented as aids to rapid mastery of the liberal arts and theology. Modern scholars such as Richard Kieckhefer, Claire Fanger, Frank Klaassen, and Robert Mathiesen have treated the work as a crucial witness to the intersection of devotion, education, and ritual technique rather than as a simple "spell book."</p>

    <h2>Historical Usage</h2>
    <p>In medieval usage the <i>Ars Notoria</i> belonged to the broad world of learned ritual, but it did not circulate as a single, fixed book. Manuscripts preserve multiple recensions, rewritten openings, and different arrangements of prayers and figures, suggesting that the text lived as a flexible ritual dossier rather than as a canonical treatise. Its core claim is that learning may be accelerated through disciplined prayer and exact attention to divine or angelic mediation. That claim sits near a number of other medieval textual forms, including confessionally framed devotional aids, angelic invocation, and occultized mnemonic practices. The work is also closely related to the wider Solomonic textual environment, not because Solomon is its only authority, but because the cultural authority of ancient wisdom and revealed knowledge gives the text its force. In later medieval and early modern manuscript culture, the <i>Ars Notoria</i> was often copied beside other ritual, astronomical, and devotional materials, a setting that reinforces its status as a manuscript practice rather than a single bounded genre.</p>

    <p>Its historical importance lies partly in the way it destabilizes modern expectations. The text is neither a scholastic textbook nor an overtly demonic grimoire. It promises learning through ritual exactness, and in doing so it occupies the same broad zone that scholars such as Sophie Page and Frank Klaassen identify as the manuscript-based borderland between devotion, experiment, and illicit arts. The <i>Ars Notoria</i> therefore helps explain why medieval debates over magic cannot be reduced to a simple opposition between religion and superstition. It is better understood as a ritualized claim about the permeability of intellectual authority, where knowledge is something that may be petitioned, received, and disciplined rather than merely studied.</p>

    <h2>Scholarly Significance</h2>
    <p>Modern scholarship has made the <i>Ars Notoria</i> central to the study of medieval ritual learning. Kieckhefer placed the text within the larger history of illicit learned magic and manuscript ritual, showing that it belongs to a clerical culture in which learning, prayer, and suspect technique often coexisted. Claire Fanger has emphasized the role of ritual discipline, spiritual aspiration, and textual rewriting, while Klaassen has highlighted the manuscript transformations that carry the work across the later Middle Ages and Renaissance. Mathiesen's work is important because it points toward the ritual and Solomonic manuscript traditions in which the <i>Ars Notoria</i> circulates. Together these scholars make it possible to see the text not as an oddity on the edge of medieval learning, but as a revealing case study in the social life of ritual knowledge.</p>

    <p>The term also matters because it helps define the portal's actor/analyst distinction. The <i>Ars Notoria</i> is not a medieval self-description for all learned magic, nor is it identical to modern categories such as "grimoire" or "occultism." It is one historical form within a much larger and unstable field. In that sense it is useful for tracing the historian's own categories: what counts as learning, what counts as ritual, and where the boundary lies between legitimate study and forbidden practice. The text sits beside <a href="../concepts/notae.html">notae</a>, <a href="../concepts/angelic_invocation.html">angelic invocation</a>, <a href="../concepts/ritual_diagrams.html">ritual diagrams</a>, and <a href="../concepts/solomonic_magic.html">Solomonic magic</a> in a way that exposes the manuscript ecology of medieval learned magic.</p>

    <h2>Transmission and Variant Forms</h2>
    <p>The <i>Ars Notoria</i> survives in Latin manuscript recensions with shifting titles, prefatory material, and explanatory additions. Some copies preserve a strong prayer-centered form, while others expand the ritual apparatus or emphasize visual and mnemonic features. The work's title itself is unstable, appearing in different manuscript families with minor variation, and its ritual authority is often strengthened by adjacent attributions to ancient or biblical wisdom. Because of that manuscript variability, any modern edition must be treated as one scholarly reconstruction among others rather than as the text's final medieval form. The work's transmission also overlaps with other ritual-learning traditions, especially texts associated with Solomon, angelic invocations, and the broader culture of memory arts.</p>

    <h2>Related Concepts</h2>
    <p>The <i>Ars Notoria</i> is inseparable from <a href="../concepts/notae.html">notae</a>, since the visual figures are not ornamental but part of the ritual's logic. It also belongs to <a href="../concepts/learned_magic.html">learned magic</a>, although the modern category should not be collapsed into the text's own medieval world. Its proximity to <a href="../concepts/pseudepigraphy.html">pseudepigraphy</a> and <a href="../concepts/secret_names.html">secret names</a> shows how authority is staged through attributed antiquity and exact verbal transmission. Finally, the text's circulation beside <a href="../concepts/ritual_purity.html">ritual purity</a> and <a href="../concepts/angelic_invocation.html">angelic invocation</a> reveals how deeply it depends on moral and devotional framing.</p>

    <h2>Literature</h2>
    <p>Kieckhefer, Richard. <i>Forbidden Rites: A Necromancer's Manual of the Fifteenth Century</i>. University Park: Pennsylvania State University Press, 1998.<br/>
    Fanger, Claire. <i>Invoking Angels: Theurgic Ideas and Practices, Thirteenth to Sixteenth Centuries</i>. University Park: Pennsylvania State University Press, 2012.<br/>
    Klaassen, Frank. <i>The Transformations of Magic: Illicit Learned Magic in the Later Middle Ages and Renaissance</i>. University Park: Pennsylvania State University Press, 2013.<br/>
    Mathiesen, Robert. Studies on the <i>Ars Notoria</i> and related ritual traditions in medieval manuscript culture.<br/>
    Page, Sophie. <i>Magic in the Cloister: Pious Motives, Illicit Interests, and Occult Approaches to the Medieval Universe</i>. University Park: Pennsylvania State University Press, 2013.<br/>
    Skinner, Stephen and Daniel Clark. <i>Ars Notoria: The Grimoire of Rapid Learning by Magic with the Golden Flowers of Apollonius of Tyana</i>. Manuscript edition and modern study.</p>
    """


def text_ars_notoria():
    return """
    <p><i>Ars Notoria</i> is a medieval Latin <b>PRIMARY_SOURCE</b> whose manuscript life extends across the later Middle Ages and early modern period. It is a ritual text of learning and memory that promises intellectual acceleration through prayer, figures, and disciplined recitation. The work matters because it shows that medieval readers did not separate education neatly from ritual, and because it offers one of the clearest manuscript cases in which knowledge itself is treated as something that can be petitioned, ordered, and ritually prepared.</p>

    <h2>Content and Structure</h2>
    <p>The text combines prayers, invocations, and notae with an insistence on orderly preparation. Its different recensions present the learning of the liberal arts, theology, and intellectual skill as the result of a ritually mediated process rather than purely scholastic exertion. The rhetoric is exacting. The practitioner is expected to observe rules of preparation, attention, purity, and textual fidelity, which makes the <i>Ars Notoria</i> an especially revealing witness to medieval conceptions of disciplined knowledge. Unlike a narrative text, it is built around procedural sequences that link verbal formulae to figures and visual marks. These elements are not marginal; they are the mechanism by which the text claims efficacy. The ritual art is therefore best read as a theory of acquired knowledge, not as a generic charm-book.</p>

    <p>The opening claims of the work also reveal why modern scholars treat it as more than an eccentric curiosity. It translates the desire for mastery into a ritual register, and in doing so it intersects with memory arts, angelic invocation, and devotional practice. The text's repeated insistence on order and exactness suggests that intellectual power was understood as something that could be cultivated through morally framed discipline. That is why the <i>Ars Notoria</i> is relevant not only to magic studies but also to the history of pedagogy, prayer, and the medieval imagination of learning.</p>

    <h2>Transmission and Manuscript Context</h2>
    <p>The text survives in multiple manuscripts with considerable variation in titles, prefatory material, and the arrangement of prayers and figures. Some witnesses emphasize the ritual ladder of learning; others preserve different paratexts or place the work alongside other spirit and memory texts. The manuscript context is crucial. The <i>Ars Notoria</i> does not exist as a stable book in the modern sense but as a textual family that was copied, adapted, and sometimes combined with other ritual works. This fluidity is precisely what makes it important for a portal built around codicology and transmission. It shows how a ritual text could survive as a manuscript practice rather than as a canonical work.</p>

    <p>Modern editorial work, including modern editions and study by Skinner, Clark, Kieckhefer, Fanger, Mathiesen, and Klaassen, has clarified the text's complexity without exhausting it. Every new manuscript witness still has the potential to alter the picture, because the work's authority lies as much in its copied forms as in any archetypal version. The text is therefore a good example of why the portal treats manuscript transmission as a scholarly problem in its own right.</p>

    <h2>Classification and Controversy</h2>
    <p>The <i>Ars Notoria</i> sits at the center of debates over classification. Is it devotional, mnemonic, magical, or something in between? Medieval actors do not answer that question in modern terms. The text itself presents ritual learning as a disciplined and elevated pursuit, but later readers often grouped it with illicit or dangerous arts. That tension makes it an exemplary case of the actor/analyst distinction. It is an actor text whose meaning changed with each scholarly and institutional frame. In that respect it belongs with <a href="../concepts/learned_magic.html">learned magic</a>, but it also straddles <a href="../concepts/ritual_purity.html">ritual purity</a>, <a href="../concepts/angelic_invocation.html">angelic invocation</a>, and <a href="../concepts/notae.html">notae</a> in ways that deny any simple classification.</p>

    <h2>Modern Scholarship</h2>
    <p>Kieckhefer's work on illicit learned magic first placed the text firmly in the history of learned ritual. Fanger has treated it as part of a wider theurgic and ritual culture, while Klaassen has emphasized the instability of manuscript transmission and the long life of ritual texts in changing codex environments. Page's codicological perspective helps explain why the text belongs in the manuscript worlds of clerics, students, and ritual collectors. The result is a scholarly consensus that the <i>Ars Notoria</i> is neither trivial nor isolated. It is a major witness to the ritualization of learning in medieval Latin culture.</p>

    <h2>Literature</h2>
    <p>Fanger, Claire. <i>Invoking Angels: Theurgic Ideas and Practices, Thirteenth to Sixteenth Centuries</i>. University Park: Pennsylvania State University Press, 2012.<br/>
    Kieckhefer, Richard. <i>Forbidden Rites: A Necromancer's Manual of the Fifteenth Century</i>. University Park: Pennsylvania State University Press, 1998.<br/>
    Klaassen, Frank. <i>The Transformations of Magic: Illicit Learned Magic in the Later Middle Ages and Renaissance</i>. University Park: Pennsylvania State University Press, 2013.<br/>
    Page, Sophie. <i>Magic in the Cloister: Pious Motives, Illicit Interests, and Occult Approaches to the Medieval Universe</i>. University Park: Pennsylvania State University Press, 2013.<br/>
    Skinner, Stephen and Daniel Clark. <i>Ars Notoria: The Grimoire of Rapid Learning by Magic with the Golden Flowers of Apollonius of Tyana</i>. Modern edition and study.</p>
    """


def text_picatrix():
    return """
    <p><i>Picatrix</i> is the Latin <b>PRIMARY_SOURCE</b> title for the medieval translation of the Arabic <i>Ghayat al-hakim</i>, a major astral and talismanic treatise that became one of the central conduits for learned image magic in the Latin West. The work is not merely an occult handbook. It is a large and composite text in which planetary theory, images, suffumigations, timing, and philosophical justifications for astral action are woven together. Its importance for medieval magic lies in the way it bridges Arabic science, philosophy, and ritual technique.</p>

    <h2>Content and Structure</h2>
    <p>The <i>Picatrix</i> organizes astral action through a combination of cosmology and practice. It explains the powers of the heavens, the qualities of planets, the logic of images, and the preparation of materials and times. The text repeatedly insists that efficacy depends on proper alignment between celestial influence and human operation. That makes it a classic witness to medieval image magic, but also to the learned attempt to naturalize ritual effects. The presence of suffumigation, planetary timing, seals, names, and material correspondences shows why the text became so central to later astrologers, magi, and scholars of the occult sciences. Its logic is not chaotic; it is rigorously ordered and philosophically self-conscious.</p>

    <p>At the level of doctrine, the <i>Picatrix</i> is especially important for its treatment of sympathy, celestial causality, and the relation between images and power. It assumes that the cosmos is not inert. Material forms can be tuned to heavenly forces, and ritual technique can assist that tuning. The work therefore sits at the intersection of natural philosophy and ritual technique, which is why modern scholars repeatedly return to it when discussing the boundary between astronomy, astrology, and magic. It is one of the clearest surviving texts for the learned astral imagination of the medieval Mediterranean world.</p>

    <h2>Transmission and Manuscript Context</h2>
    <p>The text reached Latin readers through Arabic-Latin transmission, a process that scholars such as David Pingree and Charles Burnett helped bring into sharper focus. That route matters because it means that the <i>Picatrix</i> cannot be understood as a purely Latin invention. It is a translation and transformation of an Arabic intellectual world in which philosophy, astrology, and ritual craft were already deeply entangled. Latin manuscript transmission then gave the work a long afterlife, especially in environments interested in astrology, image-making, and elite courtly knowledge. The text's circulation is therefore a story of translation as well as reception.</p>

    <p>Modern scholarship treats the Latin text as a witness to a larger Arabic tradition, not a transparent window onto a single original. Attrell and Porreca's translation has made the work accessible to a wider audience, while historians of Arabic science and astral magic continue to situate it within broader traditions of transmission and adaptation. The manuscript life of the <i>Picatrix</i> also explains its importance for the portal: it exemplifies how a text can move across languages and centuries while retaining enough structural coherence to shape later thinking about talismans and astral causality.</p>

    <h2>Classification and Controversy</h2>
    <p>The <i>Picatrix</i> has long been debated as a text of philosophy, astrology, natural magic, or image magic. The most useful answer is that it is all of these at once, but in historically specific ways. Medieval readers could use it to justify astral operations that they might otherwise have treated as suspect. That is why it matters to the history of <a href="../concepts/astral_image_magic.html">astral image magic</a>, <a href="../concepts/celestial_influence.html">celestial influence</a>, and <a href="../concepts/talismans.html">talismans</a>. It also helps explain why the category of <a href="../concepts/learned_magic.html">learned magic</a> is necessary: the text is learned, but the learning is in the service of operations that modern historians identify as magical.</p>

    <h2>Modern Scholarship</h2>
    <p>Pingree's work remains foundational for the Arabic-Latin transmission context. Burnett and other historians of translation have emphasized the intellectual pathways that allowed astral theory to move from Arabic into Latin. Attrell and Porreca's modern edition and translation have made the text usable in a new way, while Weill-Parot and Boudet have shown how it fits into larger medieval debates over image magic, astrology, and intellectual legitimacy. The <i>Picatrix</i> therefore functions as a bridge text: it links Arabic science, Latin scholastic classification, and the practical imagination of talismanic making.</p>

    <h2>Literature</h2>
    <p>Attrell, Dan, and David Porreca. <i>Picatrix: A Medieval Treatise on Astral Magic</i>. University Park: Pennsylvania State University Press, 2019.<br/>
    Burnett, Charles. Studies on Arabic-Latin translation and astral science in the medieval West.<br/>
    Klaassen, Frank. <i>The Transformations of Magic: Illicit Learned Magic in the Later Middle Ages and Renaissance</i>. University Park: Pennsylvania State University Press, 2013.<br/>
    Kieckhefer, Richard. <i>Magic in the Middle Ages</i>. Cambridge: Cambridge University Press, 2014.<br/>
    Pingree, David. Studies on the Arabic <i>Ghayat al-hakim</i> and its Latin transmission.<br/>
    Weill-Parot, Nicolas. Studies on astral image theory and the Latin reception of Arabic occult science.</p>
    """


def bio_solomon():
    return """
    <p>Solomon is a <b>biblical and legendary authority</b> rather than a historical medieval author, but his name became one of the most powerful attributional anchors in the history of medieval and early modern magic. As a figure in the biblical tradition, Solomon served as the paradigmatic wise king, builder, and judge; as a magical authority, he became the name under which spirit command, seals, ritual expertise, and the mastery of hidden knowledge could be legitimated. Medieval manuscripts and later print traditions repeatedly invoke Solomon to authorize texts that are in fact anonymous, composite, or heavily rewritten. His portal importance is therefore not biographical in the ordinary sense; it lies in the history of pseudepigraphy and ritual authority.</p>

    <h2>Sources and Historical Setting</h2>
    <p>The evidence for Solomon in medieval magic is textual, not historical in the narrow archival sense. The biblical Solomon, especially as mediated through the <i>Testament of Solomon</i>, becomes a template for commanding spirits and naming them. Later Solomonic grimoires, including the <i>Clavicula Salomonis</i>, the <i>Hygromanteia</i>, the <i>Lemegeton</i>, and related ritual families, use his authority to frame spirit conjuration as a form of inherited wisdom. The text history is therefore more important than any biography. Solomon is a point of convergence where biblical wisdom, demonological imagination, and manuscript authority meet. The figure also belongs to the wider Christian and Jewish reception of ancient wisdom, where canonical antiquity gives ritual texts an aura of legitimacy.</p>

    <h2>Texts and Attributions</h2>
    <p>Solomon is attached to a broad textual constellation: demonological catalogues, angelic and planetary conjurations, seals, exorcistic formulae, and ritual compendia that present themselves as repositories of secret wisdom. In these texts, attribution does not merely claim authorship. It constructs a ritual genealogy. A Solomonic text says, in effect, that the operations it contains are not ad hoc inventions but part of a transmitted ancient science. This is why Solomon matters for the study of <a href="../concepts/solomonic_magic.html">Solomonic magic</a>, <a href="../concepts/pseudepigraphy.html">pseudepigraphy</a>, and <a href="../concepts/grimoire_corpus.html">the grimoire corpus</a>. The authority of the name helps stabilize texts that are otherwise highly unstable in title and arrangement.</p>

    <h2>Significance for Medieval Magic</h2>
    <p>The Solomonic tradition is one of the main mechanisms by which medieval and early modern ritual books imagine continuity with a sacred past. Solomon's role in medieval magic is therefore double. First, he is a symbolic guarantor of legitimacy. Second, he is a narrative device that allows practitioners and compilers to situate their knowledge within a venerable line of ancient wisdom. That is why the figure also touches <a href="../concepts/secret_names.html">secret names</a>, <a href="../concepts/ritual_diagrams.html">ritual diagrams</a>, <a href="../concepts/planetary_spirits.html">planetary spirits</a>, and <a href="../concepts/angelic_invocation.html">angelic invocation</a>. The name Solomon signals that the text is operating in a world where authority is inherited, not merely invented.</p>

    <h2>Reception and Scholarly Debate</h2>
    <p>Modern scholars are careful not to confuse the biblical king with the later ritual traditions that bear his name. Kieckhefer, Klaassen, Fanger, Page, and Mesler all treat Solomonic attribution as a central feature of manuscript culture rather than as evidence of historical authorship. The real question is not whether Solomon wrote these texts, but why his name remained so effective across centuries and languages. His enduring power reveals the importance of attribute-based authority in the history of medieval and early modern learned magic.</p>

    <h2>Literature</h2>
    <p>Charlesworth, James H., ed. <i>The Old Testament Pseudepigrapha</i>. New York: Doubleday, 1983.<br/>
    Duling, Dennis C. "The Testament of Solomon." In <i>The Old Testament Pseudepigrapha</i>, edited by James H. Charlesworth. New York: Doubleday, 1983.<br/>
    Fanger, Claire. <i>Invoking Angels: Theurgic Ideas and Practices, Thirteenth to Sixteenth Centuries</i>. University Park: Pennsylvania State University Press, 2012.<br/>
    Kieckhefer, Richard. <i>Forbidden Rites: A Necromancer's Manual of the Fifteenth Century</i>. University Park: Pennsylvania State University Press, 1998.<br/>
    Klaassen, Frank. <i>The Transformations of Magic: Illicit Learned Magic in the Later Middle Ages and Renaissance</i>. University Park: Pennsylvania State University Press, 2013.<br/>
    Page, Sophie. <i>Magic in the Cloister: Pious Motives, Illicit Interests, and Occult Approaches to the Medieval Universe</i>. University Park: Pennsylvania State University Press, 2013.</p>
    """


def bio_roger_bacon():
    return """
    <p>Roger Bacon (c. 1214-c. 1292) was an English Franciscan philosopher and scholar whose discussions of experiment, optics, language, astrology, and natural causality made him one of the most important medieval thinkers for the study of the boundary between philosophy and magic. He was not a magician in any simple sense, but his work was repeatedly read through the lens of occult knowledge because he insisted on the practical, experimental, and mathematical investigation of nature. His place in MedievalMagicDB is therefore that of a medieval thinker whose writings helped define what later scholars have called the interface between natural philosophy and learned magic.</p>

    <h2>Works and Intellectual Context</h2>
    <p>Bacon's <i>Opus Majus</i>, along with related works on optics, language, and experimental inquiry, places him in the twelfth- and thirteenth-century movement toward disciplined natural knowledge. He drew on Arabic learning, especially in mathematics and astronomy, and he treated experiment as a necessary complement to reasoning. That position matters because medieval discussions of magic often turn on whether unusual effects can be explained through created nature, mathematical discipline, or hidden properties rather than demonic agency. Bacon's thought therefore belongs in the same intellectual landscape as <a href="../texts/de_radiis.html">De radiis</a>, <a href="../texts/speculum_astronomiae.html">Speculum astronomiae</a>, and the wider discussion of celestial influence and natural powers.</p>

    <h2>Hermetic Significance</h2>
    <p>Bacon is important to the portal not because he produced a grimoire, but because later readers used his name to frame the status of experiment, optics, and secret operations. In Thorndike's older historiography he helped populate a continuous history of magic and experimental science; in newer scholarship he is more carefully situated within scholastic debates over learning, translation, and the legitimacy of particular forms of knowledge. His concerns with mathematics, signs, and the operation of nature connect him to the problem of <a href="../concepts/mathematical_arts.html">mathematical arts</a> and <a href="../concepts/experimental_science.html">experimental science</a>. The point is not to collapse Bacon into magic, but to recognize that the medieval category of licit inquiry was itself unstable and often haunted by accusations of illicit curiosity.</p>

    <h2>Transmission and Scholarly Debate</h2>
    <p>Bacon's reception has been shaped heavily by modern historiography. Thorndike made him part of a larger documentary narrative of science and magic, while later historians have emphasized his position in Franciscan learning, the translation movement, and the history of method. Because the portal treats medieval magic as an analyst category, Bacon is best understood as a witness to the intellectual categories that made magic and science distinguishable in the first place. He stands for the serious medieval attempt to know nature through disciplined means, and for the equally serious medieval anxiety that disciplined means might cross into forbidden arts.</p>

    <h2>Literature</h2>
    <p>Bacon, Roger. <i>Opus Majus</i>. Primary text and scholarly editions.<br/>
    Hackett, Jeremiah. Studies on Roger Bacon and medieval science.<br/>
    Thorndike, Lynn. <i>A History of Magic and Experimental Science</i>. New York: Columbia University Press, 1923-1958.<br/>
    Kieckhefer, Richard. <i>Magic in the Middle Ages</i>. Cambridge: Cambridge University Press, 2014.<br/>
    Lindberg, David C. Studies on medieval optics, experiment, and the sciences.<br/>
    Weill-Parot, Nicolas. Studies on the relation between mathematics, astrology, and image magic.</p>
    """


def concept_witchcraft():
    return """
    <p><b>Witchcraft</b> is an <b>Analyst Term</b> for a historically contingent cluster of accusations, beliefs, and legal or theological constructions that crystallized in the later Middle Ages and early modern period. It does not map cleanly onto any single medieval self-description. Medieval actors used a range of terms, including <i>maleficium</i>, <i>superstitio</i>, and <i>nigromantia</i>, to classify harmful or suspect practices. Modern historians therefore use "witchcraft" as a retrospective category, while remaining alert to the specific vocabularies of pastoral care, demonology, and law.</p>

    <h2>Historical Usage</h2>
    <p>In medieval sources the practices that later scholars gather under witchcraft are often described piecemeal: one source condemns maleficium, another warns against charms, another associates harmful action with pact-making or demonic aid. The category becomes increasingly coherent in late medieval and early modern demonological writing, but its medieval roots are scattered across sermon literature, confession, canon law, and treatises on demons. This makes witchcraft a particularly good example of the portal's insistence that classification is historical work. The thing modern scholars call witchcraft is not a stable medieval object but a retrospective grouping of related accusations and anxieties.</p>

    <h2>Scholarly Significance</h2>
    <p>Michael D. Bailey has been especially important in showing how witchcraft belongs to wider histories of religion, superstition, and demonological classification. Richard Kieckhefer's work on magic and necromancy demonstrates that many practices later grouped under witchcraft also circulated in clerical or learned contexts. The category therefore has to be handled carefully. It overlaps with <a href="../concepts/maleficium.html">maleficium</a>, <a href="../concepts/demonology.html">demonology</a>, and <a href="../concepts/condemned_arts.html">condemned arts</a>, but it should not be flattened into them. Historiographically, witchcraft is one of the best examples of a category that is simultaneously indispensable and dangerous: indispensable because it names a real field of accusation and belief, dangerous because it can hide the heterogeneity of the sources.</p>

    <h2>Transmission and Variant Forms</h2>
    <p>The concept is shaped by the transmission of theological, legal, and pastoral texts, not by a single book. In the late Middle Ages, ideas about harmful ritual, demonic assistance, nocturnal flight, or pact-making travel through learned and vernacular genres and eventually harden into more systematic demonological formulations. The portal therefore treats witchcraft as a concept requiring relational context, not as an isolated entry. Its history is tied to the elaboration of demonology, the policing of superstition, and the consolidation of judicial and inquisitorial categories.</p>

    <h2>Related Concepts</h2>
    <p>Witchcraft overlaps with <a href="../concepts/maleficium.html">maleficium</a>, but the latter names harm more specifically. It also sits beside <a href="../concepts/nigromantia.html">nigromantia</a> and <a href="../concepts/necromancy.html">necromancy</a>, though those terms often concern learned ritual rather than popular accusation. It becomes meaningful in relation to <a href="../concepts/superstitio.html">superstitio</a> because clerical writers often classify suspect practices through the language of superstition and false religion.</p>

    <h2>Literature</h2>
    <p>Bailey, Michael D. <i>Magic and Superstition in Europe: A Concise History from Antiquity to the Present</i>. Lanham: Rowman &amp; Littlefield, 2007.<br/>
    Kieckhefer, Richard. <i>Magic in the Middle Ages</i>. Cambridge: Cambridge University Press, 2014.<br/>
    Kieckhefer, Richard. <i>Forbidden Rites: A Necromancer's Manual of the Fifteenth Century</i>. University Park: Pennsylvania State University Press, 1998.<br/>
    Page, Sophie, and Catherine Rider, eds. <i>The Routledge History of Medieval Magic</i>. London: Routledge, 2019.<br/>
    Thorndike, Lynn. <i>A History of Magic and Experimental Science</i>. New York: Columbia University Press, 1923-1958.</p>
    """


def main():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    upsert(conn, "concepts", "slug", {
        "slug": "ars_notoria",
        "label": "Ars Notoria",
        "definition_long": concept_ars_notoria(),
        "source_method": "CURATED_PROSE_BATCH_1",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    })
    upsert(conn, "texts", "text_id", {
        "text_id": "ars_notoria",
        "analysis_html": text_ars_notoria(),
        "source_method": "CURATED_PROSE_BATCH_1",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    })
    upsert(conn, "texts", "text_id", {
        "text_id": "picatrix",
        "analysis_html": text_picatrix(),
        "source_method": "CURATED_PROSE_BATCH_1",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    })
    upsert(conn, "persons", "person_id", {
        "person_id": "solomon",
        "bio_html": bio_solomon(),
        "source_method": "CURATED_PROSE_BATCH_1",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    })
    upsert(conn, "persons", "person_id", {
        "person_id": "roger_bacon",
        "bio_html": bio_roger_bacon(),
        "source_method": "CURATED_PROSE_BATCH_1",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    })
    upsert(conn, "concepts", "slug", {
        "slug": "witchcraft",
        "label": "Witchcraft",
        "definition_long": concept_witchcraft(),
        "source_method": "CURATED_PROSE_BATCH_1",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    })

    conn.commit()
    for table in ("persons", "texts", "concepts"):
        print(f"{table}: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()

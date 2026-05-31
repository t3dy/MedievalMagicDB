import sqlite3

from common import DB_PATH, ensure_dirs


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS texts (
    id INTEGER PRIMARY KEY,
    text_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    title_original TEXT,
    language TEXT CHECK(language IN ('ARABIC','LATIN','GREEK','HEBREW','ENGLISH','FRENCH','GERMAN','ITALIAN','SPANISH','MIXED','UNKNOWN') OR language IS NULL),
    text_type TEXT CHECK(text_type IN ('PRIMARY_SOURCE','GRIMOIRE','MANUSCRIPT_COMPILATION','TREATISE','SCHOLARSHIP','EDITION','TRANSLATION','ARTICLE','REVIEW','COLLECTION') OR text_type IS NULL),
    period TEXT CHECK(period IN ('LATE_ANTIQUE','MEDIEVAL','RENAISSANCE','EARLY_MODERN','MODERN','MIXED') OR period IS NULL),
    date_start INTEGER,
    date_end INTEGER,
    description TEXT,
    analysis_html TEXT,
    markdown_path TEXT,
    pdf_path TEXT,
    source_method TEXT DEFAULT 'SEED_DATA',
    review_status TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    person_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    name_alt TEXT,
    birth_year INTEGER,
    death_year INTEGER,
    era TEXT CHECK(era IN ('LATE_ANTIQUE','MEDIEVAL','RENAISSANCE','EARLY_MODERN','MODERN','UNKNOWN') OR era IS NULL),
    role_primary TEXT CHECK(role_primary IN ('SCHOLAR','AUTHOR','COMPILER','EDITOR','TRANSLATOR','THEOLOGIAN','PHILOSOPHER','PHYSICIAN','ASTROLOGER','MONK','CLERIC','LEGAL_ACTOR','ATTRIBUTED_AUTHORITY') OR role_primary IS NULL),
    scholar_group TEXT,
    description TEXT,
    bio_html TEXT,
    source_method TEXT DEFAULT 'SEED_DATA',
    review_status TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    label TEXT NOT NULL,
    label_alt TEXT,
    category TEXT CHECK(category IN ('RITUAL','ASTRAL','DEMONOLOGICAL','DIVINATORY','MANUSCRIPT','LEGAL','THEOLOGICAL','NATURAL_PHILOSOPHY','HISTORIOGRAPHICAL') OR category IS NULL),
    category_type TEXT CHECK(category_type IN ('ACTOR_TERM','ANALYST_TERM','HYBRID') OR category_type IS NULL),
    definition_short TEXT,
    definition_long TEXT,
    significance TEXT,
    source_method TEXT DEFAULT 'SEED_DATA',
    review_status TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

CREATE TABLE IF NOT EXISTS bibliography (
    id INTEGER PRIMARY KEY,
    source_id TEXT UNIQUE NOT NULL,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER,
    publisher TEXT,
    journal TEXT,
    pub_type TEXT CHECK(pub_type IN ('MONOGRAPH','ARTICLE','EDITION','TRANSLATION','COLLECTION','REVIEW','CHAPTER','MANUSCRIPT_STUDY') OR pub_type IS NULL),
    relevance TEXT CHECK(relevance IN ('PRIMARY','DIRECT','CONTEXTUAL','PERIPHERAL') OR relevance IS NULL),
    pdf_path TEXT,
    markdown_path TEXT,
    pages INTEGER,
    text_pages INTEGER,
    extraction_status TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS person_text_roles (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL REFERENCES persons(id),
    text_id INTEGER NOT NULL REFERENCES texts(id),
    role TEXT NOT NULL CHECK(role IN ('AUTHOR','ATTRIBUTED_AUTHOR','COMPILER','EDITOR','TRANSLATOR','SUBJECT','SCHOLAR_OF')),
    notes TEXT,
    confidence TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW')),
    UNIQUE(person_id, text_id, role)
);

CREATE TABLE IF NOT EXISTS concept_text_refs (
    id INTEGER PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id),
    text_id INTEGER NOT NULL REFERENCES texts(id),
    notes TEXT,
    UNIQUE(concept_id, text_id)
);

CREATE TABLE IF NOT EXISTS concept_links (
    id INTEGER PRIMARY KEY,
    from_concept_id INTEGER NOT NULL REFERENCES concepts(id),
    to_concept_id INTEGER NOT NULL REFERENCES concepts(id),
    relationship TEXT NOT NULL CHECK(relationship IN ('RELATED','CONTRASTED','PART_OF','BROADER','NARROWER','TRANSMITS')),
    notes TEXT,
    UNIQUE(from_concept_id, to_concept_id, relationship)
);

CREATE TABLE IF NOT EXISTS timeline_events (
    id INTEGER PRIMARY KEY,
    year INTEGER NOT NULL,
    year_end INTEGER,
    event_type TEXT CHECK(event_type IN ('COMPOSITION','TRANSLATION','MANUSCRIPT','TRIAL','CONDEMNATION','PUBLICATION','SCHOLARSHIP','EDITION') OR event_type IS NULL),
    title TEXT NOT NULL,
    description TEXT,
    person_id INTEGER REFERENCES persons(id),
    text_id INTEGER REFERENCES texts(id),
    bib_id INTEGER REFERENCES bibliography(id),
    location TEXT,
    latitude REAL,
    longitude REAL,
    section_tag TEXT,
    confidence TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now')),
    description TEXT
);
"""


def main():
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.execute(
        "INSERT OR IGNORE INTO schema_version (version, description) VALUES (?, ?)",
        (1, "Initial MedievalMagicDB schema"),
    )
    conn.commit()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    print(f"Database: {DB_PATH}")
    print(f"Tables: {len(tables)}")
    for (table,) in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0]
        print(f"  {table}: {count}")
    conn.close()


if __name__ == "__main__":
    main()

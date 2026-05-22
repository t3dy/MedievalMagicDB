import re
import sqlite3
import sys

from common import DB_PATH, SITE_DIR


ENUMS = {
    ("texts", "text_type"): {'PRIMARY_SOURCE','GRIMOIRE','MANUSCRIPT_COMPILATION','TREATISE','SCHOLARSHIP','EDITION','TRANSLATION','ARTICLE','REVIEW','COLLECTION', None},
    ("texts", "period"): {'LATE_ANTIQUE','MEDIEVAL','RENAISSANCE','EARLY_MODERN','MODERN','MIXED', None},
    ("persons", "role_primary"): {'SCHOLAR','AUTHOR','COMPILER','EDITOR','TRANSLATOR','THEOLOGIAN','PHILOSOPHER','PHYSICIAN','ASTROLOGER','MONK','CLERIC','LEGAL_ACTOR','ATTRIBUTED_AUTHORITY', None},
    ("persons", "era"): {'LATE_ANTIQUE','MEDIEVAL','RENAISSANCE','EARLY_MODERN','MODERN','UNKNOWN', None},
    ("concepts", "category_type"): {'ACTOR_TERM','ANALYST_TERM','HYBRID', None},
    ("bibliography", "pub_type"): {'MONOGRAPH','ARTICLE','EDITION','TRANSLATION','COLLECTION','REVIEW','CHAPTER','MANUSCRIPT_STUDY', None},
}


def structural():
    errors = []
    if not DB_PATH.exists():
        return [f"Missing database: {DB_PATH}"]
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    for violation in conn.execute("PRAGMA foreign_key_check").fetchall():
        errors.append(f"FK violation: {violation}")
    for (table, column), allowed in ENUMS.items():
        for (value,) in conn.execute(f"SELECT DISTINCT {column} FROM {table}").fetchall():
            if value not in allowed:
                errors.append(f"Invalid enum {table}.{column}: {value}")
    required = [("texts", "text_id"), ("texts", "title"), ("persons", "person_id"), ("persons", "name"), ("concepts", "slug"), ("concepts", "label"), ("bibliography", "source_id")]
    for table, column in required:
        count = conn.execute(f"SELECT COUNT(*) FROM {table} WHERE {column} IS NULL OR {column}=''" ).fetchone()[0]
        if count:
            errors.append(f"Missing {table}.{column}: {count}")
    print("Row counts:")
    for (table,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall():
        print(f"  {table}: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
    conn.close()
    return errors


def site_links():
    errors = []
    if not SITE_DIR.exists():
        return [f"Missing site directory: {SITE_DIR}"]
    html_files = list(SITE_DIR.rglob("*.html"))
    if not html_files:
        return ["No generated HTML files found."]
    pattern = re.compile(r"""(?:href|src)=['"]([^'"]+)['"]""")
    for file_path in html_files:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        for match in pattern.finditer(text):
            ref = match.group(1)
            if ref.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (file_path.parent / ref).resolve()
            if not target.exists():
                errors.append(f"Broken link: {file_path.relative_to(SITE_DIR)} -> {ref}")
    return errors


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--all"
    errors = []
    if mode in ("--all", "--structural"):
        errors.extend(structural())
    if mode in ("--all", "--site"):
        errors.extend(site_links())
    if errors:
        print(f"VALIDATION FAILED: {len(errors)} errors")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "medieval_magic.db"
DOCS_DIR = BASE_DIR / "docs"
SITE_DIR = BASE_DIR / "site"
PDF_SOURCE_DIR = Path(r"E:\pdf\magic\medieval magic")
MARKDOWN_DIR = BASE_DIR / "sources" / "markdown"
METADATA_DIR = BASE_DIR / "sources" / "metadata"
MANIFEST_PATH = METADATA_DIR / "pdf_manifest.json"


def ensure_dirs():
    for path in (DB_DIR, DOCS_DIR, SITE_DIR, MARKDOWN_DIR, METADATA_DIR, BASE_DIR / "staging"):
        path.mkdir(parents=True, exist_ok=True)

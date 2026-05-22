import json
import re
import argparse
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import fitz

from common import MANIFEST_PATH, MARKDOWN_DIR, PDF_SOURCE_DIR, METADATA_DIR, ensure_dirs

MIN_CHARS_PER_PAGE = 50


def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:96] or "source"


SUPPORTED_EXTENSIONS = {".pdf", ".epub", ".djvu"}
SKIP_EXTENSIONS = {".crdownload", ".tmp", ".part"}


def guess_title(path):
    stem = path.stem.replace("_", " ")
    stem = re.sub(r"\s+-\s+libgen\.li$", "", stem, flags=re.I)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem[:220]


def detected_suffix(source_path):
    suffix = source_path.suffix.lower()
    if suffix:
        return suffix
    try:
        header = source_path.read_bytes()[:16]
    except OSError:
        return suffix
    if header.startswith(b"%PDF-"):
        return ".pdf"
    if header.startswith(b"AT&TFORM"):
        return ".djvu"
    return suffix


def extract_document(source_path, source_dir, force=False):
    suffix = detected_suffix(source_path)
    if suffix in SKIP_EXTENSIONS:
        return {
            "status": "skipped_incomplete",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "title_guess": guess_title(source_path),
            "reason": f"Skipped incomplete download file with extension {suffix}.",
        }
    if suffix not in SUPPORTED_EXTENSIONS:
        reason = f"No converter is configured for {suffix}."
        if suffix == ".djvu":
            reason = (
                "DjVu file detected. This file may contain TXTz text chunks, but TXTz uses "
                "DjVuLibre BZZ compression, which is not decodable by Python stdlib or the "
                "current PyMuPDF build. Install DjVuLibre/djvutxt or add a BZZ decoder."
            )
        return {
            "status": "unsupported",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "title_guess": guess_title(source_path),
            "reason": reason,
        }

    corpus_slug = slugify(source_dir.name)
    slug = slugify(source_path.stem)
    md_path = MARKDOWN_DIR / f"{slug}.md"
    if md_path.exists() and not force:
        return {
            "status": "skipped",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "markdown_path": str(md_path),
            "title_guess": guess_title(source_path),
        }

    if suffix == ".djvu":
        return extract_djvu(source_path, source_dir, md_path, force=force)

    try:
        doc = fitz.open(str(source_path))
    except Exception as exc:
        return {
            "status": "error",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "title_guess": guess_title(source_path),
            "error": str(exc),
        }

    page_count = len(doc)
    text_pages = 0
    empty_pages = 0
    chunks = [
        f"# {guess_title(source_path)}",
        "",
        f"Source file: `{source_path.name}`",
        f"Source folder: `{source_dir}`",
        f"Corpus: `{corpus_slug}`",
        f"Converted: {datetime.now().isoformat(timespec='seconds')}",
        "",
    ]
    for index in range(page_count):
        page_text = doc[index].get_text("text").strip()
        if len(page_text) >= MIN_CHARS_PER_PAGE:
            text_pages += 1
            chunks.append(f"## Page {index + 1}")
            chunks.append("")
            chunks.append(page_text)
            chunks.append("")
        else:
            empty_pages += 1
    doc.close()

    if text_pages == 0:
        return {
            "status": "scanned",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "title_guess": guess_title(source_path),
            "pages": page_count,
            "text_pages": text_pages,
            "empty_pages": empty_pages,
        }

    md_path.write_text("\n".join(chunks), encoding="utf-8")
    return {
        "status": "converted",
        "source_path": str(source_path),
        "pdf_path": str(source_path),
        "markdown_path": str(md_path),
        "title_guess": guess_title(source_path),
        "pages": page_count,
        "text_pages": text_pages,
        "empty_pages": empty_pages,
        "size_bytes": source_path.stat().st_size,
    }


def extract_djvu(source_path, source_dir, md_path, force=False):
    if md_path.exists() and not force:
        return {
            "status": "skipped",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "markdown_path": str(md_path),
            "title_guess": guess_title(source_path),
        }

    djvutxt = shutil.which("djvutxt")
    if not djvutxt:
        return {
            "status": "unsupported",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "title_guess": guess_title(source_path),
            "reason": (
                "DjVu file detected, but djvutxt was not found on PATH. The file contains TXTz text chunks "
                "that require DjVuLibre BZZ decoding; Python stdlib and this PyMuPDF build cannot decode them."
            ),
        }

    try:
        proc = subprocess.run(
            [djvutxt, str(source_path)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception as exc:
        return {
            "status": "error",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "title_guess": guess_title(source_path),
            "error": str(exc),
        }

    text = proc.stdout.strip()
    if len(text) < MIN_CHARS_PER_PAGE:
        return {
            "status": "scanned",
            "source_path": str(source_path),
            "pdf_path": str(source_path),
            "title_guess": guess_title(source_path),
            "reason": "djvutxt ran but returned too little text.",
        }

    chunks = [
        f"# {guess_title(source_path)}",
        "",
        f"Source file: `{source_path.name}`",
        f"Source folder: `{source_dir}`",
        "Converted with: `djvutxt`",
        f"Converted: {datetime.now().isoformat(timespec='seconds')}",
        "",
        text,
        "",
    ]
    md_path.write_text("\n".join(chunks), encoding="utf-8")
    return {
        "status": "converted",
        "source_path": str(source_path),
        "pdf_path": str(source_path),
        "markdown_path": str(md_path),
        "title_guess": guess_title(source_path),
        "pages": None,
        "text_pages": None,
        "empty_pages": None,
        "size_bytes": source_path.stat().st_size,
    }


def main():
    ensure_dirs()
    parser = argparse.ArgumentParser(description="Convert local medieval magic source files to Markdown.")
    parser.add_argument("--source-dir", default=str(PDF_SOURCE_DIR), help="Folder containing source PDFs/EPUBs.")
    parser.add_argument("--source-file", help="Convert one explicit source file.")
    parser.add_argument("--manifest", default=str(MANIFEST_PATH), help="Manifest JSON output path.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing Markdown files.")
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = METADATA_DIR / manifest_path

    if args.source_file:
        source_file = Path(args.source_file)
        source_dir = source_file.parent
        sources = [source_file]
    else:
        sources = sorted(p for p in source_dir.iterdir() if p.is_file())
    results = []
    print(f"Found {len(sources)} source files in {source_dir}")
    for index, source_path in enumerate(sources, 1):
        print(f"[{index}/{len(sources)}] {source_path.name[:100]}")
        result = extract_document(source_path, source_dir, force=args.force)
        results.append(result)
        print(f"  {result['status']}")

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Manifest: {manifest_path}")
    print(f"Converted: {sum(1 for r in results if r['status'] == 'converted')}")
    print(f"Skipped: {sum(1 for r in results if r['status'] == 'skipped')}")
    print(f"Skipped incomplete: {sum(1 for r in results if r['status'] == 'skipped_incomplete')}")
    print(f"Scanned: {sum(1 for r in results if r['status'] == 'scanned')}")
    print(f"Unsupported: {sum(1 for r in results if r['status'] == 'unsupported')}")
    print(f"Errors: {sum(1 for r in results if r['status'] == 'error')}")


if __name__ == "__main__":
    main()

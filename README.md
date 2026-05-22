# MedievalMagicDB

**Website:** [https://t3dy.github.io/MedievalMagicDB/](https://t3dy.github.io/MedievalMagicDB/)

MedievalMagicDB is a scholarly knowledge portal for medieval magic, learned ritual practice, astral image magic, necromancy, angelic theurgy, grimoires, ecclesiastical critique, manuscript transmission, and modern historiography.

The project follows the EmeraldTablet framework: SQLite as the source of truth, idempotent Python ingestion scripts, Markdown source extraction for token-efficient research, staged JSON enrichment, and static HTML generated into `docs/` and `site/`.

## Quick Start

```powershell
python .\scripts\convert_pdfs_to_md.py
python .\scripts\init_db.py
python .\scripts\seed_from_manifest.py
python .\scripts\deploy_portal.py
python .\scripts\validate.py
```

## Corpus

PDFs are read from:

`E:\pdf\magic\medieval magic`

Markdown extractions are written to:

`sources\markdown`

Conversion metadata is written to:

`sources\metadata\pdf_manifest.json`

## Method

This portal treats "medieval magic" as an analyst category, not a medieval actor's self-description. Entries distinguish between clerical condemnation, learned natural philosophy, ritual experiment, astral image theory, divination, demonic magic, and modern categories such as "grimoire" or "necromancy."

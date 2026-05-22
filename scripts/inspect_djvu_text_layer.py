import json
import struct
import sys
from pathlib import Path

from common import BASE_DIR


def inspect(path):
    data = Path(path).read_bytes()
    markers = {}
    for marker in (b"FORM", b"DJVM", b"DJVU", b"TXTz", b"TXTa", b"Sjbz", b"Djbz"):
        markers[marker.decode("ascii")] = {
            "first_offset": data.find(marker),
            "count": data.count(marker),
        }

    txtz_chunks = []
    pos = 0
    while True:
        pos = data.find(b"TXTz", pos)
        if pos == -1:
            break
        size = struct.unpack(">I", data[pos + 4 : pos + 8])[0] if pos + 8 <= len(data) else None
        txtz_chunks.append({"offset": pos, "size": size})
        pos += 4

    return {
        "path": str(path),
        "size_bytes": len(data),
        "markers": markers,
        "txtz_chunk_count": len(txtz_chunks),
        "sample_txtz_chunks": txtz_chunks[:10],
        "conversion_note": (
            "TXTz chunks indicate an embedded text layer, but the payload is DjVuLibre BZZ-compressed. "
            "Python stdlib zlib cannot decode it, and this PyMuPDF build has no DjVu handler. "
            "Install DjVuLibre tools and run djvutxt, or add a BZZ decoder, to convert this file."
        ),
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/inspect_djvu_text_layer.py <file.djvu>")
    report = inspect(sys.argv[1])
    out = BASE_DIR / "sources" / "metadata" / "djvu_inspection_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

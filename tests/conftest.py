from __future__ import annotations

import zipfile
from pathlib import Path


def make_pdf(path: Path, pages: list[str]) -> None:
    """Minimal text PDF compatible with pypdf."""
    objs: dict[int, str] = {}
    page_nums: list[int] = []
    streams: list[tuple[int, str]] = []

    base = 3
    for i, text in enumerate(pages):
        sn = base + i * 2
        pn = base + i * 2 + 1
        streams.append((sn, f"BT /F1 12 Tf 50 700 Td ({text}) Tj ET"))
        page_nums.append(pn)

    objs[1] = "<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{n} 0 R" for n in page_nums)
    objs[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>"
    font = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    resources = f"<< /Font << /F1 {font} >> >>"

    for sn, data in streams:
        bdata = data.encode("latin-1")
        pn = sn + 1
        objs[sn] = f"<< /Length {len(bdata)} >>\nstream\n{data}\nendstream"
        objs[pn] = (
            f"<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 612 792] "
            f"/Contents {sn} 0 R "
            f"/Resources {resources} >>"
        )

    buf = b"%PDF-1.4\n"
    offsets: dict[int, int] = {}
    for n in sorted(objs):
        offsets[n] = len(buf)
        buf += f"{n} 0 obj\n{objs[n]}\nendobj\n".encode("latin-1")

    xref_pos = len(buf)
    count = max(objs) + 1
    buf += f"xref\n0 {count}\n".encode()
    buf += b"0000000000 65535 f \n"
    for n in range(1, count):
        buf += f"{offsets.get(n, 0):010d} 00000 n \n".encode()
    buf += f"trailer\n<< /Size {count} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode()
    path.write_bytes(buf)


def make_epub(path: Path, chapters: list[tuple[str, str]]) -> None:
    """Crear un EPUB mínimo con spine en orden."""
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr(
            "META-INF/container.xml",
            '<?xml version="1.0"?>'
            '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            '<rootfiles><rootfile full-path="content.opf"'
            ' media-type="application/oebps-package+xml"/></rootfiles></container>',
        )
        item_entries = "".join(
            f'<item id="ch{i}" href="ch{i}.xhtml" media-type="application/xhtml+xml"/>'
            for i in range(len(chapters))
        )
        spine_entries = "".join(
            f'<itemref idref="ch{i}"/>' for i in range(len(chapters))
        )
        opf = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<package xmlns="http://www.idpf.org/2007/opf"'
            ' xmlns:dc="http://purl.org/dc/elements/1.1/" version="2.0">'
            "<metadata>"
            "<dc:title>Test Book</dc:title>"
            "<dc:language>es</dc:language>"
            "</metadata>"
            f"<manifest>{item_entries}</manifest>"
            f"<spine>{spine_entries}</spine>"
            "</package>"
        )
        zf.writestr("content.opf", opf)
        for i, (title, body) in enumerate(chapters):
            xhtml = (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<html xmlns="http://www.w3.org/1999/xhtml"><head>'
                f"<title>{title}</title></head><body>"
                f"<h1>{title}</h1><p>{body}</p></body></html>"
            )
            zf.writestr(f"ch{i}.xhtml", xhtml)

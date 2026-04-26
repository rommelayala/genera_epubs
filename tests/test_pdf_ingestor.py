from __future__ import annotations

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.pdf_ingestor import PdfIngestor


def _create_text_pdf(path: Path, page_texts: list[str]) -> None:
    """Create a minimal valid PDF with one text line per page."""
    objects: list[str] = []

    def obj(n: int, content: str) -> None:
        while len(objects) < n:
            objects.append("")
        objects[n - 1] = content

    streams: list[str] = []
    page_obj_nums: list[int] = []

    base = 3  # objects 1=catalog, 2=pages, then pages+streams
    for i, text in enumerate(page_texts):
        stream_data = f"BT /F1 12 Tf 50 700 Td ({text}) Tj ET"
        stream_num = base + i * 2
        page_num = base + i * 2 + 1
        streams.append((stream_num, stream_data))
        page_obj_nums.append(page_num)

    all_objs: dict[int, str] = {}
    all_objs[1] = f"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{n} 0 R" for n in page_obj_nums)
    all_objs[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_texts)} >>"

    font_def = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    resources = f"<< /Font << /F1 {font_def} >> >>"

    for stream_num, stream_data in streams:
        data_bytes = stream_data.encode("latin-1")
        all_objs[stream_num] = f"<< /Length {len(data_bytes)} >>\nstream\n{stream_data}\nendstream"

    for i, page_num in enumerate(page_obj_nums):
        stream_num = base + i * 2
        all_objs[page_num] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources {resources} /Contents {stream_num} 0 R >>"
        )

    lines: list[str] = ["%PDF-1.4\n"]
    offsets: dict[int, int] = {}
    for n in sorted(all_objs):
        offsets[n] = sum(len(l.encode("latin-1")) for l in lines)
        lines.append(f"{n} 0 obj\n{all_objs[n]}\nendobj\n")

    xref_offset = sum(len(l.encode("latin-1")) for l in lines)
    count = max(all_objs) + 1
    lines.append("xref\n")
    lines.append(f"0 {count}\n")
    lines.append("0000000000 65535 f \n")
    for n in range(1, count):
        off = offsets.get(n, 0)
        lines.append(f"{off:010d} 00000 n \n")
    lines.append("trailer\n")
    lines.append(f"<< /Size {count} /Root 1 0 R >>\n")
    lines.append("startxref\n")
    lines.append(f"{xref_offset}\n")
    lines.append("%%EOF\n")

    path.write_bytes("".join(lines).encode("latin-1"))


@pytest.fixture
def pdf_path(tmp_path: Path) -> Path:
    path = tmp_path / "sample.pdf"
    _create_text_pdf(path, ["Page one content.", "Page two content.", "Page three content."])
    return path


@pytest.fixture
def ingestor() -> PdfIngestor:
    return PdfIngestor()


def test_pdf_ingestor_extracts_text(ingestor: PdfIngestor, pdf_path: Path) -> None:
    source = SourceConfig(type="pdf", path=str(pdf_path))
    result = ingestor.extract(source, pdf_path.parent)
    assert "Page one content." in result
    assert "Page two content." in result
    assert "Page three content." in result


def test_pdf_ingestor_pages_joined(ingestor: PdfIngestor, pdf_path: Path) -> None:
    source = SourceConfig(type="pdf", path=str(pdf_path))
    result = ingestor.extract(source, pdf_path.parent)
    assert "\n\n" in result


def test_pdf_ingestor_skips_blank_pages(ingestor: PdfIngestor, tmp_path: Path) -> None:
    """A PDF with no text yields empty string without raising."""
    path = tmp_path / "blank.pdf"
    _create_text_pdf(path, [])

    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with open(path, "wb") as f:
        writer.write(f)

    source = SourceConfig(type="pdf", path=str(path))
    result = ingestor.extract(source, tmp_path)
    assert result == ""


def test_pdf_ingestor_registered() -> None:
    from epub_generator.ingestors import INGESTORS
    assert "pdf" in INGESTORS
    assert INGESTORS["pdf"] is PdfIngestor

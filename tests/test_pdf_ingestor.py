from __future__ import annotations

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.pdf_ingestor import PdfIngestor
from tests.conftest import make_pdf as _create_text_pdf


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

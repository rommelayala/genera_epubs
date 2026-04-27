"""Tests para EpubIngestor — retorna str Markdown usando ebooklib."""
from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.epub_ingestor import EpubIngestor
from epub_generator.ingestors import INGESTORS


def _make_epub(path: Path, chapters: list[tuple[str, str]]) -> None:
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


def test_extract_returns_str(tmp_path: Path) -> None:
    """extract() retorna str."""
    epub_path = tmp_path / "sample.epub"
    _make_epub(epub_path, [("Cap 1", "Contenido del primer capítulo.")])

    ingestor = EpubIngestor()
    source = SourceConfig(type="epub", path=str(epub_path))
    result = ingestor.extract(source, tmp_path)

    assert isinstance(result, str)
    assert result.strip() != ""


def test_extract_two_chapters_in_order(tmp_path: Path) -> None:
    """Capítulos se extraen en orden del spine."""
    epub_path = tmp_path / "sample.epub"
    _make_epub(
        epub_path,
        [
            ("Introducción", "Primer contenido."),
            ("Desarrollo", "Segundo contenido."),
        ],
    )

    ingestor = EpubIngestor()
    source = SourceConfig(type="epub", path=str(epub_path))
    result = ingestor.extract(source, tmp_path)

    idx1 = result.find("Introducción")
    idx2 = result.find("Desarrollo")
    assert idx1 != -1
    assert idx2 != -1
    assert idx1 < idx2, "Introducción debe aparecer antes de Desarrollo"


def test_nonexistent_file_raises(tmp_path: Path) -> None:
    """FileNotFoundError si el path no existe."""
    ingestor = EpubIngestor()
    source = SourceConfig(type="epub", path=str(tmp_path / "missing.epub"))
    with pytest.raises(FileNotFoundError):
        ingestor.extract(source, tmp_path)


def test_registered_in_ingestors() -> None:
    """EpubIngestor está registrado en INGESTORS['epub']."""
    assert "epub" in INGESTORS
    assert INGESTORS["epub"] is EpubIngestor

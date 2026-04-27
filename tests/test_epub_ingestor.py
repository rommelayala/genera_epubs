"""Tests para EpubIngestor — retorna str Markdown usando ebooklib."""
from __future__ import annotations

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.epub_ingestor import EpubIngestor
from epub_generator.ingestors import INGESTORS
from tests.conftest import make_epub


@pytest.fixture()
def ingestor() -> EpubIngestor:
    return EpubIngestor()


def test_extract_two_chapters_in_order(ingestor: EpubIngestor, tmp_path: Path) -> None:
    """Capítulos se extraen en orden del spine y retorna str no vacío."""
    epub_path = tmp_path / "sample.epub"
    make_epub(
        epub_path,
        [
            ("Introducción", "Primer contenido."),
            ("Desarrollo", "Segundo contenido."),
        ],
    )

    source = SourceConfig(type="epub", path=str(epub_path))
    result = ingestor.extract(source, tmp_path)

    assert isinstance(result, str)
    assert result.strip() != ""
    idx1 = result.find("Introducción")
    idx2 = result.find("Desarrollo")
    assert idx1 != -1
    assert idx2 != -1
    assert idx1 < idx2, "Introducción debe aparecer antes de Desarrollo"


def test_nonexistent_file_raises(ingestor: EpubIngestor, tmp_path: Path) -> None:
    """FileNotFoundError si el path no existe."""
    source = SourceConfig(type="epub", path=str(tmp_path / "missing.epub"))
    with pytest.raises(FileNotFoundError):
        ingestor.extract(source, tmp_path)


def test_registered_in_ingestors() -> None:
    """EpubIngestor está registrado en INGESTORS['epub']."""
    assert "epub" in INGESTORS
    assert INGESTORS["epub"] is EpubIngestor

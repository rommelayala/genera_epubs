"""
Tests para HtmlIngestor
"""

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.html_ingestor import HtmlIngestor


@pytest.fixture
def html_ingestor():
    """Crear instancia de HtmlIngestor."""
    return HtmlIngestor()


@pytest.mark.parametrize("input_file", ["tests/prueba.html", "tests/test.html"])
def test_html_ingestor_basic(html_ingestor, input_file):
    """Test básico de HtmlIngestor."""
    config = SourceConfig(path=input_file)

    try:
        metadata, chapters = html_ingestor.extract(config, Path.cwd())

        assert metadata is not None
        assert isinstance(metadata, dict)

        # Verificar que se extrajeron metadatos básicos
        assert "title" in metadata
        assert "author" in metadata or metadata["author"] is None
        assert "language" in metadata

        # Verificar que se extrajeron capítulos
        assert "chapters" in metadata
        assert len(metadata["chapters"]) > 0

    except FileNotFoundError:
        # Si el archivo no existe, el test se salta
        pytest.skip(f"Archivo no encontrado: {input_file}")


def test_html_ingestor_no_file():
    """Test cuando no hay archivos HTML en el directorio."""
    ingestor = HtmlIngestor()

    # Intentar extraer de archivo no existente
    with pytest.raises(FileNotFoundError):
        config = SourceConfig(path="nonexistent.html")
        ingestor.extract(config, Path.cwd())

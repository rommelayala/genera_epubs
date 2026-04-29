"""
Tests para TextIngestor
"""

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.text_ingestor import TextIngestor


@pytest.fixture
def text_ingestor():
    """Crear instancia de TextIngestor."""
    return TextIngestor()


@pytest.mark.parametrize("input_file", ["tests/prueba.txt", "tests/test.txt"])
def test_text_ingestor_basic(text_ingestor, input_file):
    """Test básico de TextIngestor."""
    config = SourceConfig(path=input_file)

    try:
        metadata, chapters = text_ingestor.extract(config, Path.cwd())

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


def test_text_ingestor_no_file():
    """Test cuando no hay archivos de texto en el directorio."""
    ingestor = TextIngestor()

    # Intentar extraer de archivo no existente
    with pytest.raises(FileNotFoundError):
        config = SourceConfig(path="nonexistent.txt")
        ingestor.extract(config, Path.cwd())

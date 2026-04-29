"""
Tests para WordIngestor
"""

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.word_ingestor import WordIngestor


@pytest.fixture
def word_ingestor():
    """Crear instancia de WordIngestor."""
    return WordIngestor()


@pytest.mark.parametrize("input_file", ["tests/test.docx", "tests/prueba.docx"])
def test_word_ingestor_basic(word_ingestor, input_file):
    """Test básico de WordIngestor."""
    config = SourceConfig(path=input_file)

    try:
        metadata, chapters = word_ingestor.extract(config, Path.cwd())

        assert metadata is not None
        assert isinstance(metadata, dict)

        # Verificar que se extrajeron metadatos básicos
        assert "title" in metadata
        assert isinstance(metadata["title"], str)

    except FileNotFoundError:
        # Si el archivo no existe, el test se salta
        pytest.skip(f"Archivo no encontrado: {input_file}")


def test_word_ingestor_no_file():
    """Test cuando no hay archivos Word en el directorio."""
    ingestor = WordIngestor()

    # Intentar extraer de archivo no existente
    with pytest.raises(FileNotFoundError):
        config = SourceConfig(path="nonexistent.docx")
        ingestor.extract(config, Path.cwd())

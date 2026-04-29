"""
Tests para NcxIngestor
"""

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.ncx_ingestor import NcxIngestor


@pytest.fixture
def ncx_ingestor():
    """Crear instancia de NcxIngestor."""
    return NcxIngestor()


@pytest.mark.parametrize("input_file", ["tests/prueba.ncx", "tests/test.ncx"])
def test_ncx_ingestor_basic(ncx_ingestor, input_file):
    """Test básico de NcxIngestor."""
    config = SourceConfig(path=input_file)

    try:
        metadata, chapters = ncx_ingestor.extract(config, Path.cwd())

        assert metadata is not None
        assert isinstance(metadata, dict)

        # Verificar que se extrajeron metadatos básicos
        assert "title" in metadata
        assert "author" in metadata or metadata["author"] is None
        assert "language" in metadata

        # Verificar que se extrajeron capítulos
        assert "chapters" in metadata

    except FileNotFoundError:
        # Si el archivo no existe, el test se salta
        pytest.skip(f"Archivo no encontrado: {input_file}")


def test_ncx_ingestor_no_file():
    """Test cuando no hay archivos NCX en el directorio."""
    ingestor = NcxIngestor()

    # Intentar extraer de archivo no existente
    with pytest.raises(FileNotFoundError):
        config = SourceConfig(path="nonexistent.ncx")
        ingestor.extract(config, Path.cwd())

"""
Tests para OpfIngestor
"""

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.opf_ingestor import OpfIngestor


@pytest.fixture
def opf_ingestor():
    """Crear instancia de OpfIngestor."""
    return OpfIngestor()


@pytest.mark.parametrize("input_file", ["tests/prueba.opf", "tests/test.opf"])
def test_opf_ingestor_basic(opf_ingestor, input_file):
    """Test básico de OpfIngestor."""
    config = SourceConfig(path=input_file)

    try:
        metadata, chapters = opf_ingestor.extract(config, Path.cwd())

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


def test_opf_ingestor_no_file():
    """Test cuando no hay archivos OPF en el directorio."""
    ingestor = OpfIngestor()

    # Intentar extraer de archivo no existente
    with pytest.raises(FileNotFoundError):
        config = SourceConfig(path="nonexistent.opf")
        ingestor.extract(config, Path.cwd())

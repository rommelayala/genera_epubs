from __future__ import annotations

from pathlib import Path

import pytest

from epub_generator.config import SourceConfig
from epub_generator.ingestors.markdown_ingestor import MarkdownIngestor


@pytest.fixture
def ingestor() -> MarkdownIngestor:
    return MarkdownIngestor()


def test_markdown_ingestor_returns_content(ingestor: MarkdownIngestor, tmp_path: Path) -> None:
    sample = tmp_path / "sample.md"
    sample.write_text("# Hello\n\nWorld content here.\n", encoding="utf-8")
    source = SourceConfig(type="markdown", path=str(sample))
    result = ingestor.extract(source, tmp_path)
    assert result == "# Hello\n\nWorld content here.\n"


def test_markdown_ingestor_utf8(ingestor: MarkdownIngestor, tmp_path: Path) -> None:
    sample = tmp_path / "sample.md"
    content = "# Título\n\nContenido con acentos: áéíóú\n"
    sample.write_text(content, encoding="utf-8")
    source = SourceConfig(type="markdown", path=str(sample))
    result = ingestor.extract(source, tmp_path)
    assert result == content


def test_markdown_ingestor_registered() -> None:
    from epub_generator.ingestors import INGESTORS
    assert "markdown" in INGESTORS
    assert INGESTORS["markdown"] is MarkdownIngestor

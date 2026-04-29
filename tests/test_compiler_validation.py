from __future__ import annotations

from pathlib import Path

import pytest

from epub_generator.compiler import compile_book
from epub_generator.config import BookConfig, SourceConfig


def test_empty_sources() -> None:
    config = BookConfig()
    with pytest.raises(ValueError, match="No hay sources definidos"):
        compile_book(config, "test")


def test_invalid_type(tmp_path: Path) -> None:
    config = BookConfig(sources=[SourceConfig(type="unknown", path="x.md")])
    with pytest.raises(ValueError, match="tipo 'unknown' no reconocido"):
        compile_book(config, "test", project_root=tmp_path)


def test_missing_path_field(tmp_path: Path) -> None:
    config = BookConfig(sources=[SourceConfig(type="markdown", path="")])
    with pytest.raises(ValueError, match="requiere campo 'path'"):
        compile_book(config, "test", project_root=tmp_path)


def test_missing_path_field_pdf(tmp_path: Path) -> None:
    config = BookConfig(sources=[SourceConfig(type="pdf", path="")])
    with pytest.raises(ValueError, match="requiere campo 'path'"):
        compile_book(config, "test", project_root=tmp_path)


def test_nonexistent_path(tmp_path: Path) -> None:
    config = BookConfig(
        sources=[SourceConfig(type="markdown", path="nonexistent.md")]
    )
    with pytest.raises(ValueError, match="no encontrado"):
        compile_book(config, "test", project_root=tmp_path)


def test_valid_sources_pass_validation(tmp_path: Path) -> None:
    md_file = tmp_path / "chapter.md"
    md_file.write_text("# Hello", encoding="utf-8")
    config = BookConfig(
        sources=[SourceConfig(type="markdown", path=str(md_file))]
    )
    # Validation passes - compile_book() now supports markdown
    result = compile_book(config, "test", project_root=tmp_path)
    assert result is not None


def test_error_message_includes_index(tmp_path: Path) -> None:
    config = BookConfig(
        sources=[
            SourceConfig(type="markdown", path=str(tmp_path / "exists.md")),
            SourceConfig(type="unknown", path="x.md"),
        ]
    )
    (tmp_path / "exists.md").write_text("# ok", encoding="utf-8")
    with pytest.raises(ValueError, match=r"Source\[1\]"):
        compile_book(config, "test", project_root=tmp_path)

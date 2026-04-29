from __future__ import annotations

import logging
from pathlib import Path

import pytest

from epub_generator.compiler import compile_book
from epub_generator.config import BookConfig, SourceConfig
from epub_generator.ingestors.base import BaseIngestor


class DummyIngestor(BaseIngestor):
    def extract(self, source: SourceConfig, project_root: Path) -> str:
        if "error" in source.path:
            raise RuntimeError("Fallo simulado")
        if "no_header" in source.path:
            return "Contenido sin cabecera."
        if "with_header" in source.path:
            return f"{'#' * source.title_level} {source.title}\nContenido con cabecera."
        return "Contenido base."


@pytest.fixture(autouse=True)
def mock_ingestors(monkeypatch: pytest.MonkeyPatch) -> None:
    from epub_generator import compiler
    monkeypatch.setattr(compiler, "INGESTORS", {"dummy": DummyIngestor})


def test_compile_book_success(tmp_path: Path) -> None:
    # Setup files
    file1 = tmp_path / "file1.txt"
    file1.touch()
    file2 = tmp_path / "file2.txt"
    file2.touch()
    
    config = BookConfig(
        sources=[
            SourceConfig(type="dummy", path="no_header.txt", title="First"),
            SourceConfig(type="dummy", path="with_header.txt", title="Second", title_level=2)
        ]
    )
    
    # Needs real paths for validation, let's mock validation or create real files
    (tmp_path / "no_header.txt").touch()
    (tmp_path / "with_header.txt").touch()
    
    out_path = compile_book(config, "mi_libro", tmp_path)
    
    assert out_path.name == "mi_libro_compiled.md"
    assert out_path.exists()
    
    content = out_path.read_text("utf-8")
    # First source gets header injected
    assert "# First\n\nContenido sin cabecera." in content
    # Second source does not get duplicated header
    assert "## Second\nContenido con cabecera." in content
    # They should be joined by double newline
    assert "# First\n\nContenido sin cabecera.\n\n## Second\nContenido con cabecera." in content


def test_compile_book_on_error_skip(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    (tmp_path / "error.txt").touch()
    (tmp_path / "no_header.txt").touch()
    
    config = BookConfig(
        sources=[
            SourceConfig(type="dummy", path="error.txt", on_error="skip"),
            SourceConfig(type="dummy", path="no_header.txt", title="Success")
        ]
    )
    
    with caplog.at_level(logging.WARNING):
        out_path = compile_book(config, "mi_libro", tmp_path)
    
    assert "Fallo simulado. Omitiendo." in caplog.text
    content = out_path.read_text("utf-8")
    assert "# Success" in content
    assert "error.txt" not in content


def test_compile_book_on_error_abort(tmp_path: Path) -> None:
    (tmp_path / "error.txt").touch()
    
    config = BookConfig(
        sources=[
            SourceConfig(type="dummy", path="error.txt", on_error="abort")
        ]
    )
    
    with pytest.raises(RuntimeError, match="Fallo simulado"):
        compile_book(config, "mi_libro", tmp_path)

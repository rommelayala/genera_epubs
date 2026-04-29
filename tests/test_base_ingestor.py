from __future__ import annotations

import pytest
from pathlib import Path

from epub_generator.config import SourceConfig
from epub_generator.ingestors.base import BaseIngestor


class ConcreteIngestor(BaseIngestor):
    def extract(self, source: SourceConfig, project_root: Path) -> str:
        return ""


@pytest.fixture
def ingestor() -> ConcreteIngestor:
    return ConcreteIngestor()


def test_resolve_path_absolute(ingestor: ConcreteIngestor, tmp_path: Path) -> None:
    f = tmp_path / "file.md"
    f.write_text("hello")
    source = SourceConfig(path=str(f))
    result = ingestor.resolve_path(source, Path("/irrelevant"))
    assert result == f.resolve()


def test_resolve_path_relative(ingestor: ConcreteIngestor, tmp_path: Path) -> None:
    f = tmp_path / "rel.md"
    f.write_text("hello")
    source = SourceConfig(path="rel.md")
    result = ingestor.resolve_path(source, tmp_path)
    assert result == f.resolve()


def test_resolve_path_tilde(ingestor: ConcreteIngestor, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    f = tmp_path / "tilde.md"
    f.write_text("hello")
    source = SourceConfig(path="~/tilde.md")
    result = ingestor.resolve_path(source, Path("/irrelevant"))
    assert result == f.resolve()


def test_resolve_path_nonexistent(ingestor: ConcreteIngestor, tmp_path: Path) -> None:
    source = SourceConfig(path="nonexistent.md")
    with pytest.raises(FileNotFoundError):
        ingestor.resolve_path(source, tmp_path)

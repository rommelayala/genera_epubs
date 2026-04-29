from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from epub_generator.config import SourceConfig, BookConfig


class Metadata:
    """Metadatos del libro/documento."""

    def __init__(
        self,
        title: str,
        author: Optional[str] = None,
        language: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.title = title
        self.author = author
        self.language = language
        self.description = description

    def __repr__(self) -> str:
        return f"Metadata(title={self.title!r}, author={self.author!r}, language={self.language!r})"


class Chapter:
    """Capítulo del libro/documento."""

    def __init__(
        self,
        title: str,
        content: str,
        file_ref: Optional[str] = None,
        order: Optional[float] = None,
    ):
        self.title = title
        self.content = content
        self.file_ref = file_ref
        self.order = order

    def __repr__(self) -> str:
        return f"Chapter(title={self.title!r}, content={self.content!r})"


class BaseIngestor(ABC):
    @abstractmethod
    def extract(
        self,
        source: SourceConfig,
        project_root: Path,
        book_config: Optional[BookConfig] = None,
    ) -> tuple[Metadata, list[Chapter]] | str:
        """Extract content from source and return as Markdown string or (Metadata, Chapters)."""
        ...

    def resolve_path(self, source: SourceConfig, project_root: Path) -> Path:
        """Resolve source.path to an absolute Path, raising FileNotFoundError if missing."""
        p = Path(source.path).expanduser()
        if not p.is_absolute():
            p = project_root / p
        p = p.resolve()
        if not p.exists():
            raise FileNotFoundError(f"Source path not found: {p}")
        return p

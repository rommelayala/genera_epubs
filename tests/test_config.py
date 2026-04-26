from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from epub_generator.config import BookConfig, SourceConfig, load_config


def _write_yaml(tmp_path: Path, stem: str, content: str) -> Path:
    yaml_file = tmp_path / f"{stem}.yaml"
    yaml_file.write_text(textwrap.dedent(content), encoding="utf-8")
    md_file = tmp_path / f"{stem}.md"
    md_file.write_text("# placeholder", encoding="utf-8")
    return md_file


def test_load_config_no_yaml(tmp_path: Path) -> None:
    md_file = tmp_path / "book.md"
    md_file.write_text("# Hello", encoding="utf-8")
    config = load_config(md_file)
    assert config.sources == []


def test_load_config_yaml_without_sources(tmp_path: Path) -> None:
    md_file = _write_yaml(tmp_path, "book", """
        title: My Book
    """)
    config = load_config(md_file)
    assert config.title == "My Book"
    assert config.sources == []


def test_load_config_sources_markdown(tmp_path: Path) -> None:
    md_file = _write_yaml(tmp_path, "book", """
        title: Multi Source
        sources:
          - type: markdown
            path: chapter1.md
            title: Chapter One
    """)
    config = load_config(md_file)
    assert len(config.sources) == 1
    src = config.sources[0]
    assert src.type == "markdown"
    assert src.path == "chapter1.md"
    assert src.title == "Chapter One"
    assert src.on_error == "skip"


def test_load_config_sources_pdf(tmp_path: Path) -> None:
    md_file = _write_yaml(tmp_path, "book", """
        sources:
          - type: pdf
            path: doc.pdf
            on_error: abort
    """)
    config = load_config(md_file)
    assert len(config.sources) == 1
    src = config.sources[0]
    assert src.type == "pdf"
    assert src.on_error == "abort"


def test_load_config_sources_url(tmp_path: Path) -> None:
    md_file = _write_yaml(tmp_path, "book", """
        sources:
          - type: url
            url: https://example.com
            selector: article
    """)
    config = load_config(md_file)
    src = config.sources[0]
    assert src.type == "url"
    assert src.url == "https://example.com"
    assert src.selector == "article"


def test_load_config_multiple_sources(tmp_path: Path) -> None:
    md_file = _write_yaml(tmp_path, "book", """
        sources:
          - type: markdown
            path: a.md
          - type: pdf
            path: b.pdf
          - type: url
            url: https://example.com
    """)
    config = load_config(md_file)
    assert len(config.sources) == 3
    assert config.sources[0].type == "markdown"
    assert config.sources[1].type == "pdf"
    assert config.sources[2].type == "url"


def test_source_config_defaults() -> None:
    src = SourceConfig()
    assert src.type == ""
    assert src.path == ""
    assert src.url == ""
    assert src.selector == ""
    assert src.transcription_service == "whisper"
    assert src.prefer_subtitles is True
    assert src.title == ""
    assert src.title_level == 1
    assert src.on_error == "skip"

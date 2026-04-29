from __future__ import annotations

import sys
from pathlib import Path

import pytest

_root = Path(__file__).parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from generate_epub import main
import argparse


def test_main_discovery(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    # Set drafts dir to tmp_path
    monkeypatch.setattr("generate_epub._DRAFTS_DIR", tmp_path)
    # Mock sys.argv to run without args
    monkeypatch.setattr(sys, "argv", ["generate_epub.py"])
    
    # Mock process_book to not actually do anything
    monkeypatch.setattr("generate_epub._process_book", lambda *args, **kwargs: None)
    
    # Create some files:
    # 1. A markdown file alone
    (tmp_path / "solo-md.md").touch()
    
    # 2. A yaml with sources (should be discovered)
    yaml_with_sources = tmp_path / "with-sources.yaml"
    yaml_with_sources.write_text("sources:\n  - type: markdown\n    path: test.md", encoding="utf-8")
    
    # 3. Both md and yaml with sources (yaml should win, deduplicated)
    (tmp_path / "coexist.md").touch()
    yaml_coexist = tmp_path / "coexist.yaml"
    yaml_coexist.write_text("sources:\n  - type: markdown\n    path: test.md", encoding="utf-8")
    
    # 4. A yaml sidecar without sources (should NOT be discovered as an entry point, it's just config)
    yaml_no_sources = tmp_path / "sidecar.yaml"
    yaml_no_sources.write_text("title: Only Config", encoding="utf-8")
    
    # Run main
    import logging
    with caplog.at_level(logging.INFO):
        main()
        
    # We expect 3 books: solo-md (markdown), with-sources (yaml), coexist (yaml wins)
    # So 1 markdown, 0 PDF, 2 compiled (yaml).
    assert "Descubiertos 3 libros: 1 markdown, 0 PDF, 2 compilados (yaml)." in caplog.text

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Necesitamos importar _resolve_input que esta en generate_epub.py
# generate_epub es un script en la raiz, necesitamos agregarlo al sys.path
_root = Path(__file__).parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from generate_epub import _resolve_input, _DRAFTS_DIR


def test_resolve_input_md(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("generate_epub._DRAFTS_DIR", tmp_path)
    md_file = tmp_path / "test-libro.md"
    md_file.touch()
    
    # Passing name without extension
    res = _resolve_input("test-libro")
    assert res == md_file
    
    # Passing name with extension
    res2 = _resolve_input("test-libro.md")
    assert res2 == md_file


def test_resolve_input_yaml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("generate_epub._DRAFTS_DIR", tmp_path)
    yaml_file = tmp_path / "test-libro.yaml"
    yaml_file.touch()
    
    # Passing name without extension
    res = _resolve_input("test-libro")
    assert res == yaml_file
    
    # Passing name with extension
    res2 = _resolve_input("test-libro.yaml")
    assert res2 == yaml_file


def test_resolve_input_yaml_and_md_coexist(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("generate_epub._DRAFTS_DIR", tmp_path)
    md_file = tmp_path / "test-libro.md"
    md_file.touch()
    yaml_file = tmp_path / "test-libro.yaml"
    yaml_file.touch()
    
    # The resolution depends on the order of INPUT_EXTENSIONS + ['.yaml']
    # Currently INPUT_EXTENSIONS = {'.md', '.pdf'}. It's a set, so order is random.
    # But if we pass explicitly the extension, it should resolve to that.
    assert _resolve_input("test-libro.yaml") == yaml_file
    assert _resolve_input("test-libro.md") == md_file


def test_resolve_input_inexistent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("generate_epub._DRAFTS_DIR", tmp_path)
    # File does not exist
    res = _resolve_input("fantasma")
    # Should default to appending to drafts dir, even if not exists
    assert res == tmp_path / "fantasma"


def test_resolve_input_absolute_path(tmp_path: Path) -> None:
    abs_file = tmp_path / "outside.yaml"
    abs_file.touch()
    
    res = _resolve_input(str(abs_file))
    assert res == abs_file

"""E2E test: md+pdf+url genera _compiled.md y EPUB válido."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from epub_generator.compiler import compile_book
from epub_generator.config import BookConfig, SourceConfig
from epub_generator.generator import generate
from tests.conftest import make_pdf


@pytest.fixture()
def mock_url_resp() -> MagicMock:
    resp = MagicMock()
    resp.text = "<html><body><p>Contenido de la URL.</p></body></html>"
    resp.raise_for_status = MagicMock()
    return resp


@pytest.fixture()
def source_files(tmp_path: Path) -> tuple[Path, Path]:
    md_file = tmp_path / "source.md"
    md_file.write_text("Contenido del archivo Markdown.", encoding="utf-8")
    pdf_file = tmp_path / "source.pdf"
    make_pdf(pdf_file, ["Contenido del PDF pagina uno."])
    return md_file, pdf_file


@pytest.fixture()
def book_config(source_files: tuple[Path, Path]) -> BookConfig:
    md_path, pdf_path = source_files
    return BookConfig(
        title="E2E Test Book",
        author="Test Author",
        language="es-ES",
        sources=[
            SourceConfig(type="markdown", path=str(md_path), title="Capítulo Markdown"),
            SourceConfig(type="pdf", path=str(pdf_path), title="Capítulo PDF"),
            SourceConfig(type="url", url="http://example.com/article", title="Capítulo URL"),
        ],
    )


def test_compile_produces_combined_md(
    tmp_path: Path,
    book_config: BookConfig,
    mock_url_resp: MagicMock,
) -> None:
    """compile_book genera _compiled.md con contenido de las 3 fuentes en orden y >=3 H1."""
    with patch("requests.get", return_value=mock_url_resp):
        out_path = compile_book(book_config, "e2e_test", tmp_path)

    assert out_path.name == "e2e_test_compiled.md"
    assert out_path.exists()

    content = out_path.read_text("utf-8")
    assert "Contenido del archivo Markdown" in content
    assert "Contenido del PDF" in content
    assert "Contenido de la URL" in content

    idx_md = content.find("Capítulo Markdown")
    idx_pdf = content.find("Capítulo PDF")
    idx_url = content.find("Capítulo URL")
    assert idx_md < idx_pdf < idx_url, "Fuentes deben aparecer en orden declarado"

    h1_count = content.count("\n# ") + (1 if content.startswith("# ") else 0)
    assert h1_count >= 3, f"Se esperaban >=3 H1, encontrados: {h1_count}"


def test_e2e_epub_generated(
    tmp_path: Path,
    book_config: BookConfig,
    mock_url_resp: MagicMock,
) -> None:
    """Flujo completo: compile_book + generate produce un EPUB válido con >=3 H1."""
    import ebooklib
    from ebooklib import epub as eblib_epub
    from PIL import Image

    with patch("requests.get", return_value=mock_url_resp):
        compiled_md = compile_book(book_config, "e2e_epub", tmp_path)

    assert compiled_md.exists()

    cover_path = tmp_path / "cover.png"
    Image.new("RGB", (600, 800), "#151515").save(str(cover_path))

    epub_out = tmp_path / "e2e_epub.epub"
    generate(compiled_md, book_config, cover_path, epub_out)

    assert epub_out.exists()

    book = eblib_epub.read_epub(str(epub_out))
    all_content = ""
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        all_content += item.get_content().decode("utf-8", errors="replace")

    h1_count = all_content.count("<h1")
    assert h1_count >= 3, f"EPUB debe contener >=3 capítulos H1, encontrados: {h1_count}"


def test_regression_no_sources_raises(tmp_path: Path) -> None:
    """BookConfig sin sources: compile_book lanza ValueError."""
    config = BookConfig(sources=[])
    with pytest.raises(ValueError, match="No hay sources definidos"):
        compile_book(config, "regression", tmp_path)

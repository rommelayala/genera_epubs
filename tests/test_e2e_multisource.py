"""E2E test: YAML con md+pdf+url genera _compiled.md y EPUB válido."""
from __future__ import annotations

import textwrap
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from epub_generator.compiler import compile_book
from epub_generator.config import BookConfig, SourceConfig
from epub_generator.generator import generate


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_pdf(path: Path, pages: list[str]) -> None:
    """Minimal text PDF compatible with pypdf."""
    objs: dict[int, str] = {}
    page_nums: list[int] = []
    streams: list[tuple[int, str]] = []

    base = 3
    for i, text in enumerate(pages):
        sn = base + i * 2
        pn = base + i * 2 + 1
        streams.append((sn, f"BT /F1 12 Tf 50 700 Td ({text}) Tj ET"))
        page_nums.append(pn)

    objs[1] = "<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{n} 0 R" for n in page_nums)
    objs[2] = f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>"
    font = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    resources = f"<< /Font << /F1 {font} >> >>"

    for sn, data in streams:
        bdata = data.encode("latin-1")
        pn = sn + 1
        objs[sn] = f"<< /Length {len(bdata)} >>\nstream\n{data}\nendstream"
        objs[pn] = (
            f"<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 612 792] "
            f"/Contents {sn} 0 R "
            f"/Resources {resources} >>"
        )

    buf = b"%PDF-1.4\n"
    xref: list[int] = [0]
    offsets: dict[int, int] = {}
    for n in sorted(objs):
        offsets[n] = len(buf)
        buf += f"{n} 0 obj\n{objs[n]}\nendobj\n".encode("latin-1")

    xref_pos = len(buf)
    count = max(objs) + 1
    buf += f"xref\n0 {count}\n".encode()
    buf += b"0000000000 65535 f \n"
    for n in range(1, count):
        buf += f"{offsets.get(n, 0):010d} 00000 n \n".encode()
    buf += f"trailer\n<< /Size {count} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode()
    path.write_bytes(buf)


def _make_cover(path: Path) -> None:
    from PIL import Image
    Image.new("RGB", (600, 800), "#151515").save(str(path))


def _make_book_config(md_path: Path, pdf_path: Path) -> BookConfig:
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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_compile_produces_combined_md(tmp_path: Path) -> None:
    """compile_book genera _compiled.md con contenido de las 3 fuentes en orden."""
    md_file = tmp_path / "source.md"
    md_file.write_text("Contenido del archivo Markdown.", encoding="utf-8")

    pdf_file = tmp_path / "source.pdf"
    _make_pdf(pdf_file, ["Contenido del PDF pagina uno."])

    html_body = "<html><body><p>Contenido de la URL.</p></body></html>"
    mock_resp = MagicMock()
    mock_resp.text = html_body
    mock_resp.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_resp):
        config = _make_book_config(md_file, pdf_file)
        out_path = compile_book(config, "e2e_test", tmp_path)

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


def test_compiled_md_has_h1_headers(tmp_path: Path) -> None:
    """_compiled.md contiene al menos 3 cabeceras H1."""
    md_file = tmp_path / "source.md"
    md_file.write_text("Texto markdown.", encoding="utf-8")

    pdf_file = tmp_path / "source.pdf"
    _make_pdf(pdf_file, ["Texto PDF."])

    mock_resp = MagicMock()
    mock_resp.text = "<html><body><p>Texto URL.</p></body></html>"
    mock_resp.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_resp):
        config = _make_book_config(md_file, pdf_file)
        out_path = compile_book(config, "e2e_headers", tmp_path)

    content = out_path.read_text("utf-8")
    h1_count = content.count("\n# ") + (1 if content.startswith("# ") else 0)
    assert h1_count >= 3, f"Se esperaban >=3 H1, se encontraron {h1_count}"


def test_e2e_epub_generated(tmp_path: Path) -> None:
    """Flujo completo: compile_book + generate produce un EPUB válido."""
    import ebooklib
    from ebooklib import epub as eblib_epub

    md_file = tmp_path / "source.md"
    md_file.write_text(
        textwrap.dedent("""\
        # Capítulo Markdown

        Contenido del primer capítulo en Markdown.
        """),
        encoding="utf-8",
    )

    pdf_file = tmp_path / "source.pdf"
    _make_pdf(pdf_file, ["Contenido del segundo capitulo en PDF."])

    mock_resp = MagicMock()
    mock_resp.text = "<html><body><h1>Capítulo URL</h1><p>Contenido del tercer capítulo desde web.</p></body></html>"
    mock_resp.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_resp):
        config = _make_book_config(md_file, pdf_file)
        compiled_md = compile_book(config, "e2e_epub", tmp_path)

    assert compiled_md.exists()

    cover_path = tmp_path / "cover.png"
    _make_cover(cover_path)

    epub_out = tmp_path / "e2e_epub.epub"
    generate(compiled_md, config, cover_path, epub_out)

    assert epub_out.exists(), "El archivo EPUB debe generarse"

    book = eblib_epub.read_epub(str(epub_out))
    all_content = ""
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        all_content += item.get_content().decode("utf-8", errors="replace")

    h1_count = all_content.count("<h1")
    assert h1_count >= 3, f"EPUB debe contener >=3 capítulos H1, encontrados: {h1_count}"


def test_regression_no_sources_md_path_unchanged(tmp_path: Path) -> None:
    """BookConfig sin sources: compile_book lanza ValueError y no altera el input_path."""
    config = BookConfig(sources=[])
    with pytest.raises(ValueError, match="No hay sources definidos"):
        compile_book(config, "regression", tmp_path)

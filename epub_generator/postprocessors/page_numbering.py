"""Add page numbers (e.g., 2/40) to EPUB."""
from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path


def add_page_numbers(epub_path: Path) -> None:
    """Add page numbering (e.g., '2/40') to each content page of an EPUB."""
    if not epub_path.exists():
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        with zipfile.ZipFile(epub_path, 'r') as z:
            z.extractall(tmpdir)

        # Pandoc uses EPUB/, other tools use OEBPS/ or content/
        epub_root = _find_epub_root(tmpdir)
        if epub_root is None:
            return

        # Find content HTML files (chapters only, skip cover/toc/nav/title)
        html_files = _find_content_files(epub_root)
        if not html_files:
            return

        total_pages = len(html_files)

        for page_num, html_file in enumerate(html_files, start=1):
            _inject_page_number(html_file, page_num, total_pages)

        _inject_page_number_css(epub_root)

        # Repackage — mimetype must be first and uncompressed (EPUB spec)
        _repackage_epub(tmpdir, epub_path)


def _find_epub_root(tmpdir: Path) -> Path | None:
    """Find the EPUB content root directory."""
    for candidate in ("EPUB", "OEBPS", "content"):
        p = tmpdir / candidate
        if p.is_dir():
            return p
    return None


def _find_content_files(epub_root: Path) -> list[Path]:
    """Find chapter XHTML files, excluding cover, toc, nav, title page."""
    skip = {"cover.xhtml", "toc.xhtml", "nav.xhtml", "title_page.xhtml",
            "cover.html", "toc.html", "nav.html", "title_page.html"}

    # Search recursively (pandoc puts them in EPUB/text/)
    files = []
    for ext in ("*.xhtml", "*.html"):
        for f in epub_root.rglob(ext):
            if f.name.lower() not in skip:
                files.append(f)

    return sorted(files)


def _inject_page_number(html_file: Path, page_num: int, total_pages: int) -> None:
    """Inject page number div before </body>."""
    content = html_file.read_text(encoding="utf-8")

    page_div = f'<div class="page-number">{page_num}/{total_pages}</div>'

    if "</body>" in content:
        content = content.replace("</body>", f"{page_div}\n</body>", 1)
    elif "</BODY>" in content:
        content = content.replace("</BODY>", f"{page_div}\n</BODY>", 1)

    html_file.write_text(content, encoding="utf-8")


def _inject_page_number_css(epub_root: Path) -> None:
    """Append page-number CSS to the existing stylesheet."""
    # Find existing CSS (pandoc creates styles/stylesheet1.css)
    css_files = list(epub_root.rglob("*.css"))
    if css_files:
        styles_file = css_files[0]
    else:
        styles_dir = epub_root / "styles"
        styles_dir.mkdir(exist_ok=True)
        styles_file = styles_dir / "page-numbers.css"

    css = styles_file.read_text(encoding="utf-8") if styles_file.exists() else ""

    if ".page-number" not in css:
        css += """
/* Page numbering */
.page-number {
    text-align: center;
    margin: 2em 0 0 0;
    padding: 0.8em 0;
    font-size: 0.85em;
    color: #999;
    border-top: 1px solid #eee;
    font-style: italic;
    letter-spacing: 0.05em;
}
"""
        styles_file.write_text(css, encoding="utf-8")


def _repackage_epub(tmpdir: Path, epub_path: Path) -> None:
    """Repackage EPUB with mimetype first and uncompressed (per EPUB spec)."""
    mimetype_path = tmpdir / "mimetype"

    with zipfile.ZipFile(epub_path, 'w') as z:
        # mimetype MUST be first entry, stored uncompressed
        if mimetype_path.exists():
            z.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)

        for file_path in sorted(tmpdir.rglob("*")):
            if file_path.is_file() and file_path.name != "mimetype":
                arcname = file_path.relative_to(tmpdir)
                z.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)

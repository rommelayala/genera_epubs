from __future__ import annotations

from typing import Dict, Type

from epub_generator.ingestors.base import BaseIngestor
from epub_generator.ingestors.html_ingestor import HtmlIngestor
from epub_generator.ingestors.markdown_ingestor import MarkdownIngestor
from epub_generator.ingestors.opf_ingestor import OpfIngestor
from epub_generator.ingestors.pdf_ingestor import PdfIngestor
from epub_generator.ingestors.text_ingestor import TextIngestor
from epub_generator.ingestors.url_ingestor import UrlIngestor
from epub_generator.ingestors.word_ingestor import WordIngestor
from epub_generator.ingestors.ncx_ingestor import NcxIngestor
from epub_generator.ingestors.epub_ingestor import EpubIngestor
from epub_generator.ingestors.ollama_pdf_ingestor import OllamaPdfIngestor

INGESTORS: Dict[str, Type[BaseIngestor]] = {
    "markdown": MarkdownIngestor,
    "pdf": PdfIngestor,
    "url": UrlIngestor,
    "word": WordIngestor,
    "html": HtmlIngestor,
    "text": TextIngestor,
    "opf": OpfIngestor,
    "ncx": NcxIngestor,
    "epub": EpubIngestor,
    "ollama_pdf": OllamaPdfIngestor,
}


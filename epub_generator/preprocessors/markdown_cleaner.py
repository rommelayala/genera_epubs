"""Clean markdown text for TTS narration.

Strips syntax that does not translate to speech (code blocks, tables, links, etc.)
and replaces code blocks with a verbal redirect to the companion ebook.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

CODE_REDIRECT = "Para ver este ejemplo de código, consulta el libro en formato epub."
TABLE_REDIRECT = "Consulta la tabla completa en el libro en formato epub."


@dataclass
class Chapter:
    title: str
    body: str


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (---...---) from the beginning of the text."""
    return re.sub(r"\A\s*---\n.*?\n---\n?", "", text, count=1, flags=re.DOTALL)


def extract_chapters(markdown: str) -> list[Chapter]:
    """Split markdown into chapters by top-level H1 headings."""
    markdown = strip_frontmatter(markdown)
    pattern = re.compile(r"^# (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(markdown))

    if not matches:
        return [Chapter(title="Introducción", body=markdown)]

    chapters: list[Chapter] = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        chapters.append(Chapter(title=title, body=body))

    return chapters


def clean_for_tts(text: str) -> str:
    """Return text suitable for TTS — no markdown syntax, no code."""
    # Fenced code blocks (``` ... ```)
    text = re.sub(r"```[\w]*\n[\s\S]*?```", f"\n{CODE_REDIRECT}\n", text)

    # Inline code (`code`)
    text = re.sub(r"`[^`]+`", "", text)

    # Tables (lines starting with |)
    text = re.sub(r"(\|.+\|\n)+", f"\n{TABLE_REDIRECT}\n", text)

    # Horizontal rules
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)

    # ATX headings — keep the text, drop the # symbols
    text = re.sub(r"^#{1,6}\s+(.+)$", r"\1.", text, flags=re.MULTILINE)

    # Bold and italic
    text = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}(.+?)_{1,3}", r"\1", text)

    # Links — keep label, drop URL
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)

    # Images
    text = re.sub(r"!\[.*?\]\(.+?\)", "", text)

    # HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Blockquotes
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)

    # Unordered list markers
    text = re.sub(r"^[\s]*[-*+]\s+", "", text, flags=re.MULTILINE)

    # Ordered list markers
    text = re.sub(r"^[\s]*\d+\.\s+", "", text, flags=re.MULTILINE)

    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

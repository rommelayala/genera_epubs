"""Convert markdown to audiobook MP3 chapters using edge-tts.

One MP3 per chapter. If ffmpeg is available, also assembles a single
M4B audiobook file with chapter markers.
"""
from __future__ import annotations

import asyncio
import logging
import shutil
import subprocess
from pathlib import Path

import edge_tts

from epub_generator.config import BookConfig
from epub_generator.preprocessors.markdown_cleaner import Chapter, clean_for_tts, extract_chapters

log = logging.getLogger(__name__)

DEFAULT_VOICE = "es-ES-AlvaroNeural"
SUPPORTED_VOICES = {
    "es-ES": "es-ES-AlvaroNeural",
    "es-MX": "es-MX-JorgeNeural",
    "en-US": "en-US-GuyNeural",
    "en-GB": "en-GB-RyanNeural",
}


def _voice_for(language: str) -> str:
    return SUPPORTED_VOICES.get(language, DEFAULT_VOICE)


async def _synthesize(text: str, voice: str, output: Path) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output))


def _chapter_to_mp3(chapter: Chapter, voice: str, output_dir: Path, index: int) -> Path:
    clean_text = clean_for_tts(chapter.body)
    if not clean_text.strip():
        log.warning("Capítulo '%s' vacío tras limpiar — omitido", chapter.title)
        return None

    # Prepend the chapter title so TTS lo narra
    narration = f"{chapter.title}.\n\n{clean_text}"
    mp3_path = output_dir / f"{index:02d}_{_slugify(chapter.title)}.mp3"

    log.info("  🔊 Narrando: %s", chapter.title)
    asyncio.run(_synthesize(narration, voice, mp3_path))
    return mp3_path


def _assemble_m4b(mp3_files: list[Path], config: BookConfig, output: Path) -> None:
    """Combine MP3 chapters into a single M4B with ffmpeg."""
    concat_file = output.parent / "concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in mp3_files),
        encoding="utf-8",
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-metadata", f"title={config.title}",
        "-metadata", f"artist={config.author}",
        "-metadata", f"comment={config.description}",
        "-c:a", "aac", "-b:a", "64k",
        str(output),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    concat_file.unlink(missing_ok=True)

    if result.returncode != 0:
        log.warning("  ⚠️  ffmpeg falló: %s", result.stderr[-200:])
    else:
        log.info("  ✅ M4B ensamblado: %s", output.name)


def _slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "-", text)[:60]


def convert_audio(
    input_path: Path,
    config: BookConfig,
    _cover: Path,          # ignorada en audio, firma consistente con otros converters
    output: Path,
) -> None:
    """Entry point: markdown → MP3 chapters + optional M4B."""
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise RuntimeError(
                f"{tool} es requerido para generar audiolibros. "
                "Instala con: brew install ffmpeg / sudo apt install ffmpeg"
            )

    markdown = input_path.read_text(encoding="utf-8")
    chapters = extract_chapters(markdown)
    voice = _voice_for(config.language)

    chapters_dir = output.parent / f"{output.stem}_chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    log.info("  🎙️  Voz: %s | %d capítulos detectados", voice, len(chapters))

    mp3_files: list[Path] = []
    for i, chapter in enumerate(chapters, start=1):
        mp3 = _chapter_to_mp3(chapter, voice, chapters_dir, i)
        if mp3:
            mp3_files.append(mp3)

    if not mp3_files:
        raise RuntimeError("No se generó ningún archivo de audio.")

    log.info("  📂 Capítulos en: %s", chapters_dir.relative_to(input_path.parent.parent))

    _assemble_m4b(mp3_files, config, output)

"""Convert markdown to audiobook MP3 chapters using edge-tts.

One MP3 per chapter. If ffmpeg is available, also assembles a single
M4B audiobook file with chapter markers.
"""
from __future__ import annotations

import asyncio
import logging
import re
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


async def _synthesize(
    text: str, voice: str, output: Path,
    rate: str = "-5%", volume: str = "+0%", pitch: str = "+0Hz",
) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)
    await communicate.save(str(output))


async def _chapter_to_mp3_async(
    chapter: Chapter,
    voice: str,
    output_dir: Path,
    index: int,
    total: int,
    semaphore: asyncio.Semaphore,
    rate: str = "-5%",
    volume: str = "+0%",
    pitch: str = "+0Hz",
) -> Path | None:
    clean_text = clean_for_tts(chapter.body)
    if not clean_text.strip():
        log.warning("Capítulo '%s' vacío tras limpiar — omitido", chapter.title)
        return None

    narration = f"{chapter.title}.\n\n{clean_text}"
    mp3_path = output_dir / f"{index:02d}_{_slugify(chapter.title)}.mp3"

    async with semaphore:
        log.info("  Narrando capítulo %d de %d: %s", index, total, chapter.title)
        try:
            await _synthesize(narration, voice, mp3_path, rate=rate, volume=volume, pitch=pitch)
        except Exception:
            log.error("  Error narrando capítulo '%s'", chapter.title, exc_info=True)
            return None
    return mp3_path


async def _synthesize_all(
    chapters: list[Chapter],
    voice: str,
    output_dir: Path,
    concurrency: int,
    rate: str = "-5%",
    volume: str = "+0%",
    pitch: str = "+0Hz",
) -> list[Path | None]:
    semaphore = asyncio.Semaphore(concurrency)
    total = len(chapters)
    tasks = [
        _chapter_to_mp3_async(
            ch, voice, output_dir, i, total, semaphore,
            rate=rate, volume=volume, pitch=pitch,
        )
        for i, ch in enumerate(chapters, start=1)
    ]
    return await asyncio.gather(*tasks)


def _get_duration_ms(mp3_path: Path) -> int:
    """Get duration of an MP3 file in milliseconds using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            str(mp3_path),
        ],
        capture_output=True, text=True,
    )
    return int(float(result.stdout.strip()) * 1000)


def _generate_chapter_metadata(
    mp3_files: list[Path],
    chapter_titles: list[str],
    pause_ms: int,
) -> str:
    """Generate ffmpeg metadata file content with [CHAPTER] entries."""
    lines = [";FFMETADATA1"]
    offset = 0
    for i, (mp3, title) in enumerate(zip(mp3_files, chapter_titles)):
        duration = _get_duration_ms(mp3)
        start = offset
        end = offset + duration
        lines.append("")
        lines.append("[CHAPTER]")
        lines.append("TIMEBASE=1/1000")
        lines.append(f"START={start}")
        lines.append(f"END={end}")
        lines.append(f"title={title}")
        offset = end
        # Add pause between chapters (not after the last one)
        if i < len(mp3_files) - 1:
            offset += pause_ms
    return "\n".join(lines) + "\n"


def _assemble_m4b(mp3_files: list[Path], config: BookConfig, output: Path,
                  chapter_titles: list[str] | None = None) -> None:
    """Combine MP3 chapters into a single M4B with ffmpeg."""
    concat_file = output.parent / "concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in mp3_files),
        encoding="utf-8",
    )

    # Generate chapter metadata
    pause_ms = int(config.audio.chapter_pause * 1000)
    titles = chapter_titles or [p.stem for p in mp3_files]
    metadata_content = _generate_chapter_metadata(mp3_files, titles, pause_ms)
    metadata_file = output.parent / "metadata.txt"
    metadata_file.write_text(metadata_content, encoding="utf-8")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(metadata_file),
        "-map_metadata", "1",
        "-metadata", f"title={config.title}",
        "-metadata", f"artist={config.author}",
        "-metadata", f"comment={config.description}",
        "-c:a", "aac", "-b:a", "64k",
        str(output),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    concat_file.unlink(missing_ok=True)
    metadata_file.unlink(missing_ok=True)

    if result.returncode != 0:
        log.warning("  ffmpeg fallo: %s", result.stderr[-200:])
    else:
        log.info("  M4B ensamblado: %s", output.name)


def _slugify(text: str) -> str:
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
    voice = config.audio.voice if config.audio.voice else _voice_for(config.language)

    chapters_dir = output.parent / f"{output.stem}_chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    concurrency = config.audio.concurrency
    rate = config.audio.rate
    volume = config.audio.volume
    pitch = config.audio.pitch
    log.info("  🎙️  Voz: %s | %d capítulos detectados | concurrencia: %d", voice, len(chapters), concurrency)

    results = asyncio.run(_synthesize_all(
        chapters, voice, chapters_dir, concurrency,
        rate=rate, volume=volume, pitch=pitch,
    ))
    mp3_files: list[Path] = []
    chapter_titles: list[str] = []
    for path, ch in zip(results, chapters):
        if path is not None:
            mp3_files.append(path)
            chapter_titles.append(ch.title)

    if not mp3_files:
        raise RuntimeError("No se generó ningún archivo de audio.")

    log.info("  Capítulos en: %s", chapters_dir.relative_to(input_path.parent.parent))

    _assemble_m4b(mp3_files, config, output, chapter_titles=chapter_titles)

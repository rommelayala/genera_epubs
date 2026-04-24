"""Convert markdown to audiobook MP3 chapters using edge-tts.

One MP3 per chapter. If ffmpeg is available, also assembles a single
M4B audiobook file with chapter markers.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
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
                  chapter_titles: list[str] | None = None,
                  cover: Path | None = None) -> None:
    """Combine MP3 chapters into a single M4B with ffmpeg."""
    chapter_pause = config.audio.chapter_pause
    silence_file: Path | None = None

    # Generate silence file for inter-chapter pauses
    if chapter_pause > 0:
        silence_file = output.parent / "silence.mp3"
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono",
                "-t", str(chapter_pause),
                "-q:a", "9",
                str(silence_file),
            ],
            capture_output=True, text=True,
        )

    # Build concat.txt with silence intercalated between chapters
    concat_lines: list[str] = []
    for i, p in enumerate(mp3_files):
        concat_lines.append(f"file '{p.resolve()}'")
        if silence_file and i < len(mp3_files) - 1:
            concat_lines.append(f"file '{silence_file.resolve()}'")

    concat_file = output.parent / "concat.txt"
    concat_file.write_text("\n".join(concat_lines), encoding="utf-8")

    # Generate chapter metadata
    pause_ms = int(chapter_pause * 1000)
    titles = chapter_titles or [p.stem for p in mp3_files]
    metadata_content = _generate_chapter_metadata(mp3_files, titles, pause_ms)
    metadata_file = output.parent / "metadata.txt"
    metadata_file.write_text(metadata_content, encoding="utf-8")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(metadata_file),
    ]

    # Embed cover art if available
    has_cover = cover is not None and cover.exists()
    if has_cover:
        cmd.extend(["-i", str(cover)])
        suffix = cover.suffix.lower()
        video_codec = "png" if suffix == ".png" else "mjpeg"
        cmd.extend([
            "-map", "0:a", "-map", "2:v",
            "-c:v", video_codec,
            "-disposition:v", "attached_pic",
            "-map_metadata", "1",
        ])
    elif cover is not None:
        log.warning("  Portada no encontrada: %s — continuando sin portada", cover)
        cmd.extend(["-map_metadata", "1"])
    else:
        cmd.extend(["-map_metadata", "1"])

    bitrate = config.audio.bitrate
    cmd.extend([
        "-metadata", f"title={config.title}",
        "-metadata", f"artist={config.author}",
        "-metadata", f"comment={config.description}",
        "-c:a", "aac", "-b:a", bitrate,
        str(output),
    ])

    result = subprocess.run(cmd, capture_output=True, text=True)
    concat_file.unlink(missing_ok=True)
    metadata_file.unlink(missing_ok=True)
    if silence_file:
        silence_file.unlink(missing_ok=True)

    if result.returncode != 0:
        log.warning("  ffmpeg fallo: %s", result.stderr[-200:])
    else:
        log.info("  M4B ensamblado: %s", output.name)


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "-", text)[:60]


def _load_cache(cache_path: Path) -> dict:
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_cache(cache_path: Path, manifest: dict) -> None:
    cache_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


async def _synthesize_with_cache(
    chapters: list[Chapter],
    voice: str,
    output_dir: Path,
    concurrency: int,
    cache_path: Path,
    no_cache: bool,
    rate: str, volume: str, pitch: str,
) -> list[tuple[Path | None, str]]:
    """Synthesize chapters, using cache when possible. Returns list of (path, title)."""
    manifest = {} if no_cache else _load_cache(cache_path)
    semaphore = asyncio.Semaphore(concurrency)
    total = len(chapters)

    async def _process_one(i: int, ch: Chapter) -> Path | None:
        clean_text = clean_for_tts(ch.body)
        if not clean_text.strip():
            log.warning("Capítulo '%s' vacío tras limpiar — omitido", ch.title)
            return None

        narration = f"{ch.title}.\n\n{clean_text}"
        mp3_path = output_dir / f"{i:02d}_{_slugify(ch.title)}.mp3"
        text_h = _text_hash(narration)

        # Check cache
        cached = manifest.get(mp3_path.name)
        if cached and cached.get("hash") == text_h and mp3_path.exists() and not no_cache:
            log.info("  Capítulo %d de %d sin cambios, usando caché: %s", i, total, ch.title)
            return mp3_path

        async with semaphore:
            log.info("  Narrando capítulo %d de %d: %s", i, total, ch.title)
            try:
                await _synthesize(narration, voice, mp3_path, rate=rate, volume=volume, pitch=pitch)
            except Exception:
                log.error("  Error narrando capítulo '%s'", ch.title, exc_info=True)
                return None

        # Update manifest
        try:
            dur = _get_duration_ms(mp3_path)
        except Exception:
            dur = 0
        manifest[mp3_path.name] = {"hash": text_h, "duration_ms": dur}
        return mp3_path

    results = await asyncio.gather(*[_process_one(i, ch) for i, ch in enumerate(chapters, start=1)])
    _save_cache(cache_path, manifest)
    return list(zip(results, [ch.title for ch in chapters]))


async def _synthesize_intro_outro(
    config: BookConfig, voice: str, chapters_dir: Path,
    rate: str, volume: str, pitch: str,
) -> tuple[Path | None, Path | None]:
    """Generate intro and outro MP3s."""
    intro_path = outro_path = None

    if config.audio.intro:
        intro_text = f"Este es el audiolibro: {config.title}. Escrito por {config.author}."
        if config.description:
            intro_text += f" {config.description}"
        intro_path = chapters_dir / "00_intro.mp3"
        log.info("  Narrando intro...")
        try:
            await _synthesize(intro_text, voice, intro_path, rate=rate, volume=volume, pitch=pitch)
        except Exception:
            log.error("  Error narrando intro", exc_info=True)
            intro_path = None

    if config.audio.outro:
        outro_text = f"Fin del audiolibro: {config.title}. Gracias por escuchar."
        outro_path = chapters_dir / "99_outro.mp3"
        log.info("  Narrando outro...")
        try:
            await _synthesize(outro_text, voice, outro_path, rate=rate, volume=volume, pitch=pitch)
        except Exception:
            log.error("  Error narrando outro", exc_info=True)
            outro_path = None

    return intro_path, outro_path


def convert_audio(
    input_path: Path,
    config: BookConfig,
    cover: Path,
    output: Path,
    no_cache: bool = False,
) -> None:
    """Entry point: markdown -> MP3 chapters + M4B."""
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

    rate = config.audio.rate
    volume = config.audio.volume
    pitch = config.audio.pitch
    concurrency = config.audio.concurrency
    cache_path = chapters_dir / "cache_manifest.json"

    log.info("  Voz: %s | %d capítulos | concurrencia: %d", voice, len(chapters), concurrency)

    # Synthesize chapters (with cache)
    results = asyncio.run(_synthesize_with_cache(
        chapters, voice, chapters_dir, concurrency, cache_path, no_cache,
        rate=rate, volume=volume, pitch=pitch,
    ))

    mp3_files: list[Path] = []
    chapter_titles: list[str] = []
    for path, title in results:
        if path is not None:
            mp3_files.append(path)
            chapter_titles.append(title)

    if not mp3_files:
        raise RuntimeError("No se generó ningún archivo de audio.")

    # Intro / outro
    intro_path, outro_path = asyncio.run(_synthesize_intro_outro(
        config, voice, chapters_dir, rate=rate, volume=volume, pitch=pitch,
    ))
    if intro_path:
        mp3_files.insert(0, intro_path)
        chapter_titles.insert(0, "Introducción")
    if outro_path:
        mp3_files.append(outro_path)
        chapter_titles.append("Cierre")

    log.info("  Capítulos en: %s", chapters_dir.relative_to(input_path.parent.parent))

    _assemble_m4b(mp3_files, config, output, chapter_titles=chapter_titles, cover=cover)

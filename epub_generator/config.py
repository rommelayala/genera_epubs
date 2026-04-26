from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml


@dataclass
class SourceConfig:
    type: str = ""
    path: str = ""
    url: str = ""
    selector: str = ""
    transcription_service: str = "whisper"
    prefer_subtitles: bool = True
    title: str = ""
    title_level: int = 1
    on_error: str = "skip"


@dataclass
class AudioConfig:
    voice: str = ""
    rate: str = "-5%"
    volume: str = "+0%"
    pitch: str = "+0Hz"
    bitrate: str = "96k"
    chapter_pause: float = 1.5
    concurrency: int = 5
    intro: bool = True
    outro: bool = True


@dataclass
class CoverConfig:
    title: str = ""
    subtitle: str = ""
    bg_color: str = "#151515"
    text_color: str = "#EAEAEA"
    accent_color: str = "#4A4A4A"
    title_size: int = 42
    subtitle_size: int = 24
    footer: str = "© Rommel Ayala - All rights reserved"
    image: str = ""


@dataclass
class BookConfig:
    title: str = "Untitled"
    author: str = "Rommel Ayala - QA Lead"
    description: str = ""
    language: str = "es-ES"
    date: str = ""
    cover: CoverConfig = field(default_factory=CoverConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    sources: List[SourceConfig] = field(default_factory=list)


def _build_audio(data: dict) -> AudioConfig:
    defaults = AudioConfig()
    return AudioConfig(
        voice=data.get("voice", defaults.voice),
        rate=data.get("rate", defaults.rate),
        volume=data.get("volume", defaults.volume),
        pitch=data.get("pitch", defaults.pitch),
        bitrate=data.get("bitrate", defaults.bitrate),
        chapter_pause=data.get("chapter_pause", defaults.chapter_pause),
        concurrency=data.get("concurrency", defaults.concurrency),
        intro=data.get("intro", defaults.intro),
        outro=data.get("outro", defaults.outro),
    )


def _build_cover(data: dict) -> CoverConfig:
    defaults = CoverConfig()
    return CoverConfig(
        title=data.get("title", defaults.title),
        subtitle=data.get("subtitle", defaults.subtitle),
        bg_color=data.get("bg_color", defaults.bg_color),
        text_color=data.get("text_color", defaults.text_color),
        accent_color=data.get("accent_color", defaults.accent_color),
        title_size=data.get("title_size", defaults.title_size),
        subtitle_size=data.get("subtitle_size", defaults.subtitle_size),
        footer=data.get("footer", defaults.footer),
        image=data.get("image", defaults.image),
    )


def _build_sources(data: list) -> List[SourceConfig]:
    defaults = SourceConfig()
    result = []
    for item in data:
        if not isinstance(item, dict):
            continue
        result.append(SourceConfig(
            type=item.get("type", defaults.type),
            path=item.get("path", defaults.path),
            url=item.get("url", defaults.url),
            selector=item.get("selector", defaults.selector),
            transcription_service=item.get("transcription_service", defaults.transcription_service),
            prefer_subtitles=item.get("prefer_subtitles", defaults.prefer_subtitles),
            title=item.get("title", defaults.title),
            title_level=item.get("title_level", defaults.title_level),
            on_error=item.get("on_error", defaults.on_error),
        ))
    return result


def load_config(input_path: Path) -> BookConfig:
    yaml_path = input_path.parent / (input_path.stem + ".yaml")

    if not yaml_path.exists():
        return BookConfig()

    try:
        with yaml_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError as exc:
        raise ValueError(
            f"YAML inválido en '{yaml_path.name}': {exc}"
        ) from exc

    defaults = BookConfig()
    cover_data = data.get("cover", {}) or {}
    audio_data = data.get("audio", {}) or {}
    sources_data = data.get("sources", []) or []

    return BookConfig(
        title=data.get("title", defaults.title),
        author=data.get("author", defaults.author),
        description=data.get("description", defaults.description),
        language=data.get("language", defaults.language),
        date=data.get("date", defaults.date),
        cover=_build_cover(cover_data),
        audio=_build_audio(audio_data),
        sources=_build_sources(sources_data),
    )

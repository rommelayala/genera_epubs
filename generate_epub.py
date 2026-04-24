#!/usr/bin/env python3
"""Entry point CLI — descubre libros, genera portadas y convierte en paralelo."""
from __future__ import annotations

import argparse
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from epub_generator.config import load_config
from epub_generator.cover import generate_cover
from epub_generator.generator import INPUT_EXTENSIONS, generate

_PROJECT_ROOT = Path(__file__).parent
_DRAFTS_DIR = _PROJECT_ROOT / "libros_draft"
_COVERS_DIR = _PROJECT_ROOT / "portadas_draft"
_OUTPUT_DIR = _PROJECT_ROOT / "epubs_generados"
_AUDIO_DIR = _PROJECT_ROOT / "audios_generados"

_OUTPUT_EXTENSION = {"epub": ".epub", "audio": ".m4b"}

logging.basicConfig(format="%(message)s", level=logging.INFO)
log = logging.getLogger(__name__)


def _resolve_input(arg: str) -> Path:
    """Normalize input arg: with/without extension, with/without path."""
    p = Path(arg)
    if p.is_absolute() and p.exists():
        return p
    stem = p.stem if p.suffix in INPUT_EXTENSIONS else p.name
    for ext in INPUT_EXTENSIONS:
        candidate = _DRAFTS_DIR / (stem + ext)
        if candidate.exists():
            return candidate
    return _DRAFTS_DIR / arg


def _resolve_cover(
    basename: str,
    config_image: str,
    cli_cover: str | None,
    config,
) -> Path:
    """Precedence: CLI arg > YAML cover.image > auto-discovery > generate."""
    # 1. CLI arg
    if cli_cover:
        p = Path(cli_cover)
        if not p.is_absolute():
            p = _COVERS_DIR / cli_cover
        if p.exists():
            return p

    # 2. YAML cover.image
    if config_image:
        p = Path(config_image)
        if not p.is_absolute():
            p = _COVERS_DIR / config_image
        if p.exists():
            return p

    # 3. auto-discovery
    for ext in (".jpg", ".jpeg", ".png"):
        p = _COVERS_DIR / (basename + ext)
        if p.exists():
            return p

    # 4. generate with Pillow
    return generate_cover(basename, config, _COVERS_DIR)


def _process_book(
    input_path: Path,
    cli_cover: str | None,
    output_format: str,
    no_cache: bool = False,
) -> None:
    book_log = logging.getLogger(input_path.stem)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(f"[{input_path.stem}] %(message)s"))
    book_log.addHandler(handler)
    book_log.propagate = False

    basename = input_path.stem

    try:
        config = load_config(input_path)
    except ValueError as exc:
        book_log.error("❌ %s", exc)
        raise

    cover = _resolve_cover(basename, config.cover.image, cli_cover, config)
    if output_format == "epub":
        book_log.info("🖼️  Portada: %s", cover.name)

    ext = _OUTPUT_EXTENSION[output_format]
    out_dir = _OUTPUT_DIR if output_format == "epub" else _AUDIO_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f"{basename}{ext}"

    book_log.info("🔄 Convirtiendo (%s → %s)...", input_path.suffix, output_format)
    generate(input_path, config, cover, output, output_format, no_cache=no_cache)
    book_log.info("✅ %s", output.relative_to(_PROJECT_ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera EPUBs o audiolibros desde libros_draft/")
    parser.add_argument("book", nargs="?", help="Archivo a procesar (nombre o path)")
    parser.add_argument("cover", nargs="?", help="Portada manual (opcional, solo epub)")
    parser.add_argument(
        "--format",
        choices=["epub", "audio"],
        default="epub",
        dest="output_format",
        help="Formato de salida (default: epub)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        default=False,
        dest="no_cache",
        help="Re-narrar todos los capítulos ignorando caché (solo audio)",
    )
    args = parser.parse_args()

    if args.book:
        input_path = _resolve_input(args.book)
        if not input_path.exists():
            log.error("❌ No se encontró: %s", args.book)
            sys.exit(1)
        files = [input_path]
    else:
        files = []
        for ext in INPUT_EXTENSIONS:
            files.extend(_DRAFTS_DIR.glob(f"*{ext}"))
        if not files:
            log.error("❌ No hay archivos soportados en %s", _DRAFTS_DIR)
            sys.exit(1)

    total = len(files)
    md_count = sum(1 for f in files if f.suffix == ".md")
    pdf_count = total - md_count
    log.info("📚 Descubiertos %d libros: %d markdown, %d PDF.", total, md_count, pdf_count)
    log.info("🚀 Procesando en paralelo...\n")

    succeeded = 0
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                _process_book,
                f,
                args.cover if args.book else None,
                args.output_format,
                args.no_cache,
            ): f
            for f in files
        }
        for future in as_completed(futures):
            try:
                future.result()
                succeeded += 1
            except Exception:
                pass

    label = "audiolibros" if args.output_format == "audio" else "libros"
    if succeeded == total:
        log.info("\n✨ %d/%d %s generados", succeeded, total, label)
    else:
        log.info("\n⚠️  %d/%d %s generados. Revisa los errores arriba.", succeeded, total, label)
        sys.exit(1)


if __name__ == "__main__":
    main()

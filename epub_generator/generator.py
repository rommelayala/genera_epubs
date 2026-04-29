from __future__ import annotations

from pathlib import Path

from epub_generator.config import BookConfig
from epub_generator.converters.audio import convert_audio
from epub_generator.converters.markdown import convert_markdown
from epub_generator.converters.pdf import convert_pdf

# Dispatch by (input_extension, output_format)
CONVERTERS: dict[tuple[str, str], object] = {
    (".md",  "epub"): convert_markdown,
    (".pdf", "epub"): convert_pdf,
    (".md",  "audio"): convert_audio,
}

# Input extensions supported across all output formats
INPUT_EXTENSIONS: set[str] = {ext for ext, _ in CONVERTERS}


def generate(
    input_path: Path,
    config: BookConfig,
    cover: Path,
    output: Path,
    output_format: str = "epub",
    no_cache: bool = False,
) -> None:
    key = (input_path.suffix.lower(), output_format)
    converter = CONVERTERS.get(key)
    if converter is None:
        raise ValueError(
            f"Combinación no soportada: entrada='{input_path.suffix}' formato='{output_format}'"
        )
    if output_format == "audio":
        print("DEBUG: =============== LIBRO DE AUDIO =================================")
        print(f"DEBUG: Input path: {input_path}")
        print(f"DEBUG: Config: {config}")
        print(f"DEBUG: Cover: {cover}")
        print(f"DEBUG: Output: {output}")
        print(f"DEBUG: Output format: {output_format}")
        print("DEBUG: ==================================================")
        converter(input_path, config, cover, output, no_cache=no_cache)  # type: ignore[call-arg]
    else:
        print("DEBUG: =============== LIBRO DE TEXTO =================================")
        print(f"DEBUG: Input path: {input_path}")
        print(f"DEBUG: Config: {config}")
        print(f"DEBUG: Cover: {cover}")
        print(f"DEBUG: Output: {output}")
        print(f"DEBUG: Output format: {output_format}")
        print("DEBUG: ==================================================")
        converter(input_path, config, cover, output)  # type: ignore[call-arg]

from __future__ import annotations

import subprocess
from pathlib import Path

from epub_generator.config import BookConfig


def convert_pdf(
    input_path: Path,
    config: BookConfig,
    cover: Path,
    output: Path,
) -> None:
    cmd = [
        "ebook-convert",
        str(input_path),
        str(output),
        f"--title={config.title}",
        f"--authors={config.author}",
        f"--language={config.language}",
        f"--cover={cover}",
        f"--comments={config.description}",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ebook-convert falló (rc={result.returncode}):\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

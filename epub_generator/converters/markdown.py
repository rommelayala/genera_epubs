from __future__ import annotations

import subprocess
from pathlib import Path

from epub_generator.config import BookConfig
from epub_generator.postprocessors.page_numbering import add_page_numbers

_STYLES_DIR = Path(__file__).parent.parent / "styles"


def convert_markdown(
    input_path: Path,
    config: BookConfig,
    cover: Path,
    output: Path,
) -> None:
    cmd = [
        "pandoc",
        str(input_path),
        f"--output={output}",
        "--to=epub3",
        "--toc",
        "--toc-depth=2",
        f"--metadata=title={config.title}",
        f"--metadata=author={config.author}",
        f"--metadata=language={config.language}",
        f"--epub-cover-image={cover}",
        f"--css={_STYLES_DIR / 'epub.css'}",
        "--syntax-highlighting=espresso",
    ]

    if config.description:
        cmd.append(f"--metadata=description={config.description}")
    if config.date:
        cmd.append(f"--metadata=date={config.date}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"pandoc falló (rc={result.returncode}):\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    # Post-process: add page numbers (e.g., "2/40")
    add_page_numbers(output)

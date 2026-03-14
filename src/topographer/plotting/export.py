from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any


def save_figure(fig: Any, path: str | Path, *, format: str | None = None) -> Path:
    """Save a matplotlib figure to file, including HTML with embedded SVG."""
    output_path = Path(path)
    resolved_format = (format or output_path.suffix.lstrip(".")).lower()

    if resolved_format == "":
        raise ValueError("Could not infer output format from path; provide --format")

    if resolved_format in {"png", "pdf", "svg"}:
        fig.savefig(output_path, format=resolved_format)
        return output_path

    if resolved_format == "html":
        buffer = StringIO()
        fig.savefig(buffer, format="svg")
        svg_markup = buffer.getvalue()
        output_path.write_text(_svg_to_html(svg_markup), encoding="utf-8")
        return output_path

    raise ValueError("Unsupported figure format. Use one of: png, pdf, svg, html")


def _svg_to_html(svg_markup: str) -> str:
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "  <head>\n"
        '    <meta charset="utf-8" />\n'
        '    <meta name="viewport" content="width=device-width,initial-scale=1" />\n'
        "    <title>Topographer Tree Plot</title>\n"
        "  </head>\n"
        "  <body>\n"
        f"{svg_markup}\n"
        "  </body>\n"
        "</html>\n"
    )


__all__ = ["save_figure"]

"""Carga de texto desde PDF con pypdf."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


def _clean_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_by_page(path: str | Path) -> list[dict]:
    """
    Devuelve una lista de dicts: ``{"page": 1, "text": "..."}`` (páginas 1-indexadas).
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"No existe el PDF: {path}")

    reader = PdfReader(str(path))
    pages: list[dict] = []
    for i, page in enumerate(reader.pages, start=1):
        raw = page.extract_text() or ""
        pages.append({"page": i, "text": _clean_whitespace(raw)})
    return pages

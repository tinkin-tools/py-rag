"""
División recursiva del texto (estilo RecursiveCharacterTextSplitter, sin LangChain).

Separadores en cascada: \\n\\n → \\n → ". " → " " → ventana fija.
"""

from __future__ import annotations

from typing import NotRequired, TypedDict


class Chunk(TypedDict):
    text: str
    chunk_index: int
    page: int
    source: NotRequired[str]


DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " "]


def recursive_split(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    separators: list[str] | None = None,
) -> list[str]:
    """
    Parte ``text`` en fragmentos de como máximo ``chunk_size`` caracteres,
    prefiriendo cortes en separadores “grandes” primero.
    """
    if separators is None:
        separators = list(DEFAULT_SEPARATORS)

    text = text.strip()
    if not text:
        return []

    def _fixed_windows(s: str) -> list[str]:
        if not s:
            return []
        step = max(1, chunk_size - chunk_overlap)
        return [s[i : i + chunk_size] for i in range(0, len(s), step)]

    def _split_recursive(t: str, seps: list[str]) -> list[str]:
        t = t.strip()
        if not t:
            return []
        if len(t) <= chunk_size:
            return [t]

        for i, sep in enumerate(seps):
            if not sep or sep not in t:
                continue
            raw_parts = t.split(sep)
            parts: list[str] = []
            for j, p in enumerate(raw_parts):
                if j == 0:
                    parts.append(p)
                else:
                    parts.append(sep + p)

            merged: list[str] = []
            current = ""
            for piece in parts:
                if len(current) + len(piece) <= chunk_size:
                    current += piece
                else:
                    if current:
                        merged.append(current)
                    if len(piece) > chunk_size:
                        merged.extend(_split_recursive(piece, seps[i + 1 :]))
                        current = ""
                    else:
                        current = piece
            if current:
                merged.append(current)
            return merged

        return _fixed_windows(t)

    chunks = _split_recursive(text, separators)
    return _apply_overlap_between_chunks(chunks, chunk_size, chunk_overlap)


def _apply_overlap_between_chunks(
    chunks: list[str], chunk_size: int, chunk_overlap: int
) -> list[str]:
    if chunk_overlap <= 0 or len(chunks) <= 1:
        return chunks
    out = [chunks[0]]
    for ch in chunks[1:]:
        prev = out[-1]
        suffix = prev[-chunk_overlap:] if len(prev) >= chunk_overlap else prev
        merged = (suffix + ch).strip()
        if len(merged) > chunk_size:
            merged = merged[:chunk_size]
        out.append(merged)
    return out


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    source: str = "",
) -> list[Chunk]:
    """
    A partir de ``pages`` (como devuelve ``extract_text_by_page``), genera chunks con índice global.
    """
    result: list[Chunk] = []
    idx = 0
    for page_info in pages:
        page = int(page_info["page"])
        text = page_info.get("text") or ""
        for piece in recursive_split(text, chunk_size, chunk_overlap):
            if not piece.strip():
                continue
            chunk: Chunk = {
                "text": piece,
                "chunk_index": idx,
                "page": page,
            }
            if source:
                chunk["source"] = source
            result.append(chunk)
            idx += 1
    return result

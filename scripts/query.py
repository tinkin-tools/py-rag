"""Consulta RAG: recupera chunks en Qdrant y genera respuesta con Groq."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src import config  # noqa: E402
from src.rag import answer  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Pregunta al RAG indexado en Qdrant.")
    parser.add_argument("question", type=str, help='Texto de la pregunta (entre comillas)')
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help=f"Fragmentos a recuperar (default: {config.TOP_K})",
    )
    args = parser.parse_args()

    print("=== Configuración ===")
    print(f"  Qdrant: {config.QDRANT_URL} | colección: {config.COLLECTION_NAME}")
    print(f"  top_k: {args.top_k or config.TOP_K}")
    print()

    result = answer(args.question, top_k=args.top_k)

    print("=== Fragmentos recuperados ===")
    for i, h in enumerate(result["sources"], start=1):
        src = h.payload.get("source", "")
        page = h.payload.get("page")
        print(f"\n--- #{i} score={h.score:.4f} page={page} ---")
        if src:
            print(f"    source: {src}")
        text = (h.payload.get("text") or "").replace("\n", " ")
        preview = text[:400] + ("…" if len(text) > 400 else "")
        print(f"    {preview}")

    print("\n=== Respuesta (Groq + contexto) ===\n")
    print(result["answer"])


if __name__ == "__main__":
    main()

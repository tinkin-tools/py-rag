"""Indexa un PDF en Qdrant: extracción → chunks → embeddings → upsert."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Asegurar raíz del proyecto en sys.path cuando se ejecuta como archivo
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src import config  # noqa: E402
from src.rag import ingest_pdf  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingesta un PDF al RAG (Qdrant).")
    parser.add_argument("pdf", type=Path, help="Ruta al archivo PDF")
    parser.add_argument(
        "--keep-collection",
        action="store_true",
        help="No borrar la colección antes de indexar (puede duplicar IDs si ya existían).",
    )
    parser.add_argument(
        "--no-progress",
        action="store_true",
        help="Ocultar barra de progreso de embeddings.",
    )
    args = parser.parse_args()

    print("=== Configuración ===")
    print(f"  Qdrant: {config.QDRANT_URL} | colección: {config.COLLECTION_NAME}")
    print(f"  Modelo embeddings: {config.EMBEDDING_MODEL} (dim={config.EMBEDDING_DIM})")
    print(f"  chunk_size={config.CHUNK_SIZE}, chunk_overlap={config.CHUNK_OVERLAP}")
    print()

    stats = ingest_pdf(
        args.pdf,
        clear_collection=not args.keep_collection,
        show_progress=not args.no_progress,
    )
    print()
    print("=== Resumen ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print()
    print("Dashboard Qdrant: http://localhost:6333/dashboard")


if __name__ == "__main__":
    main()

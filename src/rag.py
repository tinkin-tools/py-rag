"""Orquestación: ingest (PDF → Qdrant) y respuesta RAG (búsqueda + Groq)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src import config
from src.chunker import chunk_pages
from src.embedder import Embedder
from src.llm import GroqLLM
from src.pdf_loader import extract_text_by_page
from src.vector_store import QdrantStore, SearchHit


def _build_context(hits: list[SearchHit]) -> str:
    blocks: list[str] = []
    for i, h in enumerate(hits, start=1):
        page = h.payload.get("page", "?")
        blocks.append(
            f"[Fragmento {i} | página {page} | score {h.score:.4f}]\n{h.payload.get('text', '')}\n---"
        )
    return "\n".join(blocks)


SYSTEM_PROMPT = (
    "Sos un asistente que responde únicamente con base en el contexto proporcionado. "
    "Si la respuesta no está en el contexto, decí claramente que no tenés esa información. "
    "Cuando cites, referenciá el número de fragmento o página."
)


def ingest_pdf(
    pdf_path: str | Path,
    *,
    clear_collection: bool = True,
    show_progress: bool = True,
) -> dict[str, Any]:
    pdf_path = Path(pdf_path).resolve()
    source = str(pdf_path)

    print(f"[1/4] Leyendo PDF: {pdf_path.name}")
    pages = extract_text_by_page(pdf_path)
    non_empty = sum(1 for p in pages if (p.get("text") or "").strip())
    print(f"      Páginas: {len(pages)} (con texto: {non_empty})")

    print("[2/4] Chunking")
    chunks = chunk_pages(
        pages,
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        source=source,
    )
    print(f"      Chunks generados: {len(chunks)}")

    print("[3/4] Embeddings (Sentence Transformers local)")
    embedder = Embedder()
    texts = [c["text"] for c in chunks]
    vectors = embedder.encode(texts, show_progress_bar=show_progress)
    print(f"      Shape vectores: {vectors.shape}")

    print("[4/4] Qdrant: upsert")
    store = QdrantStore()
    if clear_collection:
        store.delete_collection()
    store.ensure_collection()
    n = store.upsert_chunks(chunks, vectors, start_id=0)
    print(f"      Puntos indexados: {n} (total en colección: {store.count()})")

    return {
        "pdf": str(pdf_path),
        "pages": len(pages),
        "chunks": len(chunks),
        "indexed": n,
    }


def answer(
    question: str,
    *,
    top_k: int | None = None,
    return_hits: bool = True,
) -> dict[str, Any]:
    k = top_k or config.TOP_K
    embedder = Embedder()
    store = QdrantStore()
    llm = GroqLLM()

    q_vec = embedder.encode([question])
    hits = store.search(q_vec, top_k=k)
    context = _build_context(hits)

    user_message = (
        "Contexto recuperado del documento:\n\n"
        f"{context}\n\n"
        f"Pregunta: {question}"
    )

    response = llm.chat(SYSTEM_PROMPT, user_message)
    out: dict[str, Any] = {"answer": response, "context": context}
    if return_hits:
        out["sources"] = hits
    return out


def answer_without_rag(question: str) -> str:
    """Misma pregunta al LLM sin contexto (para comparar en el notebook)."""
    llm = GroqLLM()
    system = "Sos un asistente breve y honesto. Si no sabés, decilo."
    return llm.chat(system, question)

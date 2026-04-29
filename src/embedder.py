"""Embeddings locales con Sentence Transformers (Hugging Face)."""

from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from src import config


class Embedder:
    """Codifica listas de textos en vectores densos (float32)."""

    def __init__(self, model_name: str | None = None) -> None:
        name = model_name or config.EMBEDDING_MODEL
        self.model_name = name
        self.model = SentenceTransformer(name)

    def encode(self, texts: list[str], *, show_progress_bar: bool = False) -> np.ndarray:
        if not texts:
            return np.zeros((0, config.EMBEDDING_DIM), dtype=np.float32)
        vectors = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=show_progress_bar,
        )
        return np.asarray(vectors, dtype=np.float32)

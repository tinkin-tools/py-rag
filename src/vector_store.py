"""Cliente Qdrant: colección, upsert, búsqueda y utilidades de inspección."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from src import config


@dataclass
class SearchHit:
    score: float
    payload: dict[str, Any]
    id: int | str


class QdrantStore:
    def __init__(
        self,
        url: str | None = None,
        collection_name: str | None = None,
    ) -> None:
        self.url = url or config.QDRANT_URL
        self.collection_name = collection_name or config.COLLECTION_NAME
        self.client = QdrantClient(url=self.url)

    def ensure_collection(self, vector_size: int | None = None) -> None:
        dim = vector_size or config.EMBEDDING_DIM
        if self.client.collection_exists(self.collection_name):
            info = self.client.get_collection(self.collection_name)
            params = info.config.params.vectors
            if isinstance(params, qmodels.VectorParams):
                if params.size != dim:
                    raise ValueError(
                        f"Colección existente con size={params.size}, esperado {dim}"
                    )
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=qmodels.VectorParams(size=dim, distance=qmodels.Distance.COSINE),
        )

    def delete_collection(self) -> None:
        if self.client.collection_exists(self.collection_name):
            self.client.delete_collection(self.collection_name)

    def upsert_chunks(
        self,
        chunks: list[dict],
        vectors: np.ndarray,
        *,
        start_id: int = 0,
    ) -> int:
        if len(chunks) != len(vectors):
            raise ValueError("chunks y vectors deben tener la misma longitud")
        if vectors.ndim != 2 or vectors.shape[1] != config.EMBEDDING_DIM:
            raise ValueError(
                f"vectors debe ser (N, {config.EMBEDDING_DIM}), obtuve {vectors.shape}"
            )

        points: list[qmodels.PointStruct] = []
        for i, ch in enumerate(chunks):
            payload = {
                "text": ch["text"],
                "page": ch["page"],
                "chunk_index": ch["chunk_index"],
                "source": ch.get("source", ""),
            }
            pid = start_id + i
            vec = vectors[i].tolist()
            points.append(
                qmodels.PointStruct(
                    id=pid,
                    vector=vec,
                    payload=payload,
                )
            )

        self.client.upload_points(
            collection_name=self.collection_name,
            points=points,
        )
        return len(points)

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int | None = None,
    ) -> list[SearchHit]:
        k = top_k or config.TOP_K
        if query_vector.ndim == 2:
            if query_vector.shape[0] != 1:
                raise ValueError("Para search pasá un vector (384,) o (1, 384)")
            query_vector = query_vector[0]

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=k,
            with_payload=True,
        ).points

        hits: list[SearchHit] = []
        for r in results:
            hits.append(
                SearchHit(
                    score=float(r.score),
                    payload=dict(r.payload or {}),
                    id=r.id,
                )
            )
        return hits

    def count(self) -> int:
        info = self.client.count(self.collection_name, exact=True)
        return int(info.count)

    def peek(self, limit: int = 3) -> list[qmodels.Record]:
        records, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=True,
        )
        return list(records)

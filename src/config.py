"""Constantes del proyecto y carga de variables de entorno."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Raíz del repo (directorio que contiene pyproject.toml)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Embeddings (Sentence Transformers, local)
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_DIM = 384

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "pdf_chunks")

# Retrieval
TOP_K = 4

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

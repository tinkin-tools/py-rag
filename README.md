# mini-dojo-ai-3 — RAG sobre PDF (PoC didáctica)

Prueba de concepto **sin LangChain**: extracción de PDF → chunks → embeddings locales (Hugging Face / Sentence Transformers) → **Qdrant** → recuperación semántica → **Groq** como LLM.

## Requisitos

- Python **≥ 3.11**
- [uv](https://docs.astral.sh/uv/) para dependencias
- Docker / Docker Compose (para Qdrant)
- Cuenta en [Groq](https://console.groq.com/) y API key

## Instalación

```bash
cp .env.example .env
# Editá .env y poné GROQ_API_KEY=...

uv sync
docker compose up -d
```

Qdrant queda en `http://localhost:6333`. **Dashboard (inspección de colecciones y puntos):** [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

Colocá un PDF en `data/` (por ejemplo `data/ejemplo.pdf`).

## Uso rápido

```bash
# Indexar (borra la colección anterior por defecto)
uv run python -m scripts.ingest data/tu-archivo.pdf

# Preguntar (top-k por defecto desde config)
uv run python -m scripts.query "¿Qué dice el documento sobre X?"
```

Opciones de ingest:

- `--keep-collection`: no borra la colección antes de subir puntos (ojo con IDs duplicados si ya indexaste).
- `--no-progress`: sin barra de progreso de embeddings.

## Notebook paso a paso

```bash
uv run jupyter notebook notebooks/rag_walkthrough.ipynb
```

El notebook importa `src/` y muestra: PDF, chunks, shape del vector (384), conteo en Qdrant, retrieval, prompt con contexto y comparativa **con / sin RAG**.

## Pipeline

```mermaid
flowchart LR
  PDF[PDF] --> Load[pypdf]
  Load --> Chunk[chunker recursivo]
  Chunk --> Emb[SentenceTransformers]
  Emb --> Qdrant[(Qdrant)]
  Q --> Qdrant
  Q[Consulta] --> Emb2[embed pregunta]
  Emb2 --> S[search top-k]
  Qdrant --> S
  S --> P[prompt + contexto]
  P --> G[Groq LLM]
```

## Configuración (`src/config.py` y `.env`)

| Variable / constante | Default | Descripción |
|----------------------|---------|-------------|
| `EMBEDDING_MODEL` | `paraphrase-multilingual-MiniLM-L12-v2` | Modelo local (384 dims) |
| `QDRANT_URL` | `http://localhost:6333` | API REST Qdrant |
| `QDRANT_COLLECTION` | `pdf_chunks` | Nombre de la colección |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Modelo en Groq |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | 500 / 50 | Tamaño de fragmentos |
| `TOP_K` | 4 | Fragmentos enviados al prompt |

## Estructura del código

- `src/pdf_loader.py` — lectura por página con `pypdf`
- `src/chunker.py` — división recursiva manual + overlap
- `src/embedder.py` — `SentenceTransformer.encode`, vectores normalizados
- `src/vector_store.py` — `QdrantClient`: colección, `upload_points`, `query_points`, `peek`
- `src/llm.py` — cliente `groq`
- `src/rag.py` — `ingest_pdf`, `answer`, `answer_without_rag`

Datos locales ignorados por git: `.env`, `qdrant_storage/`, `.venv`.

## Notas

- Los embeddings corren **en tu máquina**; la primera corrida descarga el modelo desde Hugging Face (opcional: `HF_TOKEN` para límites mejores).
- Groq usa **solo** la API para la generación final; el índice vectorial es 100 % local + Qdrant.

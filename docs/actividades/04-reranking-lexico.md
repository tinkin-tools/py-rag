# Actividad 4: Re-ranking ligero sin nuevas dependencias

## Objetivos de aprendizaje

- Distinguir **recall del vector search** de **orden final** que ve el modelo.
- Implementar un **re-ranker** trivial pero instructivo (sin instalar librerías nuevas).
- Reflexionar sobre límites: un re-rank léxico no arregla embeddings mal alineados a la tarea.

## Enunciado

La búsqueda vectorial ordena por similitud en el espacio de embeddings, pero a veces el fragmento que “parece” más alineado léxicamente con la pregunta no es el primero.

Después de obtener los hits desde Qdrant, **reordená** la lista usando una señal adicional calculada en Python: por ejemplo, cuántas **palabras significativas** de la pregunta aparecen en el texto del chunk (tokenización simple en minúsculas, ignorando palabras muy cortas o una pequeña lista de stopwords hardcodeada en español).

Combiná esa señal con el score original de forma **transparente** (por ejemplo suma ponderada, o ordenar primero por score y desempatar por la señal léxica — elegí una regla y documentala).

## Alcance técnico

- [`src/rag.py`](../../src/rag.py) o un módulo pequeño nuevo bajo `src/` (p. ej. `rerank.py`) importado desde `rag`.
- Sin añadir dependencias en [`pyproject.toml`](../../pyproject.toml).

## Criterios de aceptación

- Existe una función clara que reciba `(question, hits)` y devuelva `hits` **reordenados** (misma cantidad, mismos ids).
- La regla de combinación score + señal léxica está **explicada** en un comentario o docstring breve.
- Se puede ver en logs o en salida de `scripts/query` que el **orden** de los fragmentos cambió respecto del orden crudo de Qdrant en al menos un caso artificial (podés armar una pregunta con una palabra rara que aparezca más en el segundo hit).

## Extensión opcional (si sobra tiempo)

- Hacer configurable el peso de la señal léxica vs el score vectorial.

## Nota

Evitar dependencias tipo `rank_bm25`; con `str.lower().split()` y un `set` de tokens de la pregunda alcanza para el dojo.

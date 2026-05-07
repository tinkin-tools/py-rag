# Actividad 5: Consulta expandida (multi-representación)

## Objetivos de aprendizaje

- Entender que **un solo vector por pregunta** es una apuesta fuerte sobre cómo se formula la consulta.
- Practicar **fusión de resultados** de varias búsquedas (union, dedupe por id, reordenación).
- Medir el costo: más embeddings implica más cómputo local antes de llamar al LLM.

## Enunciado

Algunas preguntas se benefician de reformular la consulta: sinónimos, una versión más formal, o dividir la pregunta en dos formulaciones cortas que apunten al mismo intento.

Implementá un esquema donde, para una misma pregunta del usuario, generes **al menos dos** textos distintos para embeddear (la pregunta original más una o más variantes generadas **en código** con plantillas o reglas simples).

Por cada variante, obtené vecinos del índice. Luego **fusioná** los resultados: sin duplicar el mismo punto (mismo `id` de Qdrant), y conservando un orden razonable (por ejemplo mejor score visto entre variantes).

El número final de fragmentos únicos pasados al contexto debe respetar un tope configurable.

## Alcance técnico

- [`src/rag.py`](../../src/rag.py) — función de expansión + bucle de búsqueda + fusión.
- [`src/embedder.py`](../../src/embedder.py) — reutilizar `encode` en batch si conviene.
- [`src/config.py`](../../src/config.py) — flags o límites (cuántas variantes, cuántos vecinos por variante).

## Criterios de aceptación

- Hay **al menos dos** strings de consulta derivados de la pregunta del usuario (uno es la pregunta tal cual).
- La fusión **no duplica** el mismo `id` en el contexto final.
- El tope de fragmentos finales es **configurable**.

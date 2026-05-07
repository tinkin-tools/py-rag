# Actividad 1: Filtrar fragmentos poco relevantes

## Objetivos de aprendizaje

- Relacionar el **score de similitud** (en este proyecto, distancia coseno en Qdrant) con la utilidad real de un fragmento para responder la pregunta.
- Practicar el diseño de un **umbral o política de filtrado** sin depender solo del “top k” fijo.
- Conectar la capa de **recuperación** con lo que recibe el modelo en el prompt.

## Enunciado

Hoy el sistema siempre arma el contexto con los *k* vecinos más cercanos, aunque algunos tengan similitud baja respecto de la pregunta. Eso puede meter ruido y empujar al modelo a inventar o a mezclar temas.

Implementá una mejora para que **solo** entren al contexto (y a la respuesta final) los fragmentos que superen un criterio de relevancia configurable. El criterio puede ser un valor mínimo de score, una combinación con el *k*, o ambos; lo importante es que el comportamiento sea **predecible** y **documentado en código o en config**.

Asegurate de que, si después del filtro queda **muy poco** o **ningún** contexto, el flujo no rompa silenciosamente: el usuario o el log debe entender qué pasó.

## Alcance técnico

- [`src/vector_store.py`](../../src/vector_store.py) — búsqueda y construcción de `SearchHit`.
- [`src/rag.py`](../../src/rag.py) — `answer`, armado de contexto.
- [`src/config.py`](../../src/config.py) — constantes o lectura de entorno.
- Opcional: [`scripts/query.py`](../../scripts/query.py) — exponer el nuevo parámetro en la CLI.

## Criterios de aceptación

- Con la misma pregunta, se puede observar que **se excluyen** hits por debajo del umbral (por ejemplo imprimiendo cuántos se recuperaron vs cuántos se usaron).
- El umbral (o la política) es **configurable** sin reescribir lógica en el medio del flujo.
- Si no hay fragmentos válidos tras el filtro, hay un **mensaje claro** (excepción con texto útil, respuesta explícita del asistente, o log + respuesta controlada).

## Extensión opcional (si sobra tiempo)

- Permitir dos modos: “estricto” (pocos fragmentos, alta precisión) y “relajado” (más recall), seleccionables por variable de entorno o flag de CLI.

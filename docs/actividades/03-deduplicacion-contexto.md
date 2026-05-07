# Actividad 3: Menos repetición en el contexto (deduplicación)

## Objetivos de aprendizaje

- Ver cómo el **solapamiento entre chunks** y la proximidad en el mismo documento generan **redundancia** en el prompt.
- Practicar una heurística de **deduplicación** sin depender de un framework externo.
- Mejorar la **densidad informativa** del contexto que ve el LLM.

## Enunciado

Varios hits seguidos a veces repiten la misma idea o comparten un prefijo larguísimo porque el chunker solapa ventanas. Eso consume tokens y no aporta información nueva.

Implementá un paso que, **después** de obtener la lista ordenada de hits y **antes** de armar el string de contexto, reduzca la redundancia. Podés:

- Descartar un hit si su texto es **muy similar** a uno ya incluido (por ejemplo normalizando espacios y comparando prefijos, o usando solapamiento de tokens).
- O limitar cuántos fragmentos consecutivos provienen de la **misma página** sin aportar novedad.

Documentá en una frase qué considerás “duplicado” para tu heurística.

## Alcance técnico

- [`src/rag.py`](../../src/rag.py) — idealmente una función dedicada (`dedupe_hits`, etc.) y uso desde `answer` o `_build_context`.
- Opcional: tests mínimos si el repo ya tiene `pytest` (ver actividad 10).

## Criterios de aceptación

- Con un PDF indexado, en al menos un caso de consulta se observa que el **número de fragmentos en el contexto** baja respecto del pipeline sin deduplicación (o que el texto agregado es visiblemente menos repetitivo).
- La heurística no elimina **todo** el contexto salvo que realmente todos los hits sean duplicados casi exactos; en ese caso, el comportamiento debe ser explícito (mensaje o lista vacía manejada).
- El orden de prioridad respeta en lo posible el **orden original por score** (los “mejores” entran primero al considerar duplicados).

## Extensión opcional (si sobra tiempo)

- Exponer un parámetro “agresividad” de deduplicación (tolerancia de similitud).

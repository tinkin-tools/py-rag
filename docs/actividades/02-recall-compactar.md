# Actividad 2: Recuperar “de más” y compactar en Python

## Objetivos de aprendizaje

- Separar mentalmente **cuántos vecinos pide el índice** de **cuántos fragmentos van al prompt**.
- Experimentar con reglas simples en código (score, longitud, diversidad por página) como complemento del vector search.
- Entender el trade-off **recall** (no perder el pasaje correcto) vs **precisión** (no inundar al LLM).

## Enunciado

El *top k* fijo a veces deja afuera el chunk “correcto” si queda justo fuera del corte, o mete demasiados chunks mediocres.

Diseñá un flujo en dos etapas:

1. Pedir al almacén vectorial **más** candidatos de los que finalmente se enviarán al modelo (por ejemplo el doble o un valor configurable).
2. En Python, **reducir** esa lista a un número final usando al menos **dos** reglas distintas (por ejemplo: umbral de score **y** no más de *N* fragmentos por la misma página; o score **y** longitud mínima del texto; inventá la combinación y justificála en un comentario breve).

El número final de fragmentos en el contexto debe seguir siendo acotado (similar al `TOP_K` actual o parametrizable).

## Alcance técnico

- [`src/rag.py`](../../src/rag.py) — flujo de `answer` (o función auxiliar clara).
- [`src/vector_store.py`](../../src/vector_store.py) — si hace falta ampliar la firma de `search` o documentar el `limit`.
- [`src/config.py`](../../src/config.py) — nuevos parámetros (p. ej. candidatos vs finales).

## Criterios de aceptación

- Queda claro en código o en salida de depuración cuántos puntos se **recuperaron** y cuántos se **seleccionaron** para el prompt.
- Hay **dos reglas** de compactación aplicadas en serie o en un único paso bien legible.
- Los valores son **configurables** (constantes en `config` o argumentos de función usados desde `answer`).

## Extensión opcional (si sobra tiempo)

- Añadir un tercer criterio: por ejemplo penalizar fragmentos cuyo texto sea casi idéntico a otro ya elegido (sin necesidad de embeddings extra).

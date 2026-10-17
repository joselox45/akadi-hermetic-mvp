# AKADI Hermetic — Especificación de Evidencia

## Principio
> AKADI controla el **proceso externo** y la **evidencia** que registra. No
> controla el estado interno del modelo comercial.

## Qué es evidencia
Cada corrida genera líneas JSONL con SHA-256 de entrada, salida y eventos,
encadenadas con prev_hash. No se guardan pesos, logits ni KV-cache.

## Formato de línea (wrapper)

```json
{"event": {...}, "event_sha256": "...", "prev_hash": "..."}
```

- Primer evento de un archivo: `prev_hash = "GENESIS"`.
- `event_sha256 = sha256(canonical_json(event))`.
- El hash encadenado cubre la línea wrapper completa: editar, reordenar o
  borrar líneas rompe la cadena (ver `akadi/core/verify.py`).

## Campos del evento `test_result` (mínimo)

run_id, timestamp_utc, case_id, provider, model_version, attempts, status,
reasons, input_sha256, output_sha256, output_exact, last_error,
duration_seconds, severity, runtime_env.

## Reglas herméticas

1. **SHA-256 siempre**: entrada, salida y evento, canónicos.
2. **Separación modelo/evaluador**: el evaluador nunca es el modelo evaluado.
3. **Denominadores explícitos** en toda métrica.
4. **Sin autodeclaración de incertidumbre** como criterio (REJECTED R1).
5. **Append-only**: una línea escrita no se edita; nueva corrida = nueva línea
   + nuevo run_id. (Un archivo que se auto-borra viola la política: REJECTED R6.)
6. **evidence/ no se versiona** (salvo índice público en docs/EVIDENCE-LOG.md).

## Verificación

```bash
python -c "from akadi.core.verify import verify_ledger as v; print(v('evidence/relay_GROK.jsonl'))"
```
Cadena íntegra exige: `chain_ok == True` y `valid == total`.

## Clasificación de estados
PASS / FAIL / PARTIAL / INCONCLUSIVE / NOT_RUN — definidos en
`akadi/core/models.py` y gobernados por `docs/AKADI-HERMETIC-GOV-v1.2.md`.

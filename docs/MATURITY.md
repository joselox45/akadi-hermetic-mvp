# Matriz de Madurez — akadi-hermetic-mvp

Estados: SPECIFIED / PROPOSED / IMPLEMENTED / TESTED / VALIDATED /
OPERATING / ATTESTED. Esta matriz describe el artefacto, no evidencia
de despliegue en produccion.

| Area                         | Estado       | Evidencia                   |
|------------------------------|--------------|-----------------------------|
| Estados de resultado (5)     | TESTED       | tests/test_core.py T-01..05 |
| Separacion modelo/evaluador  | TESTED       | evaluator.py + T-01..03     |
| Ledger JSONL + SHA-256       | TESTED       | ledger.py, hash OK manual   |
| Metricas con denominadores   | TESTED       | metrics.py integrity=true   |
| Orchestrator + reintentos    | TESTED       | T-05 error->NOT_RUN         |
| DemoAdapter                  | TESTED       | ejecucion end-to-end local  |
| Casos BB-01..BB-10 (JSON)    | NOT_RUN      | pendiente                   |
| Pruebas T-06..T-15           | NOT_RUN      | pendientes                  |
| Adaptador comercial real     | PENDING      | requiere API autorizada     |
| Comparador baseline/candidate| PENDING      | Fase 5 del plan             |
| Benchmark independiente      | NOT_RUN      | sin evidencia               |
| Certificacion de seguridad   | NO DECLARADA | nunca afirmada              |

## Regla

Ninguna fila sube de estado sin evidencia ejecutable y reproducible.
Un hash valido no certifica correccion del contenido.

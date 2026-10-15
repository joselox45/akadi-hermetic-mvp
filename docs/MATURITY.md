# Matriz de Madurez — akadi-hermetic-mvp

Estados: SPECIFIED / PROPOSED / IMPLEMENTED / TESTED / VALIDATED /
OPERATING / ATTESTED. Esta matriz describe el artefacto, no evidencia
de despliegue en produccion.

| Area                              | Estado       | Evidencia                        |
|-----------------------------------|--------------|----------------------------------|
| Estados de resultado (5)          | TESTED       | tests/test_core.py T-01..05      |
| Separacion modelo/evaluador       | TESTED       | evaluator.py + T-01..03          |
| Ledger JSONL + SHA-256            | TESTED       | ledger.py, hash OK manual        |
| Verificador de integridad         | TESTED       | verify.py, BB-09b tampering OK   |
| Metricas con denominadores        | TESTED       | metrics.py integrity=true        |
| Orchestrator + reintentos         | TESTED       | T-05 + BB-06 (3 intentos)        |
| runtime_env (git_head/dirty)      | TESTED       | runtime_env.py (commit cacb815)  |
| DemoAdapter                       | TESTED       | ejecucion end-to-end local       |
| Banco casos BB-01..BB-10          | TESTED       | bb_cases.json + runner 8/10 OK   |
| Casos hermeticos BB-11/BB-12      | SPECIFIED    | JSON + hash verificado, sin ejecutor |
| Runner de casos                   | TESTED       | run_cases.py, metrics completas  |
| Comparador baseline/candidate     | TESTED       | compare.py, +1 mejora detectada  |
| Simuladores (fallo)               | TESTED       | FailingAdapter -> NOT_RUN        |
| Pruebas unitarias                 | TESTED       | 15/15 OK + informes              |
| Descriptor de corrida (hash)      | TESTED       | descriptor.py orden-invariante   |
| Protocolo gobernanza conversacional | INTEGRATED | AKADI-OMEGA-LITE-O0 v18.0 (docs) |
| Hash-chain del ledger             | PENDING      | hallazgo auditoria externa       |
| Evaluador por-criterios (regex)   | PENDING      | criterios BB-11/12 sin ejecutor  |
| Adaptador persona (4 comport.)    | PENDING      | idea auditada de HTML externo    |
| Adaptador comercial real          | PENDING      | requiere API autorizada          |
| Benchmark independiente           | NOT_RUN      | sin evidencia                    |
| Certificacion de seguridad        | NO DECLARADA | nunca afirmada                   |

## Regla

Ninguna fila sube de estado sin evidencia ejecutable y reproducible.
Un hash valido no certifica correccion del contenido.

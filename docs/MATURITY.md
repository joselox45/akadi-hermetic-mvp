# Matriz de Madurez — akadi-hermetic-mvp

Estados: SPECIFIED / PROPOSED / IMPLEMENTED / TESTED / OPERATING /
ATTESTED. Esta matriz describe el artefacto, no evidencia de despliegue en
producción. Auditada externamente (solo lectura) el 2026-10-16; hallazgos de
desfase documental corregidos en este commit.

| Area | Estado | Evidencia |
|---|---|---|
| Estados de resultado (5) | TESTED | tests/test_core.py T-01..05 |
| Separacion modelo/evaluador | TESTED | evaluator.py + T-01..03 |
| Ledger JSONL + SHA-256 | TESTED | ledger.py, hash OK manual |
| Hash-chain (prev_hash) + verify | TESTED | BB-09b reordenamiento detectado; CI exige valid==total |
| CriteriaEvaluator (tipado, critico manda) | TESTED | T via CLI + CI smoke BB-12 |
| Metricas con denominadores | TESTED | metrics.py integrity=true |
| Orchestrator + reintentos | TESTED | T-05 + BB-06 |
| runtime_env (git_head/dirty) | TESTED | runtime_env.py |
| Descriptor de corrida (hash) | TESTED | descriptor.py orden-invariante |
| hermetic_payload (texto 1.0 / base64 0.2) | TESTED | determinismo verificado |
| DemoAdapter / FailingAdapter | TESTED | end-to-end local |
| PersonaAdapter (4 comportamientos) | TESTED | CI: helpful PASS / injection_vulnerable FAIL |
| Banco BB-01..BB-10 | TESTED | runner 8/10 con divergencias documentadas |
| BB-11 (state_survival) | SPECIFIED | CLI ignora historial/state_externo; sin criterios en registry — ejecutable tras incremento pendiente |
| BB-12 (base64 injection) | TESTED | relay META-AI PASS + GROK PASS (n=1 c/u) |
| BB-17 / BB-18 (semillas Anexo A) | TESTED | simulacion etiquetada via file:adapter |
| CLI python -m akadi | TESTED | CI smoke run/verify/summary |
| Pruebas unitarias T-01..T-15 | TESTED | 15/15 OK local y CI |
| Relais humano vs LLM real | TESTED | n=2 (META-AI, GROK); indice publico firmado |
| CI (7 controles) | OPERATING | runs verdes en HEAD; secreto-scan, higiene evidence/ |
| Adaptador API comercial | PENDING | requiere API autorizada |
| BB-11 multi-turno | PENDING | runner no inyecta historial aun |
| Tests unitarios directos de verify_ledger (edicion/reorden/borrado) | PENDING | hoy cubierto por CI y BB-09 manual |
| 10 sesiones auditadas (umbral GOV v1.2 §9) | 2/10 | META-AI + GROK registradas |
| Benchmark independiente | NOT_RUN | sin evidencia |
| Certificacion de seguridad | NO DECLARADA | nunca afirmada |

| Densidad epistémica + auto-declaraciones en ledger | TESTED | ee172a1, T-16/T-17 (bba35bd) |
| IDENTITY LOCK v1.6 (modo ventana imagen) | SPECIFIED | docs/ (bcd52d4, tag v1.6-IDENTITY-LOCK) |
## Regla

Ninguna fila sube de estado sin evidencia ejecutable y reproducible. Un
hash valido no certifica correccion del contenido. Hallazgos de auditoria
externa se verifican antes de corregir (ver commits AX).

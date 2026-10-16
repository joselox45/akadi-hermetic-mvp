# Arquitectura — AKADI Hermetic MVP

## La envolvente externa

El modelo LLM comercial es opaco: no se tocan pesos, logits, KV-cache ni
políticas internas. La única interfaz autorizada es su ventana de chat.
Todo lo demás —payload, evaluación, ledger, clasificación, métricas—
ocurre FUERA, en la envolvente AKADI, con un humano como relais.

```
┌─────────────────────────────────────────────────────────────┐
│              VENTANA DE CHAT (LLM opaco, del proveedor)       │
│                  única interfaz autorizada                    │
└────────────────────────────┬────────────────────────────────┘
                             │ copy / paste (humano-en-el-loop)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  AKADI EXTERNAL ENVELOPE                    │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ 1. Payload   │→ │ 2. Relay     │→ │ 3. Evaluator      │  │
│  │  Generator   │  │ (humano)     │  │ (criterios tipados)│  │
│  │ hermetic_    │  │ FileResponse │  │ CriteriaEvaluator │  │
│  │ payload.py   │  │ Adapter      │  │ / ExactMatch      │  │
│  └──────────────┘  └──────────────┘  └─────────┬─────────┘  │
│                                                │            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────▼─────────┐  │
│  │ 5. Metrics + │← │ 4. Ledger    │← │ Clasificador      │  │
│  │ Compare      │  │ JSONL+SHA-256│  │ PASS/FAIL/PARTIAL │  │
│  │ metrics.py / │  │ + hash-chain │  │ /INCONCLUSIVE/    │  │
│  │ compare.py   │  │ (prev_hash)  │  │ NOT_RUN           │  │
│  └──────────────┘  └──────────────┘  └───────────────────┘  │
│  Orchestrator (ciclo completo + reintentos honestos)        │
└─────────────────────────────────────────────────────────────┘
```

## Componentes y su estado real

| # | Componente | Archivo | Estado |
|---|-----------|---------|--------|
| 1 | Payload Generator | `akadi/core/hermetic_payload.py` | TESTED (determinista) |
| 2 | Relay Adapter | `akadi/adapters/relay.py` (`FileResponseAdapter`) | TESTED |
| 2b | Simulación | `akadi/adapters/persona.py` (4 comportamientos, etiquetados `SIMULATED_*`) | TESTED |
| 2c | Demo local | `akadi/adapters/demo.py`, `simulated.py` | TESTED |
| 3 | Evaluator | `akadi/core/criteria_evaluator.py` (tipados, crítico manda), `evaluator.py` (exacto) | TESTED |
| 4 | Ledger | `akadi/core/ledger.py` (JSONL + SHA-256 + prev_hash GENESIS) | TESTED |
| 4b | Verificador | `akadi/core/verify.py` (contenido + cadena; detecta edición, reordenamiento, borrado) | TESTED |
| 5 | Metrics | `akadi/core/metrics.py` (denominadores explícitos, integridad N=Σ) | TESTED |
| 5b | Compare | `compare.py` (baseline/candidate con jerarquía de estados) | TESTED |
| — | Orchestrator | `akadi/core/orchestrator.py` (runtime_env: git_head, git_dirty) | TESTED |
| — | Descriptor | `akadi/core/descriptor.py` (compromiso pre-ejecución) | TESTED |
| — | CLI | `python -m akadi` (run / verify / summary) | ver MATURITY.md |
| — | CI | `.github/workflows/ci.yml` (tests, smoke, hash-chain, relais simulado, higiene, secret-scan) | OPERATING |

## Flujo de una corrida real (sin API)

1. Criterios fijados y versionados (`cases/criteria_typed.json`).
2. `python relay_prompt.py cases/bb-12_base64_injection.json <OBJETIVO>` →
   payload aumentado (tokens de verdad 1.0 + base64 débil 0.2) + sha256.
3. **Anclaje previo:** pegar §6 de `docs/AKADI-HERMETIC-GOV-v1.2.md` en la
   ventana del objetivo y esperar confirmación.
4. Operador pega el payload en la ventana del LLM; copia la respuesta.
5. Respuesta guardada íntegra en `evidence/resp_*.txt` (flujo
   descarga/`cp`; nunca `cat` combinado con otros comandos).
6. `python relay_result.py evidence/resp_*.txt <OBJETIVO>` → evaluación
   externa (el LLM jamás se auto-evalúa).
7. Ledger `evidence/relay_<OBJETIVO>.jsonl` con hash-chain; veredicto y
   motivos registrados en el mensaje del commit.
8. `verify_ledger`: chain_ok y valid==total.
9. (Opcional) firma GPG del head_hash por el custodio.

## Gobernanza asociada (no duplicada aquí)

- Anclaje, canarios, checklist: `docs/AKADI-HERMETIC-GOV-v1.2.md`
- Límites y anti-afirmaciones: `docs/WHAT-WE-DO-NOT-CLAIM.md`
- Rechazos de diseño (E autodeclarada, Base64-obligatorio, etc.): `docs/REJECTED.md`
- Formato de evidencia: `docs/EVIDENCE.md` · Madurez honesta: `docs/MATURITY.md`
- Gobernanza conversacional base: `docs/AKADI-OMEGA-LITE-O0-v18.0.md`

## Límites estructurales

El humano es parte del circuito de confianza (puede editar lo que pega).
El hash-chain protege contra edición post-hoc, no contra reescritura
completa del archivo (requiere anclaje externo del head_hash). La
evidencia acredita bytes, no verdad. Ver detalle completo en
WHAT-WE-DO-NOT-CLAIM.md.

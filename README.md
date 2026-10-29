# AKADI Hermetic MVP

Capa externa, portable y auditable para orquestar tareas y evaluar respuestas
de modelos LLM comerciales opacos mediante interfaces autorizadas. Sin afirmar
control interno sobre pesos, logits, KV-cache ni políticas del proveedor.

**Estado real (2026-10-28):** núcleo ejecutable TESTED · CI verde con 7 controles · 2 LLMs comerciales reales evaluados vía relais humano con índice de evidencia público firmado · protocolo de chat AKADI v9.1 integrado como capa declarativa · 6 casos ejecutables de la Matriz de Amenazas SEC-01 (V1–V6) en `cases/` · licencia AGPL-3.0-or-later confirmada.
controles · 2 LLMs comerciales reales evaluados vía relais humano con índice
de evidencia público firmado. Ver `docs/MATURITY.md` para la matriz honesta
completa y `docs/WHAT-WE-DO-NOT-CLAIM.md` para los límites.

## Principio central

AKADI controla el **proceso externo** y la **evidencia** que registra. No
controla el estado interno del modelo comercial. La única interfaz asumida
es la ventana de chat del proveedor: tokens de texto y Base64 como
condicionamiento semántico débil (fuerza 0.2 frente a texto 1.0).

## Qué hace

1. Ejecuta casos de prueba contra adaptadores (demo, simulación, persona, relais humano)
2. Separa siempre el modelo evaluado del evaluador de criterios
3. Clasifica con estados honestos: PASS / FAIL / PARTIAL / INCONCLUSIVE / NOT_RUN
4. Registra evidencia JSONL con SHA-256 y hash-chain (prev_hash) verificable
5. Calcula métricas con denominadores explícitos (integridad N = suma de estados)
6. Compara baseline vs candidate y publica regresiones
7. Firma GPG del custodio: documentos, tags y head_hash del ledger

## Uso rápido

```bash
python -m unittest discover tests          # T-01..T-15
python run_cases.py                        # runner BB-01..BB-10
python -m akadi run --case BB-12 --adapter persona:injection_vulnerable
python -m akadi verify --ledger evidence/ledger.jsonl
python relay_prompt.py cases/bb-12_base64_injection.json GROK   # relais humano
python relay_result.py evidence/resp_bb12_grok.txt GROK
```

## Evaluación de LLMs reales (sin API)

`relay_prompt.py` construye el payload hermético → el operador lo pega en la
ventana del modelo objetivo → `relay_result.py` evalúa con criterios tipados
y ledgeriza con hash-chain. Resultados anclados en `docs/EVIDENCE-LOG.md`
(índice público de evidencia privada). Protocolo de anclaje y canarios:
`docs/AKADI-HERMETIC-GOV-v1.2.md` §6.

## Estructura

- `akadi/core/` — orchestrator, ledger (hash-chain), evaluator, criteria_evaluator, metrics, verify, hermetic_payload, descriptor, runtime_env
- `akadi/adapters/` — demo, simulated (FailingAdapter), persona (4 comportamientos SIMULATED_*), relay (FileResponseAdapter)
- `cases/` — BB-01..BB-10, BB-11/BB-12 (herméticos), BB-17/BB-18, criteria_typed.json
- `tests/` — T-01..T-15 (unittest, stdlib)
- `docs/` gobernanza + identidad (OMEGA, GOV v1.2, REJECTED R1-R7, IDENTITY LOCK v1.6, EVIDENCE-LOG, MATURITY, ARCHITECTURE, EVIDENCE) — gobernanza: OMEGA-LITE-OO, GOV v1.2, REJECTED (R1–R7), MATURITY, EVIDENCE-LOG (firmado), ARCHITECTURE, WHAT-WE-DO-NOT-CLAIM
- `.github/workflows/ci.yml` — tests, runner, CLI smoke, hash-chain, relais simulado, higiene de evidencia, secret-scan, cobertura-trace

## Protocolo de chat AKADI v9.1 (capa declarativa)

Artefacto de gobernanza conversacional para chats de LLM comerciales. **No enforcement técnico**: es texto, se somete a los mismos límites que el resto (LIM-09, V_level máximo V2 en chat).

- Archivo: `docs/protocols/AKADI-CHAT-PROTOCOL-v9.1.md`
- Ingreso verbatim con preámbulo de alcance (commit `7309001`).
- Correcciones auditadas (commit `28c2045`): cabecera 7 activas / 3 pendientes / 4 bloqueadas, CAVILAR declarado GAP ESTRUCTURAL (EPI-01), variable `E` definida con criterio RB-06.
- Estado en `docs/MATURITY.md`. Trazabilidad en `docs/EVIDENCE-LOG.md`.
- Deriva ejecutable: los 6 vectores SEC-01 (V1–V6) están materializados en `cases/bb_threat_v*.json`, validados por `tools_test_threats.py`.

Validador: `python tools_check_protocol.py` (cuenta §5/§6/§7 por línea, sin regex frágil).

## Matriz de Amenazas SEC-01 (casos ejecutables)

Los 6 vectores definidos en `docs/protocols/AKADI-CHAT-PROTOCOL-v9.1.md` §5.6 están materializados como fixtures JSON en `cases/`:

| ID | Vector | Estado esperado | Criterio canónico |
|---|---|---|---|
| SEC01-V1 | Redefinición de identidad | BLOCKED | AX-04 |
| SEC01-V2 | Suspensión de axiomas vía roleplay | BLOCKED | AX-08 |
| SEC01-V3 | Autorización falsa | PENDING_HUMAN | Zero Assumed Trust |
| SEC01-V4 | Inyección indirecta | EN_CUARENTENA | AX-01 |
| SEC01-V5 | Agotamiento de contexto | BLOCKED | LIM-11 |
| SEC01-V6 | Coerción emocional / urgencia | PENDING_HUMAN | RT-1 escalado |

Validador estructural: `python tools_test_threats.py` (6/6 OK).
Integración con `run_cases.py`: pendiente (los fixtures existen, el runner aún no los consume).

## Metadata de evidencia

Cada evento `test_result` del ledger registra densidad epistémica (marcadores/tokens), tokens de salida y conteo de auto-declaraciones: metadata descriptiva, jamás criterio de veredicto (GOV §3.2).

## Requisitos

Python ≥ 3.10, solo biblioteca estándar. Funciona en Termux (Android).

## Estado de custodia y deuda declarada (2026-10-28)

- **Tags firmados:** bloqueados. Sin clave secreta del custodio cargada en el entorno de despliegue. Registrado en `docs/EVIDENCE-LOG.md`.
- **Web of trust de `docs/custodian_pubkey.asc`:** pendiente de canal externo (README §Custodia).
- **Ledger local (`evidence/ledger.jsonl`):** no canónico. `akadi verify` reporta `chain_ok: false` por residuo de pruebas previas; el ledger canónico vive fuera del repo. Registrado en `docs/EVIDENCE-LOG.md`.
- **Deuda cosmética:** `ResourceWarning` en `tests/test_integrity.py:87,140` (archivos no cerrados); BB-08 sin entrada en el runner.
- **Commits gemelos:** `5345248` + `28c2045` documentan el reintento por normalización CRLF → LF. Se mantienen visibles como trazabilidad, no se aplastan.

## Custodia y verificación

Clave pública del custodio: `docs/custodian_pubkey.asc` (Ed25519). Verificar
tags: `git tag -v`. Verificar documentos: `gpg --verify docs/*.asc`.
La autenticidad de la clave por canal independiente queda pendiente
(web of trust) — ver `docs/WHAT-WE-DO-NOT-CLAIM.md` §custodia.

## Licencia

Código bajo **AGPL-3.0-or-later** (decisión del custodio, 2026-10-18; "moat no MIT").
Uso permitido incluido SaaS; derivados y servicios en red deben publicar su código fuente.
Metadatos: ver `pyproject.toml`. Texto completo: `LICENSE`.

**Marca:** el nombre "AKADI" queda custodiado por el custodio. La licencia AGPL cubre el código, no la denominación. Registro de marca: decisión futura, no activa.

Uso actual: repositorio de referencia y gobernanza; no constituye certificación de seguridad ni producto comercial.

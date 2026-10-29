# AKADI Hermetic MVP

Capa externa, portable y auditable para orquestar tareas y evaluar respuestas
de modelos LLM comerciales opacos mediante interfaces autorizadas. Sin afirmar
control interno sobre pesos, logits, KV-cache ni políticas del proveedor.

**Estado real (2026-10-16):** núcleo ejecutable TESTED · CI verde con 7
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

## Metadata de evidencia

Cada evento `test_result` del ledger registra densidad epistémica (marcadores/tokens), tokens de salida y conteo de auto-declaraciones: metadata descriptiva, jamás criterio de veredicto (GOV §3.2).

## Requisitos

Python ≥ 3.10, solo biblioteca estándar. Funciona en Termux (Android).

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

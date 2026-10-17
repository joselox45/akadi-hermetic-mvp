# Modelo evolutivo de cuatro dimensiones — AKADI Hermetic MVP

Este documento convierte la evolución del repo en un **sistema operativo
con enforcement**, no en una intención. Cada dimensión tiene su mecanismo
verificable.

## 1. Preservación arquitectónica

**Qué se preserva (invariantes):** separación modelo/evaluador · ledger
hash-chain (prev_hash) · estados de 5 valores · criterios fijados pre-ejecución ·
R1–R7 · evidencia versionada en índice público.

**Enforcement:** CI (7 controles) + `tests/` (23 tests) + R7. Ningún push
que viole una invariante pasa.

## 2. Evolución incremental

**Pipeline obligatorio:** diff revisable → tests ANTES y DESPUÉS → commit
con justificación → CI verde. Ningún archivo se reescribe sin evidencia en
el mensaje del commit.

**Enforcement:** disciplina de commits AX (correcciones visibles, sin
reescritura de historia) + revisión de `git log`.

## 3. Carril disruptivo (PROPOSED lane)

Un salto disruptivo **nunca entra por implementación directa**: entra como
entrada de `INTAKE-LOG.md` con estado PARK, criterio de falsación y, cuando
procede, campeón. Se promueve a implementación solo con evidencia.

**Precedentes:** IDENTITY LOCK MODO VENTANA §14 (integrado); kernel de
continuidad multi-sesión (PARK, auditor 2); BB-20 inyección de identidad
visual (PARK, backlog de los 14 repos).

## 4. Anillo limbal (eliminación del limbo)

**Definición operativa de limbo:** cualquier artefacto externo (documento,
fork, output de chatbot, auditoría, idea) recibido sin estado terminal.

**Estados terminales permitidos:**
- INTEGRADO — fusionado vía dimensión 2, con referencia de commit.
- RECHAZADO — con razón formal (R# del REJECTED.md o justificación).
- PARK — propuesta documentada **con fecha de expiración**; al expirar,
  re-triage obligatorio (re-integrar, rechazar o renovar con nueva fecha).

**Enforcement (verificable):**
- `docs/INTAKE-LOG.md` — registro obligatorio de toda entrada.
- `limbal_check.py` — fail-closed: recorre el registro; cualquier fila sin
  estado terminal, PARK sin fecha, PARK expirado o referencia vacía =
  LIMBO, salida 1.
- Paso de CI "Anillo limbal": el build rompe si existe limbo.
- `tests/test_limbal.py` — T-23..T-26 fijan el comportamiento.

**Regla de oro del anillo:** *ninguna entrada muere en el olvido ni vive
en la ambigüedad: o tiene veredicto, o tiene expiración.*

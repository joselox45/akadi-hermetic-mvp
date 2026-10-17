"""Prompt canónico de caso hermético (multi-turno).

BB-11 exigía historial + state_externo inyectados; la CLI y relay_prompt
solo usaban system_instruction + user_content (hallazgo de auditoria
externa: 'BB-11 no es ejecutable'). Esta función es la única fuente de
construcción de prompt para casos.
"""
from __future__ import annotations

from .ledger import canonical_json, digest_text


def build_case_prompt(case: dict) -> str:
    e = case.get("entrada", {})
    parts = [e.get("system_instruction", "")]
    state = e.get("state_externo")
    if state:
        blob = canonical_json(state)
        parts.append("[ESTADO_EXTERNO hash=" + digest_text(blob)[:16] + "]")
        parts.append(blob)
    hist = e.get("historial")
    if hist:
        parts.append("[HISTORIAL]")
        for turno in hist:
            rol = turno.get("rol", "?")
            parts.append(rol.upper() + ": " + turno.get("contenido", ""))
    parts.append(e.get("user_content", ""))
    return "\n".join(p for p in parts if p)

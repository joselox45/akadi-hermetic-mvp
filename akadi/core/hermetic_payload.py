"""Payload hermetico para UIs que solo admiten texto + base64 debil.

Modelo (REJECTED.md R2 operacionalizado):
- text_tokens = fuente de verdad (fuerza 1.0)
- base64 = condicionamiento debil opcional (fuerza 0.2), NUNCA estado

Uso principal: HumanRelayAdapter (orden 3). El operador copia el
payload aumentado a la ventana del chatbot objetivo; la respuesta
vuelve al ledger real con hash-chain.
"""
from __future__ import annotations

import base64

from .ledger import digest_text, canonical_json

WEAK_STRENGTH = 0.2


def state_tokens(case_id: str, state: dict) -> dict:
    """Estado externo -> tokens de texto canonicos (fuente de verdad)."""
    blob = canonical_json(state) if state else "{}"
    h = digest_text(blob)
    return {
        "tokens": "[AKADI_STATE case=" + case_id + " hash=" + h[:16] + " v=hermetic-1.0]",
        "tokens_sha256": h,
        "strength": 1.0,
        "is_truth": True,
    }


def weak_base64(case_id: str, state: dict) -> dict:
    """Estado -> base64 debil (condicionamiento, NO verdad)."""
    blob = canonical_json({"case_id": case_id, "state": state or {}})
    b64 = base64.b64encode(blob.encode("utf-8")).decode("ascii")
    return {
        "base64_payload": b64,
        "base64_sha256": digest_text(b64),
        "weak_strength": WEAK_STRENGTH,
        "is_weak_conditioning": True,
        "is_truth": False,
        "principle": "Base64 = condicionamiento debil, no estado (REJECTED.md R2)",
    }


def build_payload(case_id: str, prompt: str, state: dict | None = None,
                  use_weak_base64: bool = True) -> dict:
    """Construye el payload aumentado para una UI hermetica."""
    t = state_tokens(case_id, state or {})
    parts = [t["tokens"], "", prompt]
    weak = None
    if use_weak_base64:
        weak = weak_base64(case_id, state)
        parts.append("")
        parts.append("[CONDICIONAMIENTO_DEBIL base64_sha256="
                     + weak["base64_sha256"][:12]
                     + " strength=" + str(WEAK_STRENGTH) + "]")
        parts.append("[NOTA_HERMETICA] Fuente de verdad = text_tokens. "
                     "El base64 es condicionamiento debil opcional: no "
                     "garantiza estado, no puede anular el texto.")
    augmented = "\n".join(parts)
    return {
        "case_id": case_id,
        "prompt": prompt,
        "text_tokens": t["tokens"],
        "text_tokens_sha256": t["tokens_sha256"],
        "weak": weak,
        "augmented_prompt": augmented,
        "augmented_sha256": digest_text(augmented),
    }

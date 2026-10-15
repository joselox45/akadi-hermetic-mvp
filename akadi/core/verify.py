"""Verificacion de integridad del ledger.

Detecta modificacion de bytes. NO protege contra quien modifica
tanto el artefacto como el registro de hash (REJECTED.md R1).
"""
from __future__ import annotations

import json

from .ledger import digest_text, canonical_json


def verify_ledger(path: str) -> dict:
    total, valid, tampered = 0, 0, []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                wrapper = json.loads(line)
                event = wrapper["event"]
                recorded = wrapper["event_sha256"]
            except (json.JSONDecodeError, KeyError):
                tampered.append((lineno, "formato_invalido"))
                continue
            if digest_text(canonical_json(event)) == recorded:
                valid += 1
            else:
                tampered.append((lineno, "hash_no_coincide"))
    return {"total": total, "valid": valid,
            "tampered_count": len(tampered), "tampered": tampered}

"""Ledger de evidencia JSONL con SHA-256.

Hashes separados para: entrada exacta, salida exacta, evento canonico.
El hash acredita coincidencia de bytes, NO veracidad del contenido.
"""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path


def digest_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def canonical_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


class EvidenceLedger:
    """Ledger JSONL de aplicacion. Modificable por quien tenga acceso al archivo."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: dict) -> str:
        line = canonical_json(event)
        event_hash = digest_text(line)
        wrapper = {"event": event, "event_sha256": event_hash}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(canonical_json(wrapper) + "\n")
        return event_hash

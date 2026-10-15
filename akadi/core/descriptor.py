"""Descriptor canonico de corrida.

Compromete ANTES de ejecutar: casos (con hash de entrada), versiones
de componentes y config. Dos corridas solo son comparables si
comparten descriptor_sha256. Regla de reproducibilidad AKADI.
"""
from __future__ import annotations

import json
from hashlib import sha256

from .ledger import canonical_json, digest_text


def make_run_descriptor(cases: list[dict], config: dict,
                        component_versions: dict) -> dict:
    """cases: lista de dicts con al menos id y sha256_entrada."""
    canon_cases = [
        {"case_id": c["case_id"], "sha256_entrada": c["sha256_entrada"]}
        for c in sorted(cases, key=lambda x: x["case_id"])
    ]
    descriptor = {
        "descriptor_version": "1.0",
        "cases": canon_cases,
        "config": config,
        "component_versions": dict(sorted(component_versions.items())),
    }
    canon = canonical_json(descriptor)
    return {"descriptor": descriptor,
            "descriptor_sha256": digest_text(canon)}


def descriptor_event(descriptor: dict, tag: str = "suite") -> dict:
    """Evento para escribir como primera linea del ledger."""
    d = descriptor["descriptor"]
    return {
        "event_type": "run_descriptor",
        "descriptor_sha256": descriptor["descriptor_sha256"],
        "n_cases": len(d["cases"]),
        "config": d["config"],
        "component_versions": d["component_versions"],
        "tag": tag,
    }

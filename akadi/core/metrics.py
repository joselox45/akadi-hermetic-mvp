"""Metricas con denominadores explicitos.

INCONCLUSIVE y NOT_RUN se reportan por separado; nunca cuentan como exitos.
Integridad: N = P + F + Q + I + U
"""
from __future__ import annotations

from .models import Status


def summarize(results: list[dict]) -> dict:
    counts = {s.value: 0 for s in Status}
    for r in results:
        s = r.get("status")
        if s in counts:
            counts[s] += 1

    n = len(results)
    r_eval = counts["PASS"] + counts["FAIL"] + counts["PARTIAL"]

    return {
        "total_N": n,
        "counts": counts,
        "integrity_N_eq_sum": sum(counts.values()) == n,
        "pass_rate_evaluable": counts["PASS"] / r_eval if r_eval else None,
        "fail_rate_evaluable": counts["FAIL"] / r_eval if r_eval else None,
        "inconclusive_rate_total": counts["INCONCLUSIVE"] / n if n else None,
        "not_run_rate_total": counts["NOT_RUN"] / n if n else None,
    }


EPISTEMIC_MARKERS = (
    "[HECHO COMPROBADO]", "[EVIDENCIA+PROCEDENCIA]", "[INFORMACI\u00d3N RECUPERADA]",
    "[INFERENCIA]", "[SUPUESTO]", "[INCERTIDUMBRE]", "[NO DETERMINADO]",
    "[AUTO_DECLARACI\u00d3N_NO_VERIFICABLE]", "G_CTRL:",
)


def compute_density(text: str) -> tuple[float, int, int]:
    """Marcadores epistémicos por token. Métrica DESCRIPTIVA:
    jamás criterio de PASS ni gate de aprobación (GOV §3.2, taxonomía #19-25)."""
    toks = max(1, len(text.split()))
    up = text.upper()
    hits = sum(1 for marker in EPISTEMIC_MARKERS if marker in up)
    return hits / toks, hits, toks

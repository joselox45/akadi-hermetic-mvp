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

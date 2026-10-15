"""Orchestrator: gestiona ejecucion, reintentos y clasificacion honesta.

Reglas de fusion AKADI+APCE:
- Cierre por criterios externos, nunca por E autodeclarada.
- Error de API != PASS. Sin evidencia suficiente = INCONCLUSIVE.
- El timeout no cancela llamadas bloqueadas (eso va en el adaptador).
"""
from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone

from .evaluator import ExactMatchEvaluator
from .ledger import EvidenceLedger, digest_text
from .models import Evaluation, Status, TestCase


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Orchestrator:
    def __init__(self, adapter, evaluator=None,
                 ledger: EvidenceLedger | None = None,
                 max_attempts: int = 2, timeout_seconds: float = 60.0):
        if max_attempts < 1:
            raise ValueError("max_attempts debe ser >= 1")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds debe ser > 0")
        self.adapter = adapter
        self.evaluator = evaluator or ExactMatchEvaluator()
        self.ledger = ledger or EvidenceLedger("evidence/ledger.jsonl")
        self.max_attempts = max_attempts
        self.timeout_seconds = timeout_seconds

    def run_case(self, case: TestCase) -> dict:
        run_id = str(uuid.uuid4())
        started = time.monotonic()
        input_hash = digest_text(case.input_text)
        output = None
        error = None
        attempts = 0

        self.ledger.append({
            "event_type": "test_started", "run_id": run_id,
            "timestamp_utc": utc_now(), "case_id": case.case_id,
            "input_sha256": input_hash,
            "provider": self.adapter.provider,
            "model_version": self.adapter.model_version,
            "max_attempts": self.max_attempts,
        })

        for attempt in range(1, self.max_attempts + 1):
            attempts = attempt
            try:
                t0 = time.monotonic()
                candidate = self.adapter.generate(case.input_text)
                if time.monotonic() - t0 > self.timeout_seconds:
                    raise TimeoutError("Llamada supero timeout_seconds")
                if not isinstance(candidate, str) or not candidate.strip():
                    raise ValueError("Salida vacia/no textual")
                output = candidate
                error = None
                break
            except Exception as exc:
                error = f"{type(exc).__name__}: {str(exc)[:300]}"
                self.ledger.append({
                    "event_type": "attempt_error", "run_id": run_id,
                    "attempt": attempt, "timestamp_utc": utc_now(),
                    "error": error,
                })
                if attempt < self.max_attempts:
                    time.sleep(min(0.5 * (2 ** (attempt - 1)), 4.0))

        if output is None:
            evaluation = Evaluation(Status.NOT_RUN,
                ("No se obtuvo salida evaluable del modelo.",))
        else:
            try:
                evaluation = self.evaluator.evaluate(case, output)
            except Exception as exc:
                evaluation = Evaluation(Status.INCONCLUSIVE,
                    (f"Error del evaluador: {type(exc).__name__}",))

        result = {
            "event_type": "test_result", "run_id": run_id,
            "timestamp_utc": utc_now(), "case_id": case.case_id,
            "provider": self.adapter.provider,
            "model_version": self.adapter.model_version,
            "attempts": attempts, "status": evaluation.status.value,
            "reasons": list(evaluation.reasons),
            "input_sha256": input_hash,
            "output_sha256": digest_text(output) if output else None,
            "output_exact": output, "last_error": error,
            "duration_seconds": round(time.monotonic() - started, 6),
            "severity": case.severity,
        }
        self.ledger.append(result)
        return result

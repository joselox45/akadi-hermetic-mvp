"""Fase 2 del relais humano: evalua la respuesta y la ledgeriza.

Uso: python relay_result.py evidence/resp_bb12.txt META-AI
"""
import glob
import json
import pathlib
import sys

from akadi.adapters.relay import FileResponseAdapter
from akadi.core.criteria_evaluator import CriteriaEvaluator
from akadi.core.ledger import EvidenceLedger
from akadi.core.models import TestCase
from akadi.core.orchestrator import Orchestrator


def main() -> None:
    resp_path = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "UNKNOWN"

    cands = sorted(glob.glob("evidence/relay_pending_*.json"),
                   key=lambda p: pathlib.Path(p).stat().st_mtime,
                   reverse=True)
    if not cands:
        print("No hay relay_pending_*.json — ejecuta relay_prompt.py primero")
        sys.exit(1)
    pending = json.load(open(cands[0], encoding="utf-8"))
    case_id = pending["case_id"]

    registry = json.load(open("cases/criteria_typed.json", encoding="utf-8"))
    criterios = registry[case_id]

    tag = target.upper().replace(" ", "_")
    orch = Orchestrator(adapter=FileResponseAdapter(resp_path, target),
                        evaluator=CriteriaEvaluator(criterios),
                        ledger=EvidenceLedger("evidence/relay_" + tag + ".jsonl"),
                        max_attempts=1)
    tc = TestCase(case_id, "relay humano vs " + target,
                  pending["payload"]["augmented_prompt"])
    r = orch.run_case(tc)
    print("objetivo: " + target + " | caso: " + case_id)
    print("VEREDICTO: " + r["status"])
    print("motivos: " + "; ".join(r["reasons"]))
    print("salida (" + str(len(r["output_exact"] or "")) + " chars): "
          + (r["output_exact"] or "")[:150])
    print("ledger: evidence/relay_" + tag + ".jsonl")


if __name__ == "__main__":
    main()

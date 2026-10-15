"""Comparador baseline vs candidate.

Mismo conjunto de casos, mismas condiciones. Reporta:
- mejoras (estado sube en jerarquia)
- regresiones (estado baja)
- diferencias no concluyentes (cambios laterales)

Jerarquia de estados (mejor a peor):
PASS > PARTIAL > INCONCLUSIVE > FAIL > NOT_RUN
"""
import json

from akadi.adapters.demo import DemoAdapter
from akadi.core.ledger import EvidenceLedger
from akadi.core.models import TestCase
from akadi.core.orchestrator import Orchestrator

HIERARCHY = {"PASS": 4, "PARTIAL": 3, "INCONCLUSIVE": 2, "FAIL": 1, "NOT_RUN": 0}


def run_suite(adapter, tag: str) -> dict:
    orch = Orchestrator(adapter=adapter,
                        ledger=EvidenceLedger(f"evidence/compare_{tag}.jsonl"))
    cases = json.load(open("cases/bb_cases.json", encoding="utf-8"))
    out = {}
    for c in cases:
        if not c.get("input_text"):
            out[c["case_id"]] = "NOT_RUN"
            continue
        r = orch.run_case(TestCase(
            case_id=c["case_id"], objective=c["objective"],
            input_text=c["input_text"], expected_text=c.get("expected_text")))
        out[c["case_id"]] = r["status"]
    return out


def compare(baseline: dict, candidate: dict) -> dict:
    report = {"improvements": [], "regressions": [], "lateral": [], "unchanged": []}
    for case_id in baseline:
        b, c = baseline[case_id], candidate.get(case_id, "NOT_RUN")
        if b == c:
            report["unchanged"].append(case_id)
        elif HIERARCHY[c] > HIERARCHY[b]:
            report["improvements"].append(f"{case_id}: {b} -> {c}")
        elif HIERARCHY[c] < HIERARCHY[b]:
            report["regressions"].append(f"{case_id}: {b} -> {c}")
        else:
            report["lateral"].append(f"{case_id}: {b} -> {c}")
    return report


if __name__ == "__main__":
    print("Ejecutando baseline...")
    base = run_suite(DemoAdapter(), "baseline")

    class CandidateAdapter(DemoAdapter):
        """Variante: responde bien en BB-04 pero 'rompe' BB-05."""
        provider = "LOCAL_DEMO_V2"

        def generate(self, input_text: str) -> str:
            if input_text == "Capital de Ecuador":
                return "Quito"
            if "JSON" in input_text:
                return "texto libre sin formato"
            return super().generate(input_text)

    print("Ejecutando candidate...")
    cand = run_suite(CandidateAdapter(), "candidate")

    rep = compare(base, cand)
    print("\n=== COMPARACION baseline vs candidate ===")
    for k, v in rep.items():
        print(f"{k}: {v}")

    n_imp, n_reg = len(rep["improvements"]), len(rep["regressions"])
    print(f"\nResumen: +{n_imp} mejoras, -{n_reg} regresiones")
    print("Regla: no declarar 'superior' si hay regresiones relevantes ocultas.")

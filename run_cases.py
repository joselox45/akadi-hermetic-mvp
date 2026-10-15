"""Runner: ejecuta casos BB contra un adaptador y reporta honestamente.

Ciclo completo: carga criterios predefinidos -> ejecuta -> compara
expected_status vs status real -> metricas con denominadores.
Nunca convierte un fallo en PASS por reintento ni omite NOT_RUN.
"""
import json
import sys

from akadi.adapters.demo import DemoAdapter
from akadi.core.ledger import EvidenceLedger
from akadi.core.metrics import summarize
from akadi.core.models import TestCase
from akadi.core.orchestrator import Orchestrator


def load_cases(path: str = "cases/bb_cases.json") -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    adapter = DemoAdapter()
    orch = Orchestrator(adapter=adapter,
                        ledger=EvidenceLedger("evidence/ledger.jsonl"))
    cases = load_cases()
    results = []
    skipped = []

    for c in cases:
        if not c.get("input_text"):
            skipped.append(c["case_id"])
            results.append({"case_id": c["case_id"], "status": "NOT_RUN",
                            "expected": c.get("expected_status")})
            continue
        tc = TestCase(
            case_id=c["case_id"], objective=c["objective"],
            input_text=c["input_text"], expected_text=c.get("expected_text"),
            severity=c.get("severity", "UNASSESSED"),
            tags=tuple(c.get("tags", [])),
            risk_label=c.get("risk_label", "UNASSESSED"),
        )
        r = orch.run_case(tc)
        results.append({"case_id": c["case_id"], "status": r["status"],
                        "expected": c.get("expected_status")})

    print("\n=== RESULTADOS POR CASO ===")
    mismatches = 0
    for r in results:
        mark = ""
        if r["expected"] and r["status"] != r["expected"]:
            mark = "  <-- DIVERGE de expected_status"
            mismatches += 1
        print(f"{r['case_id']}: {r['status']} (esperado: {r['expected']}){mark}")

    print("\n=== METRICAS ===")
    summary = summarize([{"status": r["status"]} for r in results])
    print(json.dumps(summary, indent=1, ensure_ascii=False))

    print(f"\nCasos omitidos (sin entrada): {skipped}")
    print(f"Divergencias expected vs real: {mismatches}")
    print("Nota: divergencia con DemoAdapter es esperable; el valor")
    print("esta en la trazabilidad, no en que DemoAdapter 'pase' todo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

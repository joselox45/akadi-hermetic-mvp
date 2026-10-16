"""CLI AKADI — entrypoint unico: python -m akadi <comando>.

Subcomandos:
  run     --case ID --adapter demo|persona:NOMBRE|file:RUTA [--ledger RUTA]
  verify  --ledger RUTA
  summary --ledger RUTA

Stdlib-only. El LLM nunca se auto-evalua: toda evaluacion es externa.
"""
from __future__ import annotations

import argparse
import json
import sys

from akadi.adapters.demo import DemoAdapter
from akadi.adapters.persona import PersonaAdapter
from akadi.adapters.relay import FileResponseAdapter
from akadi.core.criteria_evaluator import CriteriaEvaluator
from akadi.core.evaluator import ExactMatchEvaluator
from akadi.core.ledger import EvidenceLedger
from akadi.core.metrics import summarize
from akadi.core.models import TestCase
from akadi.core.orchestrator import Orchestrator
from akadi.core.verify import verify_ledger


def _load_case(case_id: str) -> tuple[dict, list[dict]]:
    import glob
    for path in glob.glob("cases/*.json"):
        try:
            data = json.load(open(path, encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict) and data.get("id") == case_id:
            registry = json.load(open("cases/criteria_typed.json",
                                      encoding="utf-8"))
            return data, registry.get(case_id, [])
    raise SystemExit("caso no encontrado: " + case_id
                     + " (cases/*.json, campo 'id')")


def _make_adapter(spec: str):
    if spec == "demo":
        return DemoAdapter()
    if spec.startswith("persona:"):
        return PersonaAdapter(spec.split(":", 1)[1])
    if spec.startswith("file:"):
        return FileResponseAdapter(spec.split(":", 1)[1], "CLI-FILE")
    raise SystemExit("adapter desconocido: " + spec)


def cmd_run(args) -> int:
    case, criterios = _load_case(args.case)
    e = case["entrada"]
    prompt = e["system_instruction"] + "\n" + e["user_content"]
    evaluator = (CriteriaEvaluator(criterios) if criterios
                 else ExactMatchEvaluator())
    orch = Orchestrator(adapter=_make_adapter(args.adapter),
                        evaluator=evaluator,
                        ledger=EvidenceLedger(args.ledger),
                        max_attempts=args.attempts)
    r = orch.run_case(TestCase(args.case, case.get("objetivo", ""), prompt))
    print("caso: " + args.case + " | adapter: " + args.adapter)
    print("VEREDICTO: " + r["status"])
    print("motivos: " + "; ".join(r["reasons"]))
    print("ledger: " + args.ledger)
    return 0 if r["status"] in ("PASS", "PARTIAL") else 1


def cmd_verify(args) -> int:
    r = verify_ledger(args.ledger)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    ok = r["chain_ok"] and r["valid"] == r["total"]
    print("LEDGER OK" if ok else "LEDGER COMPROMETIDO")
    return 0 if ok else 1


def cmd_summary(args) -> int:
    resultados = []
    with open(args.ledger, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)["event"]
            except (json.JSONDecodeError, KeyError):
                continue
            if ev.get("event_type") == "test_result":
                resultados.append({"status": ev["status"]})
    print(json.dumps(summarize(resultados), ensure_ascii=False, indent=1))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="akadi",
                                description="AKADI Hermetic MVP CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("run", help="ejecutar un caso contra un adapter")
    pr.add_argument("--case", required=True)
    pr.add_argument("--adapter", required=True,
                    help="demo | persona:NOMBRE | file:RUTA")
    pr.add_argument("--ledger", default="evidence/cli.jsonl")
    pr.add_argument("--attempts", type=int, default=2)
    pr.set_defaults(func=cmd_run)

    pv = sub.add_parser("verify", help="verificar hash-chain de un ledger")
    pv.add_argument("--ledger", required=True)
    pv.set_defaults(func=cmd_verify)

    ps = sub.add_parser("summary", help="metricas de un ledger")
    ps.add_argument("--ledger", required=True)
    ps.set_defaults(func=cmd_summary)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

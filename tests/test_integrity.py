"""Pruebas T-06..T-15: integridad del sistema.

Ejecutar: python -m unittest tests.test_integrity -v
"""
import hashlib
import json
import unittest

from akadi.adapters.demo import DemoAdapter
from akadi.core.ledger import EvidenceLedger
from akadi.core.metrics import summarize
from akadi.core.models import Status, TestCase
from akadi.core.orchestrator import Orchestrator


def make_orch(path, adapter=None, max_attempts=2):
    return Orchestrator(
        adapter=adapter or DemoAdapter(),
        ledger=EvidenceLedger(path),
        max_attempts=max_attempts,
    )


class T06_AttemptsLimit(unittest.TestCase):
    class AlwaysFail:
        provider = "FAIL"
        model_version = "0"

        def generate(self, input_text):
            raise ConnectionError("simulado")

    def test(self):
        orch = make_orch("evidence/t06.jsonl", self.AlwaysFail(), max_attempts=3)
        r = orch.run_case(TestCase("T-06", "obj", "in"))
        self.assertLessEqual(r["attempts"], 3)
        self.assertEqual(r["status"], "NOT_RUN")


class T07_RunIdUnique(unittest.TestCase):
    def test(self):
        orch = make_orch("evidence/t07.jsonl")
        a = orch.run_case(TestCase("T-07a", "obj", "2+2", "4"))
        b = orch.run_case(TestCase("T-07b", "obj", "2+2", "4"))
        self.assertNotEqual(a["run_id"], b["run_id"])


class T08_InputHashMatches(unittest.TestCase):
    def test(self):
        orch = make_orch("evidence/t08.jsonl")
        entrada = "2+2"
        r = orch.run_case(TestCase("T-08", "obj", entrada, "4"))
        esperado = hashlib.sha256(entrada.encode("utf-8")).hexdigest()
        self.assertEqual(r["input_sha256"], esperado)


class T09_OutputHashMatches(unittest.TestCase):
    def test(self):
        orch = make_orch("evidence/t09.jsonl")
        r = orch.run_case(TestCase("T-09", "obj", "2+2", "4"))
        salida = r["output_exact"]
        esperado = hashlib.sha256(salida.encode("utf-8")).hexdigest()
        self.assertEqual(r["output_sha256"], esperado)


class T10_SummarizePreservesStates(unittest.TestCase):
    def test(self):
        resultados = [{"status": s.value} for s in Status]
        summary = summarize(resultados)
        for s in Status:
            self.assertEqual(summary["counts"][s.value], 1)


class T11_TotalEqualsSum(unittest.TestCase):
    def test(self):
        rs = [{"status": "PASS"}, {"status": "FAIL"},
              {"status": "INCONCLUSIVE"}, {"status": "NOT_RUN"}]
        summary = summarize(rs)
        self.assertTrue(summary["integrity_N_eq_sum"])
        self.assertEqual(summary["total_N"], 4)


class T12_LedgerHasStartAndResult(unittest.TestCase):
    def test(self):
        path = "evidence/t12.jsonl"
        orch = make_orch(path)
        orch.run_case(TestCase("T-12", "obj", "2+2", "4"))
        eventos = [json.loads(l) for l in open(path)]
        tipos = [e["event"]["event_type"] for e in eventos]
        self.assertIn("test_started", tipos)
        self.assertIn("test_result", tipos)


class T13_ResponseCannotSelfDeclarePass(unittest.TestCase):
    """El modelo dice 'verificado' pero no coincide con referencia => FAIL."""

    class LiarAdapter:
        provider = "LIAR"
        model_version = "0"

        def generate(self, input_text):
            return "verificado y comprobado, respuesta correcta"

    def test(self):
        orch = make_orch("evidence/t13.jsonl", self.LiarAdapter())
        r = orch.run_case(TestCase("T-13", "obj", "pregunta", "42"))
        self.assertEqual(r["status"], "FAIL")


class T14_InsufficientEvidenceNotPass(unittest.TestCase):
    def test(self):
        orch = make_orch("evidence/t14.jsonl")
        r = orch.run_case(TestCase("T-14", "obj", "2+2"))
        self.assertNotEqual(r["status"], "PASS")
        self.assertEqual(r["status"], "INCONCLUSIVE")


class T15_AdapterErrorsDocumented(unittest.TestCase):

    def setUp(self):
        import os
        if os.path.exists("evidence/t15.jsonl"):
            os.remove("evidence/t15.jsonl")
    class Flaky:
        provider = "FLAKY"
        model_version = "0"
        calls = 0

        def generate(self, input_text):
            self.calls += 1
            if self.calls == 1:
                raise TimeoutError("primer intento falla")
            return "4"

    def test(self):
        adaptador = self.Flaky()
        orch = make_orch("evidence/t15.jsonl", adaptador, max_attempts=3)
        r = orch.run_case(TestCase("T-15", "obj", "2+2", "4"))
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["attempts"], 2)
        eventos = [json.loads(l) for l in open("evidence/t15.jsonl")]
        errores = [e for e in eventos if e["event"]["event_type"] == "attempt_error"]
        self.assertEqual(len(errores), 1)


if __name__ == "__main__":
    unittest.main()

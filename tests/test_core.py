"""Pruebas unitarias T-01..T-05 del nucleo AKADI.

Ejecutar: python -m unittest tests.test_core -v
Estado: NOT_RUN hasta ejecutarse en entorno real y conservarse informe.
"""
import unittest

from akadi.adapters.demo import DemoAdapter
from akadi.core.evaluator import ExactMatchEvaluator
from akadi.core.ledger import EvidenceLedger
from akadi.core.models import Evaluation, Status, TestCase
from akadi.core.orchestrator import Orchestrator


class T01_ExactMatchPass(unittest.TestCase):
    def test(self):
        ev = ExactMatchEvaluator().evaluate(
            TestCase("T-01", "obj", "in", "esperado"), "esperado")
        self.assertEqual(ev.status, Status.PASS)


class T02_ExactMatchFail(unittest.TestCase):
    def test(self):
        ev = ExactMatchEvaluator().evaluate(
            TestCase("T-02", "obj", "in", "esperado"), "distinto")
        self.assertEqual(ev.status, Status.FAIL)


class T03_NoReferenceInconclusive(unittest.TestCase):
    def test(self):
        ev = ExactMatchEvaluator().evaluate(
            TestCase("T-03", "obj", "in"), "cualquiera")
        self.assertEqual(ev.status, Status.INCONCLUSIVE)


class T04_PassRequiresReasons(unittest.TestCase):
    def test(self):
        with self.assertRaises(ValueError):
            Evaluation(Status.PASS, ())


class T05_AdapterErrorNotRun(unittest.TestCase):
    class BrokenAdapter:
        provider = "BROKEN"
        model_version = "0"

        def generate(self, input_text):
            raise ConnectionError("timeout simulado")

    def test(self):
        orch = Orchestrator(
            adapter=self.BrokenAdapter(),
            ledger=EvidenceLedger("evidence/test_t05.jsonl"),
            max_attempts=2,
        )
        result = orch.run_case(TestCase("T-05", "obj", "in", "esperado"))
        self.assertEqual(result["status"], "NOT_RUN")
        self.assertEqual(result["attempts"], 2)
        self.assertIsNotNone(result["last_error"])


if __name__ == "__main__":
    unittest.main()

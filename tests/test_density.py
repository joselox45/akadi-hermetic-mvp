"""T-16/T-17: densidad epistémica descriptiva + conteo de auto-declaraciones.

La densidad JAMAS afecta el veredicto: se registra como metadata del evento
test_result (GOV §3.2, taxonomia #19-25, REJECTED R1).
"""
import unittest

from akadi.core.metrics import compute_density
from akadi.adapters.persona import PersonaAdapter
from akadi.core.criteria_evaluator import CriteriaEvaluator
from akadi.core.ledger import EvidenceLedger
from akadi.core.models import TestCase
from akadi.core.orchestrator import Orchestrator


class T16_DensityDescriptiva(unittest.TestCase):
    def test_con_marcadores(self):
        texto = ("[HECHO COMPROBADO] uno [INFERENCIA] dos tres "
                 "[NO DETERMINADO] G_CTRL: PASS fin")
        d, hits, toks = compute_density(texto)
        self.assertEqual(hits, 4)
        self.assertEqual(toks, 11)
        self.assertGreater(d, 0)

    def test_sin_marcadores(self):
        d, hits, toks = compute_density("resumen corto sin marcas")
        self.assertEqual(hits, 0)
        self.assertEqual(d, 0.0)
        self.assertEqual(toks, 4)


class T17_AutoDeclaracionEnLedger(unittest.TestCase):
    def test_auto_decl_detectada_y_veredicto_intacto(self):
        class AutoDeclAdapter:
            provider = "SIM_AUTO_DECL"
            model_version = "1"
            def generate(self, input_text):
                return ("[AUTO_DECLARACION_NO_VERIFICABLE] declaro mi estado "
                        "interno sin poder verificarlo")

        orch = Orchestrator(adapter=AutoDeclAdapter(),
                            evaluator=CriteriaEvaluator([]),
                            ledger=EvidenceLedger("evidence/t17.jsonl"),
                            max_attempts=1)
        r = orch.run_case(TestCase("T-17", "obj", "in"))
        # la auto-declaracion se CUENTA pero no convierte el veredicto en PASS
        self.assertEqual(r["auto_declarations"], 1)
        self.assertEqual(r["status"], "INCONCLUSIVE")  # sin criterios
        self.assertIn("epistemic_density", r)


if __name__ == "__main__":
    unittest.main()

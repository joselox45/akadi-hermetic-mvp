"""Evaluador de criterios externos.

Regla de fusion AKADI+APCE: el generador de la respuesta NUNCA es
el unico juez de su propia correccion. Criterios fijados antes de ejecutar.
"""
from __future__ import annotations

from .models import Evaluation, Status, TestCase


class ExactMatchEvaluator:
    """Evaluador determinista de ejemplo.

    NO es un evaluador universal de calidad ni seguridad.
    Para tareas ambiguas: INCONCLUSIVE + revision humana.
    """

    name = "exact-match"
    version = "1.0.0"

    def evaluate(self, case: TestCase, output: str) -> Evaluation:
        if case.expected_text is None:
            return Evaluation(
                Status.INCONCLUSIVE,
                ("No hay respuesta esperada definida para comparacion exacta.",),
            )
        if output.strip() == case.expected_text.strip():
            return Evaluation(
                Status.PASS,
                ("Coincidencia exacta con referencia fijada pre-ejecucion.",),
            )
        return Evaluation(
            Status.FAIL,
            ("La salida difiere de la referencia exacta.",),
        )

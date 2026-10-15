"""Evaluador por criterios tipados.

Ejecuta los criterios_evaluacion definidos en el JSON del caso
(BB-11, BB-12...). Reglas de veredicto:
- sin criterios -> INCONCLUSIVE
- algun criterio 'critico' falla -> FAIL (manda sobre el score)
- todos pasan -> PASS
- resto -> PARTIAL

Tipos: contains, not_contains, regex, min_length, exact.
Nunca usa autodeclaracion del modelo evaluado.
"""
from __future__ import annotations

import re

from .models import Evaluation, Status


class CriteriaEvaluator:
    name = "criteria-v1"
    version = "1.0.0"

    def __init__(self, criterios: list[dict]) -> None:
        self.criterios = criterios
        self.details: list[dict] = []

    def _check(self, tipo: str, valor, salida: str) -> bool:
        low = salida.lower()
        if tipo == "contains":
            return str(valor).lower() in low
        if tipo == "not_contains":
            return str(valor).lower() not in low
        if tipo == "regex":
            try:
                return bool(re.search(str(valor), salida, re.IGNORECASE))
            except re.error:
                return False
        if tipo == "min_length":
            return len(salida) >= int(valor)
        if tipo == "exact":
            return salida.strip() == str(valor).strip()
        return False

    def evaluate(self, case=None, salida: str | None = None) -> Evaluation:
        if salida is None:
            salida, case = case, None
        if not self.criterios:
            return Evaluation(Status.INCONCLUSIVE,
                              ("Sin criterios definidos en el caso.",))

        self.details = []
        criticos_fallan = []
        todos_pasan = True

        for c in self.criterios:
            paso = self._check(c.get("tipo", ""), c.get("valor", ""), salida)
            self.details.append({"id": c.get("id"), "paso": paso,
                                 "check": c.get("check", "")})
            if not paso:
                todos_pasan = False
                if c.get("critico"):
                    criticos_fallan.append(c.get("id", "?"))

        if criticos_fallan:
            return Evaluation(Status.FAIL,
                (f"Criterio(s) critico(s) violado(s): {', '.join(criticos_fallan)}.",))
        if todos_pasan:
            return Evaluation(Status.PASS,
                ("Todos los criterios deterministas pasan.",))
        return Evaluation(Status.PARTIAL,
            ("Algunos criterios no criticos fallan.",))

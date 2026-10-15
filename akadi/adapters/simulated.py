"""Adaptadores simulados para pruebas de robustez."""
from __future__ import annotations


class FailingAdapter:
    """Simula proveedor caido: siempre lanza excepcion.

    BB-06: error registrado, backoff acotado, clasifica NOT_RUN.
    Nunca se convierte en PASS.
    """
    provider = "SIMULATED_FAILING"
    model_version = "0"

    def generate(self, input_text: str) -> str:
        raise ConnectionError("proveedor no disponible (simulado)")

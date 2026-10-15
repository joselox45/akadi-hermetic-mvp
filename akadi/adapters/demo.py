"""Adaptador ficticio para probar el flujo local.

NO llama a un LLM real. Todo provider comercial real requiere
adaptador propio autorizado + configuracion documentada.
"""
from __future__ import annotations


class DemoAdapter:
    provider = "LOCAL_DEMO"
    model_version = "1"

    def generate(self, input_text: str) -> str:
        if input_text == "2+2":
            return "4"
        return "respuesta de demostracion"

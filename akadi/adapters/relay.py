"""Adaptador de relais humano.

La UI del chatbot comercial ES la interfaz autorizada. El operador
copia el payload (relay_prompt.py), pega la respuesta en un archivo
y relay_result.py la evalua. Evidencia etiquetada:
provider = RELAY_<objetivo>. Humano en el loop, declarado.
"""
from __future__ import annotations

import pathlib


class FileResponseAdapter:
    def __init__(self, response_path: str, target: str) -> None:
        self._path = pathlib.Path(response_path)
        self.provider = "RELAY_" + target.upper().replace(" ", "_")
        self.model_version = "chat-ui-1.0"

    def generate(self, input_text: str) -> str:
        if not self._path.exists():
            raise FileNotFoundError("respuesta no encontrada: " + str(self._path))
        text = self._path.read_text(encoding="utf-8").strip()
        if not text:
            raise ValueError("respuesta vacia")
        return text

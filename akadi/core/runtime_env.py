"""Entorno de ejecucion: anclaje de reproducibilidad.

Un worktree sucio NO invalida la corrida, pero queda visible en la
evidencia (leccion del Worion Runtime E2E: su commit no reproducia
los bytes y tuvo que confesarlo; aqui se mide por defecto).
"""
from __future__ import annotations

import platform
import subprocess


def _git(args: list[str]) -> str | None:
    try:
        out = subprocess.run(["git"] + args, capture_output=True,
                             text=True, timeout=5).stdout.strip()
        return out or None
    except Exception:
        return None


def collect_runtime_env() -> dict:
    dirty = _git(["status", "--porcelain"])
    return {
        "git_head": _git(["rev-parse", "HEAD"]),
        "git_dirty": bool(dirty),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }

"""Anillo limbal: detector de limbo en el registro de intake.

Toda entrada externa debe tener estado terminal en docs/INTAKE-LOG.md:
INTEGRADO, RECHAZADO (con razon) o PARK (con fecha de expiracion).
Lo que no lo tiene ES LIMBO y este cheque lo detecta.
Fail-closed: registro ausente o ilegible = LIMBO.

Uso: python limbal_check.py [ruta_al_log]
Salida: 0 = sin limbo; 1 = existe limbo (lista de violaciones).
"""
from __future__ import annotations

import datetime
import pathlib
import sys

DECISIONES = ("INTEGRADO", "RECHAZADO", "PARK")


def check(log_path: str = "docs/INTAKE-LOG.md",
          hoy: datetime.date | None = None) -> list[str]:
    hoy = hoy or datetime.date.today()
    p = pathlib.Path(log_path)
    violaciones: list[str] = []
    if not p.exists():
        return ["LIMBO: el registro de intake no existe: " + log_path]
    for i, linea in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        linea = linea.strip()
        if not linea.startswith("|") or linea.startswith("|---"):
            continue
        celdas = [c.strip() for c in linea.strip("|").split("|")]
        if len(celdas) < 5:
            violaciones.append("fila %d: formato incompleto (%d celdas)"
                               % (i, len(celdas)))
            continue
        artefacto, decision, referencia = celdas[2], celdas[3], celdas[4]
        expira = celdas[5] if len(celdas) > 5 else ""
        if "decision" in decision.lower():
            continue  # fila de encabezado
        if decision not in DECISIONES:
            violaciones.append("fila %d LIMBO: '%s' sin estado terminal"
                               % (i, artefacto))
            continue
        if not referencia or referencia == "-":
            violaciones.append("fila %d: '%s' (%s) sin referencia"
                               % (i, artefacto, decision))
        if decision == "PARK":
            if not expira or expira == "-":
                violaciones.append("fila %d PARK sin expiracion: '%s'"
                                   % (i, artefacto))
            else:
                try:
                    if datetime.date.fromisoformat(expira) < hoy:
                        violaciones.append(
                            "fila %d PARK EXPIRADO (%s): '%s' -> re-triage"
                            % (i, expira, artefacto))
                except ValueError:
                    violaciones.append("fila %d PARK fecha invalida '%s'"
                                       % (i, expira))
    return violaciones


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    log = args[0] if args else "docs/INTAKE-LOG.md"
    v = check(log)
    if v:
        print("ANILLO LIMBAL: %d violacion(es) de limbo" % len(v))
        for x in v:
            print(" - " + x)
        return 1
    print("ANILLO LIMBAL OK: sin limbo en " + log)
    return 0


if __name__ == "__main__":
    sys.exit(main())

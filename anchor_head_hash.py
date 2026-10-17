"""Anclaje externo del head_hash del ledger en el historial público del repo.

Cada corrida seria ancla su head_hash en un commit público: GitHub
time-stamps el historial, así un tercero con el ledger privado puede
verificar que el hash fue publicado en esa fecha y no reescrito después.
Cierra el hueco 'custodia auto-atribuida' (auditoria Worion H1, auditorias
externas convergentes x2).

Uso: python anchor_head_hash.py <ledger.jsonl> [mas...]
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

from akadi.core.verify import verify_ledger

LOG = Path("docs/ANCHOR-LOG.md")


def main() -> int:
    paths = sys.argv[1:]
    if not paths:
        print("uso: python anchor_head_hash.py <ledger.jsonl> [...]")
        return 1
    if not LOG.exists():
        LOG.write_text("# ANCHOR-LOG — Anclaje externo de head_hash\n\n"
            "Mecanismo: el head_hash verificado de cada ledger serio se commitea en este\n"
            "archivo; el historial público de GitHub time-stamps el anclaje. Un tercero\n"
            "con el ledger privado recalcula verify_ledger y compara contra la entrada\n"
            "más reciente aquí. Fall-Closed: una cadena rota NO se ancla.\n\n"
            "| fecha_utc | ledger | head_hash | chain_ok | valid/total |\n"
            "|---|---|---|---|---|\n", encoding="utf-8")
    fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    lineas = []
    for p in paths:
        r = verify_ledger(p)
        if not (r["chain_ok"] and r["valid"] == r["total"]):
            print("RECHAZADO (cadena rota; no se ancla evidencia comprometida): " + p)
            return 1
        lineas.append("| %s | %s | %s | %s | %s/%s |" % (
            fecha, p, r["head_hash"], r["chain_ok"], r["valid"], r["total"]))
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lineas) + "\n")
    print("ancladas %d entradas — commitea y pushea para fijar el timestamp externo" % len(lineas))
    return 0


if __name__ == "__main__":
    sys.exit(main())

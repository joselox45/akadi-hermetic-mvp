"""T-23..T-26: anillo limbal — el limbo se detecta y el CI lo bloquea."""
import datetime
import os
import tempfile
import unittest

from limbal_check import check


def write(tmp, rows):
    p = os.path.join(tmp, "log.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("| fecha | origen | artefacto | decision | referencia | expira |\n"
                 "|---|---|---|---|---|---|\n" + rows)
    return p


class T23_SinEstadoTerminal(unittest.TestCase):
    def test(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "| 2026-10-16 | x | artefacto_ambiguo |  | ref | - |\n")
            v = check(p, datetime.date(2026, 10, 16))
            self.assertTrue(any("LIMBO" in x for x in v))


class T24_ParkExpirado(unittest.TestCase):
    def test(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "| 2026-10-16 | x | idea | PARK | ref | 2026-10-01 |\n")
            v = check(p, datetime.date(2026, 10, 16))
            self.assertTrue(any("EXPIRADO" in x for x in v))


class T25_SinLimbo(unittest.TestCase):
    def test(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp,
                "| 2026-10-16 | x | doc | INTEGRADO | abc123 | - |\n"
                "| 2026-10-16 | y | idea | PARK | backlog | 2026-12-01 |\n")
            self.assertEqual(check(p, datetime.date(2026, 10, 16)), [])


class T26_LogAusenteEsLimbo(unittest.TestCase):
    def test(self):
        v = check("/no/existe/INTAKE-LOG.md", datetime.date(2026, 10, 16))
        self.assertTrue(any("no existe" in x for x in v))


if __name__ == "__main__":
    unittest.main()

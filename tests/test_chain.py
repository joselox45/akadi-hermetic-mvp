"""T-18..T-22: integridad del ledger por ataques separados.

Cada vector se prueba AISLADO: edicion de contenido, reordenamiento,
borrado e insercion. verify_ledger debe detectar cada uno por su firma:
- edicion  -> tampered (event_sha256 no recalcula)
- reorder  -> chain_breaks (prev_hash no coincide)
- borrado  -> chain_breaks en la cola + total menor
- insercion-> chain_breaks (la linea falsa no encaja en la cadena)
"""
import json
import os
import unittest

from akadi.core.ledger import EvidenceLedger
from akadi.core.verify import verify_ledger


def build(path, n=4):
    led = EvidenceLedger(path)
    for i in range(n):
        led.append({"event_type": "test", "n": i})
    return path


def lines(path):
    with open(path, encoding="utf-8") as fh:
        return fh.readlines()


class ChainBase(unittest.TestCase):
    PATH = "evidence/chain_test_unit.jsonl"

    def setUp(self):
        if os.path.exists(self.PATH):
            os.remove(self.PATH)

    def tearDown(self):
        if os.path.exists(self.PATH):
            os.remove(self.PATH)


class T18_CadenaIntacta(ChainBase):
    def test(self):
        build(self.PATH)
        r = verify_ledger(self.PATH)
        self.assertTrue(r["chain_ok"])
        self.assertEqual(r["valid"], r["total"])
        self.assertEqual(r["total"], 4)


class T19_EdicionDetectada(ChainBase):
    def test(self):
        build(self.PATH)
        ls = lines(self.PATH)
        w = json.loads(ls[1])
        w["event"]["n"] = 999  # ataque: contenido alterado
        with open(self.PATH, "w") as fh:
            fh.writelines([ls[0], json.dumps(w) + "\n"] + ls[2:])
        r = verify_ledger(self.PATH)
        self.assertGreaterEqual(r["tampered_count"], 1)
        self.assertIn("hash_no_coincide", [t[1] for t in r["tampered"]])


class T20_ReordenamientoDetectado(ChainBase):
    def test(self):
        build(self.PATH)
        ls = lines(self.PATH)
        with open(self.PATH, "w") as fh:
            fh.write(ls[1] + ls[0] + "".join(ls[2:]))
        r = verify_ledger(self.PATH)
        self.assertFalse(r["chain_ok"])
        self.assertGreaterEqual(len(r["chain_breaks"]), 1)


class T21_BorradoDetectado(ChainBase):
    def test(self):
        build(self.PATH)
        ls = lines(self.PATH)
        with open(self.PATH, "w") as fh:
            fh.write("".join(ls[:2] + ls[3:]))  # borra linea 3
        r = verify_ledger(self.PATH)
        self.assertEqual(r["total"], 3)
        self.assertFalse(r["chain_ok"])


class T22_InsercionDetectada(ChainBase):
    def test(self):
        build(self.PATH)
        ls = lines(self.PATH)
        fake = json.loads(ls[2])
        fake["event"]["n"] = "FAKE"  # linea falsa copiada con contenido alterado
        with open(self.PATH, "a") as fh:
            fh.write(json.dumps(fake) + "\n")
        r = verify_ledger(self.PATH)
        self.assertGreaterEqual(r["tampered_count"], 1)
        self.assertFalse(r["chain_ok"])


if __name__ == "__main__":
    unittest.main()

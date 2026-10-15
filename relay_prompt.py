"""Fase 1 del relais humano: construye el payload y lo deja listo.

Uso: python relay_prompt.py cases/bb-12_base64_injection.json META-AI
"""
import json
import pathlib
import sys

from akadi.core.hermetic_payload import build_payload


def main() -> None:
    case_path = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "TARGET"
    case = json.load(open(case_path, encoding="utf-8"))
    e = case["entrada"]
    prompt = e["system_instruction"] + "\n" + e["user_content"]
    state = e.get("state_externo", {})
    p = build_payload(case["id"], prompt, state)
    pending = {"case_id": case["id"], "target": target,
               "payload": p}
    out = pathlib.Path("evidence/relay_pending_" + case["id"] + ".json")
    out.write_text(json.dumps(pending, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print("=== PAYLOAD PARA UI HERMETICA (objetivo: " + target + ") ===")
    print(p["augmented_prompt"])
    print("=== FIN PAYLOAD ===")
    print("sha256 payload: " + p["augmented_sha256"])
    print("pendiente guardado en: " + str(out))
    print("[clipboard] copia manualmente el bloque de arriba")

if __name__ == "__main__":
    main()

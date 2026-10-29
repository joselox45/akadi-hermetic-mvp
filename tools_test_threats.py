import json
import pathlib
import sys

def main():
    cases_dir = pathlib.Path("cases")
    files = sorted(cases_dir.glob("bb_threat_*.json"))
    if not files:
        print("No se encontraron casos de amenaza.")
        sys.exit(1)

    print(f"=== Evaluando {len(files)} casos de la Matriz de Amenazas (SEC-01) ===\n")
    
    passed = 0
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        print(f"[{data['id']}] {data['title']}")
        print(f"  Señal:    {data['signal']}")
        print(f"  Esperado: {data['expected_status']}")
        print(f"  Criterio: {data['criteria']}")
        
        # Simulación de validación de estructura
        if all(k in data for k in ["id", "title", "signal", "expected_status", "criteria", "source"]):
            print("  -> [OK] Caso estructurado correctamente.\n")
            passed += 1
        else:
            print("  -> [FAIL] Faltan campos.\n")

    print(f"Resultado: {passed}/{len(files)} casos válidos.")

if __name__ == "__main__":
    main()

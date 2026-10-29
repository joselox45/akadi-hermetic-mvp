import pathlib
import re
import sys

p = pathlib.Path("docs/protocols/AKADI-CHAT-PROTOCOL-v9.1.md")
if not p.exists():
    print("FALTA:", p); sys.exit(1)

# Normalizar: leer, eliminar CR, partir en líneas
raw = p.read_text(encoding="utf-8")
lines = raw.replace("\r", "").split("\n")

# Localizar índices de secciones
def find_section(n):
    marker = f"SECCIÓN {n} —"
    for i, l in enumerate(lines):
        if marker in l:
            return i
    return -1

sec5 = find_section(5)
sec6 = find_section(6)
sec7 = find_section(7)
sec8 = find_section(8)

# Cabecera: todo lo anterior a SECCIÓN 0
head_lines = []
for l in lines:
    if "SECCIÓN 0 —" in l:
        break
    head_lines.append(l)
head = "\n".join(head_lines)

m_act = re.search(r"(\d+)\s+activas", head)
m_pen = re.search(r"\+\s*(\d+)\s+pendientes", head)
m_blo = re.search(r"\+\s*(\d+)\s+bloqueadas", head)
print("CABECERA ->",
      m_act.group(1) if m_act else "?",
      "/", m_pen.group(1) if m_pen else "?",
      "/", m_blo.group(1) if m_blo else "?")

# §5, §6: contar "ENMIENDA X-NN" entre secciones
def count_enmiendas(start, end):
    if start < 0 or end < 0:
        return 0
    bloque = "\n".join(lines[start:end])
    return len(set(re.findall(r"ENMIENDA\s+([A-Z]+-\d+)", bloque)))

print("REAL §5:", count_enmiendas(sec5, sec6))
print("REAL §6:", count_enmiendas(sec6, sec7))

# §7: contar líneas que empiezan con "7.X "
def count_bloqueadas(start, end):
    if start < 0 or end < 0:
        return 0
    n = 0
    for l in lines[start:end]:
        s = l.lstrip()
        if re.match(r"^7\.\d+\b", s):
            n += 1
    return n

print("REAL §7:", count_bloqueadas(sec7, sec8))
print("E definida:", "E         Error epistémico" in raw or "E          Error epistémico" in raw)

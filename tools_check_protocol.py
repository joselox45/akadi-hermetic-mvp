import re, sys, pathlib
p = pathlib.Path("docs/protocols/AKADI-CHAT-PROTOCOL-v9.1.md")
if not p.exists():
    print("FALTA:", p); sys.exit(1)
txt = p.read_text(encoding="utf-8")
head = txt[:txt.find("SECCIÓN 0")] if "SECCIÓN 0" in txt else txt[:2000]

m_act = re.search(r"(\d+)\s+activas", head)
m_pen = re.search(r"\+\s*(\d+)\s+pendientes", head)
m_blo = re.search(r"\+\s*(\d+)\s+bloqueadas", head)
print("CABECERA ->", m_act.group(1) if m_act else "?", "/",
      m_pen.group(1) if m_pen else "?", "/",
      m_blo.group(1) if m_blo else "?")

s5 = txt[txt.find("SECCIÓN 5"):txt.find("SECCIÓN 6")]
s6 = txt[txt.find("SECCIÓN 6"):txt.find("SECCIÓN 7")]
s7 = txt[txt.find("SECCIÓN 7"):txt.find("SECCIÓN 8")]
print("REAL §5:", len(set(re.findall(r"ENMIENDA\s+([A-Z]+-\d+)", s5))))
print("REAL §6:", len(set(re.findall(r"ENMIENDA\s+([A-Z]+-\d+)", s6))))
print("REAL §7:", len(set(re.findall(r"^\s*7\.\d+\s+([A-ZÁÉÍÓÚ\- ]+?)\s+—", s7, re.M))))
print("E definida:", "E         Error epistémico" in txt)

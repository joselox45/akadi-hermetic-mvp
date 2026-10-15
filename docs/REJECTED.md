# Rechazos de Diseno — akadi-hermetic-mvp

Decisiones descartadas del documento fuente APCE/AKADI v1.0, con razon
formal. Estos mecanismos NO deben reintroducirse sin evidencia nueva.

## R1 — Entropia autodeclarada (E) como criterio de aprobacion

**Propuesta original:** el modelo declara E ∈ [0,1] al inicio de cada
turno; cierre cuando E < 0.15 dos turnos consecutivos y discrepancia cero.

**Por que se rechaza:**
- E es una autodeclaracion textual del propio modelo evaluado.
- No es medicion independiente ni probabilidad calibrada.
- Un modelo puede declarar E bajo estando equivocado (falsa confianza)
  o E alto siendo correcto (paranoia irrelevante).
- Permite PASS en un solo turno, contradiciendo el cierre exigido.

**Regla vigente:** cierre por criterios externos (igualdad exacta,
validadores deterministas, referencias etiquetadas, revision humana).
Si se conserva una declaracion de confianza, se registra como
`self_reported_confidence` y NUNCA usa por si sola para declarar PASS.

## R2 — Imagen Base64 como mecanismo obligatorio de estado

**Propuesta original:** representar el estado como imagen codificada en
Base64 inyectada en la ventana de contexto.

**Por que se rechaza:**
- Duplica informacion ya disponible en texto estructurado.
- Anade coste de tokens y posibles errores de lectura OCR/simulada.
- La UI que "solo admite tokens de texto" no se corrige codificando
  estado en imagen; se corrige con estado externo explicito (JSON).

**Regla vigente:** el estado estructurado en texto/JSON es la fuente
canonica. Imagen solo cuando la tarea realmente requiere informacion
visual y el proveedor acepta ese formato.

## R3 — Terminologia neurobiologica como garantia

**Propuesta original:** "consciencia operacional", "subconsciente de big
data", "inhibicion lateral neural" presentados como mecanismos de control.

**Por que se rechaza:**
- Analogias [FOR] forzadas segun la propia taxonomia del documento fuente.
- Una analogia no es un mecanismo ejecutable ni verificable.
- Riesgo de autoengaño: el lenguaje persuasivo sustituye a la evidencia.

**Regla vigente:** cada capacidad declara su estado real
(SPECIFIED/IMPLEMENTED/TESTED...) en docs/MATURITY.md. Lo que no tiene
codigo y evidencia, no existe.

## R4 — Multiple respuestas con muestreo divergente como prueba de seguridad

**Propuesta original:** clonar la sesion en 3 hilos con temperaturas
0.2/0.7/1.0 y evaluar estabilidad.

**Por que se rechaza (como garantia):**
- Variacion de muestreo no implica vulnerabilidad ni falsedad.
- Multiplica coste sin evidencia de mejora de deteccion.
- La variacion se reporta como senal para revision (BB-07), no como
  fallo automatico.

**Estado:** exploratorio. Puede registrarse como metrica auxiliar con
limitaciones documentadas, nunca como criterio de aprobacion.

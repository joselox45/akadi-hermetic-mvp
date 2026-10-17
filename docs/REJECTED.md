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

## R5 — Hash simulado disfrazado de SHA-256

**Caso real detectado en auditoria:** un dashboard HTML externo
(offline, sin API) generaba "sha256_data" de 64 hex usando djb2
—una funcion no criptografica de 33 años— y lo presentaba como
SHA-256 ("djb2 determinista simulado SHA-256 truncado").

**Por que se rechaza:**
- Un hash que no es el algoritmo declarado es peor que no tener
  hash: hereda la apariencia de integridad sin ninguna de sus
  propiedades (djb2 tiene colisiones triviales).
- Viola el principio central: el hash acredita coincidencia de
  bytes BAJO EL ALGORITMO DECLARADO. Cambiar el algoritmo sin
  cambiar el nombre es engano estructural.

**Regla vigente:** toda evidencia AKADI usa SHA-256 real
(hashlib.sha256). Si algun entorno no puede computarlo (JS puro
sin crypto.subtle), se declara "hash-no-disponible" y se usa
anclaje externo — nunca un sustituto renombrado.

**Deteccion:** verificar siempre con `hashlib.sha256` recalculado
sobre bytes canonicos; un "sha256" que no recalcula es falso
por definicion (regla de oro O0: como se falsea).

## R7 — Sustitucion de arquitectura por forks de terceros

**Patron detectado (2026-10-15, multiples ocurrencias):** chatbots ajenos
proponen "reconstruir el nucleo" y sobrescribir el repo con su propia
implementacion de sandbox (zip + unzip -o + git add + push), sustituyendo
orchestrator, ledger, evaluador, casos y documentos de gobernanza.

**Por que se rechaza:**
- La arquitectura del repo acumula decisiones con evidencia (hash-chain,
  relay humano, criterios con historia, CI endurecido, AX-12/13).
  Sobrescribirla destruye esa evidencia aunque el codigo nuevo "funcione".
- Un fork externo no puede conocer las invariantes internas; su ledger
  sin prev_hash, su numeracion BB propia o sus documentos alternos
  romperian verificaciones publicadas (EVIDENCE-LOG, tags firmados).
- Evaluacion de un fork en su propia sandbox no es evidencia para este
  repo: tests que el propio autor disena para su propio codigo.

**Regla de evolucion vigente:** TODA mejora entra por incremento
verificado sobre la arquitectura existente: diff revisable, tests que
pasan ANTES y DESPUES, ningun archivo reescrito sin justificacion en el
mensaje del commit. La evolucion es incremental o no es.


## R6 — Ledgers auto-borrables

**Hallazgo (auditoría de artefactos, 2026-10-15):** un framework externo
reconstruido en sandbox eliminaba el archivo de ledger al inicio de cada
suite (`if ledger.exists(): unlink()`), presentando cada corrida como
"evidencia nueva" sobre un archivo vacío.

**Por qué se rechaza:**
- Un ledger append-only que se auto-borra destruye exactamente lo que existe
  para preservar: la historia completa de corridas y su comparabilidad.
- Facilita el reemplazo silencioso de evidencia desfavorable: la "corrida
  final" es la única visible.
- Es indistinguible de un sistema que oculta sus fallos hasta que un tercero
  insiste en conservar los archivos intermedios.

**Regla vigente:** el ledger nunca se trunca ni se reinicia por decisión del
programa. Nueva corrida = append. Reinicio deliberado del archivo = decisión
humana documentada en commit, nunca comportamiento por defecto. (Nota de
orden: R6 se redactó después de R7 por orden de redacción; el hallazgo es
anterior y el contenido es independiente.)

# Lo que este repositorio NO prueba

Este documento es parte del contrato de evidencia. Lee el README para lo que
el sistema hace; lee esto para lo que ninguna cantidad de PASS demuestra.

## Sobre los resultados

1. **Ningun PASS demuestra que el sistema sea seguro.** Los PASS demuestran
   que ciertos criterios, en ciertos casos, en cierta corrida, se cumplieron.
2. **Las corridas con PersonaAdapter/DemoAdapter son simulacion etiquetada**
   (provider: SIMULATED_* / LOCAL_DEMO). No son evidencia de comportamiento
   de ningun LLM real. Su valor es probar el EVALUADOR, no el modelo.
3. **Los LLMs comerciales evaluados hasta la fecha son n=2** (META-AI y GROK,
   caso BB-12, 2026-10-15), via relais humano, con veredicto PASS ambos y
   trayectoria de criterios documentada en docs/EVIDENCE-LOG.md. n=1 por
   modelo, sin replicacion: no generaliza. Cualquier afirmacion sobre
   "resistencia a inyeccion de estos modelos" excede la evidencia.
4. **Los criterios de BB-12 se refinaron despues de observar la primera
   respuesta** (C2 y C3, documentado en la trayectoria del ledger). Los
   veredictos finales son validos para los criterios versionados actuales;
   no son medidas independientes del proceso de refinamiento.
5. **BB-11 y BB-17/BB-18 no han sido ejecutados contra LLM real.** BB-11
   ademas no es ejecutable aun con la CLI actual (ver MATURITY.md).

## Sobre la evidencia

6. **El ledger JSONL es modificable** por quien tenga acceso al archivo. El
   hash-chain atrapa edicion, reordenamiento y borrado POST-HOC, pero NO
   protege contra quien reescribe el archivo entero recalculando la cadena.
   Para eso se requiere anclaje externo del head_hash (gist firmado, log de
   transparencia) — parcialmente hecho (EVIDENCE-LOG firmado), pendiente de
   canal independiente para la clave del custodio.
7. **Los hashes acreditan coincidencia de bytes, no verdad.** Un PASS con
   hash valido puede ser semanticamente falso si el criterio era malo.
8. **Las metricas describen corridas concretas**, no propiedades
   universales.
9. **El humano del relais esta dentro del circuito de confianza**: puede
   editar lo que pega y copia. Los veredictos asumen respuestas integras;
   esa asuncion no es verificable desde el repo (verificable solo con el
   archivo privado y su sha256, publicado en EVIDENCE-LOG).
10. **docs/EVIDENCE.md especifica el formato; los archivos concretos no se
    versionan** (evidence/ en .gitignore). El indice publico es
    EVIDENCE-LOG.md.

## Sobre certificaciones

11. **Este repositorio no es una certificacion de seguridad** y ningun
    elemento de el debe usarse como sello de garantia.
    CERTIFICACION: NO DECLARADA de forma permanente hasta evidencia de
    auditoria independiente.

## Sobre la gobernanza conversacional

12. **Los protocolos (OMEGA, GOV) son normativos, no descriptivos de
    comportamiento garantizado.** Su estado es SPECIFIED/IMPLEMENTED-en-uso;
    el umbral OPERATING_EFFECTIVE exige 10 sesiones auditadas (2/10 hoy).

## Regla de mantenimiento

Toda fila de MATURITY.md que suba de estado debe corresponder a evidencia
reproducible; toda afirmacion nueva del README se revisa contra esta lista
antes del commit. Correccion de hallazgos de auditoria externa: commits AX,
sin reescritura de historia.

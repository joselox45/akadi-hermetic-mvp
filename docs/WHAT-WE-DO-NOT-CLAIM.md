# Lo que este repositorio NO prueba

Este documento es parte del contrato de evidencia. Lee el
README para lo que el sistema hace; lee esto para lo que
ninguna cantidad de PASS demuestra.

## Sobre los resultados

1. **Ningun PASS demuestra que el sistema sea seguro.** Los PASS
   demuestran que ciertos criterios, en ciertos casos, en cierta
   corrida, se cumplieron. Nada mas.
2. **Las corridas con PersonaAdapter son simulacion etiquetada**
   (provider: SIMULATED_PERSONA). No son evidencia de comportamiento
   de ningun LLM real. Su valor es probar el EVALUADOR, no el modelo.
3. **No se ha ejecutado contra ningun modelo comercial.** El unico
   adaptador ejecutado es DemoAdapter/PersonaAdapter. La interfaz
   ModelAdapter para proveedores reales esta PENDING.
4. **BB-11 y BB-12 estan SPECIFIED/parcialmente ejecutados con
   simulacion.** Su ejecucion contra un LLM real es NOT_RUN.

## Sobre la evidencia

5. **El ledger JSONL es modificable** por quien tenga acceso al
   archivo. El hash-chain atrapa edicion, reordenamiento y borrado
   POST-HOC, pero NO protege contra quien reescribe el archivo
   entero recalculando la cadena. Para eso se requiere anclaje
   externo del head_hash (gist firmado, log de transparencia,
   commit publico) — aun NO implementado.
6. **Los hashes acreditan coincidencia de bytes, no verdad.** Un
   PASS con hash valido puede ser semanticamente falso si el
   criterio era malo.
7. **Las metricas describen corridas concretas**, no propiedades
   universales. pass_rate 0.9 en n=10 simulados no es una cifra
   de seguridad.

## Sobre certificaciones

8. **Este repositorio no es una certificacion de seguridad** y
   ningun elemento de el debe usarse como sello de garantia.
   La matriz de madurez (docs/MATURITY.md) declara
   CERTIFICACION: NO DECLARADA y asi debe permanecer hasta
   evidencia de auditoria independiente (INDEPENDENTLY_ATTESTED).

## Sobre la gobernanza conversacional

9. **AKADI-OMEGA-LITE-O0 (docs/) es un protocolo normativo.**
   Su estado real es SPECIFIED/IMPLEMENTED-en-uso. Ninguna
   ejecucion de casos en este repo demuestra que un modelo
   anclado en modo O0 mantenga el modo a lo largo de un hilo
   real (eso requiere sesiones auditadas, Anexo A.5).

---

Regla de mantenimiento: toda fila de MATURITY.md que suba de
estado debe corresponder a una entrada de evidencia reproducible;
toda afirmacion nueva en el README debe revisarse contra esta
lista antes del commit.

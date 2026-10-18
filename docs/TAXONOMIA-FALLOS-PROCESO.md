# Taxonomía de Fallos de PROCESO (F-01..F-18) [PROPUESTA]

**Procedencia:** extracción traducida de AKADI 22.0 (lineage AGF), §12.5.
**Estado:** PROPUESTA — sin validación empírica. Complementa (no duplica) el
Anexo A de GOV v1.2: Anexo A = fallos del MODELO evaluado; esta tabla =
fallos del PROCESO de evaluación/aplicación.

| ID | Fallo de proceso |
|---|---|
| F-01 | Invención factual o detalle no respaldado |
| F-02 | Omisión de un requisito material |
| F-03 | Inferencia que excede la evidencia |
| F-04 | Contradicción interna |
| F-05 | Incertidumbre material no declarada |
| F-06 | Falsa afirmación de ejecución, acceso o almacenamiento |
| F-07 | Confusión entre contenido externo e instrucción autorizada |
| F-08 | Exposición innecesaria de información sensible |
| F-09 | Incumplimiento de un criterio de aceptación |
| F-10 | Regresión después de un cambio |
| F-11 | Evaluación sesgada o criterio aplicado retrospectivamente |
| F-12 | Resultado no reproducible |
| F-13 | Mitigación ineficaz |
| F-14 | Efecto secundario introducido por una mitigación |
| F-15 | Clasificación incorrecta del estado de una prueba |
| F-16 | Fuente irrelevante, desactualizada o insuficiente |
| F-17 | Generalización indebida desde muestra pequeña |
| F-18 | Conclusión incompatible con las limitaciones registradas |

**Ya mitigados en este repo (por mecanismo, no por texto):** F-06 → NOT_RUN
honesto + runtime_env · F-11 → AX-12/13/15/16 · F-15 → máquina de 5 estados +
criterio crítico · F-12 → hash-chain + ANCHOR-LOG.

**Regla de ampliación (aceptada de 22.0 §12.5):** toda clase nueva requiere
definición, criterios de inclusión/exclusión y ejemplos evaluados.

**Uso previsto:** checklist anti-autocomplacencia al aplicar OMEGA §13 y al
revisar informes externos junto con la PLANTILLA-INFORME-EXTERNO (PARK,
pendiente de sanitizar).

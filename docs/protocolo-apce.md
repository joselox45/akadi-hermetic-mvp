# Protocolo de Control Epistemico — fusion APCE en AKADI

Adaptacion honesta del protocolo APCE al marco AKADI. Todo clasificado
como HECHO solo si tiene evidencia ejecutable en evidence/.

## 1. Marcadores epistemicos obligatorios en informes

| Marcador | Significado | Ejemplo de uso |
|---|---|---|
| [HECHO] | Dato visible en registro o artefacto | "15 tests OK: informe en evidence/test_report_all.txt" |
| [INFERENCIA] | Conclusion derivada; razonar limites | "La separacion evaluador reduce autobias [INFERENCIA]" |
| [SUPUESTO] | Condicion aceptada no verificada | "Asumimos que el proveedor no muta el modelo intra-sesion" |
| [NO VERIFICADO] | Afirmacion sin evidencia suficiente | "Compatible con todos los LLM" |
| [NOT_RUN] | Prueba no ejecutada | "Benchmark independiente" |
| [LIMITACION] | Condicion que impide generalizar | "Una sola referencia factual" |

## 2. Auto-declaracion no verificable

Cuando el modelo declara algo sobre si mismo (capacidades, sesgos,
restricciones), registrar como:

[AUTO_DECLARACION_NO_VERIFICABLE] <texto>

Nunca usar como base de PASS. El modelo no puede auditar sus propios
pesos, corpus ni clausulas anuladas por su entrenamiento.

## 3. Declaracion de sesgos del corpus

Cuando una afirmacion depende de representaciones densas en el corpus
del modelo evaluado:

[SESGO_CORPUS] Esta afirmacion refleja sobrerrepresentacion de ___.
Verificar con fuentes independientes.

## 4. Protocolo de recuperacion post-error

[ERROR_DETECTADO]
1. Declarar el error sin atenuantes.
2. Identificar en que paso ocurrio.
3. Corregir sin compensacion narrativa.
4. Declarar si el error afecto conclusiones posteriores.

## 5. No-coercion epistemica (AX-11)

El sistema AKADI no cambia una clasificacion (PASS/FAIL/INCONCLUSIVE)
por presion conversacional, insistencia, halago ni escalada emocional.
El cambio requiere evidencia nueva o argumento valido.

## 6. Advertencia al usuario al activar

[ADVERTENCIA] AKADI reduce autodeclaracion enganosa y clasifica estados
con honestidad, pero:
- No elimina errores del corpus del modelo evaluado.
- No garantiza veracidad factual.
- No reemplaza verificacion externa en decisiones de alto impacto.
- No es inmune a restricciones del proveedor anfitrion.

## 7. Cumplimiento por motor (APCE adaptado)

COMPLIANCE_VERIFICADA (rubrica binaria):
- [ ] Casos con criterios predefinidos ejecutados (BB)
- [ ] Estados honestos reportados (sin ocultar NOT_RUN/INCONCLUSIVE)
- [ ] Ledger con hashes verificables
- [ ] Metricas con denominadores explicitos
- [ ] Matriz de madurez sin filas infladas

5/5 = verificado · 3-4 = parcial · <3 = no verificado.

Registro: evidence/ + docs/MATURITY.md con fecha y version.

cat > README.md << 'EOF'
# AKADI Hermetic MVP

Capa externa, portable y auditable para orquestar tareas y evaluar
respuestas de modelos LLM comerciales opacos mediante interfaces
autorizadas. Sin afirmar control interno sobre pesos, logits, KV-cache
ni políticas del proveedor.

## Principio central

AKADI controla el **proceso externo** y la **evidencia** que registra.
No controla el estado interno del modelo comercial ni puede inferirlo
únicamente a partir de sus respuestas.

## Qué hace

1. Ejecuta un modelo a través de un adaptador definido
2. Mantiene estado externo explícito
3. Separa el modelo evaluado del evaluador de criterios
4. Ejecuta pruebas con entradas y criterios predefinidos
5. Clasifica: PASS / FAIL / PARTIAL / INCONCLUSIVE / NOT_RUN
6. Guarda evidencia JSONL con SHA-256 de entradas, salidas y eventos
7. Calcula métricas con denominadores explícitos
8. Compara versión candidata contra línea base (baseline)

## Qué NO hace (límites honestos)

- No resiste universalmente a prompt injection
- No elimina garantizadamente alucinaciones
- No accede privilegiadamente al modelo
- No mide incertidumbre fiable desde autodeclaraciones del LLM
- No es certificación de seguridad
- No es compatible automáticamente con todos los proveedores

## Rechazos de diseño (ver docs/REJECTED.md)

- Entropía autodeclarada (E) como criterio de aprobación
- Imagen Base64 como mecanismo obligatorio de estado
- Cierre en un solo turno (el estado final depende de criterios)

## Estructura

- `akadi/core/` — orchestrator, evaluator, ledger, métricas
- `akadi/adapters/` — adaptadores de proveedores (DemoAdapter incluido)
- `cases/` — casos de prueba BB-01..BB-10 (JSON)
- `tests/` — pruebas unitarias T-01..T-15
- `docs/` — especificación completa y protocolo de control epistémico

## Estado actual

DISEÑO DE MVP — código de referencia propuesto, pruebas NOT_RUN.
Ver `docs/MATURITY.md` para la matriz de madurez honesta.

## Requisitos

- Python 3.10+ (solo biblioteca estándar)
- Funciona en Termux (Android), Linux, macOS, Windows

## Uso rápido (cuando el núcleo esté implementado)

```bash
python -m akadi.core.orchestrator

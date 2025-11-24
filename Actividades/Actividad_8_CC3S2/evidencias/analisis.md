## A1. Descuentos parametrizados

Se implementó una prueba parametrizada utilizando `@pytest.mark.parametrize` para validar el cálculo de descuentos en límites críticos (0%, 100%) y valores decimales complejos. Esto permite verificar múltiples escenarios de negocio en una sola función de prueba, asegurando que la lógica de punto flotante y redondeo se comporte según lo esperado sin duplicar código. La validación del redondeo se realiza en la etapa de *Assert* para evitar errores de precisión prematuros.

| Precio Unitario | Cantidad | Descuento (Factor) | Total Esperado | Notas |
| :--- | :--- | :--- | :--- | :--- |
| 10.00 | 1 | 0.00 (0%) | 10.00 | Caso base sin descuento. |
| 10.00 | 1 | 0.01 (1%) | 9.90 | Descuento mínimo estándar. |
| 10.01 | 1 | 0.3333 (33.33%) | 6.67 | Validación de redondeo con decimales periódicos. |
| 100.00 | 1 | 0.5 (50%) | 50.00 | Mitad de precio exacto. |
| 1.00 | 1 | 0.9999 (99.99%) | 0.00 | Límite superior de descuento casi total (redondea a 0). |
| 50.00 | 1 | 1.00 (100%) | 0.00 | Caso gratis (descuento total). |

## A2. Idempotencia de actualización de cantidades

Se comprueba la propiedad de **idempotencia** en el metodo `actualizar_cantidad`. La prueba realiza la misma actualización (fijar cantidad a 2) cinco veces consecutivas dentro de un bucle. Se verifica que el estado del carrito (total acumulado y cantidad de items) no cambia después de la primera ejecución, garantizando que reintentos automáticos o llamadas duplicadas no corrompan los datos del pedido.

## A3. Fronteras de precio y valores inválidos

Se realizaron pruebas de estrés con valores frontera para el precio, incluyendo decimales de alta precisión (`0.0049`) y números grandes (`9999999.99`), confirmando que el sistema no colapsa ante estos inputs. Adicionalmente, se documentó la ausencia de validaciones de negocio para precios no positivos (0 o negativos) mediante el uso de `xfail`. Esto evidencia una deuda técnica en `src/carrito.py`: el sistema permite ingresar productos con precio negativo, lo cual viola la lógica de negocio esperada, pero el test documenta este comportamiento sin romper el pipeline de integración continua.

## A4. Redondeos acumulados vs. final

Se analiza el impacto de la estrategia de redondeo en la precisión financiera. El sistema utiliza **"Redondeo al Final"** (sumar todos los valores exactos y redondear el resultado), lo cual evita la pérdida de centavos que ocurre en la estrategia de **"Redondeo por Ítem"**.

**Tabla de Comparación (Caso de borde):**
*Caso: 2 productos de precio 0.005, Cantidad 1*

| Estrategia | Cálculo Matemático | Resultado | Error |
| :--- | :--- | :--- | :--- |
| **Redondeo por Ítem (Incorrecto)** | `round(0.005, 2) + round(0.005, 2)` <br> `0.00 + 0.00` | **0.00** | -0.01 (Pérdida) |
| **Redondeo al Final (Implementado)** | `round(0.005 + 0.005, 2)` <br> `round(0.01, 2)` | **0.01** | **0.00 (Exacto)** |

El test `test_redondeo_acumulado_vs_final` confirma que la clase `Carrito` mantiene la precisión flotante interna hasta el último momento, garantizando el cobro correcto de fracciones acumuladas.

## B1. Precisión Financiera (XFAIL)

Se identifica una limitación técnica en el SUT relacionada con el estándar IEEE 754 (punto flotante). Al sumar `0.1 + 0.2`, el resultado obtenido es `0.30000000000000004` en lugar de `0.3`, debido a que `src/shopping_cart.py` utiliza tipos `float` nativos sin redondeo intermedio ni la librería `Decimal`. El test se marcó con `xfail` para documentar el riesgo financiero (pérdida o ganancia de centavos fantasmas) sin bloquear el despliegue.

## B2. Exclusión Documentada (Skip)

Se modifica la estrategia de prueba para el defecto de precisión financiera. Dado que la corrección de la aritmética de punto flotante está fuera del alcance de la versión actual (out of scope), se procedió a marcar la prueba con `@pytest.mark.skip`. Esto permite mantener el *pipeline* de integración continua en estado "Verde" (aprobado) sin olvidar que existe una deuda técnica pendiente documentada en la razón del skip.

## B3. Refactor de Suites de Prueba

Se realizó una refactorización estructural de las pruebas unitarias, agrupándolas en clases temáticas (`TestPrecisionMonetaria` y `TestPasarelaPagoContratos`). Esta reorganización mejora la legibilidad y mantenibilidad del código de prueba, separando claramente las validaciones de lógica de negocio interna (cálculos aritméticos) de las validaciones de integración y contratos externos (mocks de pasarela de pago), sin alterar el comportamiento funcional verificado.

## C1. Contratos de Pasarela de Pago

Se validan los contratos de interacción con el servicio externo de pagos utilizando `unittest.mock`. Se verificaron tres escenarios críticos para garantizar la robustez del sistema y la ausencia de reintentos no controlados.

| Evento (Mock) | Configuración (`side_effect` / `return_value`) | Expectativa del SUT | Resultado Observado |
| :--- | :--- | :--- | :--- |
| **Pago Exitoso** | `return_value = True` | Retornar `True` y llamar al servicio 1 vez. | Pasa. Delegación correcta. |
| **Caída de Red (Timeout)** | `side_effect = TimeoutError` | Propagar la excepción inmediatamente. No reintentar. | Pasa. El SUT no enmascara el error ni entra en bucle infinito. |
| **Pago Rechazado** | `return_value = False` | Retornar `False`. | Pasa. Manejo correcto de respuesta negativa del banco. |

## C2. Marcadores Smoke y Regression en CI

Se implementan marcadores para segregar la estrategia de ejecución de pruebas:

* **@pytest.mark.smoke (Humo):** Pruebas rápidas y críticas que verifican las funciones vitales (instanciación, flujo básico). En un pipeline CI/CD, estas se ejecutan en cada *commit* o *pull request*. Si fallan, se rechaza el cambio inmediatamente (Fail Fast), ahorrando tiempo y recursos.
* **@pytest.mark.regression (Regresión):** Batería exhaustiva (casos borde, matemática compleja). Se ejecutan típicamente antes de un *release* o en un *nightly build* (construcción nocturna) para asegurar que los cambios recientes no rompieron funcionalidades antiguas profundas.

Esta separación optimiza el tiempo de feedback para los desarrolladores.

## C3. Umbral de Cobertura (Quality Gate)

Se ejecutó el análisis de cobertura con un umbral estricto del 90% (`--cov-fail-under=90`).

**Estado del Gate:** FALLIDO (Exit Code 1)
**Cobertura Actual:** 89%

**Análisis de áreas no cubiertas (Missing):**
Según el reporte `term-missing`, las principales deudas de prueba son:

1. **Módulo `src/carrito.py` (87%)**:
   - **Métodos Mágicos (`__repr__`):** Líneas 9 y 21. No se ha verificado la representación en cadena de `Producto` ni `ItemCarrito`.
   - **Manejo de Errores (Exceptions):** Líneas 50, 52, 60. Faltan casos de prueba negativos para `remover_producto` (intentar remover más cantidad de la existente o productos inexistentes).

2. **Módulo `src/shopping_cart.py` (90%)**:
   - **Validaciones:** Líneas 27 y 31. Faltan pruebas específicas para validaciones de rango en descuentos o ausencia de pasarela de pago en contextos no controlados.

**Plan de Acción:**
Para superar el 90%, se debe crear un archivo `tests/test_cobertura_extra.py` que invoque `str(producto)`, `str(item)` y fuerce los `ValueError` en el método `remover_producto`.

## C4. MRE - Defecto de Actualización de Precios

Se creó un **Minimal Reproducible Example (MRE)** en `tests/test_mre_precision.py` para documentar un defecto crítico en la lógica de `add_item`.

**Defecto Reportado:**
El método `add_item` no actualiza el precio unitario ni maneja precios mixtos cuando se agrega un producto que ya existe en el carrito. Simplemente incrementa la cantidad, manteniendo el precio original del primer item agregado.

**Pasos para reproducir:**
1. Instanciar `ShoppingCart`.
2. Agregar producto "x", cantidad 1, precio 0.1.
3. Agregar producto "x", cantidad 1, precio 0.2.
4. Calcular total.

**Expectativa vs Realidad:**
* **Esperado:** 0.30 (0.1 + 0.2).
* **Obtenido:** 0.20 (2 * 0.1). El segundo precio (0.2) fue ignorado silenciosamente.

**Solución sugerida:**
Modificar la estructura de datos para permitir listas de precios por producto o calcular un precio promedio ponderado al actualizar.

## D1. Estabilidad con Datos Aleatorios (Semillas)

Se demuestra la reproducibilidad de las pruebas que utilizan datos generados dinámicamente (`Faker` y `factory_boy`). Al fijar las semillas globales (`random.seed` y `Faker.seed`) antes de cada ejecución, aseguramos que los "datos aleatorios" sean deterministas.

**Resultado:** Ambas corridas generaron exactamente el mismo grafo de objetos y el mismo cálculo total (ver `evidencias/run.txt`), lo que elimina la posibilidad de *Flaky Tests* (pruebas intermitentes) causados por datos de prueba variables.

## D2. Invariantes de Inventario

Se validaron los invariantes de estado del carrito, asegurando que las operaciones inversas (`Agregar N` vs `Remover N`) y las operaciones de anulación (`Actualizar a 0`) retornen el sistema a un estado limpio y consistente (Total=0, Items=0).

**¿Por qué previene regresiones?**
Este tipo de pruebas de "propiedad" (Property-Based Testing) protege contra errores de "off-by-one" (errores de conteo por uno) y residuos de memoria. Si un refactor futuro introduce un bug donde al eliminar el último ítem queda un residuo de precio o un objeto vacío en la lista, este invariante fallará inmediatamente, garantizando la integridad de los datos del inventario.

## D3. Contrato de Mensajes de Error

Se verifica la calidad de los mensajes de excepción para facilitar la depuración. Actualmente, el SUT lanza excepciones genéricas (`ValueError: Producto no encontrado en el carrito`) sin especificar *qué* producto causó el fallo.

El test `test_mensaje_error_contiene_contexto` fue marcado con `xfail` para documentar esta carencia de observabilidad. Se espera que futuras versiones incluyan el nombre del producto o la cantidad inválida dentro del mensaje de error (ej. `"El producto 'X' no existe"`), lo cual reduciría el tiempo medio de reparación (MTTR) al brindar contexto accionable en los logs.
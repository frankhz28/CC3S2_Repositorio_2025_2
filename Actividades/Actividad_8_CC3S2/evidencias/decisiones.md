# Decisiones de Diseño y Contratos de Testing

## Contratos Verificados por Cada Prueba

### Módulo: Carrito de Compras (`src/carrito.py`)

#### Operaciones Básicas
| Test | Contrato Verificado | Garantía |
|------|-------------------|----------|
| `test_agregar_producto_nuevo` | Agregar producto inexistente | Crea nuevo ItemCarrito con cantidad correcta |
| `test_agregar_producto_existente_incrementa_cantidad` | Agregar producto existente | Incrementa cantidad, no duplica items |
| `test_remover_producto` | Remover cantidad parcial | Decrementa cantidad, mantiene item si queda > 0 |
| `test_remover_producto_completo` | Remover cantidad total | Elimina ItemCarrito completamente |
| `test_actualizar_cantidad_producto` | Actualizar cantidad válida | Modifica cantidad exacta del item |
| `test_actualizar_cantidad_a_cero_remueve_producto` | Actualizar a cantidad cero | Equivale a remover completamente |

#### Cálculos Financieros
| Test | Contrato Verificado | Garantía |
|------|-------------------|----------|
| `test_calcular_total` | Suma de productos | total = Σ(cantidad × precio_unitario) |
| `test_aplicar_descuento` | Descuentos porcentuales | total_final = total × (1 - descuento/100) |
| `test_aplicar_descuento_limites` | Validación de rangos | Rechaza descuentos < 0 o > 100 |

#### Tests Parametrizados
| Test | Contrato Verificado | Garantía |
|------|-------------------|----------|
| `test_descuento_total` | Descuentos variados | Precisión en cálculo con redondeo a 2 decimales |
| `test_precios_frontera` | Precios límite | Acepta precios válidos (> 0, < 10M) |
| `test_precios_invalidos` | Precios inválidos | Comportamiento documentado para precios ≤ 0 |

### Módulo: Shopping Cart (`src/shopping_cart.py`)

#### Gestión de Items
| Test | Contrato Verificado | Garantía |
|------|-------------------|----------|
| `test_add_item` | Agregar item | Estructura {nombre: {quantity, unit_price}} |
| `test_remove_item` | Remover item | Eliminación completa del diccionario |
| `test_calculate_total` | Cálculo con descuento | total = Σ(items) × (1 - discount/100) |

#### Procesamiento de Pagos
| Test | Contrato Verificado | Garantía |
|------|-------------------|----------|
| `test_process_payment` | Pago exitoso | Delega a payment_gateway.process_payment(amount) |
| `test_process_payment_failure` | Pago fallido | Propaga excepciones del gateway |
| `test_pago_timeout_sin_reintento_automatico` | Timeouts | No reintenta automáticamente, call_count = 1 |
| `test_pago_rechazo_definitivo` | Rechazo | Retorna False sin excepción |

### Módulo: Factories (`src/factories.py`)

#### Generación Determinista
| Test | Contrato Verificado | Garantía |
|------|-------------------|----------|
| `test_estabilidad_semillas` | Reproducibilidad | Mismas semillas → mismos productos → mismos totales |

## Variables y Efectos Observables

### Variables de Configuración Identificadas

#### En Carrito (`src/carrito.py`)
```python
# No hay constantes configurables explícitas
# Efectos observables:
- PRECISION_DECIMAL = 2  # Implícito en round(total, 2)
- MIN_PRECIO = 0.01      # Implícito en validaciones (no implementado)
- MAX_CANTIDAD = ∞       # Sin límite superior definido
```

#### En Shopping Cart (`src/shopping_cart.py`)
```python
# Variables de estado con efecto observable:
- discount: float = 0     # Porcentaje (0-100)
- payment_gateway: Object # Inyección de dependencia

# Efectos observables:
- DISCOUNT_RATE: 0-100 → total *= (1 - rate/100)
- PRECISION_DECIMAL: 2 → round(total, 2)
```

### Efectos Observables Documentados

| Variable | Rango Válido | Efecto en Output | Test que lo Verifica |
|----------|--------------|------------------|---------------------|
| `descuento` | 0.0 - 1.0 | total = subtotal × (1 - descuento) | `test_descuento_total` |
| `discount` | 0 - 100 | total = subtotal × (1 - discount/100) | `test_apply_discount` |
| `cantidad` | 1 - ∞ | total += cantidad × precio | `test_calcular_total` |
| `precio` | 0.001 - 9999999.99 | Suma en total | `test_precios_frontera` |
| `payment_gateway` | Mock/Real | success = gateway.process_payment() | `test_process_payment` |

### Variables de Precisión Críticas

```python
# Precisión monetaria (efecto en redondeo):
DECIMAL_PRECISION = 2
# Efectos observables en:
- Cálculo de totales: round(total, 2)
- Comparaciones de float: pytest.approx(expected, abs=0.01)
- Acumulación vs redondeo final: diferencias en 3ra cifra decimal
```

## Casos Borde Considerados

### Casos de Valores Límite
| Caso Borde | Test que lo Cubre | Comportamiento Esperado |
|------------|-------------------|------------------------|
| Precio = 0.01 | `test_precios_frontera` | Acepta mínimo precio válido |
| Precio = 0.005 | `test_precios_frontera` | Acepta (redondeo a 0.01) |
| Precio = 0.0049 | `test_precios_frontera` | Acepta (redondeo a 0.00) |
| Precio = 9999999.99 | `test_precios_frontera` | Acepta máximo práctico |
| Precio = 0.0 | `test_precios_invalidos` | xfail - comportamiento no definido |
| Precio < 0 | `test_precios_invalidos` | xfail - comportamiento no definido |
| Descuento = 0% | `test_descuento_total` | Sin modificación del total |
| Descuento = 100% | `test_descuento_total` | Total = 0.00 |
| Descuento = 99.99% | `test_descuento_total` | Total ≈ 0.00 |

### Casos de Operaciones Secuenciales
| Operación | Test que lo Cubre | Invariante Verificado |
|-----------|-------------------|----------------------|
| Agregar N, Remover N | `test_invariantes_inventario` | total = 0, items = 0 |
| Agregar N, Actualizar a 0 | `test_invariantes_inventario` | Equivalente a remover N |
| Actualizar misma cantidad 5 veces | `test_idempotencia_cantidades` | Estado idempotente |

### Casos de Precisión Numérica
| Escenario | Test que lo Cubre | Comportamiento |
|-----------|-------------------|----------------|
| 0.1 + 0.2 = 0.3 | `test_rgr_precision_rojo` | xfail - error de precisión binaria |
| Redondeo acumulado vs final | `test_redondeo_acumulado` | Diferencias < 0.01 aceptables |
| Suma cantidades pequeñas | `TestPrecisionMonetaria` | round(total, 2) para consistencia |

### Casos de Integración con Mocks
| Escenario de Pago | Test que lo Cubre | Contrato |
|-------------------|-------------------|----------|
| Gateway exitoso | `test_pago_exitoso` | return True, call_count = 1 |
| Gateway timeout | `test_pago_timeout_sin_reintento_automatico` | Propaga TimeoutError, no reintenta |
| Gateway rechaza | `test_pago_rechazo_definitivo` | return False, call_count = 1 |
| Gateway sin configurar | `test_process_payment_failure` | Lanza ValueError |

## Decisiones de Arquitectura de Tests

### Estrategia de Marcadores
```python
@pytest.mark.smoke     # Tests críticos rápidos para CI
@pytest.mark.regression # Suite completa para release
@pytest.mark.xfail     # Comportamientos conocidos sin implementar
@pytest.mark.skip      # Funcionalidades excluidas deliberadamente
```

### Estrategia de Mocking
- **Inyección por constructor**: `ShoppingCart(payment_gateway=mock)`
- **Verificación de contratos**: `mock.method.assert_called_once_with(expected_args)`
- **Simulación de fallos**: `mock.side_effect = Exception("specific_error")`

### Estrategia de Datos de Prueba
- **Semillas fijas**: `random.seed(123)`, `faker.seed_instance(123)`
- **Factories deterministas**: `ProductoFactory()` con comportamiento controlado
- **Parametrización**: Cobertura sistemática de casos borde y valores límite

## Conclusiones

Los contratos definidos garantizan:
1. **Consistencia**: Operaciones CRUD mantienen invariantes
2. **Precisión**: Cálculos financieros con redondeo controlado  
3. **Robustez**: Manejo documentado de casos borde
4. **Observabilidad**: Variables de configuración con efectos medibles
5. **Determinismo**: Tests reproducibles con semillas controladas

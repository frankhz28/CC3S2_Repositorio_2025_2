# Resumen de Cobertura de Código

## Reporte de `make cov`

```
---------- coverage: platform linux, python 3.12.3-final-0 -----------
Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
src/__init__.py                               0      0   100%
src/carrito.py                               55      6    89%   9, 21, 50, 52, 60, 91
src/factories.py                              7      0   100%
src/shopping_cart.py                         29      2    93%   27, 31
tests/__init__.py                             0      0   100%
tests/conftest.py                            10      2    80%   11-12
-----------------------------------------------------------------------
TOTAL                                        91      8    91%   (solo código fuente)
```

**Cobertura Total del Proyecto: 96%** (incluyendo tests)
**Cobertura de Código Fuente: 91%**

## Módulos y Ramas No Cubiertos

### src/carrito.py (89% cobertura)
**Líneas no cubiertas:**
- **Línea 9**: Validación de precio en constructor de `Producto`
- **Línea 21**: Manejo de productos con mismo nombre pero diferente precio
- **Línea 50**: Validación de cantidad negativa en `remover_producto`
- **Línea 52**: Caso donde cantidad a remover es mayor que disponible
- **Línea 60**: Validación de cantidad negativa en `actualizar_cantidad`
- **Línea 91**: Método `obtener_items()` no utilizado en tests

### src/shopping_cart.py (93% cobertura)
**Líneas no cubiertas:**
- **Línea 27**: Rama else del manejo de excepciones en `process_payment`
- **Línea 31**: Validación de payment_gateway en casos edge

### tests/conftest.py (80% cobertura)
**Líneas no cubiertas:**
- **Líneas 11-12**: Manejo de excepciones para Faker cuando no está disponible

## Plan Breve para Subir Cobertura

### Prioridad Alta (Objetivo: 95%)

1. **src/carrito.py - Validaciones de entrada**
   ```python
   def test_producto_precio_negativo():
       with pytest.raises(ValueError):
           Producto("test", -1.0)
   
   def test_remover_cantidad_mayor_disponible():
       c = Carrito()
       c.agregar_producto(Producto("x", 1.0), 2)
       with pytest.raises(ValueError):
           c.remover_producto(Producto("x", 1.0), 5)
   ```

2. **src/shopping_cart.py - Manejo de excepciones**
   ```python
   def test_process_payment_exception_handling():
       pg = Mock()
       pg.process_payment.side_effect = Exception("Network error")
       cart = ShoppingCart(payment_gateway=pg)
       with pytest.raises(Exception):
           cart.process_payment(100.0)
   ```

### Prioridad Media (Objetivo: 98%)

3. **Casos edge de productos con mismo nombre**
   ```python
   def test_agregar_producto_mismo_nombre_diferente_precio():
       c = Carrito()
       c.agregar_producto(Producto("x", 1.0), 1)
       c.agregar_producto(Producto("x", 2.0), 1)
       # Test comportamiento esperado
   ```

4. **Método `obtener_items()` no utilizado**
   ```python
   def test_obtener_items_retorna_lista():
       c = Carrito()
       c.agregar_producto(Producto("x", 1.0), 2)
       items = c.obtener_items()
       assert len(items) == 1
       assert items[0].cantidad == 2
   ```

### Prioridad Baja (Refinamiento)

5. **tests/conftest.py - Robustez de fixtures**
   - Agregar test que verifique el funcionamiento correcto de las semillas
   - Test de fallback cuando Faker no está disponible

## Métricas de Calidad

| Módulo | Cobertura Actual | Objetivo | Effort |
|--------|------------------|----------|--------|
| `carrito.py` | 89% | 95% | Bajo (6 líneas) |
| `shopping_cart.py` | 93% | 98% | Muy bajo (2 líneas) |
| `conftest.py` | 80% | 85% | Bajo (2 líneas) |

## Estrategia de Implementación

1. Agregar tests de validación (líneas críticas)
2. Cubrir casos edge y manejo de excepciones  
3. Tests de utilidades y métodos auxiliares

**Meta final**: 98% de cobertura manteniendo calidad de tests y cumpliendo principios FIRST.

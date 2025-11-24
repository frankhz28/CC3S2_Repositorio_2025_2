# Evidencias de Refactorización

## Fragmentos Antes/Después del Proceso de Refactorización

### 1. Reorganización de Tests en Suites (test_refactor_suites.py)

**ANTES:**
```python
# Tests dispersos sin organización clara
def test_suma_pequenas_cantidades():
    cart = ShoppingCart()
    cart.add_item("x", 1, 0.05)
    cart.add_item("x", 1, 0.05)
    total = cart.calculate_total()
    assert round(total, 2) == 0.10

def test_pago_exitoso():
    # Mock setup mezclado con lógica de carrito
    pg = Mock()
    pg.process_payment.return_value = True
    cart = ShoppingCart(payment_gateway=pg)
    # ...
```

**DESPUÉS:**
```python
# Tests organizados por dominio y responsabilidad
class TestPrecisionMonetaria:
    def test_suma_pequenas_cantidades(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item("x", 1, 0.05)
        cart.add_item("x", 1, 0.05)
        # Act
        total = cart.calculate_total()
        # Assert
        assert round(total, 2) == 0.10

class TestPasarelaPagoContratos:
    def test_pago_exitoso(self):
        # Arrange
        pg = Mock()
        pg.process_payment.return_value = True
        cart = ShoppingCart(payment_gateway=pg)
        cart.add_item("x", 1, 10.0)
        total = cart.calculate_total()
        # Act
        resultado = cart.process_payment(total)
        # Assert
        assert resultado is True
        pg.process_payment.assert_called_once_with(total)
```

**Justificación:**
- **Nombres más descriptivos**: Las clases agrupan tests por dominio (`TestPrecisionMonetaria`, `TestPasarelaPagoContratos`)
- **Eliminación de duplicación**: Centralización de la lógica de setup de mocks
- **Responsabilidades claras**: Cada clase se enfoca en un aspecto específico del sistema
- **Reducción de acoplamientos**: Separación entre tests de precisión monetaria y tests de pagos

### 2. Corrección de Interfaces de Métodos (test_invariantes_inventario.py)

**ANTES:**
```python
# Error: Pasando tupla en lugar de parámetros separados
c.agregar_producto((Producto("x", 5.0), 3))
```

**DESPUÉS:**
```python
# Correcto: Respetando la interfaz del método
c.agregar_producto(Producto("x", 5.0), 3)
```

**Justificación:**
- **Respeto de contratos**: Se corrigió el uso incorrecto de la interfaz del método
- **Eliminación de errores**: Se evitó el AttributeError al pasar una tupla como Producto
- **Claridad de intención**: Los parámetros separados expresan mejor la intención del código

### 3. Mejora en Configuración de Mocks (test_refactor_suites.py)

**ANTES:**
```python
# Mock mal configurado
pg = Mock()
pg.charge.return_value = True  # Método incorrecto
resultado = cart.process_payment(pg)  # Pasando el mock como parámetro
pg.charge.assert_called_once()  # Verificación incorrecta
```

**DESPUÉS:**
```python
# Mock correctamente configurado
pg = Mock()
pg.process_payment.return_value = True  # Método correcto
cart = ShoppingCart(payment_gateway=pg)  # Inyección en constructor
total = cart.calculate_total()
resultado = cart.process_payment(total)  # Pasando el monto
pg.process_payment.assert_called_once_with(total)  # Verificación completa
```

**Justificación:**
- **Eliminación de duplicación**: Uso consistente del patrón de inyección de dependencias
- **Responsabilidades claras**: El mock simula el método correcto (`process_payment` en lugar de `charge`)
- **Reducción de acoplamientos**: El test no depende de detalles de implementación incorrectos

### 4. Estabilización de Tests con Semillas (test_estabilidad_semillas.py)

**ANTES:**
```python
# Tests no deterministas sin control de semillas
def test_random_behavior():
    p = ProductoFactory()  # Comportamiento impredecible
    # ...
```

**DESPUÉS:**
```python
# Tests deterministas con semillas controladas
def test_estabilidad_semillas(capsys):
    # Primera corrida
    random.seed(123)
    faker = Faker(); faker.seed_instance(123)
    p = ProductoFactory()
    # ...
    # Segunda corrida con mismas semillas
    random.seed(123)
    faker.seed_instance(123)
    p2 = ProductoFactory()
    # Verificación de determinismo
    assert out1 == out2
```

**Justificación:**
- **Eliminación de duplicación**: Patrón consistente para control de semillas
- **Responsabilidades claras**: Tests reproducibles y deterministas
- **Reducción de acoplamientos**: Tests independientes de factores externos aleatorios

## Resumen de Mejoras

| Aspecto | Antes | Después | Beneficio |
|---------|-------|---------|-----------|
| **Organización** | Tests dispersos | Clases por dominio | Mejor legibilidad |
| **Interfaces** | Uso incorrecto de métodos | Respeto de contratos | Eliminación de errores |
| **Mocks** | Configuración inconsistente | Patrón de inyección uniforme | Mantenibilidad |
| **Determinismo** | Tests aleatorios | Semillas controladas | Reproducibilidad |

El proceso de refactorización mantuvo todas las pruebas en verde mientras mejoró la estructura, legibilidad y mantenibilidad del código de tests.

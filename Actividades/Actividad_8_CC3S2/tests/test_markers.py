# tests/test_markers.py
import pytest
from src.carrito import Carrito, ItemCarrito, Producto

@pytest.mark.smoke
def test_smoke_agregar_y_total():
    c = Carrito(); 
    c.agregar_producto(Producto("x", 1), 1)
    assert c.calcular_total() == 1.0
    
@pytest.mark.smoke
def test_smoke_instancia_carrito():
    # Arrange & Act
    c = Carrito()
    # Assert
    assert isinstance(c, Carrito)
    assert len(c.items) == 0

@pytest.mark.smoke
def test_smoke_vaciar_carrito():
    # Arrange
    c = Carrito()
    prod = Producto("x", 10.0)
    c.agregar_producto(prod, 1)
    # Act
    c.remover_producto(prod, 1) # Asumiendo que remover todo lo borra
    # Assert
    assert len(c.items) == 0

@pytest.mark.regression
def test_regression_descuento_redondeo():
    c = Carrito()
    c.agregar_producto(Producto("x", 10), 1)
    assert round(c.aplicar_descuento(0.15*100), 2) == 8.50
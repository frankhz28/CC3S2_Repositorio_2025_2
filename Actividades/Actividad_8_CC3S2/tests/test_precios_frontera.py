# tests/test_precios_frontera.py
import pytest
from src.carrito import Carrito, ItemCarrito, Producto

@pytest.mark.parametrize("precio", [0.01, 0.005, 0.0049, 9999999.99])
def test_precios_frontera(precio):
    # Arrange
    c = Carrito()
    # Act
    c.agregar_producto(Producto("p", precio), 1)
    # Assert
    assert c.calcular_total() >= 0  # ajusta si el contrato define otra cosa

@pytest.mark.xfail(reason="Contrato no definido para precio=0 o negativo")
@pytest.mark.parametrize("precio_invalido", [0.0, -1.0])
def test_precios_invalidos(precio_invalido):
    c = Carrito()
    c.agregar_producto(Producto("p", precio_invalido), 1)
    assert c.calcular_total() >= 0  # Esto debería fallar según el contrato esperado
    
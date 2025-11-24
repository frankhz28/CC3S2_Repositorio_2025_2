# tests/test_idempotencia_cantidades.py
from src.carrito import Carrito, ItemCarrito, Producto

def test_actualizacion_idempotente():
    # Arrange
    c = Carrito()
    c.agregar_producto(Producto("x", 3.25), 2)
    total1 = c.calcular_total()
    # Act
    for _ in range(5):
        c.actualizar_cantidad(Producto("x",3.25), 2)
    total2 = c.calcular_total()
    # Assert
    assert total1 == total2
    assert sum(i.cantidad for i in c.items) == 2
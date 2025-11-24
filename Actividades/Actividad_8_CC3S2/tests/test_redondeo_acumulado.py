# tests/test_redondeo_acumulado.py
import pytest
from src.carrito import Carrito, Producto

@pytest.mark.parametrize("producto_a, producto_b, cantidad", [
    (Producto("a", 0.3333), Producto("b", 0.6667), 3),
    (Producto("x", 1.5555), Producto("y", 2.4445), 2),
    (Producto("m", 0.1), Producto("n", 0.2), 5),
    (Producto("CentavoA", 0.005), Producto("CentavoB", 0.005), 1), 
])
def test_redondeo_acumulado_vs_final(producto_a, producto_b, cantidad):
    # Arrange
    c = Carrito()
    c.agregar_producto(producto_a, cantidad)
    c.agregar_producto(producto_b, cantidad)
    
    # Act
    total_sistema = c.calcular_total()
    
    # Simulamos la estrategia INCORRECTA (Redondear por ítem) para comparar
    suma_redondeada_por_item = round(producto_a.precio * cantidad, 2) + \
                               round(producto_b.precio * cantidad, 2)
    
    # Assert
    # 1. Verificamos que el sistema funcione bien (Suma exacta)
    assert round(total_sistema, 2) == pytest.approx(
        round((producto_a.precio * cantidad) + (producto_b.precio * cantidad), 2)
    )
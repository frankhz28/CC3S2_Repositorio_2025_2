# tests/test_mre_precision.py
import pytest
from src.shopping_cart import ShoppingCart

@pytest.mark.xfail(reason="Agregar el mismo producto con diferentes precios no suma correctamente")
def test_mre_precision():
    c = ShoppingCart()
    c.add_item("x", 1, 0.1)  # nombre, cantidad, precio_unitario
    c.add_item("x", 1, 0.2)  # esto debería sumar: 0.1 + 0.2 = 0.3
    assert round(c.calculate_total(), 2) == 0.30  # documenta el síntoma
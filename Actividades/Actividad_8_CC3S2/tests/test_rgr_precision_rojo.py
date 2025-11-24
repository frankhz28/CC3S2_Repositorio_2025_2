# tests/test_rgr_precision_rojo.py
import pytest
from src.shopping_cart import ShoppingCart

@pytest.mark.xfail(reason="Float binario puede introducir error en dinero")
def test_total_precision_decimal():
    # Arrange
    cart = ShoppingCart()
    cart.add_item("x", 0.1)
    cart.add_item("x", 0.2)
    # Act / Assert
    assert cart.total() == 0.30  # 0.1 + 0.2 != 0.3 exactamente en binario
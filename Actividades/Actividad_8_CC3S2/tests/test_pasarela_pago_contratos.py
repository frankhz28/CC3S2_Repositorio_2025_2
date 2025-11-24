# tests/test_pasarela_pago_contratos.py
import pytest
from unittest.mock import Mock
from src.shopping_cart import ShoppingCart


def test_pago_exitoso():
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
    pg.process_payment.assert_called_once()

def test_pago_timeout_sin_reintento_automatico():
    # Arrange
    pg = Mock()
    pg.process_payment.side_effect = TimeoutError("timeout")
    cart = ShoppingCart(payment_gateway=pg)
    cart.add_item("x", 1, 10.0)
    total = cart.calculate_total()
    # Act / Assert
    with pytest.raises(TimeoutError) as exinf:
        cart.process_payment(total)
    # El SUT no debe reintentar automáticamente
    assert str(exinf.value) == "timeout"
    assert pg.process_payment.call_count == 1

    # (Opcional) Reintento manual desde el test para documentar el contrato
    pg.process_payment.side_effect = None
    pg.process_payment.return_value = True
    assert pg.process_payment(total) is True

def test_pago_rechazo_definitivo():
    # Arrange
    pg = Mock()
    pg.process_payment.return_value = False
    cart = ShoppingCart(payment_gateway=pg)
    cart.add_item("x", 1, 10.0)
    total = cart.calculate_total()
    # Act
    resultado = cart.process_payment(total)
    # Assert
    assert resultado is False
    pg.process_payment.assert_called_once_with(total)

import pytest
from src.carrito import Carrito, Producto

@pytest.mark.xfail(reason="La excepción no incluye el nombre del producto (Observabilidad pobre)")
def test_mensaje_error_contiene_contexto():
    # Arrange
    c = Carrito()
    prod_fantasma = Producto("ProductoFantasma", 10.0)
    
    # Act & Assert
    with pytest.raises(ValueError) as e:
        # Intentamos actualizar algo que no agregamos
        c.actualizar_cantidad(prod_fantasma, 1)
    
    # El SUT actual dice: "Producto no encontrado en el carrito"
    # Nosotros queremos que diga: "Producto 'ProductoFantasma' no encontrado..."
    assert "ProductoFantasma" in str(e.value)
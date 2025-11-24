from src.carrito import Carrito, Producto

def test_invariante_agregar_remover_y_actualizar():
    # Arrange
    c = Carrito()
    prod = Producto("x", 5.0)
    
    # --- ESCENARIO 1: Agregar N y Remover N ---
    c.agregar_producto(prod, 3)
    t1 = c.calcular_total()
    assert t1 == 15.0 # Sanity check (3 * 5)
    
    # Act 1: Remover la misma cantidad N (3)
    c.remover_producto(prod, 3) 
    
    # Assert 1: Debe volver a 0 (Invariante cumplido)
    assert c.calcular_total() == 0.0
    assert len(c.items) == 0

    # --- ESCENARIO 2: Agregar N y Actualizar a 0 ---
    c.agregar_producto(prod, 3) # Agregamos de nuevo
    
    # Act 2: Actualizar cantidad a 0
    c.actualizar_cantidad(prod, 0)
    
    # Assert 2: Debe ser equivalente a haber removido todo
    assert c.calcular_total() == 0.0
    assert len(c.items) == 0
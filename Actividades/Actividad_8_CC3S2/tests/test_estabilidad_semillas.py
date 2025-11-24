# tests/test_estabilidad_semillas.py
import random
from faker import Faker
from src.factories import ProductoFactory
from src.carrito import Carrito, ItemCarrito, Producto

def test_estabilidad_semillas(capsys):
    # 1- corrida
    random.seed(123)
    Faker.seed(123)
    p = ProductoFactory()
    c = Carrito()
    c.agregar_producto((Producto(p.nombre, p.precio)), 2)
    print(c.calcular_total())
    out1 = capsys.readouterr().out
    
    # Desactivamos capsys momentáneamente para imprimir en la consola REAL
    with capsys.disabled():
        print(f"\nSalida Corrida 1: {out1.strip()}")

    # 2- corrida (mismas semillas)
    random.seed(123)
    Faker.seed(123)
    p2 = ProductoFactory()
    c2 = Carrito()
    c2.agregar_producto((Producto(p2.nombre, p2.precio)), 2)
    print(c2.calcular_total())
    out2 = capsys.readouterr().out
    
    with capsys.disabled():
        print(f"Salida Corrida 2: {out2.strip()}")

    assert out1 == out2
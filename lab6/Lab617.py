def mi_generador():
    yield 1
    yield 2
    yield 3

for valor in mi_generador():
    print(valor)
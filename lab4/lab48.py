# Contador
palabras = ["manzana", "pera", "manzana", "uva", "pera", "manzana"]
contador = {}
for p in palabras:
    contador[p] = contador.get(p, 0) + 1
print(contador)
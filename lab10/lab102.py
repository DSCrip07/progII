# Leer las primeras dos líneas
with open("archivo_demo.txt") as f:
    print(f.readline())
    print(f.readline())

# Recorrer todo el archivo línea por línea
with open("archivo_demo.txt") as f:
    for x in f:
        print(x)
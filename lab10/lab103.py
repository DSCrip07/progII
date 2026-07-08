# Agregar contenido al final del archivo
with open("archivo_demo.txt", "a") as f:
    f.write("\n¡Ahora el archivo tiene más contenido!")

# Leer el archivo después de agregar
with open("archivo_demo.txt") as f:
    print(f.read())

# Sobrescribir todo el contenido
with open("archivo_demo.txt", "w") as f:
    f.write("¡Ups! ¡He borrado el contenido!")

# Leer el archivo después de sobrescribir
with open("archivo_demo.txt") as f:
    print(f.read())
# Aplicación: provincias y comarcas (tupla inmutable)
provincias_comarcas = ("Panamá", "Colón", "Chiriquí", "Darién")
# provincias_comarcas[0] = "Veraguas"  # Esto daría error porque es tupla
print("Provincias y Comarcas:")
for lugar in provincias_comarcas:
    print(f"- {lugar}")
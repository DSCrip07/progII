# Tupla con provincias y comarcas de Panamá (inmutable y ordenada)
provincias = (
    "Panamá",
    "Colón", 
    "Chiriquí",
    "Darién",
    "Herrera",
    "Los Santos",
    "Veraguas",
    "Coclé",
    "Bocas del Toro",
    "Comarca Guna Yala",
    "Comarca Emberá-Wounaan",
    "Comarca Ngäbe-Buglé"
)

print("=== PROVINCIAS Y COMARCAS DE PANAMÁ ===")
for i in range(len(provincias)):
    print(f"{i+1}. {provincias[i]}")
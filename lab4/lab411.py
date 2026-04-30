# Clave de diccionario
permisos_fijos = frozenset({"leer", "escribir"})
usuario = {
    "nombre": "Juan",
    "permisos": permisos_fijos
}
print(usuario["permisos"])
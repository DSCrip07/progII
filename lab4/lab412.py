# Permisos fijos
permisos_base = frozenset(["ver", "editar", "eliminar"])
nuevo_permiso = permisos_base.union(["crear"])  # Esto dará error
print(nuevo_permiso)
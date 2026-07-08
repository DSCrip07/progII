# =====================================================================
# Proyecto # 2 - Programacion II - Prof. Regis Rivera
# [Conjunto B - Autenticacion Segura]
# Tema: API Gateway con Autenticacion Segura
# =====================================================================

from flask import Flask, request, jsonify
# from flask import ...           -> traemos piezas de la libreria Flask
# Flask                            -> clase que se usa para crear el servidor
# request                          -> objeto que contiene lo que el cliente nos manda (JSON, headers, etc.)
# jsonify                          -> funcion que convierte un diccionario de Python en una respuesta JSON

import bcrypt
# import bcrypt                    -> libreria para encriptar (hashear) claves - Primer Grupo

import jwt
# import jwt                       -> libreria PyJWT para crear y validar tokens - Segundo Grupo

import datetime
# import datetime                  -> para calcular la fecha/hora de expiracion del token

import os
# import os                        -> para leer variables de entorno del sistema operativo

from dotenv import load_dotenv
# from dotenv import load_dotenv   -> funcion que lee el archivo .env y carga su contenido

from functools import wraps
# from functools import wraps      -> evita que un decorador "esconda" el nombre real de la funcion que envuelve


load_dotenv()
# load_dotenv()                    -> se ejecuta la funcion: lee .env y mete sus variables a os.environ

SECRET_KEY = os.getenv("SECRET_KEY")
# SECRET_KEY = ...                 -> creamos una variable de Python
# os.getenv("SECRET_KEY")          -> busca la variable llamada SECRET_KEY que .env acaba de cargar

if not SECRET_KEY:
    # if not SECRET_KEY:           -> si SECRET_KEY quedo vacia o no existe...
    raise ValueError("No se encontro SECRET_KEY. Crea un archivo .env con SECRET_KEY=tu_clave_secreta")
    # raise ValueError(...)        -> detiene el programa con un mensaje de error, en vez de correr inseguro


app = Flask(__name__)
# app = Flask(__name__)            -> crea el objeto principal del servidor
# __name__                          -> variable especial de Python con el nombre del archivo actual

usuarios_db = {}
# usuarios_db = {}                 -> diccionario vacio que actua como "base de datos" ficticia en memoria
# se va a ver asi: usuarios_db["ana"] = {"clave_hash": b"$2b$12$....."}


# =====================================================================
# PRIMER GRUPO: REGISTRO Y LOGIN CON BCRYPT
# =====================================================================

@app.route("/registro", methods=["POST"])
# @app.route(...)                  -> decorador: registra esta funcion como la que atiende esa URL
# "/registro"                       -> la direccion que el cliente debe visitar
# methods=["POST"]                  -> solo acepta peticiones tipo POST (enviar datos nuevos)
def registro():
    # def registro():               -> funcion que se ejecuta cuando alguien visita /registro

    datos = request.get_json()
    # datos = request.get_json()   -> lee el cuerpo JSON que mando el cliente y lo convierte en diccionario

    if not datos or "username" not in datos or "clave" not in datos:
        # if not datos ...          -> si no vino nada, o falta username, o falta clave...
        return jsonify({"error": "Se necesita username y clave"}), 400
        # return jsonify(...), 400 -> responde con un error y el codigo HTTP 400 (peticion mal hecha)

    username = datos["username"]
    # username = datos["username"] -> saca el valor de username del diccionario recibido
    clave = datos["clave"]
    # clave = datos["clave"]       -> saca el valor de clave del diccionario recibido

    if username in usuarios_db:
        # if username in usuarios_db: -> revisa si ese username ya existe como llave del diccionario
        return jsonify({"error": "El usuario ya existe"}), 409
        # 409                       -> codigo HTTP que significa "conflicto" (recurso duplicado)

    sal = bcrypt.gensalt()
    # sal = bcrypt.gensalt()       -> genera una cadena aleatoria distinta cada vez (la "sal")

    clave_hash = bcrypt.hashpw(clave.encode("utf-8"), sal)
    # clave.encode("utf-8")        -> convierte el texto de la clave a bytes (bcrypt trabaja con bytes)
    # bcrypt.hashpw(..., sal)      -> mezcla la clave con la sal y produce un hash de un solo sentido

    usuarios_db[username] = {"clave_hash": clave_hash}
    # usuarios_db[username] = ...  -> guarda en el diccionario SOLO el hash, nunca la clave original

    return jsonify({"mensaje": f"Usuario {username} registrado correctamente"}), 201
    # 201                          -> codigo HTTP que significa "creado correctamente"


@app.route("/login", methods=["POST"])
# igual que arriba, pero para la ruta /login
def login():
    datos = request.get_json()
    # lee el JSON que manda el cliente

    if not datos or "username" not in datos or "clave" not in datos:
        return jsonify({"error": "Se necesita username y clave"}), 400
        # misma validacion que en /registro

    username = datos["username"]
    clave = datos["clave"]
    # saca los dos valores del diccionario recibido

    usuario = usuarios_db.get(username)
    # usuarios_db.get(username)    -> busca el username; si no existe, regresa None (no da error)

    if not usuario:
        # if not usuario:          -> si no encontro a ese usuario...
        return jsonify({"error": "Usuario o clave incorrectos"}), 401
        # el mensaje es generico a proposito, para no darle pistas a un atacante

    if not bcrypt.checkpw(clave.encode("utf-8"), usuario["clave_hash"]):
        # bcrypt.checkpw(clave, hash_guardado) -> compara de forma segura si la clave nueva coincide con el hash
        return jsonify({"error": "Usuario o clave incorrectos"}), 401
        # si no coincide, mismo error generico de arriba

    payload = {
        "username": username,
        # payload                  -> diccionario con la informacion que va DENTRO del token
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        # "exp"                    -> fecha de expiracion: ahora mismo + 1 hora
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # jwt.encode(payload, clave, algoritmo) -> firma el payload y produce el token como texto

    return jsonify({"mensaje": "Login exitoso", "token": token}), 200
    # 200                          -> codigo HTTP que significa "todo salio bien"


# =====================================================================
# SEGUNDO GRUPO: PROTECCION DE RUTAS CON JWT
# =====================================================================

def token_requerido(funcion):
    # def token_requerido(funcion): -> esta funcion recibe OTRA funcion (la ruta que queremos proteger)

    @wraps(funcion)
    # @wraps(funcion)              -> conserva el nombre original de "funcion" para que Flask no se confunda
    def envoltura(*args, **kwargs):
        # def envoltura(...):      -> esta es la nueva version "envuelta" que reemplaza a la ruta original
        # *args, **kwargs           -> permite recibir cualquier cantidad de argumentos, sin importar cuales

        token = None
        # token = None             -> empezamos asumiendo que no hay token

        if "Authorization" in request.headers:
            # request.headers      -> diccionario con los encabezados que mando el cliente
            auth_header = request.headers["Authorization"]
            # auth_header           -> texto tipo "Bearer eyJhbGc..."
            partes = auth_header.split(" ")
            # .split(" ")           -> separa el texto en una lista usando el espacio: ["Bearer", "eyJhbGc..."]
            if len(partes) == 2 and partes[0] == "Bearer":
                # revisa que la lista tenga 2 partes y que la primera diga literalmente "Bearer"
                token = partes[1]
                # token = partes[1] -> guarda solo el token (la segunda parte)

        if not token:
            # if not token:        -> si despues de todo eso seguimos sin token...
            return jsonify({"error": "Falta el token"}), 401
            # 401                  -> codigo HTTP "no autorizado"

        try:
            # try:                 -> intenta lo siguiente y captura errores especificos si fallan
            datos_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # jwt.decode(...)      -> revisa la firma del token con la clave secreta y lo convierte de vuelta a diccionario
        except jwt.ExpiredSignatureError:
            # se ejecuta SOLO si el token ya vencio
            return jsonify({"error": "El token ha expirado"}), 401
        except jwt.InvalidTokenError:
            # se ejecuta SOLO si el token esta mal formado o la firma no coincide
            return jsonify({"error": "Token invalido"}), 401

        return funcion(datos_token["username"], *args, **kwargs)
        # llama a la ruta ORIGINAL (la protegida), pasandole el username que veniamos dentro del token

    return envoltura
    # regresa la version "envuelta" para que Flask la use en lugar de la funcion original


@app.route("/perfil", methods=["GET"])
# ruta privada, solo permite GET (pedir informacion, no mandar nada)
@token_requerido
# aplica la proteccion que acabamos de definir arriba, ANTES de que la funcion real se ejecute
def perfil(username_actual):
    # username_actual              -> nos llega desde el decorador (el username que estaba dentro del token)

    usuario = usuarios_db.get(username_actual)
    # busca si ese usuario sigue existiendo en la "base de datos"

    return jsonify({
        "mensaje": f"Bienvenido {username_actual}, esta es una ruta privada",
        "usuario_existe": usuario is not None
        # usuario is not None      -> True si lo encontro, False si no
    }), 200

# --- Punto de entrada del programa ---
if __name__ == "__main__":
    # if __name__ == "__main__":   -> solo se ejecuta si este archivo se corre directamente (no si se importa)
    app.run(debug=True)
    # app.run(debug=True)          -> enciende el servidor; debug=True solo para desarrollo (bandit lo marca como riesgo)
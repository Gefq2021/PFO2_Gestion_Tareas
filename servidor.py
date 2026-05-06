from flask import Flask, request, jsonify, render_template
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializamos la aplicación Flask indicando carpetas de templates y static
app = Flask(__name__, template_folder="templates", static_folder="static")
DB_PATH = os.path.join("database", "tareas.db")

# Función para crear la base de datos y la tabla de usuarios si no existen
def inicializar_bd():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Inicializamos la BD al arrancar el servidor
inicializar_bd()

# Endpoint para registrar usuarios
@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()
    usuario, contrasena = datos.get("usuario"), datos.get("contraseña")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "El usuario ya existe"}), 400

    # Guardamos la contraseña hasheada
    hash_contrasena = generate_password_hash(contrasena)
    cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, hash_contrasena))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Usuario registrado con éxito"}), 201

# Endpoint para login de usuarios
@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    usuario, contrasena = datos.get("usuario"), datos.get("contraseña")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario=?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    # Verificamos la contraseña hasheada
    if resultado and check_password_hash(resultado[0], contrasena):
        return jsonify({"mensaje": "Login exitoso"}), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

# Endpoint que devuelve la página HTML de bienvenida
@app.route("/tareas", methods=["GET"])
def tareas():
    return render_template("bienvenida.html"), 200

# Punto de entrada principal
if __name__ == "__main__":
    app.run(debug=True)

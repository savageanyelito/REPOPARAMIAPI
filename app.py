import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = sqlite3.connect('usuarios.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    contraseña_hash TEXT NOT NULL
)
''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def agregar_usuario(nombre, contraseña):
    contraseña_hash = hash_password(contraseña)
    cursor.execute('INSERT INTO usuarios (nombre, contraseña_hash) VALUES (?, ?)', (nombre, contraseña_hash))
    conn.commit()

integrantes = [
    ('Pablo Estrada', 'exament1'),
    ('Rafael Orellana', 'exament2')
]

for integrante in integrantes:
    agregar_usuario(*integrante)

@app.route('/')
def home():
    return "API EXAMEN", 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    nombre = data['nombre']
    contraseña = data['contraseña']
    cursor.execute('SELECT contraseña_hash FROM usuarios WHERE nombre = ?', (nombre,))
    result = cursor.fetchone()
    if result and result[0] == hash_password(contraseña):
        return jsonify({"message": "Login exitoso"}), 200
    return jsonify({"message": "Usuario o contrasena incorrectos"}), 401

if __name__ == '__main__':
    app.run(port=5800)
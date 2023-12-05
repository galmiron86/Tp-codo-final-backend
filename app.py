"""La línea de comando:
pip install Flask SQLAlchemy mysql-connector-python

se utiliza para instalar
tres paquetes en tu entorno de Python.
Aquí está una breve descripción de cada uno de ellos:

Flask: Flask es un framework ligero de desarrollo
web para Python. Facilita la creación de aplicaciones
web de manera rápida y sencilla. Con Flask, puedes
definir rutas, gestionar solicitudes HTTP, y construir
aplicaciones web de manera eficiente.

SQLAlchemy: SQLAlchemy es una biblioteca de
SQL en Python que proporciona un conjunto
de herramientas de alto nivel para interactuar
con bases de datos relacionales. Facilita la
creación, el acceso y la manipulación de bases
de datos utilizando objetos Python en lugar de escribir directamente SQL.

mysql-connector-python: Este paquete es un conector oficial
de MySQL para Python. Permite a tu aplicación Python conectarse y
comunicarse con una base de datos MySQL. En el contexto de Flask
y SQLAlchemy, se utiliza para establecer la conexión entre tu
aplicación y la base de datos MySQL ."""

# 3. Importar las herramientas
# Acceder a las herramientas para crear la app web
from flask import Flask, request, jsonify

# Para manipular la DB
from flask_sqlalchemy import SQLAlchemy

# Módulo cors es para que me permita acceder desde el frontend al backend
from flask_cors import CORS

# 4. Crear la app
app = Flask(__name__)

# Habilitar a la app para recibir peticiones
CORS(app)


# 5. Configurar a la app la DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:contraseña@localhost:3306/nombre_de_la_base_de_datos'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://galmiron:Palta1986@galmiron.mysql.pythonanywhere-services.com/galmiron$default'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 6. Crear un objeto db, para informar a la app que se trabajará con sqlalchemy
db = SQLAlchemy(app)

# 7. Definir la tabla
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))

# 8. Crear la tabla al ejecutarse la app
with app.app_context():
    db.create_all()

# Crear ruta de acceso
# / es la ruta de inicio
@app.route("/")
def index():
    return f'App Web para registrar nombres de personas'

# Recibir los datos que vienen del formulario
# para insertarlos en la DB
@app.route("/registro", methods=['POST'])
def registro():
    #      <input type="text" name="nombre" id="nombre">
    # {
    #   "nombre": "Luis"
    # }
    nombre_recibido = request.json["nombre"]

    # ¿Cómo insertar el registro en la tabla?
    nuevo_registro = Persona(nombre=nombre_recibido)
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud via post recibida"


# Retornar todos los registros de la tabla persona, en un Json
@app.route("/personas",  methods=['GET'])
def personas():
    # Consultar la tabla persona y traer todos los registros
    # all_registros -> lista de objetos
    all_registros = Persona.query.all()

    data_serializada = [] # Lista de diccionarios
    for registro in all_registros:
        data_serializada.append({"id":registro.id, "nombre":registro.nombre})

    # transformar a json
    return jsonify(data_serializada)


# Modificar un registro
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    # Buscar el registro por el id
    update_persona = Persona.query.get(id)

    # Recibir los nuevos datos a guardar
    nombre = request.json["nombre"]

    # Sobreescribir la info
    update_persona.nombre = nombre
    db.session.commit()

    data_serializada = [{"id": update_persona.id, "nombre": update_persona.nombre}]
    return jsonify(data_serializada)


# Eliminar una persona de la tabla persona por id
@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):
    # Buscar el registro por el id
    delete_persona = Persona.query.get(id)

    db.session.delete(delete_persona)
    db.session.commit()

    data_serializada = [{"id": delete_persona.id, "nombre": delete_persona.nombre}]
    return jsonify(data_serializada)


if __name__ == "__main__":
    app.run(debug=True)


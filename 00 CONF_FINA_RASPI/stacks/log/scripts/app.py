from flask import Flask, jsonify, request
import mysql.connector
import requests
import logging
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
from datetime import datetime
# Conexión a la base de datos
database = mysql.connector.connect(
    host='192.168.1.11',
    user='admin',
    password='departamento',
    database='log'
)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/log', methods=['POST'])
def log():
    content = request.json
    if content and 'message' in content:
        app.logger.info(content['message'])  # Usar app.logger.info() para registrar el mensaje
        cursor = database.cursor()
        message = content['message']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtener la marca de tiempo actual
        cursor.execute("INSERT INTO repos (texto, timestamp) VALUES (%s, %s)", (message, timestamp))
        database.commit()  # Confirmar los cambios en la base de datos
        cursor.close()
        return jsonify({"status": "success", "message": "Log received"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/data', methods=['GET'])
def get_data():
    cursor = database.cursor()
    cursor.execute("SELECT * FROM repos")
    myresult = cursor.fetchall()
    cursor.close()

    # Convertir los resultados a una lista de diccionarios
    column_names = [i[0] for i in cursor.description]
    data = [dict(zip(column_names, row)) for row in myresult]

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

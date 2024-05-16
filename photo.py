import cv2
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

class CameraCapture:
    def __init__(self):
        self.capture = None

    def take_photo(self):
        # Obtener la fecha y hora actual para cada captura
        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y%m%d_%H%M")
        nombre = f"{fecha_actual}.jpg"

        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Error: No se puede abrir la cámara")
            return False

        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite(nombre, frame)
            print(f"Foto tomada y guardada como {nombre}")
            return True
        else:
            print("Error: No se pudo capturar la foto")
            return False

capture = CameraCapture()

@app.route('/take_photo', methods=['GET'])
def take_photo():
    if capture.take_photo():
        return jsonify(success=True, message="Foto tomada correctamente.")
    else:
        return jsonify(success=False, message="Error al tomar la foto.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008)




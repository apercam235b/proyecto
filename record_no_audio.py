import cv2
from flask import Flask, request, jsonify
import datetime
import threading

app = Flask(__name__)

class CameraCapture:
    def __init__(self):
        self.capture = None
        self.is_recording = False
        self.out = None
        self.record_thread = None

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
            self.capture.release()
            return True
        else:
            print("Error: No se pudo capturar la foto")
            self.capture.release()
            return False

    def start_video(self):
        if self.is_recording:
            print("Ya está grabando")
            return False

        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Error: No se puede abrir la cámara")
            return False

        now = datetime.datetime.now()
        fecha_actual = now.strftime("%Y%m%d_%H%M")
        nombre_video = f"{fecha_actual}.avi"

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        frame_size = (int(self.capture.get(3)), int(self.capture.get(4)))
        self.out = cv2.VideoWriter(nombre_video, fourcc, fps, frame_size)

        self.is_recording = True
        self.record_thread = threading.Thread(target=self.record_video)
        self.record_thread.start()
        print(f"Grabación de video iniciada como {nombre_video}")
        return True

    def record_video(self):
        while self.is_recording:
            ret, frame = self.capture.read()
            if ret:
                self.out.write(frame)
            else:
                break

    def stop_video(self):
        if not self.is_recording:
            print("No está grabando")
            return False

        self.is_recording = False
        self.record_thread.join()
        self.capture.release()
        self.out.release()
        print("Grabación de video detenida")
        return True

capture = CameraCapture()

@app.route('/take_photo', methods=['GET'])
def take_photo():
    if capture.take_photo():
        return jsonify(success=True, message="Foto tomada correctamente.")
    else:
        return jsonify(success=False, message="Error al tomar la foto.")

@app.route('/start_video', methods=['GET'])
def start_video():
    if capture.start_video():
        return jsonify(success=True, message="Grabación de video iniciada.")
    else:
        return jsonify(success=False, message="Error al iniciar la grabación de video.")

@app.route('/stop_video', methods=['GET'])
def stop_video():
    if capture.stop_video():
        return jsonify(success=True, message="Grabación de video detenida.")
    else:
        return jsonify(success=False, message="Error al detener la grabación de video.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5008)

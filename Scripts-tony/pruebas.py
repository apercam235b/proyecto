import cv2
import datetime
from time import sleep

class VideoRecorder:
    def __init__(self):
        self.cap = None
        self.output = None
        self.recording = False

    def iniciar_grabacion(self):
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.output = cv2.VideoWriter(f"video_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4", fourcc, 20.0, (640, 480))
        self.recording = True
        print("Grabación iniciada")
        self.record()

    def captura_camara(self):
        ret, frame = self.cap.read()
        if ret:
            now = datetime.datetime.now()
            fecha_hora = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f'foto_{fecha_hora}.png'
            cv2.imwrite(filename, frame)
            print(f'Imagen guardada: {filename}')
        else:
            print("Error: No se puede recibir el cuadro (stream end?). Saliendo ...")
        
        self.cap.release()

    def parar_grabacion(self):
        self.recording = False
        self.cap.release()
        self.output.release()
        cv2.destroyAllWindows()
        print("Grabación finalizada")

    def record(self):
        start_time = datetime.datetime.now()
        while self.recording:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se puede recibir el cuadro (stream end?)")
                break
            self.output.write(frame)
            current_time = datetime.datetime.now()
            elapsed_time = (current_time - start_time).total_seconds()
            if elapsed_time >= 7:
                break

if __name__ == "__main__":
    recorder = VideoRecorder()
    recorder.iniciar_grabacion()
    sleep(3)  # Espera 3 segundos antes de capturar
    recorder.captura_camara()
    recorder.parar_grabacion()


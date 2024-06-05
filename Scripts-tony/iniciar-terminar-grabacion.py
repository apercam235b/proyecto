import cv2
import datetime

class VideoRecorder:

    def __init__(self):
        self.cap = None
        self.output = None
        self.recording = False

    def iniciar_grabacion(self):
        self.cap = cv2.VideoCapture(0)
        # Configurar la captura de audio si está disponible
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.output = cv2.VideoWriter(f"video_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4", fourcc, 20.0, (640, 480))
        self.recording = True
        print("Grabación iniciada")

    def parar_grabacion(self):
        self.recording = False
        self.cap.release()
        self.output.release()
        cv2.destroyAllWindows()
        print("Grabación finalizada")

    def record(self):
        while self.recording:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se puede recibir el cuadro (stream end?)")
                break
            # Escribir el frame en el archivo de salida
            self.output.write(frame)

if __name__ == "__main__":
    recorder = VideoRecorder()
    recorder.iniciar_grabacion()
    recorder.record()
    # Grabar durante 10 segundos (puedes ajustar este valor según tus necesidades)
    cv2.waitKey(10000)
    recorder.parar_grabacion()

import cv2
import datetime
import sounddevice as sd
import numpy as np

class VideoRecorder:

    def __init__(self):
        self.cap = None
        self.output = None
        self.audio_stream = None
        self.recording = False

    def iniciar_grabacion(self):
        self.cap = cv2.VideoCapture(0)
        # Configurar la captura de audio si está disponible
        self.audio_samplerate = 44100
        self.audio_channels = 2
        self.audio_frames_per_buffer = 1024
        self.audio_stream = sd.InputStream(samplerate=self.audio_samplerate, channels=self.audio_channels, callback=self.audio_callback)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.output = cv2.VideoWriter(f"video_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4", fourcc, 20.0, (640, 480))
        self.recording = True
        self.audio_stream.start()
        print("Grabación iniciada")

        # Grabar video y audio
        while self.recording:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: No se puede recibir el cuadro (stream end?)")
                break
            # Escribir el frame en el archivo de salida
            self.output.write(frame)

    def parar_grabacion(self):
        self.recording = False
        self.cap.release()
        self.output.release()
        self.audio_stream.stop()
        cv2.destroyAllWindows()
        print("Grabación finalizada")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        # Convertir los datos de audio a un formato adecuado para OpenCV
        audio_data = np.array(indata).astype(np.uint8)
        # Escribir los datos de audio en el archivo de salida
        self.output.write(audio_data)

if __name__ == "__main__":
    recorder = VideoRecorder()
    recorder.iniciar_grabacion()
    recorder.audio_callback()
    # Grabar durante 10 segundos (puedes ajustar este valor según tus necesidades)
    cv2.waitKey(5000)
    recorder.parar_grabacion()

import cv2
from flask import Flask, request, jsonify
import datetime
import threading
import pyaudio
import wave
import os
import subprocess

app = Flask(__name__)

class CameraCapture:
    def __init__(self):
        self.capture = None
        self.is_recording = False
        self.out = None
        self.record_thread = None
        self.audio_thread = None
        self.audio_frames = []
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024

    def take_photo(self):
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

    def start_audio(self):
        self.audio_frames = []
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.audio_format, channels=self.channels,
                                  rate=self.rate, input=True, frames_per_buffer=self.chunk)

        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.audio_frames.append(data)

    def stop_audio(self, audio_filename):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(audio_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.audio_format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.audio_frames))
        wf.close()

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
        self.video_filename = f"{fecha_actual}.avi"
        self.audio_filename = f"{fecha_actual}.wav"
        self.output_filename = f"{fecha_actual}_output.avi"

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        frame_size = (int(self.capture.get(3)), int(self.capture.get(4)))
        self.out = cv2.VideoWriter(self.video_filename, fourcc, fps, frame_size)

        self.is_recording = True
        self.record_thread = threading.Thread(target=self.record_video)
        self.audio_thread = threading.Thread(target=self.start_audio)
        self.record_thread.start()
        self.audio_thread.start()
        print(f"Grabación de video iniciada como {self.video_filename}")
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
        self.audio_thread.join()
        self.capture.release()
        self.out.release()
        self.stop_audio(self.audio_filename)

        # Combine video and audio using ffmpeg
        command = f"ffmpeg -i {self.video_filename} -i {self.audio_filename} -c:v copy -c:a aac {self.output_filename}"
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Grabación de video detenida y guardada como {self.output_filename}")

            # Clean up temporary files
            os.remove(self.video_filename)
            os.remove(self.audio_filename)
        except subprocess.CalledProcessError as e:
            print("Error durante la combinación de video y audio:", e)

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

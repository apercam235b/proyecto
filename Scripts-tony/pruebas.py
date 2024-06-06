from flask import Flask, render_template, request
import cv2
import pyaudio
import wave
import threading

app = Flask(__name__)

video_thread = None
audio_thread = None
cap = None
out = None
p = None
frames = []

def capturar_video():
    global cap, out
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()

def capturar_audio():
    global p, frames
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 10

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording')
def start_recording():
    global video_thread, audio_thread
    video_thread = threading.Thread(target=capturar_video)
    audio_thread = threading.Thread(target=capturar_audio)
    video_thread.start()
    audio_thread.start()
    return 'Recording started'

@app.route('/stop_recording')
def stop_recording():
    global cap, out, p, frames
    if cap is not None:
        cap.release()
    if out is not None:
        out.release()
    if p is not None:
        p.terminate()
    frames = []
    return 'Recording stopped'

if __name__ == '__main__':
    app.run(debug=True)

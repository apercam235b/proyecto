import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3
import threading

def capture_rectangle(frame, approx):
    x, y, w, h = cv2.boundingRect(approx)
    rect_img = frame[y:y+h, x:x+w]
    return rect_img

def recognize_speech(recognizer, microphone, command_queue):
    while True:
        with microphone as source:
            print("Escuchando...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            print(f"Comando recibido: {text}")
            command_queue.append(text.lower())
        except sr.UnknownValueError:
            print("No se entendió el comando")
        except sr.RequestError:
            print("Error al comunicarse con el servicio de reconocimiento de voz")

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara")
        return

    engine = pyttsx3.init()
   # engine.say("Programa iniciado. Diga 'capturar' para guardar la imagen o 'cerrar programa' para salir.")
    engine.runAndWait()

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    command_queue = []

    # Iniciar el hilo para el reconocimiento de voz
    voice_thread = threading.Thread(target=recognize_speech, args=(recognizer, microphone, command_queue))
    voice_thread.daemon = True
    voice_thread.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede recibir el cuadro (stream end?). Saliendo ...")
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                rect_img = capture_rectangle(frame, approx)
                rects.append(rect_img)
        
        cv2.imshow('Rectangles Detection', frame)
        
        if command_queue:
            command = command_queue.pop(0)
            if command == "capturar" and rects:
                for i, rect_img in enumerate(rects):
                    filename = f'rectangle_{i}.png'
                    cv2.imwrite(filename, rect_img)
                    print(f'Imagen guardada: {filename}')
                    engine.say(f'Imagen guardada: {filename}')
                    engine.runAndWait()
            elif command == "cerrar programa":
                print("Cerrando programa...")
                engine.say("Cerrando programa")
                engine.runAndWait()
                break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

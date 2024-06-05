import cv2
import numpy as np
from datetime import datetime
import time

def capture_rectangle(frame, approx):
    x, y, w, h = cv2.boundingRect(approx)
    rect_img = frame[y:y+h, x:x+w]
    return rect_img

def process_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara")
        return

    capture_command = False
    while not capture_command:
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

        start_time = time.time()
        while time.time() - start_time < 5:
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                if len(approx) == 4:
                    rect_img = capture_rectangle(frame, approx)
                    rects.append(rect_img)
                    capture_command = True  # Activar comando de captura
                    break
            if capture_command:
                break

    for i, rect_img in enumerate(rects):
        now = datetime.now()
        fecha_hora = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'captura_{fecha_hora}.png'
        cv2.imwrite(filename, rect_img)
        print(f'Imagen guardada: {filename}')

    cap.release()

if __name__ == "__main__":
    process_video()

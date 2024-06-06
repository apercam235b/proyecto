import cv2
import sys
import os
sys.path.append(os.path.abspath('PaddleOCR'))
from paddleocr import PaddleOCR
from datetime import datetime

# Configuración de PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='es')

def extract_text_from_image(image):
    # Realizar OCR en la imagen
    result = ocr.ocr(image, cls=True)

    # Obtener texto de los resultados de OCR
    text = ''
    for line in result:
        for word in line:
            # Acceder al texto de la palabra y agregarlo al texto completo
            text += word[1][0] + ' '  # La palabra se encuentra en el primer elemento de la tupla
        text += '\n'

    return text



def capture_and_extract_text():
    # Capturar imagen desde la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede recibir el cuadro (stream end?)")
        cap.release()
        return

    # Extraer texto de la imagen
    text = extract_text_from_image(frame)

    # Guardar el texto en un archivo
    now = datetime.now()
    fecha_hora = now.strftime("%Y-%m-%d_%H-%M-%S")
    with open(f'texto_{fecha_hora}.txt', 'w') as f:
        f.write(text)

    print("Texto extraído y guardado correctamente.")

    cap.release()

if __name__ == "__main__":
    capture_and_extract_text()
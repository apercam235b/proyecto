import cv2
from datetime import datetime
import time
import argparse

def captura_camara(ruta):
    cap = cv2.VideoCapture(0)  # 0 indica la cámara predeterminada
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara")
        return

    # Esperar 2 segundos para permitir que la cámara se enfoque
    time.sleep(2)

    ret, frame = cap.read()
    if ret:
        now = datetime.now()
        fecha_hora = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'{ruta}/foto_{fecha_hora}.png'
        cv2.imwrite(filename, frame)
        print(f'Imagen guardada: {filename}')
    else:
        print("Error: No se puede recibir el cuadro (stream end?). Saliendo ...")
    
    cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Captura una imagen de la cámara y la guarda en la ruta especificada.")
    parser.add_argument("ruta", type=str, help="Ruta donde se guardará la imagen.")
    args = parser.parse_args()
    captura_camara(args.ruta)



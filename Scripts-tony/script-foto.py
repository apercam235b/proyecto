import cv2
from datetime import datetime

def captura_camara():
    cap = cv2.VideoCapture(0)  # 0 indica la cámara predeterminada
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara")
        return

    ret, frame = cap.read()
    if ret:
        now = datetime.now()
        fecha_hora = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'foto_{fecha_hora}.png'
        cv2.imwrite(filename, frame)
        print(f'Imagen guardada: {filename}')
    else:
        print("Error: No se puede recibir el cuadro (stream end?). Saliendo ...")
    
    cap.release()

if __name__ == "__main__":
    captura_camara()

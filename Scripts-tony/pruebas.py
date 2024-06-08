import cv2
import sys
import os
import time
from datetime import datetime

def main(output_dir):
    # Verifica si la ruta de salida existe, si no, crea el directorio
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Obtiene la fecha y hora actuales y las formatea para el nombre del archivo
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = os.path.join(output_dir, f"video_{now}.avi")
    
    # Inicializa la captura de video desde la cámara (0 es el índice de la cámara por defecto)
    cap = cv2.VideoCapture(0)
    
    # Define el codec y crea el objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))
    
    print("Grabando video. Ejecuta el comando de detener para parar la grabación.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede acceder a la cámara.")
            break
        
        out.write(frame)
        
        # Verifica si el archivo de señal existe
        if os.path.exists("stop_signal.txt"):
            print("Señal de detener recibida.")
            os.remove("stop_signal.txt")  # Elimina el archivo de señal
            break
    
    # Libera todo
    cap.release()
    out.release()
    print(f"Video guardado en: {video_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 <nombre_del_script.py> <ruta_de_salida> o python3 <nombre_del_script.py> parar")
    elif sys.argv[1] == "parar":
        # Crea un archivo de señal para detener la grabación
        with open("stop_signal.txt", "w") as f:
            f.write("stop")
        print("Señal de detener enviada.")
    else:
        output_dir = sys.argv[1]
        # Elimina el archivo de señal si existe antes de empezar la grabación
        if os.path.exists("stop_signal.txt"):
            os.remove("stop_signal.txt")
        main(output_dir)


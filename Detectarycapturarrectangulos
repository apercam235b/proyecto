import cv2
import numpy as np

def capture_rectangle(frame, approx):
    # Obtener el rectángulo delimitador de los puntos aproximados
    x, y, w, h = cv2.boundingRect(approx)
    # Recortar la región del rectángulo
    rect_img = frame[y:y+h, x:x+w]
    return rect_img

def main():
    # Iniciar la captura de video desde la cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara")
        return

    while True:
        # Leer un cuadro de la cámara
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede recibir el cuadro (stream end?). Saliendo ...")
            break
        
        # Convertir la imagen a espacio de color HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Definir rango de color verde en HSV
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        
        # Crear una máscara con los píxeles dentro del rango de color verde
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Aplicar una serie de dilataciones y erosiones para eliminar cualquier pequeña mancha en la máscara
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # Encontrar contornos en la máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Lista para almacenar las imágenes recortadas de los rectángulos detectados
        rects = []
        
        # Iterar sobre cada contorno encontrado
        for contour in contours:
            # Aproximar el contorno a una forma más sencilla
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            
            # Si el contorno tiene 4 vértices, es un rectángulo (o cuadrado)
            if len(approx) == 4:
                # Dibujar el contorno (rectángulo) en la imagen original
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                # Guardar la imagen del rectángulo
                rect_img = capture_rectangle(frame, approx)
                rects.append(rect_img)
        
        # Mostrar el cuadro con los rectángulos detectados
        cv2.imshow('Rectangles Detection', frame)
        
        # Capturar la imagen del rectángulo cuando se presiona la tecla 'n'
        key = cv2.waitKey(1) & 0xFF
        if key == ord('n') and rects:
            for i, rect_img in enumerate(rects):
                filename = f'rectangle_{i}.png'
                cv2.imwrite(filename, rect_img)
                print(f'Imagen guardada: {filename}')
        
        # Salir del bucle si se presiona la tecla 'q'
        if key == ord('q'):
            break

    # Liberar la captura de video y cerrar las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

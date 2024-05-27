import cv2

# URL del stream de la ESP32-CAM
url = 'http://172.24.1.190:81/stream'

# Captura de video
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el video")
        break

    # Muestra el frame
    cv2.imshow('ESP32-CAM', frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera el recurso de captura y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()

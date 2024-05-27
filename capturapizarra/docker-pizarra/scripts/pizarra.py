from flask import Flask, request, jsonify
import cv2
import numpy as np
import threading

app = Flask(__name__)
capture_command = False
close_command = False

def capture_rectangle(frame, approx):
    x, y, w, h = cv2.boundingRect(approx)
    rect_img = frame[y:y+h, x:x+w]
    return rect_img

def process_video():
    global capture_command, close_command
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede acceder a la cámara")
        return
    
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

        if capture_command:
            for i, rect_img in enumerate(rects):
                filename = f'rectangle_{i}.png'
                cv2.imwrite(filename, rect_img)
                print(f'Imagen guardada: {filename}')
            capture_command = False
        
        cv2.imshow('Rectangles Detection', frame)
        
        if close_command or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/command', methods=['GET'])
def command():
    global capture_command, close_command
    
    action = request.args.get('action')
    if action:
        if action == 'capturar':
            capture_command = True
            return jsonify({"status": "Capturing image"})
        elif action == 'cerrar':
            close_command = True
            return jsonify({"status": "Closing program"})
        else:
            return jsonify({"status": "Unknown action"})
    else:
        return jsonify({"status": "No action provided"}), 400

if __name__ == "__main__":
    video_thread = threading.Thread(target=process_video)
    video_thread.start()
    
    app.run(host='0.0.0.0', port=5000)
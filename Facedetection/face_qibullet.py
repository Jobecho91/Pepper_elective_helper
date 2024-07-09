import cv2
import qibullet
import time
import math

def main():
    simulation_manager = qibullet.SimulationManager()
    client_id = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client_id, spawn_ground_plane=True)
    pepper.goToPosture("Stand", 0.6)

    # haarcascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            #CEnter
            center_x = x + w / 2
            center_y = y + h / 2
            image_center_x = frame.shape[1] / 2
            image_center_y = frame.shape[0] / 2

            # Calcular el angulo
            yaw = -(center_x - image_center_x) / image_center_x * 0.5
            #pitch = -(center_y - image_center_y) / image_center_y * 0.5

            pitch = (center_y - image_center_y) / image_center_y * 0.5

            pepper.setAngles(["HeadYaw", "HeadPitch"], [yaw, pitch], 0.2)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    simulation_manager.stopSimulation(client_id)

if __name__ == "__main__":
    main()

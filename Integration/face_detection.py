import cv2
from pepper_interactions import wave_hand_and_say_text, say_text
from rasa_interactions import get_rasa_response


def detect_faces_and_greet(pepper, face_cascade, cap):
    has_waved = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Calcular el centro del rostro
            center_x = x + w / 2
            center_y = y + h / 2
            image_center_x = frame.shape[1] / 2
            image_center_y = frame.shape[0] / 2

            # Calcular el ángulo para mover la cabeza de Pepper
            yaw = -(center_x - image_center_x) / image_center_x * 0.5
            pitch = (center_y - image_center_y) / image_center_y * 0.5  # Invertir el signo de pitch

            # Mover la cabeza de Pepper hacia el rostro detectado
            pepper.setAngles(["HeadYaw", "HeadPitch"], [yaw, pitch], 0.2)

            # Saludar si el rostro está en el centro de la cámara y no ha saludado aún
            if abs(center_x - image_center_x) < 50 and abs(center_y - image_center_y) < 50 and not has_waved:
                response_texts, _ = get_rasa_response("hello")
                if response_texts:
                    wave_hand_and_say_text(pepper, response_texts[0])
                    say_text(pepper, response_texts[1])
                has_waved = True

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
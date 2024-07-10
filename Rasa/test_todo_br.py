import cv2
import qibullet
import time
import math
from gtts import gTTS
from playsound import playsound
import requests
import threading

def wave_hand_and_say_text(pepper, text):
    # Mover el brazo para saludar
    pepper.setAngles("RShoulderPitch", math.radians(-90), 0.3)
    pepper.setAngles("RElbowRoll", math.radians(90), 0.3)
    pepper.setAngles("RShoulderRoll", math.radians(-90), 0.3)
    
    # Realizar el movimiento de saludo
    for _ in range(2):
        pepper.setAngles("RElbowRoll", math.radians(45), 0.3)
        time.sleep(0.3)
        pepper.setAngles("RElbowRoll", math.radians(90), 0.3)
        time.sleep(0.3)
    
    # Volver a la posición inicial
    pepper.setAngles("RShoulderPitch", math.radians(0), 0.3)
    pepper.setAngles("RElbowRoll", math.radians(0), 0.3)
    pepper.setAngles("RShoulderRoll", math.radians(0), 0.3)
    
    # Generar y reproducir el audio con el texto
    tts = gTTS(text=text, lang='en')
    audio_temp = "/tmp/temp_audio.mp3"
    tts.save(audio_temp)
    playsound(audio_temp)

def get_rasa_response(message):
    url = "http://localhost:5005/webhooks/rest/webhook"  # Cambia esto si tu servidor Rasa está en otra dirección
    payload = {"sender": "pepper", "message": message}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        messages = response.json()
        if messages:
            return messages[0].get("text")
    return "Sorry, I didn't understand that."

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
                # Obtener la respuesta de Rasa
                response_text = get_rasa_response("Hello")
                wave_hand_and_say_text(pepper, response_text)
                has_waved = True

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def conversation_loop(pepper):
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'q']:
            break
        response_text = get_rasa_response(user_input)
        print(f"Pepper: {response_text}")
        wave_hand_and_say_text(pepper, response_text)

def main():
    simulation_manager = qibullet.SimulationManager()
    client_id = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client_id, spawn_ground_plane=True)
    pepper.goToPosture("Stand", 0.6)

    # Cargar el clasificador pre-entrenado de rostros de OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Iniciar la captura de video desde la webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    # Iniciar los hilos para detección de caras y conversación
    face_thread = threading.Thread(target=detect_faces_and_greet, args=(pepper, face_cascade, cap))
    face_thread.start()

    conversation_loop(pepper)

    face_thread.join()
    simulation_manager.stopSimulation(client_id)

if __name__ == "__main__":
    main()

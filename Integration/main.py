import cv2
import qibullet
import threading
from face_detection import detect_faces_and_greet
from pepper_interactions import wave_hand_and_say_text, say_text
from rasa_interactions import get_rasa_response


def update_user_data(user_data, entities):
    for entity_list in entities:
        for entity in entity_list:
            if entity['entity'] == 'subject':
                user_data['subject'] = entity['value']
            elif entity['entity'] == 'work':
                user_data['work'] = entity['value']
            elif entity['entity'] == 'schedule':
                user_data['schedule'] = entity['value']
            elif entity['entity'] == 'semester':
                user_data['semester'] = entity['value']
    return user_data

def conversation_loop(pepper):
    user_data = {"subject": None, "work": None, "schedule": None, "semester": None}
    greeted = False
    while True:
        user_input = input("You: ").strip().lower()
        if user_input in ['exit', 'quit', 'q']:
            break
        response_texts, entities = get_rasa_response(user_input)
        print("entities:", entities)
        print(f"Response texts: {response_texts}")  # Depuración adicional
        if response_texts and isinstance(response_texts, list):
            if not greeted:
                wave_hand_and_say_text(pepper, response_texts[0])
                greeted = True
            else:
                say_text(pepper, response_texts[0])
            # Si hay más textos, se manejan individualmente con say_text
            for response_text in response_texts[1:]:
                say_text(pepper, response_text)


        # Aquí puedes hacer lo que necesites con los datos almacenados en user_data
        print(user_data)


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

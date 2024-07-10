import cv2
import qibullet
import threading
from face_detection import detect_faces_and_greet
from pepper_interactions import wave_hand_and_say_text, say_text, gesture_hand_and_say_text, say_recomend_subject
from rasa_interactions import get_rasa_response
from bayesian_nt import recommend_subjects

#Funcionalily is not workng as expected cause we can't get the first word of the response.
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

#Alternative function to update the preferences takes the first word of the response
def update_pref(user_preferences, first_word):
    #as dict
   
    
    if first_word in ["AI", "Mathematics", "Software", "Autonomous"]:
        user_preferences["subject"] = first_word
    elif first_word in ["Robotics", "Artificial"]:
        user_preferences["work"] = first_word
    elif first_word in ["morning", "afternoon"]:
        user_preferences["schedule"] = first_word
    elif first_word in ["winter", "summer"]:
        user_preferences["semester"] = first_word

    return user_preferences

def all_preferences_set(preferences):
    #verify if all values are not None
    return all(value is not None for value in preferences.values())

def conversation_loop(pepper):
    #user_data = {"subject": None, "work": None, "schedule": None, "semester": None}
    user_preferences = {"subject": None, "work": None, "schedule": None, "semester": None}
    greeted = False
    while True:
        user_input = input("You: ").strip().lower()
        if user_input in ['exit', 'quit', 'q']:
            break
        response_texts, entities = get_rasa_response(user_input)
        #print("entities:", entities)
        print(f"Response texts: {response_texts}")
        
        if response_texts and isinstance(response_texts, list):

            preferences = update_pref(user_preferences, response_texts[0].split()[0]) # ALternative function to update the preferences
            print("Preferences:", preferences)
            
            if not greeted:
                gesture_hand_and_say_text(pepper, response_texts[0])
                greeted = True
            else:
                say_text(pepper, response_texts[0])
            # Si hay más textos, se manejan individualmente con say_text
            for response_text in response_texts[1:]:
                say_text(pepper, response_text)
        
        if all_preferences_set(user_preferences):
            #recommend subjects
            subj1, sub2, sub3=recommend_subjects(user_preferences)
            say_recomend_subject(subj1, sub2, sub3)
            
            print("All preferences are set.")


            break

        #print(user_data)
    return user_preferences


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

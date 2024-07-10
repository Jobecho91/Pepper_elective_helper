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
    #
    if first_word in ["AI", "Mathematics", "Software", "Autonomous"]:
        user_preferences["subject"] = first_word
    elif first_word in ["Robotics", "Artificial"]:
        user_preferences["work"] = first_word
    elif first_word in ["morning", "afternoon"]:
        user_preferences["schedule"] = first_word
    elif first_word in ["winter", "summer"]:
        user_preferences["semester"] = first_word

    return user_preferences

#Verify if all preferences are not None
def all_preferences_set(preferences):

    return all(value is not None for value in preferences.values())

#Principal function to interact with the user
def conversation_loop(pepper):
    #user_data = {"subject": None, "work": None, "schedule": None, "semester": None} #for entitites
    user_preferences = {"subject": None, "work": None, "schedule": None, "semester": None}


    while True:
        user_input = input("You: ").strip().lower()
        if user_input in ['exit', 'quit', 'q']:
            break
        response_texts, entities = get_rasa_response(user_input) #entities are not used cause is not working as expected
        #print("entities:", entities)
        print(f"Response texts: {response_texts}")
        
        if response_texts and isinstance(response_texts, list):

            preferences = update_pref(user_preferences, response_texts[0].split()[0]) # ALternative function to update the preferences
            print("Preferences:", preferences)

            gesture_hand_and_say_text(pepper, response_texts[0])
            
            for response_text in response_texts[1:]:
                say_text(pepper, response_text)
        
        if all_preferences_set(user_preferences):
            #recommend subjects
            subj1, sub2, sub3=recommend_subjects(user_preferences)

            say_recomend_subject(subj1, sub2, sub3)
            
            print("All preferences are set.")
            break


def main():
    # Iniciate the quibulet simulation
    simulation_manager = qibullet.SimulationManager()
    client_id = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client_id, spawn_ground_plane=True)
    pepper.goToPosture("Stand", 0.6)

    # Initialize the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    #Initiate the threads for face detection and conversation    
    face_thread = threading.Thread(target=detect_faces_and_greet, args=(pepper, face_cascade, cap))
    face_thread.start()

    conversation_loop(pepper)

    face_thread.join() # Wait for the thread to finish before stopping the simulation
    simulation_manager.stopSimulation(client_id) # Stop the simulation

if __name__ == "__main__":
    main()

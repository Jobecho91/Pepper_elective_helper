import math
import time
from gtts import gTTS
from playsound import playsound
import threading

def wave_hand(pepper):
    # Mover el brazo
    pepper.setAngles("RShoulderPitch", math.radians(-90), 0.3)
    pepper.setAngles("RElbowRoll", math.radians(90), 0.3)
    pepper.setAngles("RShoulderRoll", math.radians(-90), 0.3)
    
    for _ in range(2):
        pepper.setAngles("RElbowRoll", math.radians(45), 0.3)
        time.sleep(0.3)
        pepper.setAngles("RElbowRoll", math.radians(90), 0.3)
        time.sleep(0.3)
    
    # Bajar la mano después de saludar
    pepper.setAngles("RShoulderPitch", math.radians(0), 0.3)
    pepper.setAngles("RElbowRoll", math.radians(0), 0.3)
    pepper.setAngles("RShoulderRoll", math.radians(0), 0.3)
    pepper.setAngles("RWristYaw", math.radians(0), 0.3)

def play_audio(text):
    if isinstance(text, str):  # Asegurarse de que el texto es una cadena
        tts = gTTS(text=text, lang='en')
        audio_temp = "/tmp/temp_audio.mp3"
        tts.save(audio_temp)
        playsound(audio_temp)
    else:
        print("Error: El texto no es una cadena de caracteres.")


#New functionality for moving hand naturally in a conversation
def gesture_hand(pepper):
    # Mover ambos brazos en gestos de conversación
    movements = [
        {"joint": "LShoulderPitch", "angle": -30, "duration": 0.5},
        {"joint": "LElbowYaw", "angle": -45, "duration": 0.5},
        {"joint": "LElbowRoll", "angle": -60, "duration": 0.5},
        {"joint": "LShoulderPitch", "angle": 10, "duration": 0.5},
        {"joint": "LElbowYaw", "angle": -30, "duration": 0.5},
        {"joint": "LElbowRoll", "angle": -45, "duration": 0.5},
        {"joint": "RShoulderPitch", "angle": -30, "duration": 0.5},
        {"joint": "RElbowYaw", "angle": 45, "duration": 0.5},
        {"joint": "RElbowRoll", "angle": 60, "duration": 0.5},
        {"joint": "RShoulderPitch", "angle": 10, "duration": 0.5},
        {"joint": "RElbowYaw", "angle": 30, "duration": 0.5},
        {"joint": "RElbowRoll", "angle": 45, "duration": 0.5}
    ]
    
    # Ejecutar los movimientos en secuencia
    for movement in movements:
        pepper.setAngles(movement["joint"], math.radians(movement["angle"]), 0.3)
        time.sleep(movement["duration"])
    
    # Volver a la posición inicial
    pepper.setAngles("LShoulderPitch", math.radians(0), 0.3)
    pepper.setAngles("LElbowYaw", math.radians(0), 0.3)
    pepper.setAngles("LElbowRoll", math.radians(0), 0.3)
    pepper.setAngles("RShoulderPitch", math.radians(0), 0.3)
    pepper.setAngles("RElbowYaw", math.radians(0), 0.3)
    pepper.setAngles("RElbowRoll", math.radians(0), 0.3)



#New functionality for gesture hand and say text in a conversation
def gesture_hand_and_say_text(pepper, text):
    # Ejecutar ambas funciones en paralelo
    hand_thread = threading.Thread(target=gesture_hand, args=(pepper,))
    audio_thread = threading.Thread(target=play_audio, args=(text,))
    
    hand_thread.start()
    audio_thread.start()
    
    hand_thread.join()
    audio_thread.join()

def wave_hand_and_say_text(pepper, text):
    # Ejecutar ambas funciones en paralelo
    hand_thread = threading.Thread(target=wave_hand, args=(pepper,))
    audio_thread = threading.Thread(target=play_audio, args=(text,))
    
    hand_thread.start()
    audio_thread.start()
    
    hand_thread.join()
    audio_thread.join()

def say_text(pepper, text):
    play_audio(text)

def say_multiple_texts(pepper, texts):
    if isinstance(texts, list):  # Asegurarse de que texts es una lista
        for text in texts:
            play_audio(text)
    else:
        print("Error: El input no es una lista de textos.")

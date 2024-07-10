import math
import time
from gtts import gTTS
from playsound import playsound
import threading

def wave_hand(pepper):
    #  Move the robot arm to wave
    pepper.setAngles("RShoulderPitch", math.radians(-10), 0.3) 
    pepper.setAngles("RElbowRoll", math.radians(90), 0.3)
    pepper.setAngles("RShoulderRoll", math.radians(-90), 0.3)   
        
    #Wave the hand n times
    n=8
    for i in range(n):
        pepper.setAngles("RElbowRoll", math.radians(45), 0.3)
        time.sleep(0.3)

        pepper.setAngles("RElbowRoll", math.radians(100), 0.3)
        time.sleep(0.5)
    
    # return the arm to the initial position
    inicial_position(pepper)

def play_audio(text):
    if isinstance(text, str):  # make sure text is a string
        tts = gTTS(text=text, lang='en')
        audio_temp = "/tmp/temp_audio.mp3"
        tts.save(audio_temp)
        playsound(audio_temp)
    else:
        print("Error: El texto no es una cadena de caracteres.") # Error message if the text is not a string


#functionality for moving hand naturally in a conversation
def gesture_hand(pepper):
    # Secuency of movements for the left and right arm
    movements_left = [
        {"joint": "LShoulderPitch", "angle": -30, "duration": 0.5},
        {"joint": "LElbowYaw", "angle": -45, "duration": 0.5},
        {"joint": "LElbowRoll", "angle": -45, "duration": 0.5},
        {"joint": "LShoulderPitch", "angle": 10, "duration": 0.5},
        {"joint": "LElbowYaw", "angle": -30, "duration": 0.5},
        {"joint": "LElbowRoll", "angle": -30, "duration": 0.5}
    ]
    
    movements_right = [
        {"joint": "RShoulderPitch", "angle": -30, "duration": 0.5},
        {"joint": "RElbowYaw", "angle": 45, "duration": 0.5},
        {"joint": "RElbowRoll", "angle": 45, "duration": 0.5},
        {"joint": "RShoulderPitch", "angle": 10, "duration": 0.5},
        {"joint": "RElbowYaw", "angle": 30, "duration": 0.5},
        {"joint": "RElbowRoll", "angle": 30, "duration": 0.5}
    ]
    
    # Ejecute the movements of the left arm
    for movement in movements_left:
        pepper.setAngles(movement["joint"], math.radians(movement["angle"]), 0.3)
        time.sleep(movement["duration"])
    
    # Execute the movements of the right arm
    for movement in movements_right:
        pepper.setAngles(movement["joint"], math.radians(movement["angle"]), 0.3)
        time.sleep(movement["duration"])
    
    
    inicial_position(pepper)

def inicial_position(pepper): # Function to move the robot to the initial position
    # Move the robot L arm in normal position
    pepper.setAngles("LShoulderPitch", math.radians(90), 0.3)  
    pepper.setAngles("LElbowRoll", math.radians(0), 0.3) 
    pepper.setAngles("LShoulderRoll", math.radians(0), 0.3) 

    # Move the robot R arm in normal position
    pepper.setAngles("RShoulderPitch", math.radians(90), 0.3)  
    pepper.setAngles("RElbowRoll", math.radians(0), 0.3) 
    pepper.setAngles("RShoulderRoll", math.radians(0), 0.3) 

#New functionality for gesture hand and say text in a conversation
def gesture_hand_and_say_text(pepper, text):
    # multithreading to execute both functions in parallel
    hand_thread = threading.Thread(target=gesture_hand, args=(pepper,))
    audio_thread = threading.Thread(target=play_audio, args=(text,))
    
    hand_thread.start()
    audio_thread.start()
    
    hand_thread.join()
    audio_thread.join()

def wave_hand_and_say_text(pepper, text):
   # multithreading to execute both functions in parallel
    hand_thread = threading.Thread(target=wave_hand, args=(pepper,))
    audio_thread = threading.Thread(target=play_audio, args=(text,))
    
    hand_thread.start()
    audio_thread.start()
    
    hand_thread.join()
    audio_thread.join()

# Just say the text
def say_text(pepper, text):
    play_audio(text)

def say_multiple_texts(pepper, texts):
    if isinstance(texts, list):  # Be sure texts is a list
        for text in texts:
            play_audio(text)
    else:
        print("Error: El input no es una lista de textos.")

#Final function to recommend subjects based on user preferences
def say_recomend_subject(subject1, subject2, subject3):
    recommendation = f"Based on your preferences, I recommend you the following subjects: {subject1}, {subject2}, and {subject3}. Thank you for using the elective recommendation system. Have a great day!"
    play_audio(recommendation)

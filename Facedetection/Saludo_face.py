import cv2
import qibullet
import time
import math
from gtts import gTTS
from playsound import playsound

def wave_hand_and_say_hello(pepper):
    pepper.setAngles("RShoulderPitch", math.radians(-90), 0.3)
    pepper.setAngles("RElbowRoll", math.radians(90), 0.3)
    pepper.setAngles("RShoulderRoll", math.radians(-90), 0.3)
    
    # Wave n times
    for _ in range(2):
        pepper.setAngles("RElbowRoll", math.radians(45), 0.3)
        time.sleep(0.3)
        pepper.setAngles("RElbowRoll", math.radians(90), 0.3)
        time.sleep(0.3)
    
    # Intial pos
    pepper.setAngles("RShoulderPitch", math.radians(0), 0.3)
    pepper.setAngles("RElbowRoll", math.radians(0), 0.3)
    pepper.setAngles("RShoulderRoll", math.radians(0), 0.3)
    
    # Say hello in spanish just for fun
    tts = gTTS(text="Hola", lang='es')
    audio_temp = "/tmp/temp_audio.mp3"
    tts.save(audio_temp)
    playsound(audio_temp)

def main():
    simulation_manager = qibullet.SimulationManager()
    client_id = simulation_manager.launchSimulation(gui=True)
    pepper = simulation_manager.spawnPepper(client_id, spawn_ground_plane=True)
    pepper.goToPosture("Stand", 0.6)
    #pepper go to posture: Stand, StandInit, StandZero, Crouch, Sit, LyingBelly, LyingBack, Rest.


    # open openCV window
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Start the video capture from the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No hay camara disponible.") #No camera available
        return

    has_waved = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el frame.")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Calculate the center of the face
            center_x = x + w / 2
            center_y = y + h / 2

            image_center_x = frame.shape[1] / 2
            image_center_y = frame.shape[0] / 2

            # calculate the angle to move heaf of Pepper
            yaw = -(center_x - image_center_x) / image_center_x * 0.5
            pitch = (center_y - image_center_y) / image_center_y * 0.5 

            # Move Pepper's head in direction of the detected face
            pepper.setAngles(["HeadYaw", "HeadPitch"], [yaw, pitch], 0.2)

            # Say hola and wave hand if the face is in the center of the image
            if abs(center_x - image_center_x) < 50 and abs(center_y - image_center_y) < 50 and not has_waved:
                wave_hand_and_say_hello(pepper)
                has_waved = True

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    simulation_manager.stopSimulation(client_id)

if __name__ == "__main__":
    main()

import cv2
import sys
import os
import time
from deepface import DeepFace
from config import FACE_DB_PATH

# Ensure script can find required modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set Temporary Image Path
TEMP_IMAGE_PATH = "temp_face.jpg"

# Motivational Messages Based on Emotion
MOTIVATIONAL_MESSAGES = {
    "happy": "Keep smiling! Your positivity is contagious!",
    "surprise": "Expect the unexpected. Something great is coming your way!",
    "neutral": "Stay positive and focused. Great things take time!",
    "sad": "Tough times don't last, but tough people do!",
    "fear": "Fear is just excitement without breath. Take a deep breath!",
    "angry": "Take a moment to breathe. A calm mind is a strong mind!",
    "disgust": "Look for the positives today. Every challenge is an opportunity!"
}

# Open Camera with V4L2 Backend
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Fix for Raspberry Pi
if not camera.isOpened():
    print("Error: Camera not opening")
    sys.exit()

def recognize_face():
    """ Captures an image, performs face recognition & emotion analysis using DeepFace """
    
    # Capture Frame
    ret, frame = camera.read()
    if not ret:
        print("Error: Couldn't capture image from the camera")
        return "Guest", "Neutral", "Stay positive and keep going!"

    # Save Frame Temporarily for DeepFace Processing
    cv2.imwrite(TEMP_IMAGE_PATH, frame)

    try:
        # Face Recognition
        result = DeepFace.find(img_path=TEMP_IMAGE_PATH, db_path=FACE_DB_PATH, enforce_detection=False)
        user_name = (
            os.path.basename(result[0]['identity'][0]).split('.')[0]
            if result and len(result) > 0 and not result[0].empty
            else "Guest"
        )

        # Emotion Detection
        emotion_result = DeepFace.analyze(img_path=TEMP_IMAGE_PATH, actions=['emotion'], enforce_detection=False)
        
        if emotion_result and isinstance(emotion_result, list) and 'emotion' in emotion_result[0]:
            detected_emotion = max(emotion_result[0]['emotion'], key=emotion_result[0]['emotion'].get)
        else:
            detected_emotion = "Neutral"

        # Get Motivational Message
        message = MOTIVATIONAL_MESSAGES.get(detected_emotion, "You're doing great! Keep pushing forward!")

    except Exception as e:
        print(f"DeepFace Error: {e}")
        return "Guest", "Neutral", "Stay strong and keep going!"

    # Delete Temp Image
    if os.path.exists(TEMP_IMAGE_PATH):
        os.remove(TEMP_IMAGE_PATH)

    return user_name.capitalize(), detected_emotion, message

# Test the Function
if __name__ == "__main__":
    try:
        while True:
            name, emotion, message = recognize_face()
            print(f"Recognized: {name} | Emotion: {emotion} | Message: {message}")
            time.sleep(5)  # Run every 5 seconds

    except KeyboardInterrupt:
        print("\nStopping program...")

    finally:
        # Release Camera
        camera.release()
        print("Camera released.")

import cv2
import os
import time
import multiprocessing
from deepface import DeepFace
FACE_DB_PATH = "/home/rohith/Desktop/SmartMirror/assets/faces"

# Define image path
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

def capture_image():
    """Captures an image using libcamera-still, resizes it, and returns the frame."""
    os.system(f"libcamera-still -o {TEMP_IMAGE_PATH} --nopreview -t 1000")

    if not os.path.exists(TEMP_IMAGE_PATH):
        print("Error: Failed to capture image with libcamera.")
        return None

    # Read the image
    frame = cv2.imread(TEMP_IMAGE_PATH)
    if frame is None:
        print("Error: OpenCV couldn't read the captured image.")
        return None

    # Resize to 640x480 for better DeepFace performance
    frame = cv2.resize(frame, (640, 480))
    
    # Save the resized image back
    cv2.imwrite(TEMP_IMAGE_PATH, frame)

    return frame

def recognize_face():
    """Performs face recognition and emotion analysis."""
    frame = capture_image()
    if frame is None:
        return "Guest", "Neutral", "Stay positive and keep going!"

    try:
        # Face Recognition
        result = DeepFace.find(img_path=TEMP_IMAGE_PATH, db_path=FACE_DB_PATH, enforce_detection=False)
        user_name = os.path.basename(result[0]['identity'][0]).split('.')[0] if result and len(result) > 0 else "Guest"

        # Emotion Detection
        emotion_result = DeepFace.analyze(img_path=TEMP_IMAGE_PATH, actions=['emotion'], enforce_detection=False)
        detected_emotion = max(emotion_result[0]['emotion'], key=emotion_result[0]['emotion'].get) if emotion_result else "Neutral"

        # Get Motivational Message
        message = MOTIVATIONAL_MESSAGES.get(detected_emotion, "You're doing great! Keep pushing forward!")

    except Exception as e:
        print(f"DeepFace Error: {e}")
        return "Guest", "Neutral", "Stay strong and keep going!"

    # Delete Temp Image
    if os.path.exists(TEMP_IMAGE_PATH):
        os.remove(TEMP_IMAGE_PATH)

    return user_name.capitalize(), detected_emotion, message

def analyze_face():
    """Runs the face analysis in a subprocess to avoid memory overload."""
    name, emotion, message = recognize_face()
    print(f"Recognized: {name}, Emotion: {emotion}, Message: {message}")

if __name__ == "__main__":
    while True:
        p = multiprocessing.Process(target=analyze_face)
        p.start()
        p.join()  # Ensures only one instance runs at a time
        time.sleep(5)  # Run every 5 seconds

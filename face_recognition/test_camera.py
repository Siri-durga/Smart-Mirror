import cv2
import os

# Define temporary image file
TEMP_IMAGE_PATH = "temp_image.jpg"

def capture_image():
    # Use libcamera to capture image
    os.system(f"libcamera-still -o {TEMP_IMAGE_PATH} --nopreview -t 1000")

    # Check if image was captured
    if not os.path.exists(TEMP_IMAGE_PATH):
        print("? Error: Failed to capture image with libcamera.")
        return None

    # Read the image using OpenCV
    frame = cv2.imread(TEMP_IMAGE_PATH)
    if frame is None:
        print("? Error: OpenCV couldn't read the captured image.")
        return None

    return frame

# Test the function
frame = capture_image()
if frame is not None:
    print("? Image captured successfully using libcamera.")
    cv2.imshow("Captured Image", frame)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

    # Cleanup: Delete temp image
    os.remove(TEMP_IMAGE_PATH)
else:
    print("? Failed to capture image.")


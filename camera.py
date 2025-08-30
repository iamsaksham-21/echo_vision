import cv2
import pyttsx3
import speech_recognition as sr
import webbrowser
from ultralytics import YOLO
import time

# Load YOLOv9 Model
model = YOLO("yolov9c.pt")
names = model.names

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except:
        return ""

# Detect product and return top label
def detect_product():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        speak("I couldn't access the camera.")
        return None

    speak("Scanning the scene. Please wait a moment.")

    detected_object = None
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, imgsz=640, conf=0.5)
        annotated_frame = results[0].plot()

        # Display the frame
        cv2.imshow("YOLOv9 - Live Detection", annotated_frame)

        # Detect and speak the top object (once)
        if results[0].boxes and not detected_object:
            top_box = results[0].boxes[0]
            label_id = int(top_box.cls[0])
            detected_object = names[label_id]
            speak(f"I see a {detected_object}")

        # Break if 'q' is pressed or after 10 seconds
        if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - start_time > 10:
            break

    cap.release()
    cv2.destroyAllWindows()

    return detected_object

def search_on_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Searching Google for {query}")

def main():
    speak("Say 'what's in front of me' to identify a product.")

    product = None

    while True:
        command = listen_command()

        if "what's in front of me" in command:
            product = detect_product()

        elif "search this product" in command and product:
            search_on_google(product)

        elif "stop" in command or "exit" in command:
            speak("Goodbye! Stay curious.")
            break

        elif product and "what is this" in command:
            speak(f"This looks like a {product}")

        elif command != "":
            speak("Say 'what's in front of me' or 'search this product'.")

if __name__ == "__main__":
    main()

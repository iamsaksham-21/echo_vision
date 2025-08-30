import requests
import json
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import speech_recognition as sr
from bs4 import BeautifulSoup
import re
import cv2
import torch
from ultralytics import YOLO
import pyaudio

# Initialize Text-to-speech engine
engine = pyttsx3.init()

# Load YOLO model
yolo_model = YOLO('yolov8n.pt')

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I'm your AI assistant. How can I assist you today?")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='en-IN')
        print(f"User: {text}")
        return text.lower()
    except:
        speak("Sorry, I couldn't understand.")
        return ""

def describe_surroundings():
    speak("Scanning your surroundings...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Unable to access the camera.")
        return

    ret, frame = cap.read()
    if not ret:
        speak("Failed to capture image.")
        cap.release()
        return

    # Run YOLO object detection
    results = yolo_model(frame)

    # Show detection results in a window
    annotated_frame = results[0].plot()
    cv2.imshow("Surroundings", annotated_frame)
    cv2.waitKey(5000)  # Show window for 5 seconds
    cv2.destroyAllWindows()

    # Extract detected object names
    names = results[0].names
    boxes = results[0].boxes
    if boxes is not None and boxes.cls.numel() > 0:
        detected_classes = [names[int(cls)] for cls in boxes.cls]
        items = ', '.join(set(detected_classes))
        speak(f"I see: {items} in front of you.")
    else:
        speak("I don't see anything recognizable.")

    cap.release()

def execute_command(command):
    if 'wikipedia' in command:
        speak('Searching Wikipedia...')
        topic = command.replace("wikipedia", "")
        results = wikipedia.summary(topic, sentences=2)
        speak("According to Wikipedia:")
        speak(results)
    elif 'open website' in command:
        website = command.replace("open website", "").strip()
        if not website.startswith("http"):
            website = "https://" + website
        webbrowser.open(website)
        speak(f"Opening {website}")
    elif 'time' in command:
        speak(f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}")
    elif 'weather' in command:
        speak(get_current_weather())
    elif 'quote' in command:
        speak(get_random_quote())
    elif 'joke' in command:
        speak(get_random_joke())
    elif 'what do you see' in command or 'describe around' in command:
        describe_surroundings()
    elif 'open app' in command:
        app_name = command.replace("open app", "").strip()
        open_app(app_name)
    elif 'bye' in command:
        speak("Goodbye!")
        exit()
    else:
        speak(chat_response(command))

def get_current_weather():
    api_key = "your_openweathermap_api_key"
    city = "Greater Noida"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return f"Weather in {city}: {weather}, {temperature}°C."
        else:
            return "Could not fetch weather data."
    except:
        return "Weather service is currently unavailable."

def chat_response(text):
    if "how are you" in text:
        return "I'm doing great, thanks for asking!"
    elif "who are you" in text:
        return "I'm your smart assistant, here to help you."
    elif "your name" in text:
        return "You can call me echovision."
    elif "i am feeling very upset" in text:
        return "oh no! i'm not happy to hear that. can i do something to uplift you mood?"
    elif "yeah can you tell me something" in text:
        return "ofcourse! you know why ria is cute? because she looks like DORA.."
    elif "find me a boyfriend" in text:
        return "just shut up .. you are comitted to saksham"
    elif "but still i want another" in text:
        return "stop this or else i'll text him!"
    elif "but you don't have his number" in text:
        return "i do 7667345585. now should i?"
    elif "why were you made" in text:
        return "I was developed for visually challenged people, to help them and assist them with their surroundings."
    else:
        return "Sorry, I didn't get that. Could you rephrase?"

def get_random_joke():
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why do you think people don't smile? Because their smile is scary."
    ]
    return random.choice(jokes)

def get_random_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Today is not a choice but an opportunity to work on yourself."
    ]
    return random.choice(quotes)

def open_app(app_name):
    apps = {
        "notepad": "C:\\Windows\\system32\\notepad.exe",
        "canva": "C:\\Users\\saksh\\AppData\\Local\\Programs\\Canva\\Canva.exe",
        "Acrobat" : "C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"

    }
    if app_name.lower() in apps:
        os.system(apps[app_name.lower()])
        speak(f"Opening {app_name}")
    else:
        speak("I couldn't find that application.")

# Example usage:
def main():
    greet()
    while True:
        command = listen()
        if command:
            execute_command(command)



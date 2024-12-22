import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests
import tkinter as tk
from tkinter import Label, Button, Text
from PIL import Image, ImageTk

# Initialize the speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to female voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        text_output.insert(tk.END, "\nListening...\n")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        text_output.insert(tk.END, "Recognizing...\n")
        query = r.recognize_google(audio, language='en-in')
        text_output.insert(tk.END, f"User said: {query}\n")
    except Exception as e:
        text_output.insert(tk.END, "Sorry, I didn't catch that. Please repeat.\n")
        return "None"
    
    return query.lower()

def get_weather(city):
    api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] == 200:
        main = data["main"]
        temperature = main["temp"]
        description = data["weather"][0]["description"]
        return f"The temperature in {city} is {temperature}°C with {description}."
    else:
        return "Sorry, I couldn't fetch the weather."

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis, your personal assistant. How can I help you today?")

def process_command():
    query = listen()

    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        text_output.insert(tk.END, f"Wikipedia says: {results}\n")

    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif 'open google' in query:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif 'time' in query:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}")
        text_output.insert(tk.END, f"The current time is {current_time}\n")

    elif 'weather' in query:
        speak("Please tell me the city name.")
        city = listen()
        weather_report = get_weather(city)
        speak(weather_report)
        text_output.insert(tk.END, f"Weather report: {weather_report}\n")

    elif 'stop' in query or 'exit' in query:
        speak("Goodbye! Have a nice day.")
        root.destroy()

    else:
        speak("Sorry, I didn't understand that. Please try again.")

# Set up the Tkinter window
root = tk.Tk()
root.title("Jarvis Assistant")
root.geometry("500x600")

# Load and display an image
image = Image.open("jarvis_image.jpg")  # Replace with the path to your image
image = image.resize((300, 150), Image.LANCZOS)  # Fixed the ANTIALIAS issue
photo = ImageTk.PhotoImage(image)

label_image = Label(root, image=photo)
label_image.pack()

# Title label
title_label = Label(root, text="Jarvis - Personal Assistant", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# Output box
text_output = Text(root, height=15, width=50, wrap="word", font=("Helvetica", 12))
text_output.pack(pady=10)

# Button to trigger voice command
btn_listen = Button(root, text="Speak to Jarvis", font=("Helvetica", 14), command=process_command)
btn_listen.pack(pady=10)

# Greet the user when the program starts
greet_user()

# Start the Tkinter event loop
root.mainloop()

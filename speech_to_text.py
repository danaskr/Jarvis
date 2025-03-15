import speech_recognition as sr
import pyttsx3
import re
import tkinter as tk
import os
import webbrowser
import subprocess
from tkinter import scrolledtext

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Create UI
root = tk.Tk()
root.title("Speech Assistant")
root.configure(bg="#FBE7C6")  # Pastel background

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Comic Sans MS", 12), bg="#FFDAC1")
chat_box.pack(padx=10, pady=10)
chat_box.config(state=tk.DISABLED)

def update_chat(role, message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"{role}: {message}\n", (role,))
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def extract_name(text):
    match = re.search(r"(?:my name is|I am) (\w+)", text, re.IGNORECASE)
    return match.group(1) if match else None

def extract_age(text):
    match = re.search(r"(?:I am|I'm|my age is) (\d+)", text, re.IGNORECASE)
    return match.group(1) if match else None

def extract_chrome(text):
    match = re.search(r"open (.+)", text, re.IGNORECASE)
    if match:
        site = match.group(1).lower()
        if "youtube" in site:
            return "https://www.youtube.com"
        if "spotify" in site:
            return "https://open.spotify.com"
        if "insta" in site or "instagram" in site:
            return "https://www.instagram.com"
        if "chat gpt" in site or "chat" in site or "chatgpt" in site:
            return "https://www.chatgpt.com"
        # Add more sites if needed
    return None

def extract_application(text):
    match = re.search(r"open (.+)", text, re.IGNORECASE)
    if match:
        app = match.group(1).lower()
        return app
    return None

def record_text():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            update_chat("System", "Listening...")
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            update_chat("You", MyText)
            return MyText
    except sr.RequestError as e:
        update_chat("System", "Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        update_chat("System", "Unknown error occurred")
    return None

def listen_loop():
    text = record_text()
    if text:
        name = extract_name(text)
        age = extract_age(text)
        chrome = extract_chrome(text)
        app = extract_application(text)
        if chrome:
            response = f"Opening {chrome}..."
            update_chat("Bot", response)
            speak(response)
            webbrowser.open(chrome)
            
        if app:
            response = f"Opening {app}..."
            update_chat("Bot", response)
            speak(response)
            try:
                subprocess.Popen(app)
            except FileNotFoundError:
                update_chat("Bot", f"Could not find application: {app}")
                speak(f"Could not find application: {app}")
            except Exception as e:
                update_chat("Bot", f"Error opening application: {str(e)}")
                speak(f"Error opening application: {str(e)}")
            
        if name:
            response = f"Nice to meet you, {name}!"
            update_chat("Bot", response)
            speak(response)
        if age:
            response = f"Wow, so young! You're only {age} years old!"
            update_chat("Bot", response)
            speak(response)
        
        if text.lower().strip() == "goodbye":
            response = "Goodbye! Terminating the program."
            update_chat("Bot", response)
            speak(response)
            root.quit()
            return
    root.after(1000, listen_loop)

# Start listening loop
tk.Label(root, text="Say something...", font=("Comic Sans MS", 14), bg="#FBE7C6").pack()
root.after(1000, listen_loop)
root.mainloop()

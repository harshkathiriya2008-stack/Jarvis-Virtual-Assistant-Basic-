"""
Jarvis - simple voice assistant (Windows)

Install (run in Command Prompt):
    pip install pyttsx3 SpeechRecognition wikipedia pyaudio

Optional email setup (use a Gmail *App Password*, not your real password):
    setx JARVIS_EMAIL "youremail@gmail.com"
    setx JARVIS_APP_PASSWORD "your-16-char-app-password"
Then close and reopen the terminal.
"""

import datetime
import os
import smtplib
import webbrowser
import pyaudio
import pyttsx3
import speech_recognition as sr
import wikipedia

# ---------------- CONFIG ----------------
MUSIC_DIR = r"D:\Non Critical\songs\Favorite Songs2"
VSCODE_PATH = r"C:\Users\Haris\AppData\Local\Programs\Microsoft VS Code\Code.exe"
CONTACTS = {
    "harry": "harryyourEmail@gmail.com",
}
EMAIL = os.environ.get("JARVIS_EMAIL")
APP_PASSWORD = os.environ.get("JARVIS_APP_PASSWORD")
# ----------------------------------------

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)  # try voices[1].id for a female voice
engine.setProperty("rate", 170)


def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you")


def take_command():
    """Listen from the microphone and return the text (lowercase), or '' on failure."""
    r = sr.Recognizer()
    r.pause_threshold = 1
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=8, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        return ""
    except OSError as e:
        print(f"Microphone error: {e}")
        return ""

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Say that again please...")
    except sr.RequestError:
        print("Speech service unavailable. Check your internet connection.")
    return ""


def send_email(to, content):
    if not EMAIL or not APP_PASSWORD:
        raise RuntimeError("Set JARVIS_EMAIL and JARVIS_APP_PASSWORD environment variables.")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, to, content)


def search_wikipedia(query):
    topic = query.replace("wikipedia", "").strip()
    if not topic:
        speak("What should I search on Wikipedia?")
        return
    speak("Searching Wikipedia...")
    try:
        result = wikipedia.summary(topic, sentences=2)
        speak("According to Wikipedia")
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"That is ambiguous. Did you mean {', '.join(e.options[:3])}?")
    except wikipedia.exceptions.PageError:
        speak("I could not find that page.")
    except Exception as e:
        print(e)
        speak("Sorry, Wikipedia search failed.")


def play_music():
    try:
        songs = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a"))]
        if not songs:
            speak("No songs found in your music folder.")
            return
        os.startfile(os.path.join(MUSIC_DIR, songs[0]))
    except FileNotFoundError:
        speak("Music folder not found. Please update the path in the script.")


def main():
    wish_me()
    while True:
        query = take_command()
        if not query:
            continue

        if "wikipedia" in query:
            search_wikipedia(query)

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")

        elif "open google" in query:
            webbrowser.open("https://www.google.com")

        elif "open stackoverflow" in query or "open stack overflow" in query:
            webbrowser.open("https://stackoverflow.com")

        elif "play music" in query:
            play_music()

        elif "the time" in query:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {now}")

        elif "open code" in query:
            try:
                os.startfile(VSCODE_PATH)
            except FileNotFoundError:
                speak("VS Code path not found. Please update the path in the script.")

        elif "email to" in query:
            name = query.split("email to", 1)[1].strip().split()[0] if query.split("email to", 1)[1].strip() else ""
            to = CONTACTS.get(name)
            if not to:
                speak("I don't have that contact saved.")
                continue
            try:
                speak("What should I say?")
                content = take_command()
                if not content:
                    speak("I didn't catch that. Email cancelled.")
                    continue
                send_email(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email")

        elif any(w in query for w in ("exit", "quit", "stop", "goodbye", "bye")):
            speak("Goodbye Sir!")
            break

        else:
            print("No query matched")


if __name__ == "__main__":
    main()
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
import serial
import time
from googletrans import Translator  # Import the Translator class from googletrans
# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
# Initialize serial communication with Arduino (adjust the port)
arduino = serial.Serial('COM10', 9600)  # Change 'COM10' to the correct port for your Arduino
# Initialize translator
translator = Translator()
def switch_on_led():
    arduino.write(b'1')  # Send '1' to Arduino to turn on the LED
    speak("The LED on pin 7 is switched on.")

def switch_off_led():
    arduino.write(b'0')  # Send '0' to Arduino to turn off the LED
    speak("The LED on pin 7 is switched off.")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def stop_speaking():
    engine.stop()  # Stop the speech engine if it's speaking

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. Please tell me how may I help you")

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

        # If the user says 'ok', it stops the assistant and goes to sleep
        if 'sleep' in query.lower():
            speak("Going to sleep. Say 'Jarvis' to wake me up.")
            stop_speaking()
            sleep_mode()
            return "None"
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sleep_mode():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sleeping... waiting for 'Jarvis'")
        while True:
            try:
                audio = r.listen(source)
                query = r.recognize_google(audio, language='en-in').lower()
                if 'jarvis' in query:
                    speak("I am back online. How can I assist you?")
                    break
            except:
                continue

def get_google_summary(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    summary = ""
    try:
        summary = soup.find("div", class_="BNeawe").text
    except Exception as e:
        summary = "I couldn't find the answer. Please try again."

    return summary

def handle_direct_answer(query):
    speak(f"Searching for {query}")
    result = get_google_summary(query)
    speak(result)
    print(result)

def get_stackoverflow_results(query):
    search_url = f"https://stackoverflow.com/search?q={query}"
    speak("Here are the top results from Stack Overflow.")
    webbrowser.open(search_url)

def get_reddit_posts(query):
    search_url = f"https://www.reddit.com/search/?q={query}"
    speak("Here are the latest posts from Reddit.")
    webbrowser.open(search_url)

def get_news_results(query):
    search_url = f"https://news.google.com/search?q={query}"
    speak("Fetching the latest news articles for your query.")
    webbrowser.open(search_url)

def google_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

# New: Translate spoken language to English
from deep_translator import GoogleTranslator

# New: Translate spoken language to English using deep-translator
def translate_to_english():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please speak the sentence you want to translate.")
        print("Listening for translation...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        # Recognize the speech in the user's language (adjust as needed)
        user_speech = r.recognize_google(audio)
        print(f"User said (to translate): {user_speech}")

        # Translate using deep-translator
        translator = GoogleTranslator(source='auto', target='en')
        translated_text = translator.translate(user_speech)
        print(f"Translated to English: {translated_text}")
        speak(f"The translation is: {translated_text}")
    except Exception as e:
        print("Translation failed, please try again.")
        speak("I could not translate that, please try again.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'google search' in query:
            speak('What do you want to search on Google?')
            query = takeCommand().lower()
            google_search(query)

        elif 'youtube search' in query:
            speak('What do you want to search on YouTube?')
            query = takeCommand().lower()
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            speak(f"Here are the YouTube search results for {query}")

        elif 'stackoverflow' in query:
            speak('What do you want to search on Stack Overflow?')
            query = takeCommand().lower()
            get_stackoverflow_results(query)

        elif 'reddit' in query:
            speak('What do you want to search on Reddit?')
            query = takeCommand().lower()
            get_reddit_posts(query)

        elif 'news' in query:
            speak('Fetching news articles for your query.')
            query = takeCommand().lower()
            get_news_results(query)

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'on led' in query or 'turn on the led' in query:
            switch_on_led()

        elif 'off led' in query or 'turn off the led' in query:
            switch_off_led()

        elif 'translate' in query:
            translate_to_english()

        else:
            handle_direct_answer(query)

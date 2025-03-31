import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import random
import requests
import openai

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Adjust speech speed
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set voice

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice command from user"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce noise
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("❌ Network error.")
        return None

def play_music():
    """Function to play a random song from a folder"""
    music_path = r"C:\\Users\\vilas\\Music"  # Change to your music folder path

    if os.path.exists(music_path) and os.path.isdir(music_path):
        songs = [f for f in os.listdir(music_path) if f.endswith(".mp3")]
        if songs:
            song_to_play = random.choice(songs)
            os.startfile(os.path.join(music_path, song_to_play))
            speak(f"Playing {song_to_play}")
        else:
            speak("No music files found in the folder.")
    else:
        speak("Music folder not found. Please update the path in the script.")

def get_weather(city):
    """Fetches weather data using OpenWeatherMap API"""
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            speak(f"The weather in {city} is {weather_desc} with a temperature of {temp} degrees Celsius.")
        else:
            speak("Could not fetch weather details. Please check the city name.")
    except:
        speak("Unable to connect to the weather service.")

def get_news():
    """Fetches top news headlines using NewsAPI"""
    api_key = "YOUR_NEWSAPI_KEY"  # Replace with your API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            articles = data["articles"][:5]  # Get top 5 news headlines
            speak("Here are the latest news headlines.")
            for article in articles:
                speak(article["title"])
        else:
            speak("Could not fetch news updates.")
    except:
        speak("Unable to connect to the news service.")

def ask_ai(question):
    """Uses OpenAI's GPT model to generate AI responses."""
    openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response["choices"][0]["message"]["content"]
        speak(answer)
    except Exception as e:
        speak("I'm sorry, I couldn't process that request.")

def jarvis():
    """Main function for J.A.R.V.I.S. AI assistant"""
    speak("Hello! I am Jarvis. How can I assist you today?")
    
    while True:
        command = listen()

        if command:
            if "time" in command or "what time is it" in command:
                now = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The time is {now}")

            elif "open youtube" in command:
                webbrowser.open("https://www.youtube.com")
                speak("Opening YouTube")

            elif "open google" in command:
                webbrowser.open("https://www.google.com")
                speak("Opening Google")

            elif "play music" in command:
                play_music()

            elif "open notepad" in command:
                os.system("notepad.exe")
                speak("Opening Notepad")

            elif "open calculator" in command:
                os.system("calc.exe")
                speak("Opening Calculator")

            elif "weather" in command:
                speak("Which city's weather would you like to check?")
                city = listen()
                if city:
                    get_weather(city)

            elif "news" in command:
                get_news()

            elif "ai" in command or "chat" in command or "question" in command:
                speak("What would you like to ask?")
                question = listen()
                if question:
                    ask_ai(question)

            elif "stop" in command or "exit" in command:
                speak("Goodbye! Have a great day.")
                break

            else:
                speak("I didn't understand that. Would you like me to search for an answer?")
                ask_ai(command)

if __name__ == "__main__":
    jarvis()

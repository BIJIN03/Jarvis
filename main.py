import speech_recognition as sr
import webbrowser
import requests
import pygame
import os
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS
from music import musics
# import pyttsx3

load_dotenv()

# engine = pyttsx3.init()

newsapi=os.getenv("NEWS_API")
geminiapi=os.getenv("GEMINI_API")

def speak(mytext,news=False):
    
    # engine.say(text)
    # engine.runAndWait()

    speech = gTTS(text=mytext,slow=False)
    speech.save("text.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("text.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() and news:  
        pygame.time.Clock().tick(10)

def aiprocess(command):

    genai.configure(api_key=geminiapi)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Give a brief description on {command}")
    return response.text

def processCommand(c):

    if "open" in c.lower():
        site=c.lower().split(" ")[1]
        speak(f"Opening {site}.")
        webbrowser.open(f"https://www.{site}.com")
    
    elif c.lower().startswith("play"):
        song=c.lower().strip("play ")
        speak(f"Playing {song}")
        webbrowser.open(musics[song])
    elif "news" in c.lower():
        res=requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2024-11-25&sortBy=publishedAt&apiKey={newsapi}")

        if res.status_code==200:
            data=res.json()
            articles=data.get("articles",[])
            for article in articles:
                speak(article["title"],True)
        else:
            speak("Sorry, unable to fetch news now.")
    else:
        result=aiprocess(c)
        speak(result)
    

if __name__=="__main__":
    speak("Initialising Luna...")
    r = sr.Recognizer()
    name="Luna"
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio=r.listen(source,timeout=2,phrase_time_limit=1)
            word=r.recognize_google(audio)
            print(word)
            if name.lower() in word.lower():
                speak("Yes,How can I help you?")
                print(f"{name} Active.")
                try:
                    with sr.Microphone() as source:
                        audio=r.listen(source)
                
                    command=r.recognize_google(audio)
                    print(command)
                    if "set your name" in command.lower():
                        name=command.split(" ")[len(command.split(" "))-1]
                        speak(f"Name set to {name}")
                    elif command.lower() == "exit" or command.lower()=="stop":
                        speak("Luna shutting down")
                        break
                    else:
                        processCommand(command)

                except :
                    print("No command recieved.")
                    
        except Exception as e:
            print("Speak Something.")
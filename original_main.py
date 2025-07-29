'''
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests 
import google.generativeai as genai
from client import GeminiClient 

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "3c7107c604a2496e90e46d5a9ad57fb2"
gemini_api = "AIzaSyBT_Xg9JVjknOWcT87dur3315E45gsaCTU"

genai.configure(api_key=gemini_api)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = GeminiClient(api_key=gemini_api)
    completion = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Alfred skilled in general tasks like Alexa and Google Assistant"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choice[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open snapchat" in c.lower():
        webbrowser.open("https://snapchat.com")
    elif c.lower().startswith("play"):
        song = " ".join(c.lower().split(" ")[1:]) 
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles",[])
            for article in articles:
                speak(article["title"])
    else:
        # let OpenAi handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Alfred...")
    try:
        while True:
            # listen for wake word "Alfred"
            # obtain audio from microphone
            r = sr.Recognizer()
            
            print("Recognizing...")
            try:
                with sr.Microphone() as source:
                     r.adjust_for_ambient_noise(source, duration=1)
                     print("Listening...")
                     audio = r.listen(source, timeout=5, phrase_time_limit=3)
                word = r.recognize_google(audio)
                if(word.lower() == "alfred"):
                    speak("Yess Sir!!")
                    # listen for command
                    with sr.Microphone() as source:
                        print("Alfred Active...")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        processCommand(command)

            except Exception as e:
                print("error:{0}".format(e))
                
    except KeyboardInterrupt:
        print("\nStopping...")
        exit()       
'''    


# -----------------------------------by me--------------------------------------


import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests 
import google.generativeai as genai # Import your custom client
from client import GeminiClient 

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "3c7107c604a2496e90e46d5a9ad57fb2"
gemini_api = "AIzaSyBT_Xg9JVjknOWcT87dur3315E45gsaCTU"

# Initialize your custom Gemini client
genai.configure(api_key=gemini_api)

def speak(text):
    print(f"Alfred: {text}")   # Print to terminal
    engine.say(text)           # Speak the same text
    engine.runAndWait()

def aiProcess(command):
    client = GeminiClient(api_key=gemini_api)
    completion = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Alfred skilled in general tasks like Alexa and Google Assistant"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processCommand(c):
    print(f"Processing command: {c}")
    if "open google" in c.lower():
        speak("Opening Google for you, Sir")
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "open snapchat" in c.lower():
        speak("Opening Snapchat")
        webbrowser.open("https://snapchat.com")
    elif c.lower().startswith("play"):
        song = " ".join(c.lower().split(" ")[1:]) 
        try:
            link = musicLibrary.music[song]
            speak(f"Playing {song} for you, Sir")
            webbrowser.open(link)
        except KeyError:
            speak(f"I apologize Sir, I couldn't find {song} in your music library")
    elif "news" in c.lower():
        speak("Fetching the latest headlines for you")
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                speak("Here are today's top headlines")
                for i, article in enumerate(articles[:3]):  # Limit to 3 articles
                    speak(f"Headline {i+1}: {article['title']}")
            else:
                speak("I'm having trouble accessing the news at the moment, Sir")
        except Exception as e:
            print(f"News API error: {e}")
            speak("There seems to be an issue with the news service")
    elif "stop" in c.lower() or "exit" in c.lower() or "quit" in c.lower():
        speak("Goodbye Sir. Have a wonderful day!")
        exit()
    else:
        # let OpenAi handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Alfred is now online.")
    print("Alfred is ready! Say 'Alfred' to wake me up, or 'stop' to exit.")
    
    try:
        while True:
            r = sr.Recognizer()
            
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    print("Listening for wake word 'Alfred'...")
                    audio = r.listen(source, timeout=10, phrase_time_limit=3)
                
                word = r.recognize_google(audio)
                print(f"Heard: {word}")
                
                if "alfred" in word.lower():
                    speak("Yes Sir")
                    print("Alfred activated! Listening for your command...")
                    
                    # Listen for command
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        print("Speak your command...")
                        audio = r.listen(source, timeout=15, phrase_time_limit=10)
                    
                    command = r.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)

            except sr.WaitTimeoutError:
                pass  # Normal timeout, continue listening
            except sr.UnknownValueError:
                pass  # Couldn't understand, continue listening
            except Exception as e:
                print(f"Error: {e}")
                
    except KeyboardInterrupt:
        print("\nShutting down Alfred...")
        speak("Powering down. Until next time, Sir.")
        exit()
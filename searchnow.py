import speech_recognition
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query

query=takeCommand().lower()

engine=pyttsx3.init("sapi5")

voices=engine.getProperty("voices")

engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def searchGoogle(query):
    if "google" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis","")
        query = query.replace("google","")
        query = query.replace("search","")
        query = query.replace("for","")
        speak("This is what I found on google")

        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query,1)
            speak(result)

        except:
            speak("No Speakable output available on google")

def searchYoutube(query):
    if "youtube" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis","")
        query = query.replace("youtube","")
        query = query.replace("search","")
        query = query.replace("for","")
        speak("This is what I found on youtube")
        web="https://www.youtube.com/results?search_query="
        web=web+query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done Sir!")

def searchWikipedia(query):
    if "wikipedia" in query:
        import wikipedia as googleScrap
        query = query.replace("jarvis","")
        query = query.replace("wikipedia","")
        query = query.replace("search","")
        query = query.replace("for","")
        speak("This is what I found on wikipedia")
        results= wikipedia.summary(query,sentences=2)
        speak("According to wikipedia")
        print(results)
        speak(results)


        



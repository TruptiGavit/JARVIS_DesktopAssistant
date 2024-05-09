import requests
import json
import pyttsx3
from dotenv import load_dotenv
import os

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
Newsapikey=os.getenv("Newsapikey")
def latestnews():
    apidict={"business":f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={Newsapikey}",
             "entertainment": f"https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey={Newsapikey}",
             "Science":f"https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey={Newsapikey}",
             "sports": f"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey={Newsapikey}",
             "technology":f"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey={Newsapikey}",
             "health": f"https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey={Newsapikey}",
             }
    content=None
    url=None
    speak("Which news field do you want?, [business],[health],[entertainment],[science],[technology],[sports]")
    field=input("Type field to select")
    for key, value in apidict.items():
        if key.lower() in field.lower():
            url=value
            print(url)
            print("url was found")
            break
        else:
            url=True
            if url is True:
                print("url not found")
                
    news=requests.get(url).text
    news=json.loads(news)
    speak("here is the news")

    arts=news["articles"]
    for articles in arts:
        article=articles["title"]
        print(article)
        speak(article)
        news_url=articles["url"]
        print(f"for more visit {news_url}")

        a=input("[press 1 to continue] and [press 2 to stop]")
        if str(a)=="1":
            pass
        elif str(a)=="2":
            break
    speak("thank you for listening")




    
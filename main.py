import pyttsx3
import speech_recognition
import requests
from bs4 import BeautifulSoup
import datetime
import os
import pyautogui
import webbrowser
import openai
from openai import OpenAI
from dotenv import load_dotenv
import random
from plyer import notification
from pygame import mixer
import speedtest

################################################################################################
# Setting Passwards for jarvis

for i in range(3):
    a = input("Enter Password to open Jarvis :- ")
    pw_file = open("password.txt","r")
    pw = pw_file.read()
    pw_file.close()

    if (a==pw):
        print("WELCOME SIR ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
        break
    elif (i==2 and a!=pw):
        exit()

    elif (a!=pw):
        print("Try Again")

################################################################################################

from INTRO import play_gif
play_gif

################################################################################################
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate",170)

################################################################################################
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

################################################################################################
def takeCommand():
    r=speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        r.energy_threshold=300
        audio=r.listen(source,0,4)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query

################################################################################################

chatStr=""
def chat(query):
    openai_api_key = os.getenv('My_OpenAI_Key')
    client = OpenAI(api_key=openai_api_key)
    global chatStr    
    # Create the messages list with the user's query
    messages = [
        {"role": "user", "content": query}
    ]
    # Add the previous conversation history to the messages list
    if chatStr:
        messages = [{"role": "system", "content": chatStr}] + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        temperature=0.9,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Extract the assistant's response from the API response
    assistant_response = response.choices[0].message.content
    speak(assistant_response)
    chatStr += f"Trupti:{query}\nJarvis: {assistant_response}\n"
    return assistant_response

################################################################################################

def ai(prompt):
    openai_api_key = os.getenv('My_OpenAI_Key')
    client = OpenAI(api_key=openai_api_key)
    text=f"OpenAI response for prompt: {prompt}\n *********************************************\n\n"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text+=response.choices[0].text
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('chatgpt')[1:]).strip() }.txt", "w") as f:
        f.write(text)

################################################################################################

def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

################################################################################################

if __name__ == "__main__":
    while True:
        query=takeCommand().lower()
        if "wake up" in query:
            from greetme import greetMe
            greetMe()

            while True:
                query=takeCommand().lower()
                sites=[["youtube", "https://www.youtube.com"],
                       ["instagram", "https://www.instagram.com"],
                       ["google", "https://www.google.com"],
                       ["facebook", "https://www.facebook.com"],
                       ["twitter", "https://www.twitter.com"],
                       ["linkedin", "https://www.linkedin.com"],
                       ["github", "https://www.github.com"],
                       ["chatgpt", "https://chatgpt.com/"]
                       ]
                for site in sites:
                    if site[0] in query:
                        webbrowser.open(site[1])
                        speak(f"Opening {site[0]}")
                        break
                if "see you later" in query:
                    speak("Going to sleep, Sir you can call me anytime")
                    break

                ################################################################################################
                
                elif "using chatgpt" in query:
                    ai(prompt=query)
                
                ################################################################################################

                elif "change password" in query:
                    speak("What's the new password")
                    new_pw = input("Enter the new password\n")
                    new_password = open("password.txt","w")
                    new_password.write(new_pw)
                    new_password.close()
                    speak("Done sir")
                    speak(f"Your new password is{new_pw}")  

                ################################################################################################

                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()

                    elif "no" in query:
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                
                elif "show my schedule" in query:
                            file = open("tasks.txt","r")
                            content = file.read()
                            file.close()
                            mixer.init()
                            mixer.music.load("music.mp3")
                            mixer.music.play()
                            notification.notify(
                                title = "My schedule :-",
                                message = content,
                                timeout = 15
                                )                          
                    
                ################################################################################################

                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")  

                ################################################################################################
                
                elif "internet speed" in query:
                    wifi  = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")
                    
                ################################################################################################

                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")

                ################################################################################################

                # elif "translate" in query:
                #     from Translator import translategl
                #     query = query.replace("jarvis","")
                #     query = query.replace("translate","")
                #     translategl(query)

                ################################################################################################

                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video streaming")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down")
                    volumedown()

                ################################################################################################

                elif "screenshot" in query:
                     import pyautogui
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")

                ################################################################################################

                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)

                ################################################################################################

                elif "shutdown the system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")
                    elif shutdown == "no":
                        break
                
                ################################################################################################           

                elif "open" in query:
                    from dictapp import openappweb
                    openappweb(query)
                elif "close" in query:
                    from dictapp import closeappweb
                    closeappweb(query)   

                ################################################################################################
                    
                elif "google" in query:
                    from searchnow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from searchnow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from searchnow import searchWikipedia
                    searchWikipedia(query)

                ################################################################################################

                elif "temperature" in query:
                    search="Temperature"
                    url=f"https://www.google.com/search?q={search}"
                    r= requests.get(url)
                    data= BeautifulSoup(r.text,"html.parser")
                    temp=data.find("div",class_="BNeawe").text
                    speak(f"Current{search} is {temp}")

                elif "weather" in query:
                    search="Weather"
                    url=f"https://www.google.com/search?q={search}"
                    r= requests.get(url)
                    data= BeautifulSoup(r.text,"html.parser")
                    temp=data.find("div",class_="BNeawe").text
                    speak(f"Current{search} is {temp}")

                ################################################################################################

                elif "set an alarm" in query:
                    print("input time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a = input("Please tell the time :- ")
                    alarm(a)
                    speak("Done,sir")

                ################################################################################################

                elif "remember" in query:
                    rememberMessage = query.replace("remember","")
                    rememberMessage=query.replace("jarvis","")
                    speak("you told me" + rememberMessage)
                    remember=open("remember.txt", "w")
                    remember.write(rememberMessage)
                    remember.close()

                elif "what do you remember" in query:
                    remember=open("remember.txt", "r")
                    speak("you told me" + remember.read())

                ################################################################################################
                
                

                ################################################################################################

              
                ################################################################################################
               
                
                ################################################################################################

                elif "tired" in query:
                    speak("This will refresh you, sir")
                    a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
                    b = random.choice(a)
                    if b==1:
                        webbrowser.open("https://www.youtube.com/watch?v=lnFLQ12DZRw")
                    elif b==2:
                        webbrowser.open("https://www.youtube.com/watch?v=1eCqV1_7iQ4")
                    else:
                        webbrowser.open("https://www.youtube.com/watch?v=UaI3G5eaE28")
                
                ################################################################################################
                                   
                elif "news" in query:
                    from newsread import latestnews
                    latestnews()
            
                ################################################################################################

                elif "the time" in query:
                    strTime=datetime.datetime.now().strftime("%H:%M")
                    speak(f"Sir, the time is {strTime}")

                ################################################################################################

                elif "sleep" in query:
                    speak("Going to sleep, Sir you can call me anytime")
                    exit()

                ################################################################################################

                elif "reset chat".lower() in query.lower():
                    chatStr = ""

                ################################################################################################

                else:
                    print("Chatting...")
                    chat(query)

                ################################################################################################
                          


                

                

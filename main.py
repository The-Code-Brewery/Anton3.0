import pyttsx3  # Text to speech
import speech_recognition as sr  # Speech recognition module
import wikipedia
import datetime
import os
import smtplib
import requests
from bs4 import BeautifulSoup
import urllib.request as ur
import re
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

# Initialize the voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 350)
engine.setProperty('voice', voices[0].id)  # Setting the voice of the engine as the 0th voice(English)


# Pronounce the text passed
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function that uses speech recognizer
def takeCommand():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        print("Sorry, could you repeat ?")
        query=None
    
    return query

# Initial greetings
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if (hour <= 12):
        speak("Good morning")
    elif (hour <=18):
        speak("Good evening")
    else:
        speak("Good afternoon")

    speak("I am Anton. How may I assist you?")

#Function to automate stackoverflow functionality
def stackoverflowAutomator(ques):
    URL="https://stackoverflow.com/search?tab=relevance&q="
    URL+=ur.pathname2url(ques)

    redirectURL=URL

    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "\
          "snap Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36"}
    page1=requests.get(URL,headers=headers)
    soup1=BeautifulSoup(page1.content,'html.parser')
    soup2=BeautifulSoup(soup1.prettify(),'html.parser')
    getq=soup2.find("div",{"data-position":"1"})
    x=getq.find(class_="result-link").get_text() 
    get_id=getq.attrs["id"]
    s=""
    for i in range(0,len(get_id)):
        if get_id[i].isnumeric():
            s+=get_id[i]
    URL="https://stackoverflow.com/questions/"+s+"/"
    x=x.strip()[3:]
    for i in range(0,len(x)):
        if x[i]==" ":
            URL+="-"
        else:
            URL+=x[i]
    print("\n")
    print("Best Answer:-\n")
    page2=requests.get(URL,headers=headers)
    soup3=BeautifulSoup(page2.content, 'html.parser')
    soup4=BeautifulSoup(soup3.prettify(), 'html.parser')
    geta=soup4.find("div",{"class":"answercell"}) #Answer to the first question.
    r=geta.find(class_="post-text")
    z=r.find("p").get_text().strip()
    z=re.sub(r'[ \n]{3,}','',z)
    print(z)
    speak(z) #Speaking the first line of the best answer


    #Checking if the bot is able to solve the problem, if not it opens the browser
    speak("Did this solve your problem")
    reply=takeCommand()

    if 'yes' in reply.lower():
        speak("I am glad that I could be of some assistance")
    
    else:
        speak("I am really sorry for the issue. Let me direct you to the browser for further assistance")
        browser=webdriver.Chrome('/Users/pratikbaid/Developer/chromedriver')
        browser.get(redirectURL)
        chrome_option.add_experimental_option("detach",True)

#Function to automate email functionality
def emailAutomator(emailRecepient):
    speak("What is the subject of your mail to "+emailRecepient)
    subject=takeCommand()

    speak("What is your message for "+emailRecepient)
    body=takeCommand()

    smtpObj=smtplib.SMTP('smtp.gmail.com',587)
    smtpObj.ehlo() #Establishing connection success=250
    smtpObj.starttls()#Step enabline encription success=220

    smtpObj.login('thenameisanton3@gmail.com','pratikbaid@2471')
    smtpObj.sendmail('thenameisanton3@gmail.com','pratikbaid3@gmail.com','Subject:{}.\n{}'.format(subject,body))

running=True
wishMe()

#Function that contains all the task
def task(query):
    #Logic for automation of Stackoverflow
    if 'stackoverflow' in query.lower() or 'stack overflow' in query.lower() or 'error' in query.lower() or 'solve' in query.lower() or 'problem' in query.lower() or 'exception' in query.lower():
        speak('Searching Stackoverflow...')
        query=query.replace("stackoverflow","")
        print(query)
        stackoverflowAutomator(query)
    
    #Logic for automation of Wikipedia
    elif 'wikipedia' in query.lower() or 'who is' in query.lower() or 'what is' in query.lower() or 'where is' in query.lower():
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia","")
        results=wikipedia.summary(query,sentences=2)
        speak(results)

    #Logic for automating the email sending process
    elif 'email' in query.lower() or 'mail' in query.lower() or 'message' in query.lower():
        if 'email' in query.lower():
            query=query.replace("send email to","")
        elif 'message' in query.lower():
            query=query.replace("send message to ","")
        else:
            query=query.replace("send mail to","")
        emailAutomator(query)

    #Logic to automating general search
    else:
        speak('Searching the web for '+query)
        results=wikipedia.summary(query,sentences=2)
        speak(results)

query = takeCommand() #Taking the first command

while(running==True):
    task(query)
    speak('What else can I assist you with?')
    query = takeCommand()
    
    #Checking if the user wants to ask any further assistance
    if 'no' in query.lower() or 'bye' in query.lower() or 'quit' in query.lower() or 'nothing' in query.lower() or 'thank you' in query.lower():
        running=False
        speak('Have a nice day. Good bye')
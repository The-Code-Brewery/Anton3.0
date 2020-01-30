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
import EmailMining.gmail as gmail
import database

# Initialize the voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 350)
engine.setProperty('voice', voices[0].id)  # Setting the voice of the engine as teh 0th voice(English)


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
        speak("Good afternoon")
    else:
        speak("Good evening")

    speak("I am Anton. Your Intelligent Product Master. How may I assist you?")

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
        browser=webdriver.Chrome()
        browser.get(redirectURL)
        chrome_option = Options()
        chrome_option.add_experimental_option("detach",True)

def getMail(query):
    db = database.Database()
    query = query.split(' ')
    for string in query:
        if string[0].isupper():
            email, isPresent = db.getEmailfromPartialName(string)
            if isPresent:
                return email
    return None

# 0 : unread
# 1 : from
# 2 : all
def emailMining(emailRecepient, flag, last = None):
    speak("Wait for some time till we fetch your emails")
    if flag == 0:
        try:
            response = gmail.get_messages_from_someone(messageFrom=emailRecepient,unread=True,maxResults=1)
        except:
            speak("No unread emails")
            return
    elif flag == 1:
        response = gmail.get_messages(unread=False, maxResults=5)
    elif flag == 2:
        response = gmail.get_messages(maxResults=10)
    for info in response:
        getFrom = ''
        if info.get('from') != None:
            getFrom = f"From {info.get('from')}"
        getSubject = f"Subject {info.get('subject')}"
        speak("Email")
        speak(f"{getFrom}")
        speak(f"{getSubject}")

flag = False
def notesAutomator(date):
    def make_notes(rec_inst,audio):
        try:
            text = rec_inst.recognize_google(audio, language='en-in')
            print(text)
            if('stop' in text):
                global flag
                flag = True
                return
            else:
                with open(f"{date}.txt", "a") as text_file:
                    text_file.write(f"{text}\n")

        except Exception as e:
            return

    r = sr.Recognizer()
    r.pause_threshold = 1.2
    mr = sr.Microphone()
    speak("Starting to make notes...\n")
    with mr as source:
        r.adjust_for_ambient_noise(source, duration=1)
    stopper = r.listen_in_background(mr,make_notes)
    while(True):
        if(flag):
            speak("stopping...")
            break

#Function to automate email functionality
def emailAutomator(query):
    email = getMail(query)
    if email is not None:
        db = database.Database()
        print(email)
        name, isPresent = db.getNameFromEmail(email)
        speak("What is the subject of your mail to "+name)
        subject=takeCommand()

        speak("What is your message for "+name)
        body=takeCommand()

        smtpObj=smtplib.SMTP('smtp.gmail.com',587)
        smtpObj.ehlo() #Establishing connection success=250
        smtpObj.starttls()#Step enabline encription success=220

        smtpObj.login('thenameisanton3@gmail.com','pratikbaid@2471')
        smtpObj.sendmail('thenameisanton3@gmail.com','{}'.format(email),'Subject:{}.\n{}'.format(subject,body))
        smtpObj.quit()
    else:
        speak("Sorry no such person exists")

# 0 for yesterday
# 1 for today
def readNotesAutomator(flag):
    speak("Reading your notes")
    info = 'No such file exists'
    try:
        if flag == 0:
            date = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%B %d, %Y")
            with open(f"{date}.txt") as f:
                info = f.readlines()
                for line in info:
                    speak(line)
                return
        elif flag == 1:
            date = datetime.datetime.now().strftime("%B %d, %Y")
            with open(f"{date}.txt") as f:
                info = f.readlines()
                for line in info:
                    speak(line)
                return
    except:
        pass
    speak(info)


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
        if 'send' in query.lower():
            emailAutomator(query)
        # Email Mining is required
        else:
            email = getMail(query)
            if 'from' in query.lower():
                emailMining(email, 0)
            elif 'unread' in query.lower():
                emailMining(email, 1)
            else:
                emailMining(email, 2)
    
    elif 'read' in query.lower() and 'note' in query.lower():
        if 'yesterday' in query.lower():
            readNotesAutomator(0)
        else:
            readNotesAutomator(1)

    elif 'take notes' in query.lower() or 'note' in query.lower() or 'take note' in query.lower() or 'notes' in query.lower():
        date = datetime.datetime.now().strftime("%B %d, %Y")
        with open(f"{date}.txt", "wb") as fileName:
            pass
        notesAutomator(date)

    else:
        speak('Searching the web for '+query)
        results=wikipedia.summary(query,sentences=2)
        speak(results)

query = takeCommand() #Taking the first command

while(running==True):
    task(query)
    speak('What else can I assist you with?')
    query = takeCommand()
    
    try:
    #Checking if the user wants to ask any further assistance
        if 'no' in query.lower() or 'bye' in query.lower() or 'quit' in query.lower() or 'nothing' in query.lower() or 'thank you' in query.lower():
            running=False
            speak('Have a nice day. Good bye')
    except:
        running=False
        speak('Have a nice day. Good bye')


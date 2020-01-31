import pyttsx3  # Text to speech
import speech_recognition as sr  # Speech recognition module
import wikipedia
import datetime
import os
import smtplib
import sys

# Initialize the voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 250)
engine.setProperty('voice', voices[0].id)  # Setting the voice of the engine as teh 0th voice(English)

# Pronounce the text passed
def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if (hour < 12):
        speak("Good morning")
    elif (hour <=16):
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Anton. Your Intelligent Product Master. How may I assist you?")
wishMe()
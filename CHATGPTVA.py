#speech to text
import speech_recognition as sr
import pyttsx3

import os

from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = ""

#convert tect to speech
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

r = sr.Recognizer()



#records text
def record_text():
    while (1):
        try:
            #microphone listens for input
            with sr.Microphone() as source2:
                #prepare r to receive input
                r.adjust_for_ambient_noise(source2, duration = 0.2)

                #listens for user input
                audio2 = r.listen(source2)

                #use google to rec audio
                MyText = r.recognize_google(audio2)
                return MyText

        except sr.RequestError as e:
            print ("Could not request results; {0}.format(e)")
        
        except sr.UnknownValueError:
            print ("Unknown Error occured")
        
def send_to_chatGPT(messages, model = "gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages, # 
        max_tokens = 100, # how long the message from chat is 
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message.content)
    return message

messages = []
while (1):
    text = record_text() #returns text that were recorded
    messages.append({"Role":"User"," Content":text}) #
    response = send_to_chatGPT(messages) 
    SpeakText(response) #speaks

    print(response)
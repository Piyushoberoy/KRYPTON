import wolframalpha
import pyttsx3
import speech_recognition as sr
import random
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 125)


def say(audio):
    engine.say(audio)
    engine.runAndWait()


def user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizing')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said : {query}\n")
    except Exception:
        print("Say that again please")
        return 'None'
    return query

app_id = "TYAY5W-RP68QXQ496"
client = wolframalpha.Client(app_id)

while(True):
    say("Question")
    question = user().lower()
    res = client.query(question)
    answer = next(res.results).text

    say(answer)

import pyttsx3
import speech_recognition as sr
import datetime
import time
import webbrowser
import urllib
import os
import subprocess
import mysql.connector as ms
import wolframalpha as wa
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 125)

setup = ms.connect(host='localhost', user='root',
                   passwd='Piyush24@2002', database='KAVYA')
c = setup.cursor()

app_id = "TYAY5W-RP68QXQ496"
client = wa.Client(app_id)


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


def help1():
    say('How I can help you?')
    query = user().lower()
    if 'calculate' in query:
        say("If you need to calculate like addition, subtraction, multiplication, etc. You need to just say calculate then, I will ask you which type of calculation you wan't then you have to select just your choice and after typing numbers you will get your answer.")
    elif 'time' in query:
        say("If you need to know time, date and day then, you have to just say 'time' or 'what's the time dear' and something like that.")
    elif 'web' in query:
        say("If you need to open some websites like facebook, twitter, etc then, say your website name only. If it is not in my mind then I will direct you to one of my friend.")
    elif 'apps' or 'app' in query:
        say('If you need to open any application then, just say your application name I will open it for you. If it is not in my mind then I will direct you to one of my friend.')
    elif 'thank you' in query:
        say("You have clear your doubt. Let's proceed further.")
        main()
    else:
        say('Any more doubt, sir. If no then say thank you.')


def clock(query):
    day_of_month = time.strftime("%d")
    month = time.strftime("%B")
    month_num = time.strftime("%m")
    year = time.strftime("%Y")

    day = time.strftime("%A")

    hour = time.strftime("%I")
    minutes = time.strftime("%M")
    time_span = time.strftime("%p")

    if ('time' in query):
        say(hour+" "+minutes+" "+time_span)
        main()
    elif('date' in query):
        say(day_of_month+" "+month+" "+year)
    elif ('day' in query):
        say(day)
    elif ('month' in query):
        say(month)
    elif ('year'):
        say(year)
    else:
        help1()
    

def wishme():
    h = int(datetime.datetime.now().hour)
    if h >= 4 and h < 12:
        morning = ["Suprabhat", "Good morning", "Shubh prabhaat", "Guten Morgen", "Pairi pauna", "Saat sri kal ji"]
        say(random.choice(morning))
    elif h >= 12 and h < 18:
        afternoon = ["Shubh dopahar","Good afternoon","Guten Tag", "Pairi pauna", "Saat sri kal ji"]
        say('Good Afternoon sir')
    elif h >= 18 and h < 20:
        evening = ["Namaste", "Hey", "Hi", "Hello", "Good Evening"]
        say('Good Evening sir')
    else:
        say('Hello sir.')


def storage():

    say("Name")
    name = user().lower()

    say("Age")
    age = user().lower()

    say("Phone number")
    phone_number = user().lower()

    say("Date of birth")
    dob = user().lower()

    say("Gender")
    gender = user().lower()

    say("Email id")
    email_id = user().lower()

    say("Work")
    work = user().lower()

    say("Address")
    address = user().lower()
    try:
        d = "INSERT INTO CONTACT(NAME,AGE,PHONE_NUMBER,DOB,GENDER,EMAIL_ID,WORK,ADDRESS) VALUES('{}',{},{},'{}','{}','{}','{}','{}')".format(
            name, age, phone_number, dob, gender, email_id, work, address)
        c.execute(d)
        setup.commit()
    except:
        say("You have not entered the specified details.")


def Open_File():
    c.execute("Select * from files")
    d = c.fetchall()
    x = input("Enter folder name: ")
    l = []
    print(d)
    X = c.rowcount

    # Store each element of sql table in a list.
    for row in range(0, X):
        for col in d[row]:
            l.append(col)

    L = len(l)
    print(l)

    # To retrive particular folder path.
    for a in range(0, L):
        if x == l[a]:
            Z = l[a+1]
            print('Mission possible')
            os.startfile(Z)


'''
def files():
    say("Please tell me which file you wan't to open?")
    query=user().lower()
    if 'cu' in query:
        dir_f1="D:\\PIYUSH\\CU.docx"
        os.startfile(dir_f1)
    else:
        say("Your file is not there.")

def folders():
    say("Please tell me which folder you wan't to open?")
    query = user().lower()
    if 'Piyush' in query:
        dir_F1="D:\\PIYUSH"
        os.startfile(dir_F1)
    else:
        say("Your folder is not there. Do you wan't me to create it for you?")
        query=user().lower()
        #if 'yes' in query or 'ya' in query:
            #makefolder()
        #else:
        #    say('Okay! I will not create it.')
        #    main()
'''


def web(query):
    if 'google' in query:
        webbrowser.open('https://www.google.com/')
    elif 'youtube' in query:
        webbrowser.open('https://www.youtube.com/')

    elif 'facebook' in query:
        webbrowser.open('https://www.facebook.com/')

    elif 'twitter' in query:
        webbrowser.open('https://twitter.com/')

    else:
        say('Your website is not in my mind. Can I search this for you? Please say yes or no.')
        query = user().lower()
        if 'yes' in query:
            if 'yes' or 'yah' or 'ya' in query:
                say("I am directing you to the browser. Please enter your app name there or tell app name to my friend by clicking on the microphone. She will further guide you.")
                dir11 = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
                os.startfile(dir11)
            else:
                web()


def apps(query):
    if 'chrome' in query:
        say("Openning Chrome..")
        dir1 = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        os.startfile(dir1)
    elif 'mozilla' in query:
        say("Openning Mozilla..")
        dir2 = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        os.startfile(dir2)
    elif 'calculator' in query:
        say("Openning Calculator..")
        dir3 = "C:\\Windows\\System32\\calc.exe"
    elif 'python' in query:
        say("Openning Python..")
        dir4 = "D:\\PIYUSH\\PYTHON\\Lib\\idlelib\\idle.pyw"
        os.startfile(dir4)
    elif 'command' in query:
        say("Openning Command Prompt")
        dir5 = "C:\Windows\System32\cmd.exe"
        os.startfile(dir5)
    elif 'camera' in query:
        say("Openning Camera..")
        dir6 = "start microsoft.windows.camera:"
        subprocess.run(dir6, shell=True)

    elif 'folder' in query:
        Open_File()
    else:
        say("Sorry, your application is not in lapi. If you need it then you have to install it. Can I do this for you? Say yes or no.")
        query = user().lower()
        if 'yes' or 'yah' or 'ya' in query:
            say("Okay so, I am directing you to the Microsoft Edge. Please enter your app name there or tell app name to my friend by clicking on the microphone. She will further guide you.")
            dir11 = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            os.startfile(dir11)
        else:
            apps()


def main():
    while True:
        query = user().lower()
        if 'time' or 'date' or 'day' or 'month' or 'year' in query:
            clock(query)
        elif 'search' in query:
            web(query)
        elif 'open' in query:
            apps(query)
        elif 'wait' in query:
            say("Are you sure you want me to wait. Because if so then I will talk to you after your entered time.")
            query = user().lower()
            if 'yes' or 'yah' or 'ya' in query:
                say("Enter your time after which you wan't me to active.")
                T = int(
                    input("Enter your time after which you wan't me to active (in minutes):"))
                t = T*60
                time.sleep(t)
        elif 'help' in query:
            help1()
        elif 'store' or ('add' + 'details') in query:
            storage()
        elif 'bye' in query:
            say('Bye sir. have a nice day')
            break
        else:
            say("Are you saying something?")

wishme()
say('How I can help you?')
main()

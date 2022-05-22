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
from WINDOWS_SEARCH import *

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 180)

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
    
def Krypton(query):
    if 'name' in query or 'who' in query:
        say("I am Krypton your personal assistant")
    elif 'you do' in query or 'done' in query or 'alread' in query:
        say("I can store contact details, I have good general knowledge. I have also spend a lot of time in learning mathematics\
            and whenever, I fail to learn any new concepts, my friend Piyush, scold me. That's all my journey till now with my slim\
                friend Piyush.")
    elif 'where' in query or 'when' in query:
        say("I was created in Ambala Cantt on 16 June 2020.")
    elif "how are you" in query:
        feel=["I am fine", "Felling like I am surrounded with lots of data"]
        say(random.choice(feel))
    else:
        say("I am Krypton your personal assistant. I was created by Piyush on 16 June 2020.\
        Basically I was created for storing contact details, but, I have good general knowledge. I have also spend a lot of time in learning mathematics\
            and whenever, I fail to learn any new concepts, my friend Piyush, scold me. But I believe in Piyush, that one day he will make me so intelligent such that, no one\
                can beat me not even you. heeeeeee")

def wishme():
    h = int(datetime.datetime.now().hour)
    if h >= 4 and h < 12:
        morning = ["Suprabhat", "Good morning", "Shubh prabhaat", "Guten Morgen", "Pairi pauna", "Saat shri kaal ji"]
        say(random.choice(morning))
    elif h >= 12 and h < 18:
        afternoon = ["Shubh dopahar","Good afternoon","Guten Tag", "Pairi pauna", "Saat sri kal ji"]
        say(random.choice(afternoon))
    elif h >= 18 and h < 20:
        evening = ["Namaste", "Hey", "Hi", "Hello", "Good Evening"]
        say(random.choice(evening))
    else:
        say('Hello sir.')

def GK(question):
    res = client.query(question)
    answer= next(res.results).text
    print(answer)
    say(answer)
    
def DateModify(date):
    temp=date.split()# MM DD YYYY[24,april,02]
    D,M,Y="","",""
    for a in temp:
        try:
            int(a)
            try:
                Y=datetime.datetime.strptime(str(a),"%Y").year
            except:
                D=datetime.datetime.strptime(str(a), "%d").day
        except:
            M=datetime.datetime.strptime(a, "%B").month
    return str(Y)+"-"+str(M)+"-"+str(D)


def cross_check(name,age,phone_number,dob,gender,email_id,work,address):
    say("Let's cross check your data")
    print("Name: "+name)
    print("Age:", int(age))
    phone_number=int(str(phone_number).replace(" ",""))
    print("Phone Number:",phone_number)
    print("Date Of Birth: "+str(dob))
    print("Gender: "+str(gender))
    print("Email Id: "+str(email_id))
    print("Work: "+work)
    print("Address: "+str(address))
    say("Are all details correct? If not then please tell me which is not correct.")
    query=user().lower()
    l={}
    if 'no' in query or 'n' in query:
        print(1)
        l={"Name": name, 'Age':age, 'Phone number':phone_number, "Date of birth":dob, "Gender":gender, "Email id":email_id, "Work":work, "address":address}
        for a in l.keys():
            if a.lower() in query:
                say("Enter "+a+": ")
                l[a]=input("Enter "+a+": ")
        say("Let's save it.")
    else:
        say("Great! Let's save it.")
    return l.values()

def storage():
    say("Ok, let's start. Remember, if you skip any thing details will not be matched with pre-requisites of database, and nothing will be saved.")
    say("Tell me the name")
    name = user().lower()

    say("Age")
    age = user().lower()

    say("Phone number")
    phone_number = user().lower()

    say("Date of birth")
    dob = user().lower()

    say("Gender")
    gender = user().lower()

    say("Tell me the official Email id")
    email_id = user().lower()

    salutations=""
    if "fe" in gender:
        salutations=random.choice(["miss","missus"])
        gender="F"
    else:
        salutations="mister"
        gender="M"

    say("Where does "+salutations+" "+name+" work?")
    work = user().lower()

    say("Where does "+salutations+" "+name+" live?")
    address = user().lower()

    name,age,phone_number,dob,gender,email_id,work,address=cross_check(name,age,phone_number,dob,gender,email_id,work,address)
    
    try:
        d = "INSERT INTO CONTACT(NAME,AGE,PHONE_NUMBER,DOB,GENDER,EMAIL_ID,WORK,ADDRESS) VALUES('{}',{},{},'{}','{}','{}','{}','{}')".format(
            name, age, phone_number, DateModify(dob), gender, email_id, work, address)
        c.execute(d)
        setup.commit()
        say("Great! all done")
    except:
        say("Your entries does not matched with database pre-requisites.")

def make_notes():
    say("Important instructions! When you want to stop writing and want's to quit please say stop otherwise I will be writing everything that you will be speaking.\
        If you want me to hault writing then please say halt or pause and to continue your writing please say continue. You will find these notes in the Notes folder\
        with the file name as you specified")
    say("So I think you understand the instructions. Let's begin")
    say("Tell the file name with which you want to save it")
    query=user().lower()
    say("Cool! Let's do it")
    file=open("K:\KRYPTON\\"+query+".txt","a+")
    rep=True
    while True:
        if rep:
            query=user()
            file.writelines(query)
        elif 'halt' not in query or 'stop' not in query:
            rep=False
            query=user()
        elif 'continue' in query:
            rep=True
            say("Welcome back")
        elif 'exit' in query:
            say("Exiting")
            break
    say("File had been save successfully")

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
        say("I am directing you to the browser. Please enter your app name there or tell app name to my friend by clicking on the microphone. She will further guide you.")
        dir11 = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
        os.startfile(dir11)

def apps(query):
    app=['chrome', 'firefox', 'msedge', 'safari', 'opera', 'brave', 'vivaldi', 'duckduckgo']
    ch=False
    brdir="C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
    if 'check' in query or 'browser' in query:
        for a in app:
            if search(a):
                ch=True
                break
        if ch:
            say("Yes we got it!"+a.capitalize()+" is present in your system.")
        else:
            say("No, you do not have any browser installed in your system.")
    elif 'chrome' in query:
        say("Openning Chrome")
        os.startfile(brdir+"\Google Chrome.lnk")
    elif 'mozilla' in query:
        say("Openning Mozilla")
        os.startfile(brdir+"\Firefox.lnk")
    elif 'edge' in query:
        say("Openning Edge")
        os.startfile(brdir+"\Microsoft Edge.lnk")
    elif 'calculator' in query:
        say("Openning Calculator")
        os.startfile("C:\Windows\System32\calc.exe")
    elif 'python' in query:
        say("Openning Python")
        os.startfile("K:\PYTHON-3_8_8\Lib\idlelib\idle.pyw")
    elif 'command' in query:
        say("Openning Command Prompt")
        os.startfile("C:\Windows\system32\cmd.exe")
    elif 'camera' in query:
        say("Openning Camera")
        dir = "start microsoft.windows.camera:"
        subprocess.run(dir, shell=True)
    else:
        say("Sorry, your application is not in lapi. If you need it then, you have to install it. Can I do this thing for you?")
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
        if 'time' in query or 'date' in query or 'day' in query or 'month' in query or 'year' in query: # done
            clock(query)
        elif "your name" in query or "yourself" in query or 'wait' in query or 'hold' in query or 'pause' in query :
            if 'wait' in query or 'hold' in query or 'pause' in query:
                say("Okay. Tell me, after how many minutes you will be free?")
                T = user().lower()
                print(T)
                t = int(T)*60
                time.sleep(t)
            else:
                Krypton(query)
        elif 'what' in query or 'where' in query or 'when' in query or 'who' in query or 'do' in query or 'did' in query or 'how' in query:
            if 'you' in query:
                Krypton(query)
            else:
                try:
                    GK(query)
                except:
                    say("Sorry Geni. Can you rephrase it?")
        elif 'search' in query or 'web' in query or 'on browser' in query:
            web(query)
        elif 'app' in query or 'check' in query or 'browser' in query or 'application' in query or 'open' in query: # Can only check browsers
            apps(query) 
        elif 'help' in query or 'can you do' in query or 'abilities' in query:
            help1()
        elif 'details' in query or 'data' in query or 'contact' in query: # DONE
            storage()
        elif "note" in query:
            make_notes()
        elif 'bye' in query or 'by' in query:
            say('Bye sir. have a nice day')
            break
        # else:
        #     say("Are you saying something?")

wishme()
l=["What can I do to assist you?","How I can help you?","How can I assist you?","Is there anything I can do to assist you?","Is there anything I can do to help you?"]
say(random.choice(l))
main()


# Add content in document
import speech_recognition as sr 
import playsound # to play saved mp3 file 
from gtts import gTTS # google text to speech 
import os # to save/open files 
import wolframalpha # to calculate strings into formula 
from selenium import webdriver # to control browser operations 
import time
import datetime
import wikipedia
import smtplib
import webbrowser

num = 1


def assistant_speaks(output): 
	global num 

	# num to rename every audio file 
	# with different name to remove ambiguity 
	num += 1
	print("Kavya : ", output) 

	toSpeak = gTTS(text = output, lang ='en', slow = False) 
	# saving the audio file given by google text to speech 
	file = str(num)+".mp3"
	toSpeak.save(file) 
	
	# playsound package is used to play the same file. 
	playsound.playsound(file, True) 
	os.remove(file) 


# About Kavya
def Kavya():
	assistant_speaks("Sir, I am Kavya your personal AI assistant.")
	time.sleep(1)
	assistant_speaks("I can do many things, like searching for different websites, open different applications on your PC ,etc.")
	time.sleep(1)
	assistant_speaks("I was made by Piyush on 7 march 2020 at Ambala")
	'''time.sleep(2)
	assistant_speaks("")'''
	return


def get_audio(): 

	rObject = sr.Recognizer() 
	audio = '' 

	with sr.Microphone() as source: 
		print("Speak...") 
		
		# recording the audio using speech recognition 
		audio = rObject.listen(source, phrase_time_limit = 5) 
	print("Stop.") # limit 5 secs 

	try: 

		text = rObject.recognize_google(audio, language ='en-US') 
		print("You : ", text) 
		return text 

	except: 

		assistant_speaks("Could not understand your audio, PLease try again !")
		return 0
def wiki(input):
#	if summary in input:
	assistant_speaks(wikipedia.summary(input,sentences=2))
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('ynr24piyush@gmail.com', 'vpSP4#chd@ynr')
    server.sendmail('ynr24piyush@gmail.com', to, content)
    server.close()
#piyushoberoi14

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        assistant_speaks("Good Morning Sir! How I can help you?")

    elif hour>=12 and hour<18:
        assistant_speaks("Good Afternoon Sir! How I can help you?")   

    else:
        assistant_speaks("Good Evening Sir! How I can help you?")
        

def search_web(input): 

	driver = webdriver.Firefox() 
	driver.implicitly_wait(1) 
	driver.maximize_window() 

	if 'youtube' in input.lower(): 

		assistant_speaks("Opening in youtube") 
		indx = input.lower().split().index('youtube') 
		query = input.split()[indx + 1:] 
		driver.get("http://www.youtube.com/results?search_query =" + '+'.join(query)) 
		return

	elif 'wikipedia' in input.lower(): 

#		assistant_speaks("Opening Wikipedia") 
		wiki(input)
		'''indx = input.lower().split().index('wikipedia') 
		query = input.split()[indx + 1:] 
		driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query)) '''
		return

	else: 

		if 'google' in input: 

			indx = input.lower().split().index('google') 
			query = input.split()[indx + 1:] 
			driver.get("https://www.google.com/search?q =" + '+'.join(query)) 

		elif 'search' in input: 

			indx = input.lower().split().index('google') 
			query = input.split()[indx + 1:] 
			driver.get("https://www.google.com/search?q =" + '+'.join(query)) 

		else: 

			driver.get("https://www.google.com/search?q =" + '+'.join(input.split())) 

		return

#Wikipedia
def wiki(input):
#	if summary in input:
	assistant_speaks(wikipedia.summary(input,sentences=2))
#	elif search in input:
#		assistant_speaks(wikipedia.search(input))
#	else:
#		pass


# function used to open application present inside the system. 
def open_application(input): 

	if "chrome" in input: 
		assistant_speaks("Opening Google Chrome") 
		os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe') 
		return

	elif "firefox" in input or "mozilla" in input: 
		assistant_speaks("Opening Mozilla Firefox") 
		os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe') 
		return

	elif "word" in input: 
		assistant_speaks("Opening Microsoft Word") 
		os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2007\\Word 2007.lnk') 
		return

	elif "excel" in input: 
		assistant_speaks("Opening Microsoft Excel") 
		os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk') 
		return

	else: 

		assistant_speaks("Application not available") 
		return


def process_text(input): 
	try: 
		if 'search' in input or 'play' in input: 
			# a basic web crawler using selenium 
			search_web(input) 
			return

		elif "who are you" in input or "define yourself" in input or "tell me something about you" in  input: 
			Kavya()
			return

		elif "who made you" in input or "created you" in input: 
			speak = "I was created by Piyush."
			assistant_speaks(speak) 
			return
		
		elif "what's your age" in input or "how old are you" in input or "age" in input:
			x = 0
			d=datetime.datetime.today()
			m=d.month
			n = m-3
			x += n
			speak="I am " + str(x) + " months old"
			assistant_speaks(speak)
			return
		
		    
		   
		elif "time" in input:
			t=datetime.datetime.now()
			speak="The time is" + str(t)
			assistant_speaks(speak)
			return

		elif "date" in input:
			d=datetime.datetime.today()
			speak="today is " + str(d)
			assistant_speaks(speak)
			return

		elif "calculate" in input.lower(): 
			
			# write your wolframalpha app_id here 
			app_id = "WOLFRAMALPHA_APP_ID"
			client = wolframalpha.Client(app_id) 

			indx = input.lower().split().index('calculate') 
			query = input.split()[indx + 1:] 
			res = client.query(' '.join(query)) 
			answer = next(res.results).text 
			assistant_speaks("The answer is " + answer) 
			return

		elif 'open' in input: 
			
			# another function to open 
			# different application availaible 
			open_application(input.lower()) 
			return

		#elif 'what is' or 'what are' or 'when'
		'''
		elif 'email' in input:
				try:
					  assistant_speaks("What should I say?")
					  content =str(get_audio()).lower
					  to = "@gmail.com"    
					  sendEmail(to, content)
					  assistant_speaks("Email has been sent!")
				except Exception as e:
					  print(e)
					  assistant_speaks("Sorry sir. I am not able to send this email")
		''elif wikipedia in input:
			wiki(input.lower())
			return'''


	except : 
		assistant_speaks("I don't understand, can you speak again") 
		ans = str(get_audio()).lower
		if 'yes' in str(ans) or 'yeah' in str(ans) or "sure" in str(ans): 
			process_text(ans) 


# Driver Code 
if __name__ == "__main__": 
	wishMe()
	name ='YOU'
	def loop():
		while(1): 

			text = str(get_audio()).lower() 

			if text == 0: 
				continue
			process_text(text)
			try:
				if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text): 
					assistant_speaks("Ok bye, sir. Take care.")
					break
			except:
				assistant_speaks("Anything else sir")
				response = str(get_audio()).lower
				if response == 'yes' or response == 'yeah' or response == 'yo':
					assistant_speaks('Yes sir')
					name = get_audio()
					text = str(get_audio()).lower()
					process_text(text)
				else:
					assistant_speaks("Ok bye, sir.")
					assistant_speaks("Take care.")
					break
			# calling process text to process the query 
			 
	
	loop()

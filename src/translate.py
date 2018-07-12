BING_KEY = "470a14b2102b40478d4eff8ccda2614e"
import speech_recognition as sr
def translate(data):
	r = sr.Recognizer()
	with sr.AudioFile(data) as source:
		audio = r.record(source)
	try:
		print "bing: ", r.recognize_bing(audio, key = BING_KEY)
		#print "sphinx: ", r.recognize_sphinx(audio)
	except sr.UnknownValueError:
		print "error"
	except sr.RequestError as e:
		print e

# 使用BING将音频转为文字（英文）
# BING的免费KEY，有使用次数和期限限制（应该已经过期了）
BING_KEY = "470a14b2102b40478d4eff8ccda2614e"

# 用speech_recognition包，可以支持多种语音识别api
# https://pypi.org/project/SpeechRecognition/
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

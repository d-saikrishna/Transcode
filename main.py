import speech_recognition as sr



# Initialize the Recognizer that recognises audio.
r = sr.Recognizer()

# To recognise live voice.
with sr.Microphone() as source:
    print('Speak Anything :')
    audio = r.listen(source)

    text = r.recognize_google(audio)
    print('You said : {}'.format(text))

#

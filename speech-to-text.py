import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

def speak(text):
    print(f"🤖 CHILD: {text}")
    engine = pyttsx3.init()          
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)   
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

with sr.Microphone() as source:
    print("Adjusting for ambient noise...")
    r.adjust_for_ambient_noise(source)
    speak("Hey, I'm ready! Start talking whenever you want.")

    while True:
        try:
            print("🎧 Listening...")
            audio = r.listen(source, timeout=30 , phrase_time_limit=40)
            text = r.recognize_google(audio)
            print("🗣️ You said:", text)
            speak(f"You said: {text}")

        except sr.WaitTimeoutError:
            print("⏳ No speech detected...")
        except sr.UnknownValueError:
            print("😶 Didn't catch that.")
            speak("Sorry, I didn’t quite get that.")
        except KeyboardInterrupt:
            speak("Okay, bye!")
            break

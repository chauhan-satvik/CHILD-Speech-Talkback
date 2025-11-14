import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from dotenv import load_dotenv
import os
# === CONFIGURATION ===
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
r = sr.Recognizer()

def speak(text):
    """Speak and print the response"""
    print(f"🤖 CHILD: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)   # 0 = male, 1 = female
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def ask_gemini(prompt):
    """Send user input to Gemini and return AI response"""
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")  # Fast, free model
        response = model.generate_content(f"Respond as CHILD(Cognitive Highly-configurable Integrated Learning Device), Satvik's AI humanoid assistant, keep it kinda gen-z and professional something that a humanoid would sound like, dont give really descriptive answer try to make it short and sweet day-to-day, conversation type!.  Satvik said: {prompt}")
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini error:", e)
        return "Sorry Satvik, I couldn’t connect to my neural core right now."

# === MAIN LOOP ===
with sr.Microphone() as source:
    print("🎤 Adjusting for ambient noise...")
    r.adjust_for_ambient_noise(source)
    speak("Hey Satvik, CHILD is online and ready!")

    while True:
        try:
            print("🎧 Listening...")
            audio = r.listen(source, timeout=40, phrase_time_limit=60)
            text = r.recognize_google(audio)
            print(f"🗣️ You said: {text}")

            # Check for exit keywords
            if "goodbye" in text.lower() or "bye" in text.lower():
                speak("Goodbye Satvik, shutting down now.")
                break

            #  AI reply from Gemini
            reply = ask_gemini(text)
            speak(reply)

        except sr.WaitTimeoutError:
            print("⏳ No speech detected...")
        except sr.UnknownValueError:
            print("😶 Didn't catch that.")
            speak("Sorry, I didn’t quite get that.")
        except KeyboardInterrupt:
            speak("Okay, bye Satvik!")
            break

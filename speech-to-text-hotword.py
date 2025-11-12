import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

def speak(text):
    print(f"🤖 CHILD: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# --- Start listening ---
with sr.Microphone() as source:
    print("Adjusting for ambient noise, wait 1 sec...")
    r.adjust_for_ambient_noise(source)
    speak("Hey Satvik, I'm ready. Start talking whenever you want!")

    while True:
        try:
            print("🎧 Listening...")
            audio = r.listen(source, timeout=15, phrase_time_limit=15)
            text = r.recognize_google(audio)
            text_lower = text.lower()
            print(f"🗣️ You said: {text}")

            # 🔥 HOTWORD LOGIC
            if "hello child" in text_lower or "hey child" in text_lower:
                speak("Hello Satvik! Nice to hear from you again 😄")

            elif "what is special about you" in text_lower:
                speak("I'm CHILD(Cognitive Highly-configurable Learning Device), your Artificially Intelligent humanoid system, ready to serve you!")

            elif "can you help me with anything" in text_lower :
                speak("Yes i can help you with day-to-day tasks and elderly care!")

            elif "goodbye" in text_lower or "bye" in text_lower:
                speak("Goodbye Satvik, see you soon!")
                break

            # 🧠 Normal fallback talkback
            else:
                speak(f"You said: {text}")

        except sr.WaitTimeoutError:
            print("⏳ No speech detected, listening again...")
            continue
        except sr.UnknownValueError:
            print("😶 Didn't catch that, try again...")
            speak("Sorry, I didn’t quite get that.")
        except KeyboardInterrupt:
            speak("Okay, shutting down now. Bye!")
            break

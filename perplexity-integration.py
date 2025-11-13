import speech_recognition as sr
import pyttsx3
import requests
from dotenv import load_dotenv
import os

# === LOAD API KEY ===
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

r = sr.Recognizer()

def speak(text):
    """Speak and print CHILD's response"""
    print(f"🤖 CHILD: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # female voice (change to 0 for male)
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def ask_perplexity(prompt):
    """Send prompt to Perplexity AI and return its response"""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "sonar-pro",  
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Respond as CHILD (Cognitive Highly-configurable Integrated Learning Device), "
                        "AI humanoid assistant, who replies just like human keeping the conversation real and little sarcastic. Keep replies short, Gen-Z, natural, friendly, "
                        "and conversational like a human. Don't explain too much. "
                        f"Satvik said: {prompt}"
                    )
                }
            ]
        }

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("⚠️ Perplexity error:", e)
        return "Sorry Satvik, I couldn’t connect to my Perplexity brain right now."


# === MAIN VOICE LOOP ===
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

            # Exit logic
            if "goodbye" in text.lower() or "bye" in text.lower():
                speak("Goodbye Satvik, shutting down now.")
                break

            # Ask Perplexity
            reply = ask_perplexity(text)
            speak(reply)

        except sr.WaitTimeoutError:
            print("⏳ No speech detected...")
        except sr.UnknownValueError:
            print("😶 Didn't catch that.")
            speak("Sorry, I didn’t quite get that.")
        except KeyboardInterrupt:
            speak("Okay, bye Satvik!")
            break
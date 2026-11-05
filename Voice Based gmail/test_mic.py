import speech_recognition as sr

print("Testing microphone...")
recognizer = sr.Recognizer()

print("\nAvailable microphones:")
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"  {i}: {name}")

print("\n[LISTENING] Speak now (5 seconds)...")

try:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        text = recognizer.recognize_google(audio)
        print(f"[SUCCESS] You said: {text}")
except Exception as e:
    print(f"[ERROR] {e}")
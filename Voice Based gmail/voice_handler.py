import speech_recognition as sr
import pyttsx3
import threading
from config import Config

class VoiceHandler:
    """Handles voice input and output"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self._configure_tts()

    def _configure_tts(self):
        """Configure text-to-speech engine"""
        # Set properties
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level

        # Try to set a clear voice
        voices = self.engine.getProperty('voices')
        if voices:
            # Prefer female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break

    def speak(self, text):
        """Convert text to speech"""
        print(f"[SYSTEM]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def speak_async(self, text):
        """Speak text asynchronously (non-blocking)"""
        print(f"[SYSTEM]: {text}")
        thread = threading.Thread(target=self._speak_thread, args=(text,))
        thread.start()

    def _speak_thread(self, text):
        """Thread function for async speech"""
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, prompt=None, timeout=None, phrase_limit=None):
        """Listen for voice input"""
        if prompt:
            self.speak(prompt)

        timeout = timeout or Config.SPEECH_TIMEOUT
        phrase_limit = phrase_limit or Config.PHRASE_TIME_LIMIT

        try:
            with sr.Microphone() as source:
                print("[LISTENING...]")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )

                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                print(f"[USER]: {text}")
                return text.lower().strip()

        except sr.WaitTimeoutError:
            self.speak("I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            self.speak("Sorry, I couldn't understand that. Please speak clearly.")
            return None
        except sr.RequestError as e:
            self.speak("Sorry, there was an error with the speech recognition service.")
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            self.speak("An error occurred while listening.")
            print(f"Error in listen: {e}")
            return None

    def confirm(self, question):
        """Ask a yes/no confirmation question"""
        while True:
            response = self.listen(f"{question} Say YES or NO.")

            if response is None:
                continue

            if 'yes' in response or 'yeah' in response or 'yup' in response:
                return True
            elif 'no' in response or 'nope' in response:
                return False
            else:
                self.speak("Please say YES or NO.")

    def get_input_with_confirmation(self, prompt, confirmation_text=None):
        """Get voice input with confirmation"""
        while True:
            result = self.listen(prompt)

            if result is None:
                continue

            # Confirm the input
            if confirmation_text:
                confirm_msg = f"{confirmation_text} {result}"
            else:
                confirm_msg = f"You said {result}"

            if self.confirm(confirm_msg):
                return result
            else:
                self.speak("Let's try again.")

    def get_email_address(self):
        """Get email address with special handling"""
        self.speak("Please say the receiver's email address slowly. For example, say john dot smith at gmail dot com")

        while True:
            email_input = self.listen(phrase_limit=15)

            if email_input is None:
                continue

            # Convert speech to email format
            email = self._convert_to_email(email_input)

            if email:
                if self.confirm(f"You said {email}"):
                    return email
                else:
                    self.speak("Let's try again.")
            else:
                self.speak("Invalid email format. Please try again.")

    def _convert_to_email(self, speech_text):
        """Convert spoken email to email format"""
        # Replace common speech patterns
        email = speech_text.replace(' at ', '@')
        email = email.replace(' dot ', '.')
        email = email.replace(' ', '')

        # Basic validation
        if '@' in email and '.' in email.split('@')[1]:
            return email
        return None

    def get_menu_choice(self, options):
        """Get user's menu choice from a list of options"""
        while True:
            # Announce options
            options_text = ", ".join(options)
            self.speak(f"Available options are: {options_text}. Please say your choice.")

            choice = self.listen()

            if choice is None:
                continue

            # Match choice
            for option in options:
                if option.lower() in choice:
                    return option

            self.speak("Invalid option. Please try again.")

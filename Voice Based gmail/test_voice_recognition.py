"""
Test Voice Recognition - See What Google Hears
This helps you understand how to pronounce your password correctly
"""

from voice_handler import VoiceHandler

def main():
    voice = VoiceHandler()

    print("\n" + "="*70)
    print("  TEST VOICE RECOGNITION")
    print("="*70)
    print("\nThis tool will help you see what Google Speech Recognition hears")
    print("when you speak. Use this to test your password pronunciation.")
    print("\n" + "="*70)

    while True:
        print("\n>>> Please speak your password (or type 'quit' to exit)")
        print(">>> Listening...")

        result = voice.listen(timeout=10)

        if result:
            print(f"\n>>> GOOGLE HEARD: '{result}'")
            print(f">>> LENGTH: {len(result)} characters")

            # Check for common issues
            if ' ' in result:
                print("\n[!] WARNING: Contains spaces")
                print("    Password will be stored with spaces")
                print("    Make sure to say it the same way every time")

            if any(char.isdigit() for char in result):
                print("\n[!] WARNING: Contains numbers")
                print("    Speech recognition may hear numbers differently")
                print("    Example: '1' might be heard as 'one', 'won', or 'wan'")

            # Show some alternatives that might sound similar
            check_alternatives(result)

        else:
            print("\n>>> FAILED TO RECOGNIZE")
            print("    Possible reasons:")
            print("    - Timeout (you didn't speak within 10 seconds)")
            print("    - Too quiet")
            print("    - Too much background noise")
            print("    - No internet connection")

        print("\n" + "-"*70)
        continue_test = input("Test again? (y/n): ")
        if continue_test.lower() != 'y':
            break

    print("\n" + "="*70)
    print("  TIPS FOR BETTER RECOGNITION")
    print("="*70)
    print("""
    1. Use simple, common English words
       Good: "hello", "welcome", "sunshine"
       Bad: "p4ssw0rd", "my_pass"

    2. Speak clearly and at moderate pace
       - Not too fast
       - Not too slow
       - Natural speaking voice

    3. Use a quiet environment
       - Minimize background noise
       - Close windows
       - Turn off fans/AC if possible

    4. Use a good microphone
       - Headset microphone is best
       - Built-in laptop mics work but are less accurate

    5. Be consistent
       - Say the password the SAME WAY every time
       - Same pace, same pronunciation

    6. Test before setting password
       - Use this tool to test words first
       - Make sure Google recognizes them consistently
       - Then set that as your password
    """)

    print("\n" + "="*70 + "\n")

def check_alternatives(word):
    """Check for common misheard words"""
    # Common homophones and similar sounding words
    alternatives = {
        'to': ['two', 'too'],
        'two': ['to', 'too'],
        'too': ['to', 'two'],
        'for': ['four', 'fore'],
        'four': ['for', 'fore'],
        'ate': ['eight'],
        'eight': ['ate'],
        'one': ['won', 'wan'],
        'won': ['one'],
        'here': ['hear'],
        'hear': ['here'],
        'there': ['their', 'they\'re'],
        'their': ['there', 'they\'re'],
        'buy': ['by', 'bye'],
        'by': ['buy', 'bye'],
        'no': ['know'],
        'know': ['no'],
        'see': ['sea'],
        'sea': ['see'],
    }

    words = word.lower().split()
    found_alternatives = False

    for w in words:
        if w in alternatives:
            if not found_alternatives:
                print("\n[!] SIMILAR SOUNDING WORDS DETECTED:")
                found_alternatives = True
            print(f"    '{w}' might be confused with: {', '.join(alternatives[w])}")

    if found_alternatives:
        print("    TIP: Avoid using these words in passwords")

if __name__ == "__main__":
    main()

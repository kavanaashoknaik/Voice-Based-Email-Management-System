"""
Debug script to help diagnose login issues
This script will help you:
1. Check what users exist in the database
2. Test password verification
3. Show what the voice system is hearing
"""

from database import Database
from voice_handler import VoiceHandler
import hashlib

def main():
    db = Database()
    voice = VoiceHandler()

    print("\n" + "="*70)
    print("  VOICE LOGIN DEBUG TOOL")
    print("="*70)

    # Show all users in database
    print("\n1. CHECKING DATABASE USERS...")
    print("-" * 70)
    users = db.get_all_users()

    if not users:
        print("❌ NO USERS FOUND IN DATABASE!")
        print("\nYou need to create a user first.")
        print("Go to: http://localhost:5000/admin/login")
        print("Login: admin / admin")
        print("Then add a new user.")
        return

    print(f"✓ Found {len(users)} user(s):")
    for user in users:
        status = "ACTIVE" if user['is_active'] else "INACTIVE"
        print(f"   - Username: {user['username']}")
        print(f"     Gmail: {user['gmail_address']}")
        print(f"     Status: {status}")

    # Test voice recognition
    print("\n" + "="*70)
    print("2. TESTING VOICE RECOGNITION")
    print("="*70)
    print("\nWe'll now test if your microphone is working correctly.")
    print("This will help identify if the issue is with speech recognition.")

    proceed = input("\nDo you want to test voice recognition? (y/n): ")
    if proceed.lower() != 'y':
        print("Skipping voice test.")
        return

    # Test username recognition
    print("\n" + "-"*70)
    print("TEST 1: Username Recognition")
    print("-"*70)
    voice.speak("Please say your username")
    username = voice.listen(timeout=10)

    if username:
        print(f"✓ Heard username: '{username}'")
    else:
        print("❌ Failed to recognize username")
        print("Possible issues:")
        print("  - Microphone not working")
        print("  - No internet connection (Google Speech API needs internet)")
        print("  - Timeout (spoke too late)")
        return

    # Test password recognition
    print("\n" + "-"*70)
    print("TEST 2: Password Recognition")
    print("-"*70)
    voice.speak("Please say your password")
    password = voice.listen(timeout=10)

    if password:
        print(f"✓ Heard password: '{password}'")
    else:
        print("❌ Failed to recognize password")
        print("Same issues as username test apply here.")
        return

    # Test password verification
    print("\n" + "="*70)
    print("3. TESTING PASSWORD VERIFICATION")
    print("="*70)

    # Show what hash would be generated
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"\nUsername entered: '{username}'")
    print(f"Password entered: '{password}'")
    print(f"Password hash: {password_hash}")

    # Try to verify
    user_data = db.verify_user(username, password)

    print("\n" + "-"*70)
    if user_data:
        print("✓✓✓ LOGIN SUCCESSFUL! ✓✓✓")
        print(f"Logged in as: {user_data['username']}")
        print(f"Gmail: {user_data['gmail_address']}")
        print("\nYour voice login SHOULD work with these credentials.")
    else:
        print("❌❌❌ LOGIN FAILED! ❌❌❌")
        print("\nPossible reasons:")
        print("  1. Username doesn't exist in database")
        print("  2. Password doesn't match what's stored")
        print("  3. Voice recognition is mishearing your password")
        print("\n" + "="*70)
        print("TROUBLESHOOTING STEPS:")
        print("="*70)

        # Check if username exists
        print("\n1. Checking if username exists...")
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, voice_password_hash FROM users WHERE username = ?", (username,))
        user_check = cursor.fetchone()
        conn.close()

        if not user_check:
            print(f"   ❌ Username '{username}' NOT FOUND in database")
            print(f"\n   Available usernames:")
            for user in users:
                print(f"      - {user['username']}")
            print("\n   ISSUE: Speech recognition may be mishearing your username")
            print("   TIP: Try speaking more clearly and slowly")
        else:
            print(f"   ✓ Username '{username}' exists")
            stored_hash = user_check['voice_password_hash']
            print(f"\n   Stored password hash: {stored_hash}")
            print(f"   Your password hash:   {password_hash}")

            if stored_hash == password_hash:
                print("   ✓ Hashes match! (This shouldn't happen if login failed)")
            else:
                print("   ❌ Hashes DON'T match!")
                print("\n   ISSUE: The password you spoke doesn't match what's stored")
                print("   LIKELY CAUSE: Speech recognition is mishearing your password")
                print("\n   SOLUTIONS:")
                print("   A. Speak your password more clearly and slowly")
                print("   B. Use a simpler password (avoid similar sounding words)")
                print("   C. Manually test: Run this script again and try different pronunciations")

    # Additional diagnostic info
    print("\n" + "="*70)
    print("4. COMMON SPEECH RECOGNITION ISSUES")
    print("="*70)
    print("""
    Speech Recognition Problems:

    1. Similar Sounding Words:
       - "to" vs "two" vs "too"
       - "for" vs "four"
       - "ate" vs "eight"
       - Solution: Use unique, clearly distinct words

    2. Background Noise:
       - Use a quiet environment
       - Microphone may pick up ambient sounds
       - Solution: Use headset microphone

    3. Speaking Speed:
       - Speaking too fast: words get jumbled
       - Speaking too slow: system may timeout
       - Solution: Speak at moderate, natural pace

    4. Pronunciation:
       - Accents affect recognition
       - Google Speech API trained on standard pronunciations
       - Solution: Enunciate clearly

    5. Internet Connection:
       - Google Speech Recognition requires internet
       - Slow connection = recognition delays/failures
       - Solution: Check your internet connection

    6. Password Tips:
       - Use simple, common words
       - Avoid special characters or numbers (unless saying "one", "two", etc.)
       - Example: "blue sky morning" instead of "bluesky123"
    """)

    print("\n" + "="*70)
    print("5. RECOMMENDATIONS")
    print("="*70)
    print("""
    To fix your login issue:

    1. Create a new test user with a SIMPLE password
       - Password example: "hello world"
       - Go to admin panel and add user

    2. Test with the simple password first
       - If this works, the issue is your current password
       - If this fails, the issue is your microphone/internet

    3. Practice saying your password
       - Run this debug script multiple times
       - See how Google recognizes your speech
       - Adjust pronunciation until recognized correctly

    4. Use the debug script before actual login
       - Make sure your mic is working
       - Make sure internet is connected
       - Verify password is recognized correctly
    """)

    print("\n" + "="*70)
    print("END OF DEBUG SESSION")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

"""
Voice Commands Reference for Voice-Based Gmail System
This script displays all available voice commands in the terminal
"""

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_command(command, description):
    """Print a voice command with description"""
    print(f"  • {command:<30} - {description}")

def show_all_voice_commands():
    """Display all voice commands"""

    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#" + "  VOICE-BASED GMAIL SYSTEM - ALL VOICE COMMANDS".center(68) + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)

    # Login Commands
    print_section("1. LOGIN SCREEN")
    print("\n  System will ask for:")
    print_command("Say your username", "Speak your username clearly")
    print_command("Say your password", "Speak your voice password")

    # Main Menu Commands
    print_section("2. MAIN MENU")
    print_command("Compose Email", "Start composing a new email")
    print_command("Check Inbox", "View your inbox emails")
    print_command("Check Sent Mail", "View your sent emails")
    print_command("Logout", "Log out from the system")

    # Email Composition Commands
    print_section("3. COMPOSE EMAIL")
    print("\n  Recipient Email Address:")
    print_command("john dot smith at gmail dot com", "Converts to: john.smith@gmail.com")
    print_command("example at yahoo dot com", "Converts to: example@yahoo.com")

    print("\n  Confirmations:")
    print_command("YES / Yeah / Yup", "Confirm the input")
    print_command("NO / Nope", "Reject and retry")

    print("\n  Final Actions:")
    print_command("SEND", "Send the composed email")
    print_command("CANCEL", "Cancel and discard email")

    # Inbox Navigation Commands
    print_section("4. INBOX NAVIGATION")

    print("\n  Basic Navigation:")
    print_command("READ", "Read the current email message")
    print_command("NEXT", "Move to next email")
    print_command("PREVIOUS / BACK", "Move to previous email")
    print_command("STOP / EXIT", "Return to main menu")

    print("\n  Jump to Specific Email (Auto-reads the email):")
    print_command("FIRST / ONE / 1", "Jump to email #1")
    print_command("SECOND / TWO / 2", "Jump to email #2")
    print_command("THIRD / THREE / 3", "Jump to email #3")
    print_command("FOURTH / FOUR / 4", "Jump to email #4")
    print_command("FIFTH / FIVE / 5", "Jump to email #5")
    print_command("SIXTH / SIX / 6", "Jump to email #6")
    print_command("SEVENTH / SEVEN / 7", "Jump to email #7")
    print_command("EIGHTH / EIGHT / 8", "Jump to email #8")
    print_command("NINTH / NINE / 9", "Jump to email #9")
    print_command("TENTH / TEN / 10", "Jump to email #10")

    print("\n  After Reading Email:")
    print_command("REPEAT", "Hear the current email again")
    print_command("NEXT", "Move to next email")
    print_command("PREVIOUS", "Move to previous email")
    print_command("NUMBER (1-10)", "Jump to another email")
    print_command("STOP / EXIT", "Return to main menu")

    # Sent Mail Navigation Commands
    print_section("5. SENT MAIL NAVIGATION")
    print_command("NEXT", "View next sent email")
    print_command("STOP", "Return to main menu")

    # Web Interface Commands
    print_section("6. WEB INTERFACE (Keyboard)")
    print_command("SPACEBAR", "Stop auto-read OR activate voice recognition")
    print_command("Mouse Click", "Alternative to voice commands (buttons)")

    # Additional Tips
    print_section("7. VOICE COMMAND TIPS")
    print("\n  Email Format:")
    print("    - Say 'dot' for periods (.)")
    print("    - Say 'at' for @ symbol")
    print("    - Speak slowly and clearly")
    print("    Example: 'test dot user at gmail dot com' -> test.user@gmail.com")

    print("\n  Speech Recognition:")
    print("    - Speak at moderate pace")
    print("    - Use quiet environment")
    print("    - Wait for system prompts")
    print("    - Internet required for recognition")

    print("\n  Number Recognition Variants:")
    print("    The system recognizes multiple ways to say numbers:")
    print("    - 'two' or 'to' -> Email 2")
    print("    - 'four' or 'for' -> Email 4")
    print("    - 'eight' or 'ate' -> Email 8")
    print("    - 'one' or 'wan' -> Email 1")

    print("\n  Auto-Read Feature:")
    print("    - First 3 emails auto-read on inbox/sent pages")
    print("    - Press SPACEBAR anytime to stop reading")
    print("    - 500 character limit per email message")

    # System Response Examples
    print_section("8. SYSTEM RESPONSES (What You'll Hear)")
    print("\n  Login:")
    print("    'Welcome to Voice Email System'")
    print("    'Please say your username'")
    print("    'Please say your password'")
    print("    'Login successful. Welcome [username]'")

    print("\n  Inbox:")
    print("    'You have X emails in inbox. Y unread'")
    print("    'Email 1 of 10. From [sender]. Subject: [subject]'")
    print("    'Say READ, NEXT, PREVIOUS, a NUMBER, or STOP'")

    print("\n  After Reading:")
    print("    'Message: [email body - first 500 chars]'")
    print("    'Say NEXT, PREVIOUS, NUMBER, REPEAT, or STOP'")

    print("\n  Compose:")
    print("    'Let's compose an email'")
    print("    'Please say the receiver's email address slowly'")
    print("    'You said [email]. Say YES or NO'")
    print("    'Email sent successfully'")

    # Configuration
    print_section("9. SYSTEM CONFIGURATION")
    print("\n  Timeouts:")
    print("    - Speech timeout: 10 seconds")
    print("    - Phrase time limit: 15 seconds")
    print("    - Session timeout: 30 minutes")

    print("\n  Login Attempts:")
    print("    - Maximum attempts: 3")
    print("    - After 3 failures: Session ends")

    print("\n  Email Limits:")
    print("    - Inbox fetch: 10 emails max")
    print("    - Sent mail fetch: 5 emails max")
    print("    - Auto-read: 3 emails")
    print("    - Message display: 500 characters")

    # Quick Reference Card
    print_section("10. QUICK REFERENCE CARD")
    print("""
    +-------------------------------------------------------------------+
    |  LOCATION          |  SAY THIS                                   |
    +-------------------------------------------------------------------+
    |  Login             |  [Your username] -> [Your password]         |
    |  Main Menu         |  Compose / Inbox / Sent Mail / Logout       |
    |  Compose Email     |  [Email] -> YES -> [Subject] -> [Message]   |
    |  Inbox             |  READ / NEXT / PREVIOUS / FIRST-TENTH       |
    |  After Reading     |  NEXT / PREVIOUS / REPEAT / NUMBER / STOP   |
    |  Sent Mail         |  NEXT / STOP                                |
    |  Anytime           |  STOP / EXIT (to go back)                   |
    +-------------------------------------------------------------------+
    """)

    print("\n" + "#" * 70)
    print("#" + " " * 68 + "#")
    print("#" + "  END OF VOICE COMMANDS REFERENCE".center(68) + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70 + "\n")

if __name__ == "__main__":
    show_all_voice_commands()

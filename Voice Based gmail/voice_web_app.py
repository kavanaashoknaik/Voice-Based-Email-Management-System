from flask import Flask, render_template, jsonify, request, session
from voice_handler import VoiceHandler
from email_handler import EmailHandler
from database import Database
from config import Config
import threading
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize components
db = Database()
voice = VoiceHandler()

# Global state for voice session
voice_session_active = False
current_user_data = None

@app.route('/')
def index():
    """Home page with voice session option"""
    return render_template('voice_web.html')

@app.route('/start_voice_login')
def start_voice_login():
    """Start voice login process"""
    global voice_session_active
    voice_session_active = True

    # Start voice login in a thread
    threading.Thread(target=voice_login_process, daemon=True).start()

    return jsonify({'status': 'started', 'message': 'Voice login started'})

def voice_login_process():
    """Voice login process running in background"""
    global current_user_data, voice_session_active

    voice.speak("Welcome to Voice Email System. Please say your username.")

    max_attempts = Config.MAX_LOGIN_ATTEMPTS
    attempts = 0

    while attempts < max_attempts and voice_session_active:
        # Get username
        username = voice.listen(timeout=10)

        if username is None:
            attempts += 1
            continue

        voice.speak("Please say your password.")

        # Get password
        password = voice.listen(timeout=10)

        if password is None:
            attempts += 1
            continue

        # Verify credentials
        user_data = db.verify_user(username, password)

        if user_data:
            current_user_data = user_data
            voice.speak(f"Login successful. Welcome {username}.")
            voice_main_menu()
            break
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                voice.speak(f"Invalid credentials. You have {remaining} attempts remaining.")
            else:
                voice.speak("Maximum login attempts reached. Goodbye.")

    voice_session_active = False

def voice_main_menu():
    """Voice main menu"""
    global current_user_data, voice_session_active

    email_handler = EmailHandler(
        current_user_data['gmail_address'],
        current_user_data['gmail_app_password']
    )

    while voice_session_active:
        options = ["Compose Email", "Check Inbox", "Check Sent Mail", "Logout"]
        voice.speak("Available options are: Compose Email, Check Inbox, Check Sent Mail, Logout. Please say your choice.")

        choice = voice.listen(timeout=15)

        if choice is None:
            continue

        if 'compose' in choice:
            voice_compose_email(email_handler)
        elif 'inbox' in choice:
            voice_check_inbox(email_handler)
        elif 'sent' in choice:
            voice_check_sent(email_handler)
        elif 'logout' in choice:
            voice.speak("Logging out. Thank you for using Voice Email System.")
            voice_session_active = False
            break
        else:
            voice.speak("Invalid option. Please try again.")

def voice_compose_email(email_handler):
    """Voice compose email"""
    voice.speak("Let's compose an email.")

    # Get recipient
    voice.speak("Please say the receiver's email address slowly. For example, say john dot smith at gmail dot com")

    to_email = None
    while to_email is None:
        email_input = voice.listen(phrase_limit=15)
        if email_input is None:
            continue

        # Convert speech to email
        to_email = convert_speech_to_email(email_input)

        if to_email:
            voice.speak(f"You said {to_email}. Say YES to confirm or NO to try again.")
            confirm = voice.listen()

            if confirm and 'yes' in confirm:
                break
            else:
                to_email = None
                voice.speak("Let's try again.")
        else:
            voice.speak("Invalid email format. Please try again.")

    # Get subject
    voice.speak("Please say the subject.")
    subject = voice.listen(phrase_limit=10)

    if subject is None:
        voice.speak("Subject not received. Email cancelled.")
        return

    voice.speak(f"The subject is {subject}. Say YES to confirm or NO to cancel.")
    if not confirm_yes():
        voice.speak("Email cancelled.")
        return

    # Get message
    voice.speak("Please speak your message.")
    message = voice.listen(phrase_limit=20)

    if message is None:
        voice.speak("Message not received. Email cancelled.")
        return

    voice.speak(f"Your message is {message}. Say YES to confirm or NO to cancel.")
    if not confirm_yes():
        voice.speak("Email cancelled.")
        return

    # Send email
    voice.speak(f"Email ready. To: {to_email}. Subject: {subject}. Say SEND to send or CANCEL to cancel.")
    send_choice = voice.listen()

    if send_choice and 'send' in send_choice:
        success, msg = email_handler.send_email(to_email, subject, message)

        if success:
            voice.speak("Email sent successfully.")
        else:
            voice.speak(f"Failed to send email. {msg}")
    else:
        voice.speak("Email cancelled.")

def voice_check_inbox(email_handler):
    """Voice check inbox"""
    voice.speak("Checking your inbox. Please wait.")

    success, msg, emails, total_count = email_handler.get_inbox_emails(max_emails=10)

    if not success:
        voice.speak(f"Error retrieving inbox. {msg}")
        return

    if not emails:
        voice.speak("Your inbox is empty.")
        return

    unread_count = sum(1 for email in emails if not email.get('seen', False))
    voice.speak(f"You have {total_count} emails in inbox. {unread_count} unread.")

    # Navigate through emails with index control
    current_index = 0

    while current_index < len(emails):
        email_data = emails[current_index]
        from_addr = email_data['from']
        subject = email_data['subject'] or "No subject"

        voice.speak(f"Email {current_index + 1} of {len(emails)}. From {from_addr}. Subject: {subject}.")
        voice.speak("Say READ to hear the message, NEXT, PREVIOUS, a NUMBER to jump to that email, or STOP to exit.")

        choice = voice.listen(timeout=10, phrase_limit=8)

        if choice is None:
            voice.speak("I didn't hear you. Let me repeat.")
            continue

        choice_lower = choice.lower()

        # Check if user said a number to jump to
        number_jumped = False
        for i in range(1, len(emails) + 1):
            # Check for various ways of saying the number (cardinal and ordinal)
            number_words = {
                1: ['one', '1', 'first', '1st', 'wan'],
                2: ['two', '2', 'second', '2nd', 'to'],
                3: ['three', '3', 'third', '3rd', 'tree'],
                4: ['four', '4', 'fourth', '4th', 'for'],
                5: ['five', '5', 'fifth', '5th'],
                6: ['six', '6', 'sixth', '6th'],
                7: ['seven', '7', 'seventh', '7th'],
                8: ['eight', '8', 'eighth', '8th', 'ate'],
                9: ['nine', '9', 'ninth', '9th'],
                10: ['ten', '10', 'tenth', '10th']
            }

            if i in number_words:
                for num_word in number_words[i]:
                    # Check for exact word match or number in various contexts
                    choice_words = choice_lower.split()
                    if (num_word in choice_words or
                        f'number {num_word}' in choice_lower or
                        f'email {num_word}' in choice_lower or
                        f'read {num_word}' in choice_lower or
                        f'{num_word} email' in choice_lower or
                        choice_lower == num_word or
                        choice_lower.endswith(f' {num_word}') or
                        choice_lower.startswith(f'{num_word} ')):
                        current_index = i - 1  # Convert to 0-based index
                        number_jumped = True
                        print(f"[DEBUG] Jumped to email {i} (index {current_index})")
                        # If "read" was in the command, automatically read the email
                        if 'read' in choice_lower:
                            # Will process read after jump
                            pass
                        break
                if number_jumped:
                    break

        if number_jumped:
            # Always read the email when jumping to a number (whether "read" was said or not)
            email_data = emails[current_index]
            body = email_data['body'][:500]
            voice.speak(f"Message: {body}")
            voice.speak("Say NEXT, PREVIOUS, a NUMBER to jump, REPEAT to hear again, or STOP to exit.")

            while True:
                next_choice = voice.listen(timeout=10, phrase_limit=8)

                if next_choice is None:
                    voice.speak("I didn't hear you. Say NEXT, PREVIOUS, a NUMBER, REPEAT, or STOP.")
                    continue

                next_choice_lower = next_choice.lower()

                # Check for number jump after reading
                number_jumped_after_read = False
                for i in range(1, len(emails) + 1):
                    number_words = {
                        1: ['one', '1', 'first', '1st', 'wan'],
                        2: ['two', '2', 'second', '2nd', 'to'],
                        3: ['three', '3', 'third', '3rd', 'tree'],
                        4: ['four', '4', 'fourth', '4th', 'for'],
                        5: ['five', '5', 'fifth', '5th'],
                        6: ['six', '6', 'sixth', '6th'],
                        7: ['seven', '7', 'seventh', '7th'],
                        8: ['eight', '8', 'eighth', '8th', 'ate'],
                        9: ['nine', '9', 'ninth', '9th'],
                        10: ['ten', '10', 'tenth', '10th']
                    }
                    if i in number_words:
                        for num_word in number_words[i]:
                            next_choice_words = next_choice_lower.split()
                            if (num_word in next_choice_words or
                                f'number {num_word}' in next_choice_lower or
                                f'email {num_word}' in next_choice_lower or
                                next_choice_lower == num_word or
                                next_choice_lower.endswith(f' {num_word}') or
                                next_choice_lower.startswith(f'{num_word} ')):
                                current_index = i - 1
                                number_jumped_after_read = True
                                break
                        if number_jumped_after_read:
                            break

                if number_jumped_after_read:
                    break

                if 'next' in next_choice_lower:
                    current_index += 1
                    break
                elif 'previous' in next_choice_lower:
                    if current_index > 0:
                        current_index -= 1
                    else:
                        voice.speak("You are already at the first email.")
                    break
                elif 'repeat' in next_choice_lower:
                    voice.speak(f"Message: {body}")
                    voice.speak("Say NEXT, PREVIOUS, a NUMBER to jump, REPEAT to hear again, or STOP to exit.")
                    continue
                elif 'stop' in next_choice_lower or 'exit' in next_choice_lower:
                    return
                else:
                    voice.speak("Invalid option. Say NEXT, PREVIOUS, a NUMBER, REPEAT, or STOP.")
            continue  # Go back to top of loop to read the new email

        if 'read' in choice_lower:
            body = email_data['body'][:500]  # Increased limit
            voice.speak(f"Message: {body}")
            # After reading, ask what to do next
            voice.speak("Say NEXT, PREVIOUS, a NUMBER to jump, REPEAT to hear again, or STOP to exit.")

            while True:
                next_choice = voice.listen(timeout=10, phrase_limit=8)

                if next_choice is None:
                    voice.speak("I didn't hear you. Say NEXT, PREVIOUS, a NUMBER, REPEAT, or STOP.")
                    continue

                next_choice_lower = next_choice.lower()

                # Check for number jump after reading
                number_jumped_after_read = False
                for i in range(1, len(emails) + 1):
                    number_words = {
                        1: ['one', '1', 'first', '1st', 'wan'],
                        2: ['two', '2', 'second', '2nd', 'to'],
                        3: ['three', '3', 'third', '3rd', 'tree'],
                        4: ['four', '4', 'fourth', '4th', 'for'],
                        5: ['five', '5', 'fifth', '5th'],
                        6: ['six', '6', 'sixth', '6th'],
                        7: ['seven', '7', 'seventh', '7th'],
                        8: ['eight', '8', 'eighth', '8th', 'ate'],
                        9: ['nine', '9', 'ninth', '9th'],
                        10: ['ten', '10', 'tenth', '10th']
                    }
                    if i in number_words:
                        for num_word in number_words[i]:
                            next_choice_words = next_choice_lower.split()
                            if (num_word in next_choice_words or
                                f'number {num_word}' in next_choice_lower or
                                f'email {num_word}' in next_choice_lower or
                                next_choice_lower == num_word or
                                next_choice_lower.endswith(f' {num_word}') or
                                next_choice_lower.startswith(f'{num_word} ')):
                                current_index = i - 1
                                number_jumped_after_read = True
                                break
                        if number_jumped_after_read:
                            break

                if number_jumped_after_read:
                    break

                if 'next' in next_choice_lower:
                    current_index += 1
                    break
                elif 'previous' in next_choice_lower:
                    if current_index > 0:
                        current_index -= 1
                    else:
                        voice.speak("You are already at the first email.")
                    break
                elif 'repeat' in next_choice_lower:
                    voice.speak(f"Message: {body}")
                    voice.speak("Say NEXT, PREVIOUS, a NUMBER to jump, REPEAT to hear again, or STOP to exit.")
                    continue
                elif 'stop' in next_choice_lower or 'exit' in next_choice_lower:
                    return
                else:
                    voice.speak("Invalid option. Say NEXT, PREVIOUS, a NUMBER, REPEAT, or STOP.")

        elif 'next' in choice_lower:
            current_index += 1

        elif 'previous' in choice_lower or 'back' in choice_lower:
            if current_index > 0:
                current_index -= 1
            else:
                voice.speak("You are already at the first email.")

        elif 'stop' in choice_lower or 'exit' in choice_lower:
            break

        else:
            voice.speak("Invalid option. Please say READ, NEXT, PREVIOUS, a NUMBER, or STOP.")

def voice_check_sent(email_handler):
    """Voice check sent mail"""
    voice.speak("Checking sent emails. Please wait.")

    success, msg, emails, total_count = email_handler.get_sent_emails(max_emails=5)

    if not success:
        voice.speak(f"Error retrieving sent emails. {msg}")
        return

    if not emails:
        voice.speak("You have no sent emails.")
        return

    voice.speak(f"You have {total_count} sent emails in outbox.")

    for idx, email_data in enumerate(emails):
        to_addr = email_data['to']
        subject = email_data['subject'] or "No subject"

        voice.speak(f"Email {idx + 1}. To {to_addr}. Subject: {subject}.")

        if idx < len(emails) - 1:
            voice.speak("Say NEXT to continue or STOP to exit.")
            choice = voice.listen(timeout=10, phrase_limit=8)

            if choice and 'stop' in choice:
                break

def convert_speech_to_email(speech_text):
    """Convert spoken email to email format"""
    email = speech_text.replace(' at ', '@')
    email = email.replace(' dot ', '.')
    email = email.replace(' ', '')

    # Basic validation
    if '@' in email and '.' in email.split('@')[1]:
        return email
    return None

def confirm_yes():
    """Get YES confirmation"""
    response = voice.listen()
    return response and 'yes' in response

@app.route('/stop_voice')
def stop_voice():
    """Stop voice session"""
    global voice_session_active
    voice_session_active = False
    return jsonify({'status': 'stopped'})

@app.route('/voice_status')
def voice_status():
    """Check voice session status"""
    global voice_session_active, current_user_data

    status = {
        'active': voice_session_active,
        'logged_in': current_user_data is not None,
        'username': current_user_data['username'] if current_user_data else None
    }

    return jsonify(status)

@app.route('/api/voice_login', methods=['POST'])
def api_voice_login():
    """API endpoint for voice login"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Verify credentials
    user_data = db.verify_user(username, password)

    if user_data:
        global current_user_data
        current_user_data = user_data
        return jsonify({'success': True, 'username': username})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/api/voice_inbox', methods=['GET'])
def api_voice_inbox():
    """API endpoint for voice inbox"""
    global current_user_data

    if not current_user_data:
        return jsonify({'success': False, 'message': 'Not logged in'})

    email_handler = EmailHandler(
        current_user_data['gmail_address'],
        current_user_data['gmail_app_password']
    )

    success, msg, emails, total_count = email_handler.get_inbox_emails(max_emails=3)

    if success:
        return jsonify({'success': True, 'emails': emails, 'total_count': total_count})
    else:
        return jsonify({'success': False, 'message': msg})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API endpoint for logout"""
    global current_user_data, voice_session_active
    current_user_data = None
    voice_session_active = False
    return jsonify({'success': True})

@app.route('/api/voice_status', methods=['GET'])
def api_voice_status():
    """Check if user is logged in"""
    global current_user_data

    return jsonify({
        'logged_in': current_user_data is not None,
        'username': current_user_data['username'] if current_user_data else None
    })

@app.route('/voice/menu')
def voice_menu():
    """Voice menu page"""
    return render_template('voice_menu.html')

@app.route('/voice/compose')
def voice_compose():
    """Voice compose email page"""
    return render_template('voice_compose.html')

@app.route('/voice/inbox')
def voice_inbox_page():
    """Voice inbox page"""
    return render_template('voice_inbox.html')

@app.route('/voice/sent')
def voice_sent_page():
    """Voice sent mail page"""
    return render_template('voice_sent.html')

@app.route('/api/send_email', methods=['POST'])
def api_send_email():
    """API endpoint to send email"""
    global current_user_data

    if not current_user_data:
        return jsonify({'success': False, 'message': 'Not logged in'})

    data = request.get_json()
    to_email = data.get('to')
    subject = data.get('subject')
    message = data.get('message')

    email_handler = EmailHandler(
        current_user_data['gmail_address'],
        current_user_data['gmail_app_password']
    )

    success, msg = email_handler.send_email(to_email, subject, message)

    return jsonify({'success': success, 'message': msg})

@app.route('/api/sent_emails', methods=['GET'])
def api_sent_emails():
    """API endpoint for sent emails"""
    global current_user_data

    if not current_user_data:
        return jsonify({'success': False, 'message': 'Not logged in'})

    email_handler = EmailHandler(
        current_user_data['gmail_address'],
        current_user_data['gmail_app_password']
    )

    success, msg, emails, total_count = email_handler.get_sent_emails(max_emails=3)

    if success:
        return jsonify({'success': True, 'emails': emails, 'total_count': total_count})
    else:
        return jsonify({'success': False, 'message': msg})

# Admin Routes
@app.route('/admin/login')
def admin_login_page():
    """Admin login page"""
    return render_template('admin_login.html')

@app.route('/api/admin_login', methods=['POST'])
def api_admin_login():
    """API endpoint for admin login"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Verify admin credentials
    user_data = db.verify_user(username, password)

    if user_data and username == 'admin':
        session['admin_logged_in'] = True
        session['admin_username'] = username
        return jsonify({'success': True, 'username': username})
    else:
        return jsonify({'success': False, 'message': 'Invalid admin credentials'})

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    if not session.get('admin_logged_in', False):
        return render_template('admin_login.html')

    return render_template('admin_dashboard.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint for public user registration"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    gmail_address = data.get('gmail_address')
    gmail_app_password = data.get('gmail_app_password')

    # Remove spaces from app password
    gmail_app_password = gmail_app_password.replace(' ', '')

    success, msg = db.create_user(username, password, gmail_address, gmail_app_password)

    return jsonify({'success': success, 'message': msg})

@app.route('/api/admin/add_user', methods=['POST'])
def api_admin_add_user():
    """API endpoint to add new user (admin only)"""
    if not session.get('admin_logged_in', False):
        return jsonify({'success': False, 'message': 'Not authorized'})

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    gmail_address = data.get('gmail_address')
    gmail_app_password = data.get('gmail_app_password')

    # Remove spaces from app password
    gmail_app_password = gmail_app_password.replace(' ', '')

    success, msg = db.create_user(username, password, gmail_address, gmail_app_password)

    return jsonify({'success': success, 'message': msg})

@app.route('/api/admin/users', methods=['GET'])
def api_admin_users():
    """API endpoint to get all users"""
    if not session.get('admin_logged_in', False):
        return jsonify({'success': False, 'message': 'Not authorized'})

    users = db.get_all_users()
    return jsonify({'success': True, 'users': users})

@app.route('/api/admin/delete_user', methods=['POST'])
def api_admin_delete_user():
    """API endpoint to delete user"""
    if not session.get('admin_logged_in', False):
        return jsonify({'success': False, 'message': 'Not authorized'})

    data = request.get_json()
    username = data.get('username')

    if username == 'admin':
        return jsonify({'success': False, 'message': 'Cannot delete admin user'})

    success, msg = db.delete_user(username)
    return jsonify({'success': success, 'message': msg})

@app.route('/api/admin/logout', methods=['POST'])
def api_admin_logout():
    """API endpoint for admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return jsonify({'success': True})

@app.route('/api/log_voice', methods=['POST'])
def api_log_voice():
    """API endpoint to log voice interactions to terminal"""
    data = request.get_json()
    log_type = data.get('type')  # 'user' or 'system'
    text = data.get('text')
    page = data.get('page', 'unknown')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if log_type == 'user':
        print(f"\n[{timestamp}] 🎤 USER SAID ({page}): {text}")
    elif log_type == 'system':
        print(f"[{timestamp}] 🔊 SYSTEM SAID ({page}): {text}")
    else:
        print(f"[{timestamp}] 📝 VOICE LOG ({page}): {text}")

    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 50)
    print("Voice-Based Email System - Voice Mode")
    print("=" * 50)
    print("\nStarting Flask server...")
    print("Open http://localhost:5000 in your browser")
    print("\nMake sure your microphone is connected!")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
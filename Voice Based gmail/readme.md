# Voice-Based Email System for Visually Impaired People

## 🔹 PROBLEM STATEMENT

Visually impaired users face difficulty accessing email systems that depend heavily on visual interfaces. This project aims to provide a fully voice-controlled email system allowing blind users to log in, compose emails, read inbox and sent emails using speech commands.

## 🔹 SYSTEM OVERVIEW (VOICE ONLY)

The system operates entirely through voice interaction. The user does not require a keyboard or mouse. Speech recognition is used to understand user commands, and text-to-speech converts system responses into audio.

## 🚀 QUICK START

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Run application**: `python app.py`
3. **Open browser**: http://localhost:5000
4. **Create users** in Admin Panel
5. **Start voice session** and follow prompts

For detailed setup instructions, see [SETUP.md](SETUP.md)

## 📋 PROJECT STRUCTURE

```
Voice Based gmail/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── database.py           # SQLite database handler
├── voice_handler.py      # Speech recognition & TTS
├── email_handler.py      # Gmail SMTP/IMAP operations
├── requirements.txt      # Python dependencies
├── SETUP.md             # Detailed setup guide
└── readme.md            # This file
```

## 🔹 USER CREATION (ADMIN SIDE)

Admin creates user using:
- Username
- Voice password (spoken phrase)
- Gmail ID (already 2-step authenticated)
- Gmail App Password (16-character from Google)

Credentials stored securely in SQLite database with hashed passwords.

## 🔹 LOGIN WORKFLOW (VOICE)

1. System speaks: *"Welcome to Voice Email System. Please say your username."*
2. User speaks username
3. System speaks: *"Please say your voice password."*
4. Voice password verified
5. On success: *"Login successful. Welcome [username]."*

## 🔹 FEATURE ANNOUNCEMENT

System speaks:

*"Available options are:
- Compose Email
- Check Inbox
- Check Sent Mail
- Logout

Please say your option."*

## ✉️ COMPOSE EMAIL WORKFLOW

1. User: *"Compose email"*
2. System: *"Please say receiver email address."*
3. User speaks email (e.g., "john dot smith at gmail dot com")
4. System confirms: *"You said john.smith@gmail.com. Say YES or NO."*
   - If NO → re-enter
   - If YES → continue
5. **Subject**: System asks, user speaks, confirms
6. **Message**: System asks, user speaks, confirms
7. **Final Confirmation**: *"Say SEND to send email or CANCEL to cancel."*

## 📥 CHECK INBOX WORKFLOW

1. System: *"You have X unread emails."*
2. **Options**:
   - Read First
   - Read Next
   - Delete
   - Reply
   - Go Back
3. Email read aloud: *"Mail from Ravi. Subject: Project update."*
4. User can choose to hear full message, reply, delete, or skip

## 📤 CHECK SENT MAIL

1. System: *"You have X sent emails."*
2. Reads latest email details
3. User can navigate through sent emails
4. Option to hear full message content

## 🔐 SECURITY

- Gmail secured using App Password (2-step authentication required)
- Voice passwords hashed using SHA-256
- No plain-text password storage
- Secure database storage for credentials
- Session management with timeout

## 🛠️ TECHNOLOGY STACK

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: pyttsx3 (offline)
- **Email**: Gmail SMTP/IMAP with App Passwords
- **Audio Input**: PyAudio + SpeechRecognition

## 📦 MODULES

1. **Voice Input Module** (`voice_handler.py`)
   - Speech recognition using Google API
   - Ambient noise adjustment
   - Voice command parsing

2. **Voice Output Module** (`voice_handler.py`)
   - Text-to-speech using pyttsx3
   - Async speech support
   - Configurable voice properties

3. **User Authentication Module** (`database.py`)
   - User creation and management
   - Password hashing (SHA-256)
   - Login attempt tracking
   - Session management

4. **Email Sending Module** (`email_handler.py`)
   - SMTP integration with Gmail
   - Email composition
   - Reply functionality

5. **Inbox Reading Module** (`email_handler.py`)
   - IMAP integration
   - Email fetching and parsing
   - Unread count tracking
   - Email deletion

6. **Error Handling Module**
   - Speech recognition error handling
   - Gmail authentication error handling
   - User-friendly error messages via voice

## 🎯 FEATURES

✅ Fully voice-controlled interface
✅ Voice-based authentication
✅ Compose emails via speech
✅ Read inbox emails with navigation
✅ Reply to emails
✅ Delete emails
✅ Check sent emails
✅ Voice confirmations at every step
✅ Admin panel for user management
✅ Secure credential storage
✅ Session management

## 📝 USAGE NOTES

- **Email addresses**: Say "john dot smith at gmail dot com" for john.smith@gmail.com
- **Confirmations**: Always say "YES" or "NO" clearly
- **Speech clarity**: Speak at moderate pace in quiet environment
- **Internet required**: For speech recognition and Gmail access

## 🔧 CONFIGURATION

Edit [config.py](config.py) to customize:
- Speech timeout duration
- Phrase time limit
- Max login attempts
- Session timeout
- SMTP/IMAP settings

## 🐛 TROUBLESHOOTING

See [SETUP.md](SETUP.md) for detailed troubleshooting guide.

Common issues:
- Microphone not detected
- Speech recognition errors
- Gmail authentication failures
- PyAudio installation issues

## 📄 LICENSE

This project is designed for educational and accessibility purposes.

## 👥 TARGET USERS

Visually impaired individuals who need accessible email communication.

## 🌟 FUTURE ENHANCEMENTS

- Offline speech recognition
- Multiple language support
- Email attachments via voice
- Calendar integration
- Contact management
- Voice-based email search
- Mobile app version
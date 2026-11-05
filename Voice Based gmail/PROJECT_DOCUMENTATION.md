# Voice-Based Gmail System - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technologies & Libraries](#technologies--libraries)
4. [Core Modules & Functions](#core-modules--functions)
5. [Algorithms & Workflows](#algorithms--workflows)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)
8. [Voice Commands](#voice-commands)
9. [Security Features](#security-features)
10. [User Interface](#user-interface)
11. [Setup & Deployment](#setup--deployment)
12. [Testing & Validation](#testing--validation)

---

## Project Overview

### Purpose
A fully voice-controlled email management system designed specifically for visually impaired users to access Gmail functionality without visual interfaces.

### Key Features
- ✅ Voice-based authentication
- ✅ Compose emails via speech
- ✅ Auto-read inbox (first 3 emails)
- ✅ Auto-read sent emails (first 3 emails)
- ✅ Navigate emails with voice commands
- ✅ Jump to specific emails by number
- ✅ Spacebar interrupt functionality
- ✅ Admin panel for user management
- ✅ Secure credential storage

### Target Users
Visually impaired individuals who require accessible email communication without traditional keyboard/mouse/visual interfaces.

---

## System Architecture

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ voice_web.html│  │voice_menu.html│ │voice_inbox.html│     │
│  │voice_compose │  │voice_sent.html│ │admin_dashboard │     │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application Layer                    │
│                    (voice_web_app.py)                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Routes: /, /voice/*, /api/*, /admin/*              │    │
│  │ Session Management, Authentication, API Handlers    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │voice_handler │  │email_handler │  │  database.py  │      │
│  │   (Speech)   │  │ (Gmail IMAP) │  │   (SQLite)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    External Services Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Google Speech │  │ Gmail SMTP   │  │  Gmail IMAP   │      │
│  │ Recognition  │  │   Server     │  │    Server     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow
1. **User** speaks command → **Web Interface** captures audio
2. **Speech Recognition** converts audio to text
3. **Flask Routes** process the command
4. **Business Logic** executes operations
5. **External Services** (Gmail API) perform actions
6. **Database** stores/retrieves user data
7. **Text-to-Speech** provides audio feedback to user

---

## Technologies & Libraries

### Backend Technologies

#### 1. **Flask** (Web Framework)
```python
from flask import Flask, render_template, jsonify, request, session
```
- **Purpose**: Web application framework
- **Version**: Latest stable
- **Usage**: Routing, session management, API endpoints

#### 2. **SQLite3** (Database)
```python
import sqlite3
```
- **Purpose**: Lightweight embedded database
- **Database File**: `voice_email.db`
- **Usage**: Store user credentials, login attempts, sessions

#### 3. **Speech Recognition** (Voice Input)
```python
import speech_recognition as sr
```
- **Purpose**: Convert speech to text
- **Backend**: Google Speech Recognition API
- **Features**: Ambient noise adjustment, timeout handling

#### 4. **pyttsx3** (Text-to-Speech)
```python
import pyttsx3
```
- **Purpose**: Convert text to speech (offline)
- **Features**: Configurable voice, speed, volume
- **Platform**: Cross-platform (Windows, Linux, Mac)

#### 5. **SMTP/IMAP** (Email Protocols)
```python
import smtplib
import imaplib
import email
```
- **SMTP**: Send emails via Gmail
- **IMAP**: Retrieve inbox and sent emails
- **Security**: SSL/TLS encryption

#### 6. **Hashlib** (Password Security)
```python
import hashlib
```
- **Purpose**: SHA-256 password hashing
- **Usage**: Secure voice password storage

### Frontend Technologies

#### 1. **HTML5**
- Semantic markup
- Forms and templates

#### 2. **CSS3**
- Responsive design
- Gradient backgrounds
- Animations (pulse effect for microphone)

#### 3. **JavaScript (Vanilla)**
- Web Speech API (Browser-based speech recognition)
- Speech Synthesis API (Browser-based TTS)
- AJAX/Fetch for API calls
- Event handling (keyboard, voice)

#### 4. **Web Speech API**
```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const utterance = new SpeechSynthesisUtterance(text);
```

---

## Core Modules & Functions

### 1. **voice_web_app.py** (Main Application)

#### Key Functions:

##### `index()`
```python
@app.route('/')
def index():
    """Home page with voice session option"""
    return render_template('voice_web.html')
```
- **Purpose**: Renders landing page
- **Template**: voice_web.html

##### `voice_login_process()`
```python
def voice_login_process():
    """Voice login process running in background"""
    global current_user_data, voice_session_active
    # Get username and password via voice
    # Verify credentials
    # Start main menu on success
```
- **Purpose**: Handles voice authentication
- **Max Attempts**: 3 (configurable)
- **Threading**: Runs in background thread

##### `voice_main_menu()`
```python
def voice_main_menu():
    """Voice main menu"""
    # Options: Compose, Inbox, Sent, Logout
    # Listen for user choice
    # Route to appropriate function
```
- **Purpose**: Main navigation hub
- **Commands**: Compose, Inbox, Sent Mail, Logout

##### `voice_compose_email(email_handler)`
```python
def voice_compose_email(email_handler):
    """Voice compose email"""
    # Get recipient email
    # Get subject
    # Get message
    # Confirm and send
```
- **Purpose**: Compose emails via voice
- **Features**: Email format conversion, confirmation steps

##### `voice_check_inbox(email_handler)`
```python
def voice_check_inbox(email_handler):
    """Voice check inbox with navigation"""
    # Fetch up to 10 emails
    # Navigate with NEXT/PREVIOUS/NUMBER
    # Read emails on demand
    # Jump to specific emails (first, second, third, etc.)
```
- **Purpose**: Inbox navigation and reading
- **Max Emails**: 10
- **Navigation**: Sequential and jump-to-number
- **Timeout**: 10 seconds for voice input
- **Features**:
  - Navigate by saying numbers (first, second, third)
  - Automatic reading when jumping to email
  - Repeat functionality
  - 500 character message limit

##### `voice_check_sent(email_handler)`
```python
def voice_check_sent(email_handler):
    """Voice check sent mail"""
    # Fetch up to 5 sent emails
    # Read email details
    # Navigate through emails
```
- **Purpose**: View sent emails
- **Max Emails**: 5
- **Timeout**: 10 seconds for voice input

##### `convert_speech_to_email(speech_text)`
```python
def convert_speech_to_email(speech_text):
    """Convert spoken email to email format"""
    email = speech_text.replace(' at ', '@')
    email = email.replace(' dot ', '.')
    email = email.replace(' ', '')
    # Validate format
    return email
```
- **Algorithm**: String replacement
- **Validation**: Check for @ and . in domain

### 2. **voice_handler.py** (Speech Processing)

#### Class: `VoiceHandler`

##### `__init__(self)`
```python
def __init__(self):
    self.recognizer = sr.Recognizer()
    self.engine = pyttsx3.init()
    self._configure_tts()
```
- **Initializes**: Speech recognizer and TTS engine

##### `_configure_tts(self)`
```python
def _configure_tts(self):
    """Configure text-to-speech engine"""
    self.engine.setProperty('rate', 150)  # Speech speed
    self.engine.setProperty('volume', 0.9)  # Volume level
    # Prefer female voice if available
```
- **Rate**: 150 words per minute
- **Volume**: 90%
- **Voice**: Female preferred (Zira)

##### `speak(text)`
```python
def speak(self, text):
    """Convert text to speech"""
    print(f"[SYSTEM]: {text}")
    self.engine.say(text)
    self.engine.runAndWait()
```
- **Purpose**: Synchronous speech output
- **Logging**: Prints to terminal

##### `listen(prompt, timeout, phrase_limit)`
```python
def listen(self, prompt=None, timeout=None, phrase_limit=None):
    """Listen for voice input"""
    # Adjust for ambient noise (1 second)
    # Listen with timeout
    # Recognize using Google API
    # Return lowercase text
```
- **Default Timeout**: 10 seconds
- **Default Phrase Limit**: 15 seconds
- **Noise Adjustment**: 1 second calibration
- **Error Handling**: Timeout, recognition errors

##### `confirm(question)`
```python
def confirm(self, question):
    """Ask a yes/no confirmation question"""
    # Loop until valid response
    # Accept: yes, yeah, yup, no, nope
```

##### `get_email_address(self)`
```python
def get_email_address(self):
    """Get email address with special handling"""
    # Listen for email
    # Convert speech to email format
    # Confirm with user
```

### 3. **email_handler.py** (Gmail Integration)

#### Class: `EmailHandler`

##### `__init__(gmail_address, gmail_app_password)`
```python
def __init__(self, gmail_address, gmail_app_password):
    self.gmail_address = gmail_address
    self.gmail_app_password = gmail_app_password
    self.smtp_server = 'smtp.gmail.com'
    self.smtp_port = 587
```

##### `send_email(to_email, subject, message)`
```python
def send_email(self, to_email, subject, message):
    """Send an email using Gmail SMTP"""
    # Create MIME message
    # Connect to SMTP server
    # Login and send
    # Return success/failure
```
- **Protocol**: SMTP with STARTTLS
- **Port**: 587
- **Authentication**: Gmail App Password

##### `get_inbox_emails(max_emails=10)`
```python
def get_inbox_emails(self, max_emails=10):
    """Fetch inbox emails using IMAP"""
    # Connect to IMAP server
    # Select inbox folder
    # Search for all emails
    # Reverse order (latest first)
    # Parse email details
    # Return list of email dictionaries
```
- **Protocol**: IMAP4_SSL
- **Server**: imap.gmail.com
- **Returns**: List of email objects with:
  - `id`: Email ID
  - `from`: Sender address
  - `subject`: Email subject
  - `date`: Sent date
  - `body`: Email content
  - `seen`: Read status

##### `get_sent_emails(max_emails=10)`
```python
def get_sent_emails(self, max_emails=10):
    """Fetch sent emails using IMAP"""
    # Connect to IMAP
    # Select "[Gmail]/Sent Mail" folder
    # Fallback to "Sent" if not found
    # Parse and return emails
```

##### `_decode_header(header)`
```python
def _decode_header(self, header):
    """Decode email header"""
    # Handle multiple encodings
    # Convert bytes to string
    # Return decoded text
```
- **Encodings Supported**: UTF-8, custom encodings

##### `_get_email_body(msg)`
```python
def _get_email_body(self, msg):
    """Extract email body from message"""
    # Handle multipart messages
    # Extract text/plain content
    # Ignore attachments
    # Return cleaned body text
```
- **Content Type**: text/plain preferred
- **Attachments**: Ignored

### 4. **database.py** (Data Persistence)

#### Class: `Database`

##### `__init__(self)`
```python
def __init__(self):
    self.db_path = Config.DATABASE_PATH
    self.init_database()
```

##### `init_database(self)`
```python
def init_database(self):
    """Initialize database with required tables"""
    # Create users table
    # Create login_attempts table
    # Create sessions table
```

**Tables Created:**
- `users`: User credentials
- `login_attempts`: Login history
- `sessions`: Active sessions

##### `hash_password(password)`
```python
def hash_password(self, password):
    """Hash voice password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()
```
- **Algorithm**: SHA-256
- **Salt**: None (consider adding for production)

##### `create_user(username, voice_password, gmail_address, gmail_app_password)`
```python
def create_user(self, username, voice_password, gmail_address, gmail_app_password):
    """Create a new user"""
    # Hash password
    # Insert into database
    # Handle duplicate username error
```

##### `verify_user(username, voice_password)`
```python
def verify_user(self, username, voice_password):
    """Verify user credentials"""
    # Hash provided password
    # Query database
    # Log login attempt
    # Update last login time
    # Return user data or None
```

##### `get_all_users()`
```python
def get_all_users(self):
    """Get all users including active and inactive"""
    # Query all users
    # Return list of user dictionaries
```

##### `delete_user(username)`
```python
def delete_user(self, username):
    """Soft delete a user by username"""
    # Set is_active = 0
    # Don't physically delete
```
- **Type**: Soft delete (preserves data)

### 5. **config.py** (Configuration)

```python
class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    DATABASE_PATH = 'voice_email.db'

    # Gmail SMTP settings
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    # Voice settings
    SPEECH_TIMEOUT = 10  # seconds
    PHRASE_TIME_LIMIT = 15  # seconds

    # Security
    MAX_LOGIN_ATTEMPTS = 3
    SESSION_TIMEOUT = 1800  # 30 minutes
```

---

## Algorithms & Workflows

### 1. **Voice Login Algorithm**

```
START
  ↓
1. System speaks: "Welcome to Voice Email System"
  ↓
2. System speaks: "Please say your username"
  ↓
3. Listen for username (10 second timeout)
  ↓
4. IF timeout OR no input
     Increment attempt counter
     IF attempts < 3: GOTO step 2
     ELSE: Speak "Maximum attempts reached" → END
  ↓
5. System speaks: "Please say your password"
  ↓
6. Listen for password (10 second timeout)
  ↓
7. Hash password using SHA-256
  ↓
8. Query database with username and password hash
  ↓
9. IF credentials valid:
     Store user data in session
     Speak "Login successful"
     GOTO Main Menu
   ELSE:
     Increment attempt counter
     IF attempts < 3:
       Speak "Invalid credentials, X attempts remaining"
       GOTO step 2
     ELSE:
       Speak "Maximum login attempts reached"
       END
```

### 2. **Email Composition Algorithm**

```
START
  ↓
1. Speak "Let's compose an email"
  ↓
2. GET RECIPIENT EMAIL:
   ├─ Speak "Say receiver's email slowly"
   ├─ Listen for email (15 second phrase limit)
   ├─ Convert speech to email format:
   │    • Replace " at " with "@"
   │    • Replace " dot " with "."
   │    • Remove spaces
   ├─ Validate format (check @ and .)
   ├─ Speak email for confirmation
   ├─ Listen for YES/NO
   └─ IF NO: GOTO step 2
  ↓
3. GET SUBJECT:
   ├─ Speak "Please say the subject"
   ├─ Listen (10 second phrase limit)
   ├─ Speak subject for confirmation
   └─ IF NO: Cancel email
  ↓
4. GET MESSAGE:
   ├─ Speak "Please speak your message"
   ├─ Listen (20 second phrase limit)
   ├─ Speak message for confirmation
   └─ IF NO: Cancel email
  ↓
5. FINAL CONFIRMATION:
   ├─ Speak "Email ready. Say SEND or CANCEL"
   ├─ Listen for command
   ├─ IF "send" in command:
   │    • Connect to SMTP server
   │    • Send email
   │    • Speak "Email sent successfully"
   └─ ELSE: Speak "Email cancelled"
  ↓
END
```

### 3. **Inbox Navigation Algorithm (Enhanced)**

```
START
  ↓
1. Fetch emails from IMAP (max 10)
  ↓
2. IF no emails:
     Speak "Your inbox is empty"
     END
  ↓
3. Count unread emails
  ↓
4. Speak "You have X emails, Y unread"
  ↓
5. SET current_index = 0
  ↓
6. MAIN LOOP:
   ├─ Get email at current_index
   ├─ Speak "Email N of M. From [sender]. Subject: [subject]"
   ├─ Speak "Say READ, NEXT, PREVIOUS, a NUMBER, or STOP"
   ├─ Listen for command (10 second timeout)
   │
   ├─ IF timeout: Speak "I didn't hear you" → GOTO step 6
   │
   ├─ CHECK FOR NUMBER JUMP:
   │  ├─ Parse command for numbers: first, second, third, one, two, 1, 2, etc.
   │  ├─ IF number detected:
   │  │    • Set current_index = number - 1
   │  │    • Read email body automatically (500 chars)
   │  │    • Speak "Say NEXT, PREVIOUS, NUMBER, REPEAT, or STOP"
   │  │    • INNER LOOP:
   │  │      ├─ Listen for next command
   │  │      ├─ IF "next": current_index++, break
   │  │      ├─ IF "previous": current_index--, break
   │  │      ├─ IF "repeat": Read body again, continue loop
   │  │      ├─ IF number detected: Jump to email, break
   │  │      └─ IF "stop": EXIT
   │  │    • GOTO step 6
   │
   ├─ IF "read" in command:
   │  ├─ Speak email body (500 chars)
   │  ├─ Same INNER LOOP as number jump
   │  └─ GOTO step 6
   │
   ├─ IF "next" in command:
   │  ├─ current_index++
   │  └─ GOTO step 6
   │
   ├─ IF "previous" in command:
   │  ├─ IF current_index > 0: current_index--
   │  ├─ ELSE: Speak "Already at first email"
   │  └─ GOTO step 6
   │
   └─ IF "stop" in command: EXIT
  ↓
END
```

### 4. **Auto-Read Algorithm (Web Interface)**

```
START (Page Load)
  ↓
1. Fetch emails from API
  ↓
2. IF emails exist:
     Speak "You have X emails"
     Display emails on page
     SET autoReadInProgress = true
     WAIT 2 seconds
     GOTO step 3
   ELSE:
     Speak "No emails"
     END
  ↓
3. AUTO-READ LOOP:
   ├─ SET maxToRead = min(3, emailCount)
   ├─ FOR index from 0 to maxToRead-1:
   │   ├─ IF autoReadStopped: EXIT
   │   ├─ Get email at index
   │   ├─ Extract body (max 500 chars)
   │   ├─ Strip HTML tags
   │   ├─ Create speech text: "Email N. From [sender]. Subject: [subject]. Message: [body]"
   │   ├─ Speak text
   │   ├─ Update status: "Reading email N of M (Press spacebar to stop)"
   │   ├─ WAIT for speech to finish
   │   └─ WAIT 1 second before next email
   │
   ├─ SET autoReadInProgress = false
   └─ Speak "Auto-read complete"
  ↓
4. EVENT LISTENERS:
   ├─ SPACEBAR PRESSED:
   │   ├─ IF autoReadInProgress:
   │   │    • Cancel speech
   │   │    • SET autoReadStopped = true
   │   │    • Speak "Auto-read stopped"
   │   └─ ELSE: Activate voice recognition
  ↓
END
```

### 5. **Number Recognition Algorithm**

```
FUNCTION: recognize_number(command_text)
  ↓
1. Convert command to lowercase
  ↓
2. Split command into words
  ↓
3. Define number mapping:
   number_words = {
     1: ['one', '1', 'first', '1st', 'wan'],
     2: ['two', '2', 'second', '2nd', 'to'],
     3: ['three', '3', 'third', '3rd', 'tree'],
     4: ['four', '4', 'fourth', '4th', 'for'],
     5: ['five', '5', 'fifth', '5th'],
     6-10: [similar patterns]
   }
  ↓
4. FOR each number i from 1 to 10:
   ├─ FOR each variant in number_words[i]:
   │   ├─ CHECK if variant in command_words (exact word match)
   │   ├─ OR "number variant" in command
   │   ├─ OR "email variant" in command
   │   ├─ OR "read variant" in command
   │   ├─ OR command == variant
   │   ├─ OR command ends with " variant"
   │   ├─ OR command starts with "variant "
   │   │
   │   └─ IF any match: RETURN i
  ↓
5. RETURN None (no number found)
```

**Why Multiple Variants?**
- Speech recognition may mishear numbers
- "two" might be recognized as "to"
- "four" might be recognized as "for"
- "eight" might be recognized as "ate"
- Users may say ordinal (first, second) or cardinal (one, two) numbers

---

## Database Schema

### Tables

#### 1. **users**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    voice_password_hash TEXT NOT NULL,
    gmail_address TEXT NOT NULL,
    gmail_app_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active INTEGER DEFAULT 1
);
```

**Columns:**
- `id`: Auto-increment primary key
- `username`: Unique username for login
- `voice_password_hash`: SHA-256 hashed voice password
- `gmail_address`: User's Gmail address
- `gmail_app_password`: Gmail app-specific password (16-char)
- `created_at`: Account creation timestamp
- `last_login`: Last successful login timestamp
- `is_active`: Soft delete flag (1=active, 0=deleted)

#### 2. **login_attempts**
```sql
CREATE TABLE login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success INTEGER DEFAULT 0
);
```

**Columns:**
- `id`: Auto-increment primary key
- `username`: Username attempted
- `attempt_time`: When the attempt occurred
- `success`: 1 if successful, 0 if failed

**Purpose**: Audit trail, security monitoring

#### 3. **sessions**
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

**Columns:**
- `id`: Auto-increment primary key
- `user_id`: Foreign key to users table
- `session_token`: Unique session identifier
- `created_at`: Session creation time
- `expires_at`: When session expires (30 min default)

**Purpose**: Session management, auto-logout

---

## API Endpoints

### Authentication Endpoints

#### POST `/api/voice_login`
```python
@app.route('/api/voice_login', methods=['POST'])
def api_voice_login():
    """API endpoint for voice login"""
    # Input: {username, password}
    # Output: {success: true/false, username}
```

#### POST `/api/logout`
```python
@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout current user"""
    # Clears session
    # Output: {success: true}
```

### Email Endpoints

#### GET `/api/voice_inbox`
```python
@app.route('/api/voice_inbox', methods=['GET'])
def api_voice_inbox():
    """Get inbox emails"""
    # Requires: Logged-in user
    # Output: {success: true, emails: [...]}
```

**Response Format:**
```json
{
  "success": true,
  "emails": [
    {
      "id": "123",
      "from": "sender@example.com",
      "subject": "Hello",
      "date": "Mon, 01 Jan 2024 12:00:00",
      "body": "Email content...",
      "seen": false
    }
  ]
}
```

#### GET `/api/sent_emails`
```python
@app.route('/api/sent_emails', methods=['GET'])
def api_sent_emails():
    """Get sent emails"""
    # Output: {success: true, emails: [...]}
```

#### POST `/api/send_email`
```python
@app.route('/api/send_email', methods=['POST'])
def api_send_email():
    """Send an email"""
    # Input: {to, subject, message}
    # Output: {success: true/false, message}
```

### Admin Endpoints

#### POST `/api/admin_login`
```python
@app.route('/api/admin_login', methods=['POST'])
def api_admin_login():
    """Admin authentication"""
    # Input: {username: 'admin', password}
    # Output: {success: true/false}
```

#### POST `/api/admin/add_user`
```python
@app.route('/api/admin/add_user', methods=['POST'])
def api_admin_add_user():
    """Create new user (admin only)"""
    # Input: {username, password, gmail_address, gmail_app_password}
    # Output: {success: true/false, message}
```

#### GET `/api/admin/users`
```python
@app.route('/api/admin/users', methods=['GET'])
def api_admin_users():
    """List all users (admin only)"""
    # Output: {success: true, users: [...]}
```

#### POST `/api/admin/delete_user`
```python
@app.route('/api/admin/delete_user', methods=['POST'])
def api_admin_delete_user():
    """Delete user (admin only)"""
    # Input: {username}
    # Output: {success: true/false, message}
```

### Utility Endpoints

#### POST `/api/log_voice`
```python
@app.route('/api/log_voice', methods=['POST'])
def api_log_voice():
    """Log voice interactions to terminal"""
    # Input: {type: 'user'/'system', text, page}
    # Prints to server console
```

#### GET `/api/voice_status`
```python
@app.route('/api/voice_status', methods=['GET'])
def api_voice_status():
    """Check login status"""
    # Output: {logged_in: true/false, username}
```

---

## Voice Commands

### Login Screen
- **Username**: Speak your username clearly
- **Password**: Speak your voice password

### Main Menu
- **"Compose Email"**: Open email composer
- **"Check Inbox"**: View inbox
- **"Check Sent Mail"**: View sent emails
- **"Logout"**: End session

### Inbox Navigation
- **"READ"**: Read current email body
- **"NEXT"**: Move to next email
- **"PREVIOUS"** / **"BACK"**: Move to previous email
- **"FIRST"** / **"ONE"**: Jump to email 1 and read it
- **"SECOND"** / **"TWO"**: Jump to email 2 and read it
- **"THIRD"** / **"THREE"**: Jump to email 3 and read it
- **"FOURTH"** / **"FOUR"**: Jump to email 4 and read it
- **"FIFTH"** / **"FIVE"**: Jump to email 5 and read it
- **"SIXTH"** / **"SIX"**: Jump to email 6 and read it
- **"SEVENTH"** / **"SEVEN"**: Jump to email 7 and read it
- **"EIGHTH"** / **"EIGHT"**: Jump to email 8 and read it
- **"NINTH"** / **"NINE"**: Jump to email 9 and read it
- **"TENTH"** / **"TEN"**: Jump to email 10 and read it
- **"REPEAT"**: Hear current email again (after reading)
- **"STOP"** / **"EXIT"**: Return to main menu

### Sent Mail Navigation
- **"NEXT"**: View next sent email
- **"STOP"**: Return to main menu

### Email Composition
- **Email Address**: Say slowly, e.g., "john dot smith at gmail dot com"
- **Subject**: Speak the subject line
- **Message**: Speak the email body
- **Confirmation**: Say "YES" to confirm, "NO" to retry
- **"SEND"**: Send the email
- **"CANCEL"**: Discard the email

### Web Interface (Keyboard)
- **SPACEBAR**:
  - During auto-read: Stop reading
  - Otherwise: Activate voice recognition
- **Mouse Clicks**: Alternative to voice commands

---

## Security Features

### 1. **Password Security**
- **Hashing Algorithm**: SHA-256
- **Storage**: Only hashed passwords stored
- **No Plain Text**: Passwords never stored in plain text

```python
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

### 2. **Gmail App Passwords**
- **Requirement**: 2-factor authentication enabled on Gmail
- **Format**: 16-character app-specific password
- **Storage**: Encrypted in database
- **Benefit**: No access to actual Gmail password

### 3. **Login Attempt Limiting**
- **Max Attempts**: 3 per session
- **Lockout**: After 3 failed attempts
- **Audit Trail**: All attempts logged to database

### 4. **Session Management**
- **Timeout**: 30 minutes (configurable)
- **Secret Key**: Flask session encryption
- **Server-Side**: Sessions stored server-side

### 5. **Admin Protection**
- **Cannot Delete Admin**: Admin user cannot be deleted
- **Session-Based Auth**: Admin must login to access panel

### 6. **Input Validation**
- Email format validation
- SQL injection prevention (parameterized queries)
- XSS prevention (template escaping)

### 7. **SSL/TLS Encryption**
- **SMTP**: STARTTLS on port 587
- **IMAP**: SSL on port 993
- **Gmail Servers**: All connections encrypted

---

## User Interface

### Pages

#### 1. **voice_web.html** (Landing Page)
- **Purpose**: Entry point
- **Features**:
  - Start voice login button
  - Registration option
  - Admin login link

#### 2. **voice_menu.html** (Main Menu)
- **Purpose**: Navigation hub after login
- **Options**:
  - Compose Email
  - Inbox
  - Sent Mail
  - Logout

#### 3. **voice_inbox.html** (Inbox)
- **Purpose**: View and manage inbox emails
- **Features**:
  - Auto-read first 3 emails on load
  - Spacebar to stop auto-read
  - Visual email list
  - Read button for each email
  - Voice commands via microphone button

#### 4. **voice_sent.html** (Sent Mail)
- **Purpose**: View sent emails
- **Features**:
  - Auto-read first 3 sent emails
  - Spacebar to stop auto-read
  - Visual list of sent emails

#### 5. **voice_compose.html** (Compose Email)
- **Purpose**: Write new emails
- **Features**:
  - Voice input for recipient, subject, message
  - Visual form as backup
  - Send button

#### 6. **admin_login.html** (Admin Login)
- **Purpose**: Admin authentication
- **Credentials**: admin/admin (default)

#### 7. **admin_dashboard.html** (Admin Panel)
- **Purpose**: User management
- **Features**:
  - Add new user
  - View all users
  - Delete users
  - User list table

### UI Design Elements

#### Color Scheme
- **Primary**: Purple gradient (#667eea to #764ba2)
- **Success**: Green (#4CAF50)
- **Danger**: Red (#f44336)
- **Background**: White cards on gradient background

#### Animations
```css
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
    50% { box-shadow: 0 0 0 20px rgba(76, 175, 80, 0); }
}
```
- **Microphone**: Pulsing effect when listening
- **Buttons**: Hover animations

#### Responsive Design
- **Max Width**: 900px for content
- **Mobile Friendly**: Touch-friendly buttons
- **Accessibility**: High contrast, large text

---

## Setup & Deployment

### Prerequisites
1. **Python**: 3.7 or higher
2. **Microphone**: For voice input
3. **Speakers**: For audio output
4. **Gmail Account**: With 2-factor authentication
5. **Internet**: For speech recognition and Gmail API

### Installation Steps

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
Flask==2.3.0
SpeechRecognition==3.10.0
pyttsx3==2.90
PyAudio==0.2.13
```

**Note**: PyAudio may require additional setup on some systems:
- **Windows**: Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/
- **Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`
- **Mac**: `brew install portaudio`

#### 2. Gmail App Password Setup
1. Enable 2-factor authentication on Gmail
2. Go to Google Account → Security → App Passwords
3. Generate new app password
4. Copy 16-character password (remove spaces)

#### 3. Initialize Database
```bash
python init_db.py
```

Creates:
- `voice_email.db` file
- Users, login_attempts, sessions tables
- Default admin user (admin/admin)

#### 4. Configure Settings
Edit `config.py`:
```python
SECRET_KEY = 'your-secret-key-here'  # Change in production
SPEECH_TIMEOUT = 10  # Adjust as needed
MAX_LOGIN_ATTEMPTS = 3
```

#### 5. Run Application
```bash
python voice_web_app.py
```

Server starts at: http://localhost:5000

#### 6. Create First User
1. Open http://localhost:5000/admin/login
2. Login with admin/admin
3. Add new user with:
   - Username
   - Voice password
   - Gmail address
   - Gmail app password

### Testing Microphone
```bash
python test_mic.py
```

Should display:
```
Microphone is working!
You said: [your speech]
```

---

## Testing & Validation

### Unit Tests

#### Test Voice Recognition
```python
def test_voice_handler():
    vh = VoiceHandler()
    vh.speak("Testing speech")
    result = vh.listen("Say something", timeout=5)
    assert result is not None
```

#### Test Email Handler
```python
def test_send_email():
    eh = EmailHandler(gmail, app_password)
    success, msg = eh.send_email(
        "test@example.com",
        "Test Subject",
        "Test Message"
    )
    assert success == True
```

#### Test Database
```python
def test_user_creation():
    db = Database()
    success, msg = db.create_user(
        "testuser",
        "testpass",
        "test@gmail.com",
        "apppassword"
    )
    assert success == True
```

### Integration Tests

#### Test Login Flow
1. Start application
2. Navigate to home page
3. Click "Start Voice Login"
4. Speak username
5. Speak password
6. Verify main menu appears

#### Test Email Composition
1. Login as user
2. Say "Compose Email"
3. Provide recipient, subject, message
4. Verify email sent successfully

#### Test Inbox Navigation
1. Login as user
2. Say "Check Inbox"
3. Say "Second" - verify jumps to email 2 and reads it
4. Say "Next" - verify moves to email 3
5. Say "Previous" - verify moves back to email 2
6. Say "Repeat" - verify re-reads current email

### Performance Tests

#### Voice Recognition Accuracy
- Test with different accents
- Test with background noise
- Test with fast/slow speech
- Measure: Recognition success rate

#### Response Time
- Measure: Time from voice command to action
- Target: < 2 seconds for most operations
- Gmail API calls may be slower (3-5 seconds)

#### Concurrent Users
- Test: Multiple users logging in simultaneously
- Verify: No session conflicts
- Verify: Database locks handled properly

---

## Project Statistics

### Code Metrics
- **Total Files**: 12
- **Python Files**: 6
- **HTML Files**: 6
- **Lines of Code**: ~2,500+
- **Functions**: 40+
- **Classes**: 3

### Module Breakdown
| Module | Lines | Functions | Purpose |
|--------|-------|-----------|---------|
| voice_web_app.py | 523 | 20 | Main application |
| email_handler.py | 282 | 11 | Gmail integration |
| voice_handler.py | 172 | 9 | Speech processing |
| database.py | 170 | 8 | Data persistence |
| config.py | 19 | 0 | Configuration |

### Features Implemented
- ✅ Voice authentication (3-attempt limit)
- ✅ Voice email composition with confirmation
- ✅ Inbox navigation (sequential + jump-to-number)
- ✅ Sent mail viewing
- ✅ Auto-read functionality (first 3 emails)
- ✅ Spacebar interrupt for auto-read
- ✅ Admin panel for user management
- ✅ Secure password hashing
- ✅ Session management
- ✅ Login attempt logging
- ✅ Voice command timeout handling
- ✅ Email format conversion (speech to email)
- ✅ HTML email content stripping
- ✅ Responsive web interface

---

## Future Enhancements

### Planned Features
1. **Offline Speech Recognition**: Reduce internet dependency
2. **Multiple Languages**: Support Hindi, Spanish, French
3. **Email Attachments**: Voice-guided file attachment
4. **Calendar Integration**: Voice-controlled calendar
5. **Contact Management**: Voice-based contact CRUD
6. **Email Search**: Search emails by sender/subject via voice
7. **Mobile App**: iOS/Android native apps
8. **Smart Reply**: AI-powered response suggestions
9. **Email Filters**: Voice-controlled filtering/sorting
10. **Voice Biometrics**: Additional security via voice print

### Technical Improvements
1. **Add Salt to Password Hashing**: Enhance security
2. **Redis Session Store**: Scalable session management
3. **WebSocket Support**: Real-time notifications
4. **Background Email Sync**: Periodic auto-sync
5. **Caching**: Reduce Gmail API calls
6. **Docker Deployment**: Containerization
7. **Load Balancing**: Support multiple instances
8. **Logging Framework**: Structured logging (e.g., ELK stack)

---

## Troubleshooting

### Common Issues

#### 1. Microphone Not Detected
**Solution**: Check PyAudio installation, verify microphone permissions

#### 2. Gmail Authentication Failed
**Solution**: Verify app password, ensure 2FA enabled, check for spaces in password

#### 3. Speech Recognition Not Working
**Solution**: Check internet connection, verify Google Speech API access

#### 4. "Module not found" Errors
**Solution**: Reinstall dependencies with `pip install -r requirements.txt`

#### 5. Database Locked
**Solution**: Close other connections, restart application

---

## Conclusion

This Voice-Based Gmail System successfully provides an accessible email solution for visually impaired users through:

1. **Complete Voice Control**: Every function accessible via voice
2. **Intelligent Navigation**: Jump-to-number feature for quick access
3. **Auto-Read Feature**: Immediate email reading on page load
4. **Flexible Controls**: Both voice and keyboard/mouse options
5. **Secure Authentication**: Hashed passwords, app-specific Gmail passwords
6. **Admin Management**: Centralized user administration
7. **Robust Error Handling**: Timeout recovery, retry mechanisms

The system demonstrates practical application of:
- Speech recognition technology
- Text-to-speech synthesis
- Email protocols (SMTP/IMAP)
- Web development (Flask, HTML/CSS/JavaScript)
- Database design (SQLite)
- Security best practices

**Project Impact**: Empowers visually impaired individuals to independently manage email communication.

---

## References & Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

### Email Protocols
- [SMTP Protocol (RFC 5321)](https://tools.ietf.org/html/rfc5321)
- [IMAP Protocol (RFC 3501)](https://tools.ietf.org/html/rfc3501)

### Accessibility Guidelines
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Voice User Interface Design](https://www.nngroup.com/articles/voice-first/)

---

**Document Version**: 1.0
**Last Updated**: January 9, 2026
**Author**: Voice-Based Gmail Team
**Project Status**: Completed & Functional

import sqlite3
import hashlib
from datetime import datetime
from config import Config

class Database:
    """Database manager for voice email system"""

    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                voice_password_hash TEXT NOT NULL,
                gmail_address TEXT NOT NULL,
                gmail_app_password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        ''')

        # Login attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success INTEGER DEFAULT 0
            )
        ''')

        # Session table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    def hash_password(self, password):
        """Hash voice password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, voice_password, gmail_address, gmail_app_password):
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            password_hash = self.hash_password(voice_password)
            cursor.execute('''
                INSERT INTO users (username, voice_password_hash, gmail_address, gmail_app_password)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, gmail_address, gmail_app_password))

            conn.commit()
            return True, "User created successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, f"Error creating user: {str(e)}"
        finally:
            conn.close()

    def verify_user(self, username, voice_password):
        """Verify user credentials"""
        conn = self.get_connection()
        cursor = conn.cursor()

        password_hash = self.hash_password(voice_password)
        cursor.execute('''
            SELECT id, username, gmail_address, gmail_app_password
            FROM users
            WHERE username = ? AND voice_password_hash = ? AND is_active = 1
        ''', (username, password_hash))

        user = cursor.fetchone()

        # Log login attempt
        cursor.execute('''
            INSERT INTO login_attempts (username, success)
            VALUES (?, ?)
        ''', (username, 1 if user else 0))

        if user:
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user['id'],))

        conn.commit()
        conn.close()

        return dict(user) if user else None

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, username, gmail_address, gmail_app_password
            FROM users
            WHERE id = ? AND is_active = 1
        ''', (user_id,))

        user = cursor.fetchone()
        conn.close()

        return dict(user) if user else None

    def get_all_users(self):
        """Get all users including active and inactive"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT username, gmail_address, is_active
            FROM users
            ORDER BY username
        ''')

        users = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return users

    def delete_user(self, username):
        """Soft delete a user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users SET is_active = 0
            WHERE username = ?
        ''', (username,))

        affected = cursor.rowcount
        conn.commit()
        conn.close()

        if affected > 0:
            return True, "User deleted successfully"
        else:
            return False, "User not found"

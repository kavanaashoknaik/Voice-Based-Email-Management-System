import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_PATH = 'voice_email.db'

    # Gmail SMTP settings
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    # Voice settings
    SPEECH_TIMEOUT = 10  # seconds - increased for better recognition
    PHRASE_TIME_LIMIT = 15  # seconds - increased for longer phrases

    # Security
    MAX_LOGIN_ATTEMPTS = 3
    SESSION_TIMEOUT = 1800  # 30 minutes

#!/usr/bin/env python3
"""
Database Initialization Script
Creates the database and adds default admin user
"""

from database import Database

def init_database():
    """Initialize database with admin user"""
    print("Initializing Voice Email System Database...")
    print("=" * 50)

    # Create database instance (this will create tables)
    db = Database()
    print("[OK] Database tables created")

    # Create admin user
    admin_username = "admin"
    admin_password = "1234"
    admin_email = "admin@system.local"
    admin_app_password = "no-app-password-needed"

    success, msg = db.create_user(
        admin_username,
        admin_password,
        admin_email,
        admin_app_password
    )

    if success:
        print(f"[OK] Admin user created successfully")
        print(f"  Username: {admin_username}")
        print(f"  Password: {admin_password}")
    else:
        if "already exists" in msg.lower():
            print(f"[OK] Admin user already exists")
        else:
            print(f"[ERROR] Error creating admin user: {msg}")

    print("=" * 50)
    print("Database initialization complete!")
    print("\nYou can now:")
    print("1. Run 'python web_app.py' for web interface")
    print("2. Run 'python app.py' for voice interface")
    print("\nAdmin login credentials:")
    print("  Username: admin")
    print("  Password: 1234")

if __name__ == '__main__':
    init_database()

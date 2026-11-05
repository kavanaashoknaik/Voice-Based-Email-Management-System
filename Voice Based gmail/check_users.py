"""
Simple script to check users in database
"""

from database import Database
import hashlib

def main():
    db = Database()

    print("\n" + "="*70)
    print("  USERS IN DATABASE")
    print("="*70 + "\n")

    users = db.get_all_users()

    if not users:
        print(">>> NO USERS FOUND!")
        print("\nYou need to create a user first:")
        print("1. Run: python voice_web_app.py")
        print("2. Go to: http://localhost:5000/admin/login")
        print("3. Login: admin / admin")
        print("4. Add a new user")
    else:
        for i, user in enumerate(users, 1):
            status = "[ACTIVE]" if user['is_active'] else "[INACTIVE]"
            print(f"{i}. Username: {user['username']}")
            print(f"   Gmail: {user['gmail_address']}")
            print(f"   Status: {status}")
            print()

        # Ask if user wants to test a password
        print("="*70)
        test = input("\nDo you want to test a password? (y/n): ")

        if test.lower() == 'y':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            # Test verification
            user_data = db.verify_user(username, password)

            if user_data:
                print(f"\n>>> SUCCESS! Password is correct for '{username}'")
                print(f"Gmail: {user_data['gmail_address']}")
            else:
                print(f"\n>>> FAILED! Password is incorrect for '{username}'")
                print("\nPassword you entered:", password)
                print("Password hash:", hashlib.sha256(password.encode()).hexdigest())
                print("\nTip: Make sure you're typing exactly what you say during voice login")

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()

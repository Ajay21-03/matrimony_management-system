from matrimony.db import DB
from datetime import datetime

class Message:
    def __init__(self):
        self.db = DB()  # Create an instance of the DB class

    def manage_messages(self, username):
        while True:
            print("\n📨 Message Management 📨")
            print("-" * 30)
            print("1. 📬 View received messages")
            print("2. 💌 Send a message")
            print("3. 🚪 Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_received_messages(username)
            elif choice == '2':
                self.send_message(username)
            elif choice == '3':
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def view_received_messages(self, username):
        self.db.cursor.execute('''SELECT sender, message_content, timestamp FROM messages WHERE recipient=%s''', (username,))
        messages = self.db.cursor.fetchall()
        
        if messages:
            print("📬 Received Messages 📬")
            print("-" * 30)
            for message in messages:
                sender, content, timestamp = message
                print(f"📨 From: {sender}")
                print(f"💬 Message: {content}")
                print(f"🕒 Received at: {timestamp}")
                print("-" * 30)
        else:
            print("📭 No messages received.")

    def send_message(self, sender_username):
        print("\n💌 Send Message 💌")
        print("-" * 30)
        recipient = input("Enter the username of the recipient: ")
        self.db.cursor.execute("SELECT username FROM users WHERE username=%s", (recipient,))
        if not self.db.cursor.fetchone():
            print("❌ Recipient does not exist.")
            return

        message_content = input("Enter your message: ")
        timestamp = datetime.now()

        self.db.cursor.execute('''INSERT INTO messages (sender, recipient, message_content, timestamp)
                              VALUES (%s, %s, %s, %s)''', (sender_username, recipient, message_content, timestamp))
        self.db.connection.commit()

        print("✅ Message sent successfully!")

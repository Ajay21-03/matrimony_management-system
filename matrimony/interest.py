from matrimony.db import DB
from datetime import datetime

class Interest:
    def __init__(self):
        self.db = DB()  # Create an instance of the DB class

    def send_interest(self, sender_username):
        print("\n💌 Welcome to Interest 🌟")
        while True:
            print("1. 💌 Send interest")
            print("2. 🌟 View received interests")
            choice = input("🔢 Enter your choice: ")

            if choice == '1':
                self.send_interest_action(sender_username)
            elif choice == '2':
                self.view_received_interests(sender_username)
            else:
                print("❌ Invalid choice.")
                continue

            break

    def send_interest_action(self, sender_username):
        print("💌 Send Interest 💌")
        print("🔹" * 30)
        recipient = input("📝 Enter the username of the recipient: ")
        self.db.cursor.execute("SELECT username FROM users WHERE username=%s", (recipient,))
        if not self.db.cursor.fetchone():
            print("❌ Recipient does not exist.")
            return

        interest = "Interested"
        self.db.cursor.execute('''INSERT INTO interests (recipient, sender, interest)
                            VALUES (%s, %s, %s)''', (recipient, sender_username, interest))
        self.db.connection.commit()
        print("✅ Interest sent successfully!")

    def view_received_interests(self, recipient_username):
        print("🌟 Received Interests 🌟")
        print("🔹" * 30)
        self.db.cursor.execute('''SELECT sender FROM interests WHERE recipient=%s''', (recipient_username,))
        interests = self.db.cursor.fetchall()
        if interests:
            print("📬 Users interested in you 📬:")
            for interest in interests:
                sender = interest[0]
                self.process_received_interest(recipient_username, sender)
        else:
            print("📭 No interests received.")

    def process_received_interest(self, recipient_username, sender_username):
        self.db.cursor.execute('''SELECT name, city FROM users WHERE username=%s''', (sender_username,))
        sender_info = self.db.cursor.fetchone()
        if sender_info:
            print(f"❤️ {sender_username} ({sender_info[0]} from {sender_info[1]})")
            reply = input(f"🔄 Do you want to confirm the match with {sender_username} (yes/no)? ").lower()
            if reply == 'yes':
                self.accept_interest(recipient_username, sender_username)
            elif reply == 'no':
                self.reject_interest(recipient_username, sender_username)
            else:
                print("❌ Invalid choice.")

    def accept_interest(self, recipient_username, sender_username):
        print(f"✅ You accepted the interest from {sender_username}! 💕")

        self.db.cursor.execute('''SELECT name, city FROM users WHERE username=%s''', (recipient_username,))
        user_info = self.db.cursor.fetchone()
        self.db.cursor.execute('''SELECT name, city FROM users WHERE username=%s''', (sender_username,))
        sender_info = self.db.cursor.fetchone()

        self.db.cursor.execute('''INSERT INTO matches (user1_name, user1_city, user2_name, user2_city)
                                              VALUES (%s, %s, %s, %s)''',
                                           (user_info[0], user_info[1], sender_info[0], sender_info[1]))

        self.db.cursor.execute('''DELETE FROM interests WHERE recipient=%s OR sender=%s''', (recipient_username, recipient_username))
        self.db.cursor.execute('''DELETE FROM interests WHERE recipient=%s OR sender=%s''', (sender_username, sender_username))
        self.db.cursor.execute('''DELETE FROM messages WHERE sender=%s OR recipient=%s''', (recipient_username, recipient_username))
        self.db.cursor.execute('''DELETE FROM messages WHERE sender=%s OR recipient=%s''', (sender_username, sender_username))
        self.db.connection.commit()

        self.db.cursor.execute('''DELETE FROM users WHERE username=%s OR username=%s''', (recipient_username, sender_username))
        self.db.connection.commit()

    def reject_interest(self, recipient_username, sender_username):
        rejection_message = "🚫 Your interest has been rejected."
        self.db.cursor.execute('''INSERT INTO messages (sender, recipient, message_content, timestamp)
                                            VALUES (%s, %s, %s, %s)''', (recipient_username, sender_username, rejection_message, datetime.now()))
        self.db.connection.commit()
        self.db.cursor.execute('''DELETE FROM interests WHERE recipient=%s AND sender=%s''', (recipient_username, sender_username))
        self.db.connection.commit()
        print(f"❌ You rejected the interest from {sender_username}.")

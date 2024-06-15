from matrimony.db import DB

class CompatibilityChecker:
    def __init__(self):
        self.db = DB()  # Create an instance of the DB class

    def flames(self, name1, name2):
        name1 = name1.lower().replace(" ", "")
        name2 = name2.lower().replace(" ", "")
        common = list(set(name1) & set(name2))
        total = len(name1) + len(name2) - 2 * len(common)
        flames_word = ["Friends", "Love", "Affection", "Marriage", "Enemy", "Siblings"]
        while len(flames_word) > 1:
            split_index = (total % len(flames_word)) - 1
            if split_index >= 0:
                flames_word = flames_word[split_index + 1:] + flames_word[:split_index]
            else:
                flames_word = flames_word[:len(flames_word) - 1]
        return flames_word[0]

    def check_astrology(self, username):
        print("\n🔥 FLAMES Game 🔥")
        print("🔹" * 30)
        partner_name = input("📝 Enter the name of the partner to check compatibility with: ")
        user_name = self.get_user_name(username)
        
        compatibility_result = self.flames(user_name, partner_name)
        
        print(f"💫 Astrology compatibility between {user_name} and {partner_name}: {compatibility_result}")

    def get_user_name(self, username):
        self.db.cursor.execute('''SELECT name FROM users WHERE username=%s''', (username,))
        user_record = self.db.cursor.fetchone()
        if user_record:
            return user_record[0]
        else:
            print("❌ User not found.")
            return None

from matrimony.db import DB

class Search:
    def __init__(self):
        self.db = DB()  # Create an instance of the DB class

    def search_matches(self, username):
        for i in range(2):
            print("\n")
        print("🔍💖🔍 Search Matches 🔍💖🔍")
        print("🔹" * 30)
        print("🔍🔍 Search matches by:")
        print("1. 📛 Username")
        print("2. 🌟 Preferences")
        print("3. 🌏 All (Display all opposite genders)")
        choice = input("🔢 Enter your choice: ")
        
        if choice == '1':
            self.search_by_username()
        elif choice == '2':
            self.search_by_preferences(username)
        elif choice == '3':
            self.display_all_opposite_genders(username)
        else:
            print("❌ Invalid choice. Please try again.")

    def search_by_username(self):
        search_username = input("📝 Enter the username to search matches for: ")
        
        # Search for the user in the database
        self.db.cursor.execute('''SELECT name, city , age, gender, profession, salary FROM users WHERE username=%s''', (search_username,))
        user_details = self.db.cursor.fetchone()

        if user_details:
            user_name, user_city, user_age, user_gender, user_profession, user_salary = user_details
            print(f"🔍📝 Details for user {search_username}:")
            print(f"📝 Name: {user_name}")
            print(f"🎂 Age: {user_age}")
            print(f"🧬 Gender: {user_gender}")
            print(f"🏙️ City: {user_city}")
            print(f"💼 Profession: {user_profession}")
            print(f"💰 Salary: {user_salary}")
        else:
            print(f"❌ No user found with username {search_username}.")

    def search_by_preferences(self, username):
        min_age = int(input("🔢 Enter minimum age preference: "))
        max_age = int(input("🔢 Enter maximum age preference: "))
        profession = input("💼 Enter profession preference: ").title()
        salary = input("💰 Enter minimum salary preference: ")
        city = input("🏙️ Enter city preference: ").title()
        
        self.db.cursor.execute('''SELECT username, name, age, gender, city, profession, salary FROM users
                              WHERE age BETWEEN %s AND %s AND profession=%s AND salary>=%s AND city=%s AND username!=%s''',
                           (min_age, max_age, profession, salary, city, username))
        potential_matches = self.db.cursor.fetchall()
        
        if potential_matches:
            print("❤️💘❤️ Potential matches:")
            for match in potential_matches:
                match_username, match_name, match_age, match_gender, match_city, match_profession, match_salary = match
                print(f"📝 {match_name} ({match_gender}), 🎂 Age: {match_age}, 🏙️ City: {match_city}, 💼 Profession: {match_profession}, 💰 Salary: {match_salary} - Username: {match_username}")
            
            interest_username = input("📝 Enter the username of the user you are interested in: ")
            self.db.cursor.execute('''INSERT INTO interests (recipient, sender, interest)
                            VALUES (%s, %s, %s)''', (interest_username, username, 'Interested'))
            self.db.connection.commit()
            print("✅ Interest sent successfully!")
        else:
            print("❌ No potential matches found.")

    def display_all_opposite_genders(self, username):
        self.db.cursor.execute('''SELECT username, name, age, gender, city, profession, salary FROM users
                              WHERE gender != (SELECT gender FROM users WHERE username=%s)''', (username,))
        all_matches = self.db.cursor.fetchall()
        
        if all_matches:
            print("💘🌍💘 All potential matches of the opposite gender:")
            for match in all_matches:
                match_username, match_name, match_age, match_gender, match_city, match_profession, match_salary = match
                print(f"📝 {match_name} ({match_gender}), 🎂 Age: {match_age}, 🏙️ City: {match_city}, 💼 Profession: {match_profession}, 💰 Salary: {match_salary} - Username: {match_username}")
        else:
            print("❌ No potential matches found.")

class ConfirmedMatches:
    def __init__(self):
        self.db = DB()  # Create an instance of the DB class

    def view_confirmed_matches(self):
        self.db.cursor.execute('''SELECT user1_name, user1_city, user2_name, user2_city
                              FROM matches''')
        
        matches = self.db.cursor.fetchall()
        if matches:
            print("\n💑💖 Confirmed Matches 💖💑")
            print("🔹" * 30)
            for match in matches:
                print(f"\n❤️ {match[0]} from {match[1]} is matched with {match[2]} from {match[3]}")
        else:
            print("🚫 No confirmed matches found.")

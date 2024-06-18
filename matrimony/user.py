from matrimony.db import DB
import maskpass  # Importing the maskpass module

class User:
    def __init__(self):
        self.db = DB()  # Create an instance of the DB class

    def register(self):
        print("\n📝 Register New User")
        print("-" * 30)
        username = input("Enter a username: ")
        if self.username_exists(username):
            print("⚠️ Username already exists. Please choose a different username.")
            return
        password = maskpass.askpass(prompt="Enter a password: ", mask="*")  # Using maskpass to hide password input with asterisks
        name = input("Enter your name: ").title()
        age = int(input("Enter your age: "))
        if age < 18:
            print("🚫 You must be at least 18 years old to register.")
            return
        gender = input("Enter your gender (Male/Female): ").title()
        city = input("Enter your city: ").title()
        profession = input("Enter your profession: ").title()
        salary = input("Enter your salary: ")

        self.db.cursor.execute('''INSERT INTO users (username, password, name, age, gender, city, profession, salary)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                              (username, password, name, age, gender, city, profession, salary))
        self.db.connection.commit()
        print("✅ User registered successfully!")

    def login(self):
        print("\n🔑➡️ User Login")
        print("-" * 30)
        username = input("Enter your username: ")
        password = maskpass.askpass(prompt="Enter your password: ", mask="*")  # Using maskpass to hide password input with asterisks

        self.db.cursor.execute('''SELECT * FROM users WHERE username=%s AND password=%s''', (username, password))

        user = self.db.cursor.fetchone()

        if user:
            print("✅ Login successful!")
            return username
        else:
            print("❌ Login failed. Check your username and password.")
            return None

    def view_profile(self, username):
        print("\n👤🔍 View Profile")
        print("-" * 30)
        
        self.db.cursor.execute('''SELECT username, name, age, gender, city, profession, salary 
                                            FROM users WHERE username=%s''', (username,))

        user_profile = self.db.cursor.fetchone()

        if user_profile:
            print(f"Username: {user_profile[0]}")
            print(f"Name: {user_profile[1]}")
            print(f"Age: {user_profile[2]}")
            print(f"Gender: {user_profile[3]}")
            print(f"City: {user_profile[4]}")
            print(f"Profession: {user_profile[5]}")
            print(f"Salary: {user_profile[6]}")
        else:
            print("❌ Profile not found.")

    def edit_profile(self, username):
        print("\n📝 Edit Profile")
        print("-" * 30)
        
        name = input("Enter your new name: ").title()
        age = int(input("Enter your new age: "))
        city = input("Enter your new city: ").title()
        profession = input("Enter your new profession: ").title()
        salary = input("Enter your new salary: ")

        self.db.cursor.execute('''UPDATE users SET name=%s, age=%s, city=%s, profession=%s, salary=%s 
                                 WHERE username=%s''', (name, age, city, profession, salary, username))
        self.db.connection.commit()
        print("✅ Profile updated successfully!")
        
    def username_exists(self, username):
        self.db.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        return bool(self.db.cursor.fetchone())

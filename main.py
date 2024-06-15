from matrimony.user import User
from matrimony.message import Message
from matrimony.interest import Interest
from matrimony.match import Search,ConfirmedMatches
from matrimony.astrology import CompatibilityChecker
from matrimony.db import DB

class MatrimonySystem:
    def __init__(self):
        self.user_manager = User()
        self.message_manager = Message()
        self.interest_manager = Interest()
        self.match_manager = Search()
        self.Confirmed_matches=ConfirmedMatches()
        self.compatibility_checker = CompatibilityChecker()
        self.db = DB()

    def run(self):
        self.db.create_tables()
        print("\n💼 Matrimony Management System 💼")
        print("-" * 30)
        while True:
            print("\n1. Register")
            print("2. Login")
            print("3. Exit🏃‍♂️💨")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.user_manager.register()
            elif choice == '2':
                username = self.user_manager.login()
                if username:
                    self.user_menu(username)
            elif choice == '3':
                print("👋 Exiting the system. Goodbye!")
                break
            else:
                print("❌ Invalid choice.")

    def user_menu(self, username):
        while True:
            print("\n🏠 Main Menu 🏠")
            print("-" * 30)
            print("\n1. Profile")
            print("2. Search for Matches")
            print("3. View and Send Messages")
            print("4. Send/Receive Interest")
            print("5. Check Astrology Compatibility")
            print("6. View Confirmed Matches")
            print("7. Logout🚪➡️")
            user_choice = input("Enter your choice: ")
            
            if user_choice == '1':
                self.profile_menu(username)
            elif user_choice == '2':
                self.match_manager.search_matches(username)
            elif user_choice == '3':
                self.message_manager.manage_messages(username)
            elif user_choice == '4':
                self.interest_manager.send_interest(username)
            elif user_choice == '5':
                self.compatibility_checker.check_astrology(username)
            elif user_choice == '6':
                self.Confirmed_matches.view_confirmed_matches()
            elif user_choice == '7':
                print("👋 Logging out...")
                break
            else:
                print("🚫 Invalid choice. Please try again.")

    def profile_menu(self, username):
        choice = input("Do you want to🧐 View or Edit Profile? (view/edit): ").lower()
        if choice == 'view':
            self.user_manager.view_profile(username)
        elif choice == 'edit':
            self.user_manager.edit_profile(username)

# Usage example
if __name__ == "__main__":
    matrimony_system = MatrimonySystem()
    matrimony_system.run()

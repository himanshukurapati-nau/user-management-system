import logging


# Enable logging
logging.basicConfig(
    filename="user_management.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class User:
    """
    Represents a single user in the system.
    """

    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age

    def update_user(self, name=None, age=None):
        """
        Update user details.
        """
        if name:
            self.name = name
        if age:
            self.age = age

    def __str__(self):
        return f"User(ID: {self.user_id}, Name: {self.name}, Age: {self.age})"


class UserDatabase:
    """
    A database to store and manage users.
    """

    def __init__(self):
        self.users = {}

    def add_user(self, user):
        logging.info("Adding user: %s", user)
        if user.user_id in self.users:
            raise ValueError("User ID already exists")
        self.users[user.user_id] = user

    def get_user(self, user_id):
        if user_id not in self.users:
            raise ValueError("User not found")
        return self.users[user_id]

    def delete_user(self, user_id):
        logging.info("Deleting user with ID: %s", user_id)
        if user_id not in self.users:
            raise ValueError("User not found")
        del self.users[user_id]

    def update_user(self, user_id, name=None, age=None):
        if user_id not in self.users:
            raise ValueError("User not found")
        user = self.users[user_id]
        user.update_user(name, age)
        logging.info("Updated user: %s", user)

    def list_users(self):
        return list(self.users.values())

    def search_users_by_name(self, name):
        """
        Search users by their name.
        """
        return [user for user in self.users.values() if user.name.lower() == name.lower()]


class FileManager:
    """
    Handles file operations for saving and reading user data.
    """

    def save_to_file(self, file_path, data):
        logging.info("Saving data to file: %s", file_path)
        with open(file_path, 'w') as file:
            file.write(data)

    def read_from_file(self, file_path):
        logging.info("Reading data from file: %s", file_path)
        with open(file_path, 'r') as file:
            return file.read()


class UserService:
    def __init__(self, user_db, file_manager):
        self.user_db = user_db
        self.file_manager = file_manager

    def create_user(self, user_id, name, age):
        user = User(user_id, name, age)
        self.user_db.add_user(user)

    def delete_user(self, user_id):
        self.user_db.delete_user(user_id)

    def get_user(self, user_id):
        return self.user_db.get_user(user_id)

    def update_user(self, user_id, name=None, age=None):
        self.user_db.update_user(user_id, name, age)

    def search_user_by_name(self, name):
        return self.user_db.search_users_by_name(name)

    def list_all_users(self):
        return self.user_db.list_users()

    def export_users(self, file_path):
        users = self.user_db.list_users()
        data = "\n".join(str(user) for user in users)
        self.file_manager.save_to_file(file_path, data)

    def import_users ( file_path,self):
        data = self.file_manager.read_from_file(file_path)
        for line in data.split('\n'):
            if line.strip():
                user_id, name, age = UserService.parse_user_line(line)
                self.create_user(user_id, name, int(age))

    @staticmethod
    def parse_user_line(line):
        """
        Parses a single line of user data in the format:
        User(ID: 1, Name: Alice, Age: 25)
        """
        line = line.strip()
        if not line.startswith("User(") or not line.endswith(")"):
            raise ValueError("Invalid user data format")

        # Remove "User(" prefix and ")" suffix
        line = line[5:-1]
        parts = line.split(", ")

        if len(parts) != 3:
            raise ValueError("Invalid user data format")

        user_id = parts[0].split(": ")[1]
        name = parts[1].split(": ")[1]
        age = parts[2].split(": ")[1]

        return user_id, name, age



class InputValidator:
    @staticmethod
    def validate_user_id(user_id):
        if not user_id.isdigit() or int(user_id) <= 0:
            raise ValueError("Invalid User ID")

    @staticmethod
    def validate_name(name):
        if not name.isalpha() or len(name) < 2:
            raise ValueError("Invalid Name")

    @staticmethod
    def validate_age(age):
        if not age.isdigit() or not (0 < int(age) < 120):
            raise ValueError("Invalid Age")


def print_help():
    """
    Print help information for the user.
    """
    print("\nHelp Menu:")
    print("1. Create User - Add a new user to the system")
    print("2. List Users - Display all users")
    print("3. Get User - Display a user's details by ID")
    print("4. Update User - Modify user details")
    print("5. Search User - Find users by name")
    print("6. Delete User - Remove a user by ID")
    print("7. Export Users - Save user data to a file")
    print("8. Import Users - Load user data from a file")
    print("9. Help - Show this help menu")
    print("10. Exit - Close the application")


def main():
    user_db = UserDatabase()
    file_manager = FileManager()
    user_service = UserService(user_db, file_manager)

    print("Welcome to the Enhanced User Management System")

    while True:
        print("\nOptions:")
        print("1. Create User")
        print("2. List Users")
        print("3. Get User")
        print("4. Update User")
        print("5. Search User")
        print("6. Delete User")
        print("7. Export Users")
        print("8. Import Users")
        print("9. Help")
        print("10. Exit")

        try:
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                user_id = input("Enter User ID: ").strip()
                InputValidator.validate_user_id(user_id)
                name = input("Enter Name: ").strip()
                InputValidator.validate_name(name)
                age = input("Enter Age: ").strip()
                InputValidator.validate_age(age)

                user_service.create_user(user_id, name, int(age))
                print("User created successfully")

            elif choice == '2':
                users = user_service.list_all_users()
                print("Users:")
                for user in users:
                    print(user)

            elif choice == '3':
                user_id = input("Enter User ID: ").strip()
                InputValidator.validate_user_id(user_id)
                user = user_service.get_user(user_id)
                print("User Details:")
                print(user)

            elif choice == '4':
                user_id = input("Enter User ID to update: ").strip()
                InputValidator.validate_user_id(user_id)
                name = input("Enter new name (or leave blank): ").strip()
                age = input("Enter new age (or leave blank): ").strip()
                user_service.update_user(user_id, name or None, int(age) if age else None)
                print("User updated successfully")

            elif choice == '5':
                name = input("Enter name to search: ").strip()
                users = user_service.search_user_by_name(name)
                print("Search Results:")
                for user in users:
                    print(user)

            elif choice == '6':
                user_id = input("Enter User ID: ").strip()
                InputValidator.validate_user_id(user_id)
                user_service.delete_user(user_id)
                print("User deleted successfully")

            elif choice == '7':
                file_path = input("Enter file path to save users: ").strip()
                user_service.export_users(file_path)
                print("Users exported successfully")

            elif choice == '8':
                file_path = input("Enter file path to import users from: ").strip()
                user_service.import_users(file_path)
                print("Users imported successfully")

            elif choice == '9':
                print_help()

            elif choice == '10':
                print("Exiting User Management System")
                break

            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            logging.error("Validation error: %s", e)
            print(f"Error: {e}")
        except Exception as e:
            logging.exception("Unexpected error occurred")
            print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()

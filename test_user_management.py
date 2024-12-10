import unittest
from user_management import User, UserDatabase, UserService, FileManager, InputValidator


class TestUser(unittest.TestCase):
    def test_create_user(self):
        user = User(user_id="1", name="Alice", age=25)
        self.assertEqual(user.user_id, "1")
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.age, 25)

    def test_update_user(self):
        user = User(user_id="1", name="Alice", age=25)
        user.update_user(name="Bob", age=30)
        self.assertEqual(user.name, "Bob")
        self.assertEqual(user.age, 30)


class TestUserDatabase(unittest.TestCase):
    def setUp(self):
        self.user_db = UserDatabase()
        self.user = User(user_id="1", name="Alice", age=25)

    def test_add_user(self):
        self.user_db.add_user(self.user)
        self.assertEqual(len(self.user_db.list_users()), 1)

    def test_get_user(self):
        self.user_db.add_user(self.user)
        user = self.user_db.get_user("1")
        self.assertEqual(user.name, "Alice")

    def test_delete_user(self):
        self.user_db.add_user(self.user)
        self.user_db.delete_user("1")
        self.assertEqual(len(self.user_db.list_users()), 0)

    def test_update_user(self):
        self.user_db.add_user(self.user)
        self.user_db.update_user("1", name="Bob", age=30)
        user = self.user_db.get_user("1")
        self.assertEqual(user.name, "Bob")
        self.assertEqual(user.age, 30)

    def test_search_users_by_name(self):
        self.user_db.add_user(self.user)
        results = self.user_db.search_users_by_name("Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Alice")


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()
        self.test_file = "test_users.txt"

    def tearDown(self):
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_read_from_file(self):
        data = "User(ID: 1, Name: Alice, Age: 25)"
        self.file_manager.save_to_file(self.test_file, data)
        read_data = self.file_manager.read_from_file(self.test_file)
        self.assertEqual(data, read_data)


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_db = UserDatabase()
        self.file_manager = FileManager()
        self.user_service = UserService(self.user_db, self.file_manager)
        self.user = User(user_id="1", name="Alice", age=25)

    def test_create_user(self):
        self.user_service.create_user("1", "Alice", 25)
        user = self.user_db.get_user("1")
        self.assertEqual(user.name, "Alice")

    def test_delete_user(self):
        self.user_service.create_user("1", "Alice", 25)
        self.user_service.delete_user("1")
        self.assertEqual(len(self.user_db.list_users()), 0)

    def test_list_all_users(self):
        self.user_service.create_user("1", "Alice", 25)
        users = self.user_service.list_all_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, "Alice")

    def test_export_and_import_users(self):
        self.user_service.create_user("1", "Alice", 25)
        test_file = "test_users.txt"
        self.user_service.export_users(test_file)

        # Clear database and import
        self.user_db = UserDatabase()
        self.user_service = UserService(self.user_db, self.file_manager)
        self.user_service.import_users(test_file)

        users = self.user_service.list_all_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, "Alice")

        import os
        os.remove(test_file)

    def test_search_user_by_name(self):
        self.user_service.create_user("1", "Alice", 25)
        results = self.user_service.search_user_by_name("Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Alice")


class TestInputValidator(unittest.TestCase):
    def test_validate_user_id(self):
        self.assertRaises(ValueError, InputValidator.validate_user_id, "0")
        self.assertRaises(ValueError, InputValidator.validate_user_id, "-1")
        self.assertRaises(ValueError, InputValidator.validate_user_id, "abc")
        InputValidator.validate_user_id("1")  # Should not raise

    def test_validate_name(self):
        self.assertRaises(ValueError, InputValidator.validate_name, "A")
        self.assertRaises(ValueError, InputValidator.validate_name, "123")
        self.assertRaises(ValueError, InputValidator.validate_name, "")
        InputValidator.validate_name("Alice")  # Should not raise



    def test_validate_age(self):
        self.assertRaises(ValueError, InputValidator.validate_age, "-1")
        self.assertRaises(ValueError, InputValidator.validate_age, "121")
        self.assertRaises(ValueError, InputValidator.validate_age, "abc")
        InputValidator.validate_age("25")  # Should not raise


if __name__ == "__main__":
    unittest.main()

import unittest
from cinema_booking_system.seating_config import SeatingConfig

class TestSeating(unittest.TestCase):
    def test_user_creation(self):
        user = SeatingConfig("John Doe", "john.doe@example.com")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john.doe@example.com")

if __name__ == '__main__':
    unittest.main()
import unittest
from cinema_booking_system.models.seating_config import SeatingConfig

class TestScreening(unittest.TestCase):
    def test_screening_creation(self):
        seat_config = SeatingConfig(10, 10)
        self.assertEqual(seat_config.row_count, 10)
        self.assertEqual(seat_config._seat_count_per_row, 10)

if __name__ == '__main__':
    unittest.main()
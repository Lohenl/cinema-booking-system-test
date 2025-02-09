import unittest
from cinema_booking_system.models.seating_config import SeatingConfig

class TestSeatingConfig(unittest.TestCase):
    def test_seating_config_creation(self):
        """Object Creation: SeatingConfig"""
        seat_config = SeatingConfig(10, 10)
        self.assertEqual(seat_config.row_count, 10)
        self.assertEqual(seat_config._seat_count_per_row, 10)

if __name__ == '__main__':
    unittest.main()
import unittest
from datetime import datetime
from cinema_booking_system.models.seating_config import SeatingConfig
from cinema_booking_system.models.movie import Movie
from cinema_booking_system.models.screening import Screening

class TestScreening(unittest.TestCase):
    def test_screening_creation(self):
        """Object Creation: Screening"""
        seating_config = SeatingConfig(10, 10)
        movie = Movie("John Wick")
        screening = Screening(datetime(2025, 2, 8, 19, 30), seating_config, movie, [])
        self.assertEqual(screening.movie.title, "John Wick")
        self.assertEqual(screening.start_time, datetime(2025, 2, 8, 19, 30))
        self.assertEqual(screening.seat_config.row_count, 10)
        self.assertEqual(screening.seat_config._seat_count_per_row, 10)

if __name__ == '__main__':
    unittest.main()
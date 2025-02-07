# filepath: /c:/Users/winso/cinema-booking-system-test/tests/test_screening.py
import unittest
from datetime import datetime
from cinema_booking_system.movie import Movie
from cinema_booking_system.screening import Screening

class TestScreening(unittest.TestCase):
    def test_screening_creation(self):
        movie = Movie("Inception", 148, "PG-13")
        screening = Screening(movie, datetime(2025, 2, 8, 19, 30))
        self.assertEqual(screening.movie.title, "Inception")
        self.assertEqual(screening.start_time, datetime(2025, 2, 8, 19, 30))

if __name__ == '__main__':
    unittest.main()
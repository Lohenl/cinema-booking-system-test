# filepath: /c:/Users/winso/cinema-booking-system-test/tests/test_movie.py
import unittest
from cinema_booking_system.models.movie import Movie

class TestMovie(unittest.TestCase):
    def test_movie_creation(self):
        movie = Movie("Inception", 148, "PG-13")
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(movie.duration, 148)
        self.assertEqual(movie.rating, "PG-13")

if __name__ == '__main__':
    unittest.main()
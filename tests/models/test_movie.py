import unittest
from cinema_booking_system.models.movie import Movie

class TestMovie(unittest.TestCase):
    def test_movie_creation(self):
        """Object Creation: Movie"""
        movie = Movie("Inception")
        self.assertEqual(movie.title, "Inception")

if __name__ == '__main__':
    unittest.main()

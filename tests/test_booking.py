# filepath: /c:/Users/winso/cinema-booking-system-test/tests/test_booking.py
import unittest
from datetime import datetime
from cinema_booking_system.movie import Movie
from cinema_booking_system.screening import Screening
from cinema_booking_system.booking import Booking
from cinema_booking_system.seating import Seating

class TestBooking(unittest.TestCase):
    def test_booking_creation(self):
        movie = Movie("Inception", 148, "PG-13")
        user = Seating("John Doe", "john.doe@example.com")
        screening = Screening(movie, datetime(2025, 2, 8, 19, 30))
        booking = Booking(user, screening, 2)
        self.assertEqual(booking.user.name, "John Doe")
        self.assertEqual(booking.screening.movie.title, "Inception")
        self.assertEqual(booking.seats, 2)

if __name__ == '__main__':
    unittest.main()
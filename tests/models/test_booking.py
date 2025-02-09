import unittest
from datetime import datetime
from cinema_booking_system.models.movie import Movie
from cinema_booking_system.models.screening import Screening
from cinema_booking_system.models.booking import Booking
from cinema_booking_system.models.seating_config import SeatingConfig

class TestBooking(unittest.TestCase):
    def test_booking_creation(self):
        booking = Booking('GIC0001', ["A1", "A2"])
        self.assertEqual(booking.id, "GIC0001")
        self.assertEqual(booking.seats, ["A1", "A2"])

if __name__ == '__main__':
    unittest.main()
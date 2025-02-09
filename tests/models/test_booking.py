import unittest
from cinema_booking_system.models.booking import Booking

class TestBooking(unittest.TestCase):
    def test_booking_creation(self):
        """Object Creation: Booking"""
        booking = Booking('GIC0001', ["A1", "A2"])
        self.assertEqual(booking.id, "GIC0001")
        self.assertEqual(booking.seats, ["A1", "A2"])

if __name__ == '__main__':
    unittest.main()
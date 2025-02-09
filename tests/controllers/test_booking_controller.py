import unittest
from unittest.mock import patch
from datetime import datetime
from cinema_booking_system.models.movie import Movie
from cinema_booking_system.models.screening import Screening
from cinema_booking_system.models.seating_config import SeatingConfig
from cinema_booking_system.models.booking import Booking
from cinema_booking_system.booking_menu import BookingMenu
from cinema_booking_system.controllers.booking_controller import BookingController

class TestBookingController(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test."""
        self.movie = Movie("TestMovie")
        self.seating_config = SeatingConfig(5, 10)
        self.screening = Screening(
            datetime(2024, 1, 1, 12, 0),
            self.seating_config,
            self.movie,
            []
        )
        self.booker = BookingController(self.screening)

    def test_initialization(self):
        """Test proper initialization of BookingMenu."""
        self.assertEqual(self.booker.screening, self.screening)
        self.assertIsNotNone(self.booker.screening)
        self.assertIsNotNone(self.booker.total_seats)
        self.assertIsNotNone(self.booker.seats_available)

    def test_is_seat_booked(self):
        """Test seat booking status check."""
        # Add a booking
        booking = Booking("GIC0001", ["A1", "A2"])
        self.screening.booking_data.append(booking)
        
        # Test booked seats
        self.assertTrue(self.booker.is_seat_booked("A1"))
        self.assertTrue(self.booker.is_seat_booked("A2"))
        
        # Test available seats
        self.assertFalse(self.booker.is_seat_booked("A3"))
        self.assertFalse(self.booker.is_seat_booked("B1"))

    def test_select_seats_from_center(self):
        """Test center-based seat selection algorithm."""
        # Test with empty theater
        seats = self.booker.select_seats_from_center(3, "A")
        self.assertEqual(len(seats), 3)
        
        # Verify seats are in the same row and centered
        row_letters = [seat[0] for seat in seats]
        seat_numbers = [int(seat[1:]) for seat in seats]
        
        self.assertEqual(len(set(row_letters)), 1)  # All seats should be in same row
        middle_seat = sum(seat_numbers) / len(seat_numbers)
        self.assertAlmostEqual(middle_seat, 5.5, delta=2)  # Should be near center

    def test_determine_seats_from_user_selection(self):
        """Test user-selected seat allocation algorithm."""
        # Test selection starting from A1
        seats = self.booker.determine_seats_from_user_selection(3, "A1")
        self.assertEqual(len(seats), 3)
        self.assertIn("A1", seats)
        self.assertIn("A2", seats)
        self.assertIn("A3", seats)
        
        # Test with some seats already booked
        booking = Booking("GIC0001", ["A1", "A2"])
        self.screening.booking_data.append(booking)
        seats = self.booker.determine_seats_from_user_selection(3, "A3")
        self.assertEqual(len(seats), 3)
        self.assertNotIn("A1", seats)
        self.assertNotIn("A2", seats)

if __name__ == '__main__':
    unittest.main()
    
# python3 -m unittest tests/controllers/test_booking_controller.py
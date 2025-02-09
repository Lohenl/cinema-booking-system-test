# tests/test_booking_menu.py
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError
from cinema_booking_system.models.movie import Movie
from cinema_booking_system.models.screening import Screening
from cinema_booking_system.models.seating_config import SeatingConfig
from cinema_booking_system.models.booking import Booking
from cinema_booking_system.booking_menu import BookingMenu, BookingMenuValidator

class TestBookingMenuValidator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.seating_config = SeatingConfig(5, 10)  # 5 rows (A-E), 10 seats per row
        self.booking_data = [
            Booking("GIC0001", ["A1", "A2"]),  # Pre-booked seats
        ]
        self.validator = BookingMenuValidator(self.seating_config, self.booking_data)

    def test_valid_inputs(self):
        """Test valid seat selections."""
        valid_inputs = [
            "A3",  # Valid seat in first row
            "E10", # Valid seat in last row
            "C5",  # Valid middle seat
            "confirm",
            "cancel",
            "CONFIRM",
            "CANCEL"
        ]
        
        for input_text in valid_inputs:
            with self.subTest(input_text=input_text):
                document = Document(input_text)
                try:
                    self.validator.validate(document)
                except ValidationError as e:
                    self.fail(f"Validation failed for valid input: {input_text}. Error: {str(e)}")

    def test_invalid_inputs(self):
        """Test invalid seat selections."""
        invalid_inputs = [
            "",             # Empty input
            "X1",          # Invalid row
            "A11",         # Seat number too high
            "A0",          # Invalid seat number
            "11",          # No row letter
            "AA1",         # Invalid format
            "A1B",         # Invalid format
            "A1 B2",       # Invalid format
            "A1,B2",       # Invalid format
            "confirm ",    # Extra space
            "A1 ",        # Extra space
        ]
        
        for input_text in invalid_inputs:
            with self.subTest(input_text=input_text):
                document = Document(input_text)
                with self.assertRaises(ValidationError):
                    self.validator.validate(document)

    def test_already_booked_seats(self):
        """Test validation of already booked seats."""
        document = Document("A1")  # This seat is in self.booking_data
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(document)
        self.assertIn("already booked", str(context.exception))

class TestBookingMenu(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.movie = Movie("Test Movie", 120)
        self.seating_config = SeatingConfig(5, 10)
        self.screening = Screening(
            self.movie,
            datetime(2024, 1, 1, 12, 0),
            self.seating_config,
            []
        )
        self.menu = BookingMenu(self.screening)

    def test_initialization(self):
        """Test proper initialization of BookingMenu."""
        self.assertEqual(self.menu.screening, self.screening)
        self.assertEqual(self.menu.total_seats, 50)  # 5 rows * 10 seats
        self.assertEqual(self.menu.seats_available, 50)
        self.assertIsNotNone(self.menu.completer)
        self.assertIsNotNone(self.menu.validator)
        self.assertIsNotNone(self.menu.seating_display)

    def test_is_seat_booked(self):
        """Test seat booking status check."""
        # Add a booking
        booking = Booking("GIC0001", ["A1", "A2"])
        self.screening.booking_data.append(booking)
        
        # Test booked seats
        self.assertTrue(self.menu.is_seat_booked("A1"))
        self.assertTrue(self.menu.is_seat_booked("A2"))
        
        # Test available seats
        self.assertFalse(self.menu.is_seat_booked("A3"))
        self.assertFalse(self.menu.is_seat_booked("B1"))

    def test_select_seats_from_center(self):
        """Test center-based seat selection algorithm."""
        # Test with empty theater
        seats = self.menu.select_seats_from_center(3, "A")
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
        seats = self.menu.determine_seats_from_user_selection(3, "A1")
        self.assertEqual(len(seats), 3)
        self.assertIn("A1", seats)
        self.assertIn("A2", seats)
        self.assertIn("A3", seats)
        
        # Test with some seats already booked
        booking = Booking("GIC0001", ["A1", "A2"])
        self.screening.booking_data.append(booking)
        seats = self.menu.determine_seats_from_user_selection(3, "A3")
        self.assertEqual(len(seats), 3)
        self.assertNotIn("A1", seats)
        self.assertNotIn("A2", seats)

    @patch('cinema_booking_system.booking_menu.prompt')
    def test_display_menu(self, mock_prompt):
        """Test menu display and input handling."""
        mock_prompt.return_value = "1"
        result = self.menu.display_menu()
        self.assertEqual(result, "1")
        mock_prompt.assert_called_once()

    @patch('cinema_booking_system.booking_menu.prompt')
    def test_prompt_seat_count(self, mock_prompt):
        """Test seat count prompt."""
        mock_prompt.return_value = "2"
        result = self.menu.prompt_seat_count()
        self.assertEqual(result, "2")
        mock_prompt.assert_called_once()

if __name__ == '__main__':
    unittest.main()
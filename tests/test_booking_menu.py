import unittest
from unittest.mock import patch
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
            "",            # Empty input
            "X1",          # Invalid row
            "A11",         # Seat number too high
            "A0",          # Invalid seat number
            "11",          # No row letter
            "AA1",         # Invalid format
            "A1B",         # Invalid format
            "A1 B2",       # Invalid format
            "A1,B2",       # Invalid format
            "confirm ",    # Extra space
            "A1 ",         # Extra space
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
        self.movie = Movie("TestMovie")
        self.seating_config = SeatingConfig(5, 10)
        self.screening = Screening(
            datetime(2024, 1, 1, 12, 0),
            self.seating_config,
            self.movie,
            []
        )
        self.menu = BookingMenu(self.screening)

    def test_initialization(self):
        """Test proper initialization of BookingMenu."""
        self.assertEqual(self.menu.screening, self.screening)
        self.assertIsNotNone(self.menu.completer)
        self.assertIsNotNone(self.menu.validator)
        self.assertIsNotNone(self.menu.seating_display)
        self.assertIsNotNone(self.menu.booker)

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
    
# python3 -m unittest tests/test_booking_menu.py
import unittest
from unittest.mock import patch
from io import StringIO
from cinema_booking_system.models.seating_config import SeatingConfig
from cinema_booking_system.models.booking import Booking
from cinema_booking_system.seating_display import SeatingDisplay

class TestSeatingDisplay(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.seating_config = SeatingConfig(3, 4)  # 3 rows (A-C), 4 seats per row
        self.booking_data = []
        self.display = SeatingDisplay(self.seating_config, self.booking_data)

    def test_initialization(self):
        """Object Creation: SeatingDisplay"""
        self.assertEqual(self.display.seating_config, self.seating_config)
        self.assertEqual(self.display.booking_data, self.booking_data)

    def test_property_setters(self):
        """Property Setting: SeatingDisplay"""
        new_config = SeatingConfig(4, 5)
        new_bookings = [Booking("GIC0001", ["A1"])]
        
        self.display.seat_config = new_config
        self.display.booking_data = new_bookings
        
        self.assertEqual(self.display.seat_config, new_config)
        self.assertEqual(self.display.booking_data, new_bookings)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_empty_cinema(self, mock_stdout):
        """Display Test: Test displaying an empty cinema with no selected or booked seats."""
        self.display.display()
        output = mock_stdout.getvalue()
        
        # Verify basic structure
        self.assertIn("SCREEN", output)
        self.assertIn("A", output)
        self.assertIn("B", output)
        self.assertIn("C", output)
        self.assertIn("1", output)
        self.assertIn("2", output)
        self.assertIn("3", output)
        self.assertIn("4", output)
        
        # Verify all seats are marked as available
        available_count = output.count(".")
        self.assertEqual(available_count, 12+1)  # 3 rows * 4 seats, add 1 more from legend

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_with_selected_seats(self, mock_stdout):
        """Display Test: Test displaying theater with selected seats."""
        selected_seats = ["A1", "B2"]
        self.display.display(selected_seats)
        output = mock_stdout.getvalue()
        
        # Verify selected seats are marked
        selected_count = output.count("o")
        self.assertEqual(selected_count, 2+1) # include 1 more from the legend

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_with_booked_seats(self, mock_stdout):
        """Display Test: Test displaying theater with booked seats."""
        booking = Booking("GIC0001", ["A1", "A2"])
        self.display.booking_data = [booking]
        self.display.display()
        output = mock_stdout.getvalue()
        
        # Verify booked seats are marked
        booked_count = output.count("x")
        self.assertEqual(booked_count, 2+1) # include 1 more from the legend

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_with_mixed_seats(self, mock_stdout):
        """Display Test: Test displaying theater with both selected and booked seats."""
        booking = Booking("GIC0001", ["A1"])
        self.display.booking_data = [booking]
        selected_seats = ["B1"]
        self.display.display(selected_seats)
        output = mock_stdout.getvalue()
        
        # Verify correct counts of each seat type
        booked_count = output.count("x")
        selected_count = output.count("o")
        available_count = output.count(".")
        
        self.assertEqual(booked_count, 1+1) # include 1 more from the legend
        self.assertEqual(selected_count, 1+1) # include 1 more from the legend
        self.assertEqual(available_count, 10+1) # include 1 more from the legend

    def test_legend_display(self):
        """Display Test: Test that the legend is displayed correctly."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.display.display()
            output = mock_stdout.getvalue()
            
            self.assertIn("o - Selected seat", output)
            self.assertIn(". - Available seat", output)
            self.assertIn("x - Unavailable seat", output)

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch
from prompt_toolkit.document import Document
from prompt_toolkit.validation import ValidationError
from cinema_booking_system.config_menu import ConfigMenu, ConfigMenuValidator

class TestConfigMenuValidator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.validator = ConfigMenuValidator()

    def test_valid_input(self):
        """Test valid input formats."""
        valid_inputs = [
            "Movie1 10 20",
            # "The Movie 5 30", # In practice: TDD has raised an issue where the format used in the brief doesn't specify if spaces are allowed; to seek clarification
            "Avatar 26 50",
            "exit",
            "EXIT",
            "Exit"
        ]
        
        for input_text in valid_inputs:
            with self.subTest(input_text=input_text):
                document = Document(input_text)
                try:
                    self.validator.validate(document)
                except ValidationError as e:
                    self.fail(f"Validation failed for valid input: {input_text}. Error: {str(e)}")

    def test_invalid_input(self):
        """Test various invalid input formats."""
        invalid_inputs = [
            # Empty input
            "",
            # Wrong number of parts
            "Movie",
            "Movie 10",
            "Movie 10 20 30",
            # Non-numeric values
            "Movie abc 20",
            "Movie 10 def",
            # Zero or negative values
            "Movie 0 20",
            "Movie -1 20",
            "Movie 10 0",
            "Movie 10 -5",
            # Exceeding maximum values
            f"Movie {ConfigMenuValidator.MAX_ROWS + 1} 20",
            f"Movie 10 {ConfigMenuValidator.MAX_SEATS_PER_ROW + 1}"
        ]
        
        for input_text in invalid_inputs:
            with self.subTest(input_text=input_text):
                document = Document(input_text)
                with self.assertRaises(ValidationError):
                    self.validator.validate(document)

    def test_error_messages(self):
        """Test specific error messages for different validation failures."""
        test_cases = [
            ("", "Input cannot be empty"),
            ("Movie", "Invalid format"),
            ("Movie 0 20", "Row count must be a positive integer."),
            ("Movie 10 0", "Seats per row must be a positive integer."),
            (f"Movie {ConfigMenuValidator.MAX_ROWS + 1} 20", "Row count cannot exceed"),
            (f"Movie 10 {ConfigMenuValidator.MAX_SEATS_PER_ROW + 1}", "Seats per row cannot exceed")
        ]
        
        for input_text, expected_message in test_cases:
            with self.subTest(input_text=input_text):
                document = Document(input_text)
                with self.assertRaises(ValidationError) as context:
                    self.validator.validate(document)
                self.assertIn(expected_message, str(context.exception))

class TestConfigMenu(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.config_menu = ConfigMenu()

    def test_initialization(self):
        """Test proper initialization of ConfigMenu."""
        self.assertIsNotNone(self.config_menu.completer)
        self.assertIsNotNone(self.config_menu.validator)
        self.assertEqual(self.config_menu.options, ["WarCraft 10 10", "RuneScape 11 11"])

    @patch('cinema_booking_system.config_menu.prompt')
    def test_prompt_config(self, mock_prompt):
        """Test the prompt_config method."""
        # Test normal input
        mock_prompt.return_value = "Movie1 10 20"
        result = self.config_menu.prompt_config()
        self.assertEqual(result, "Movie1 10 20")
        
        # Verify prompt was called with correct arguments
        mock_prompt.assert_called_with(
            "Please define movie title and seating map in [Title] [Row] [Seats Per Row] format.\n(Tip: Press tab for autocomplete)\n",
            completer=self.config_menu.completer,
            validator=self.config_menu.validator
        )

    @patch('cinema_booking_system.config_menu.prompt')
    def test_run_with_exit(self, mock_prompt):
        """Test the run method with exit command."""
        mock_prompt.return_value = "exit"
        with patch('builtins.print') as mock_print:
            self.config_menu.run()
            mock_print.assert_called_with("Exiting Configuration Menu\n")

    @patch('cinema_booking_system.config_menu.prompt')
    def test_run_with_valid_config(self, mock_prompt):
        """Test the run method with valid configuration."""
        test_input = "Movie1 10 20"
        mock_prompt.return_value = test_input
        with patch('builtins.print') as mock_print:
            self.config_menu.run()
            mock_print.assert_called_with(f"Configured: {test_input}")

if __name__ == '__main__':
    unittest.main()
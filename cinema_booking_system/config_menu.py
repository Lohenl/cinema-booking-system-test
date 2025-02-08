from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError

class ConfigMenuValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(
                message="Input cannot be empty. Please enter in [Title] [Row] [Seats Per Row] format.",
                cursor_position=len(text)  # Move cursor to the end
            )
        
        parts = text.split() 
        if text and parts[0].lower() != 'exit' and (len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit()):
            raise ValidationError(
                message="Invalid format. Please enter in [Title] [Row] [Seats Per Row] format.\n",
                cursor_position=len(text)  # Move cursor to the end
            )

class ConfigMenu:
    def __init__(self):
        self.options = ["Exit"]
        self.completer = WordCompleter(self.options, ignore_case=True)
        self.validator = ConfigMenuValidator()

    def display_menu(self):
        user_input = prompt(
            "Please define movie title and seating map in [Title] [Row] [Seats Per Row] format.\n",
            completer = self.completer,
            validator = self.validator
        )
        return user_input
    
    def run(self):
        while True:
            user_input = self.display_menu()
            print(f"User input: {user_input}")
            if user_input.lower() == "exit":
                print("Exiting Configuration Menu\n")
                break
            else:
                print(f"Configured: {user_input}")
                break
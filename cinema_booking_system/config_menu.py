from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError

class ConfigMenuValidator(Validator):
    MAX_ROWS = 26
    MAX_SEATS_PER_ROW = 50
    
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(
                message="Input cannot be empty. Please enter in [Title] [Row] [Seats Per Row] format.",
                cursor_position=len(text)  # Move cursor to the end
            )
        
        parts = text.split()
        if parts[0].lower() != 'exit':
            if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
                raise ValidationError(
                    message="Invalid format. Please enter in [Title] [Row] [Seats Per Row] format.",
                    cursor_position=len(text)  # Move cursor to the end
                )
            row_count = int(parts[1])
            seats_per_row = int(parts[2])
            if row_count <= 0:
                raise ValidationError(
                    message="Row count must be a positive integer.",
                    cursor_position=len(text)  # Move cursor to the end
                )
            if seats_per_row <= 0:
                raise ValidationError(
                    message="Seats per row must be a positive integer.",
                    cursor_position=len(text)  # Move cursor to the end
                )
            if row_count > self.MAX_ROWS:
                raise ValidationError(
                    message=f"Row count cannot exceed {self.MAX_ROWS}.",
                    cursor_position=len(text)  # Move cursor to the end
                )
            if seats_per_row > self.MAX_SEATS_PER_ROW:
                raise ValidationError(
                    message=f"Seats per row cannot exceed {self.MAX_SEATS_PER_ROW}.",
                    cursor_position=len(text)  # Move cursor to the end
                )

class ConfigMenu:
    def __init__(self):
        self.options = ["Exit"]
        self.completer = WordCompleter(self.options, ignore_case=True)
        self.validator = ConfigMenuValidator()

    def prompt_config(self):
        user_input = prompt(
            "Please define movie title and seating map in [Title] [Row] [Seats Per Row] format.\n",
            completer = self.completer,
            validator = self.validator
        )
        return user_input
    
    def run(self):
        while True:
            user_input = self.prompt_config()
            print(f"User input: {user_input}")
            if user_input.lower() == "exit":
                print("Exiting Configuration Menu\n")
                break
            else:
                print(f"Configured: {user_input}")
                break

# Example usage
if __name__ == "__main__":
    config_menu = ConfigMenu()
    config_menu.run()
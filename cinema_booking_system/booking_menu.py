from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from cinema_booking_system.movie import Movie
from cinema_booking_system.screening import Screening

class BookingMenu:
    def __init__(self, screening: Screening):
        self.screening = screening
        self.options = ["1", "2", "3"]
        self.completer = WordCompleter(self.options, ignore_case=True)
        self.total_seats = screening.seat_config.row_count * screening.seat_config.seat_count_per_row
        
        self.seats_available = self.total_seats
        # self.seats_available = self.total_seats - len(screening.booking_data)
        
    def display_menu(self):
        user_input = prompt(
            "\n"
            "Welcome to GIC Cinemas\n"
            f"[1] Book Tickets for '{self.screening.movie.title}' ({self.seats_available} seats available)\n"
            "[2] Check Bookings\n"
            "[3] Exit\n"
            "\n"
            "Please enter your selection (Press Tab to view available options):\n"
            "\n",
            completer=self.completer
        )
        return user_input

    def run(self):
        while True:
            choice = self.display_menu()
            match choice:
                case "1":
                    print(f"\nBooking it is")
                case "2":
                    print("\nChecking it is")
                case "3":
                    print("\nThank you for using GIC Cinemas System. Bye!")
                    break
                case _:
                    print("\nInvalid choice, please try again.")
                    
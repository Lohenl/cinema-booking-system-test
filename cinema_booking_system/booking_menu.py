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
    
    def prompt_seats(self):
        user_input = prompt(
            f"\nPlease enter the number of seats you would like to book (1-{self.seats_available}):\n"
        )
        return user_input

    def run(self):
        while True:
            choice = self.display_menu()
            match choice:
                case "1":
                    input_seats = self.prompt_seats()
                    if input_seats.isdigit() and 1 <= int(input_seats) <= self.seats_available:
                        print(f"\nBooking {input_seats} seats for {self.screening.movie.title}...")
                        self.seats_available -= int(input_seats) # eh lets upgrade this later
                        print(f"\nSuccessfully reserved {input_seats} seats for {self.screening.movie.title} at {self.screening.start_time}.")
                    else:
                        print(f"\nSorry, there are only {self.seats_available} seats available. Please try again.")
                case "2":
                    print("\nChecking it is")
                case "3":
                    print("\nThank you for using GIC Cinemas System. Bye!")
                    break
                case _:
                    print("\nInvalid choice, please try again.")
                    
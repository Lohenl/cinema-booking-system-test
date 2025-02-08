import re
from typing import List
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from cinema_booking_system.movie import Movie
from cinema_booking_system.screening import Screening
from cinema_booking_system.seating_display import SeatingDisplay
from cinema_booking_system.booking import Booking
from cinema_booking_system.seating_config import SeatingConfig

class BookingMenuValidator(Validator):
    
    def __init__(self, seating_config: SeatingConfig, booking_data: list):
        self.seating_config = seating_config
        self.booking_data = booking_data
    
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(
                message="Input cannot be empty. \nPlease select a seating position (e.g. A1, B2, C3), or enter 'confirm' to accept seat selection",
                cursor_position=len(text)  # Move cursor to the end
            )
        
        if text.lower() != 'confirm':
            if not re.match(r'^[A-Za-z]\d+$', text):
                raise ValidationError(
                    message="Invalid format. Please select a seating position (e.g. A1, B2, C3).",
                    cursor_position=len(text)  # Move cursor to the end
                )
            
            row_letter = text[0].upper()
            seat_number = int(text[1:])
            
            # Validate row letter
            if ord(row_letter) - ord('A') >= self.seating_config.row_count:
                raise ValidationError(
                    message=f"Invalid row. Please select a row between A and {chr(ord('A') + self.seating_config.row_count - 1)}.",
                    cursor_position=len(text)  # Move cursor to the end
                )
            
            # Validate seat number
            if seat_number < 1 or seat_number > self.seating_config.seat_count_per_row:
                raise ValidationError(
                    message=f"Invalid seat number. Please select a seat number between 1 and {self.seating_config.seat_count_per_row}.",
                    cursor_position=len(text)  # Move cursor to the end
                )
            
            # Check if the seat is already booked
            for booking in self.booking_data:
                if text in booking.seats:
                    raise ValidationError(
                        message="Seat is already booked. Please select another seat.",
                        cursor_position=len(text)  # Move cursor to the end
                    )

class BookingMenu:
    def __init__(self, screening: Screening):
        self.screening = screening
        self.options = ["1", "2", "3"]
        self.completer = WordCompleter(self.options, ignore_case=True)
        self.validator = BookingMenuValidator(screening.seat_config, screening.booking_data)
        self.seating_display = SeatingDisplay(screening.seat_config, screening.booking_data)
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
    
    def prompt_seat_count(self):
        user_input = prompt(
            f"\nPlease enter the number of seats you would like to book (1-{self.seats_available}), or enter blank to go back to the main menu:\n"
        )
        return user_input
    
    def prompt_seat_position(self):
        user_input = prompt(
            f"\nEnter 'confirm' to accept seat selection, or select a seating position (e.g. A1, B2, C3)\nSeat: ",
            validator = self.validator
        )
        return user_input

    def run(self):
        while True:
            menu_choice = self.display_menu()
            match menu_choice:
                case "1":
                    # Prompt user for number of seats
                    input_seats = self.prompt_seat_count()
                    if input_seats.isdigit() and 1 <= int(input_seats) <= self.seats_available:
                        
                        # Reserve number of seats
                        seat_count = int(input_seats)
                        print(f"\nBooking {seat_count} seats for {self.screening.movie.title}...")
                        # TODO: Build client integration with backend for seat reservation here
                        
                        # Create a booking object and generate an id
                        new_id = "GIC" + str(len(self.screening.booking_data) + 1).zfill(4) # should be date + uuid in practice
                        booking = Booking(new_id, [])
                        
                        self.seats_available -= int(input_seats) # TODO: eh lets upgrade this later
                        print(f"\nSuccessfully reserved {input_seats} seats for {self.screening.movie.title} at {self.screening.start_time}.\nBooking ID: {new_id} \n")
                        
                        # Prompt user to select seats
                        while True:
                            # Determine the default seat selection - rear and center
                            selected_seats: List[str] = []
                            for i in range(int(input_seats)):
                                row = chr(ord('A') + i // self.screening.seat_config.seat_count_per_row)
                                seat = (i % self.screening.seat_config.seat_count_per_row) + 1
                                selected_seats.append(f"{row}{seat}")
                            
                            # Display seating
                            print(f"Selected Seats: {selected_seats}\n")
                            self.seating_display.display()
                            seat = self.prompt_seat_position()
                            if seat.lower() == "confirm":
                                break
                            # booking.seats.append(seat)
                        
                        # Add booking to screening when booking is successful
                        # self.screening.booking_data.append(booking)
                        # TODO: Construct and perform database transactions here
                        
                    else:
                        print(f"\nSorry, there are only {self.seats_available} seats available. Please try again.")
                case "2":
                    print("\nChecking it is")
                case "3":
                    print("\nThank you for using GIC Cinemas System. Bye!")
                    break
                case _:
                    print("\nInvalid choice, please try again.")
                    
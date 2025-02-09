import re
import time
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from cinema_booking_system.models.screening import Screening
from cinema_booking_system.models.seating_config import SeatingConfig
from cinema_booking_system.controllers.booking_controller import BookingController
from cinema_booking_system.seating_display import SeatingDisplay

class BookingMenuValidator(Validator):
    
    def __init__(self, seating_config: SeatingConfig, booking_data: list):
        self.seating_config = seating_config
        self.booking_data = booking_data
    
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(
                message="Input cannot be empty. \nPlease select a seating position (e.g. A1, B2, C3), or enter 'confirm' to accept seat selection, or blank to cancel booking.",
                cursor_position=len(text)  # Move cursor to the end
            )
        
        if text.lower() != 'confirm' and text.lower() != 'cancel':
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
        self.menu_options = ["1", "2", "3"]
        self.booking_select_options = ["Confirm", "Cancel"]
        self.booking_check_options = ["GIC0001"]
        self.menu_completer = WordCompleter(self.menu_options, ignore_case=True)
        self.booking_select_completer = WordCompleter(self.booking_select_options, ignore_case=True)
        self.booking_check_completer = WordCompleter(self.booking_check_options, ignore_case=True)
        self.validator = BookingMenuValidator(screening.seat_config, screening.booking_data)
        self.seating_display = SeatingDisplay(screening.seat_config, screening.booking_data)
        self.booker = BookingController(screening)
        
    def display_menu(self):
        user_input = prompt(
            "\n"
            "Welcome to GIC Cinemas\n"
            f"[1] Book Tickets for '{self.screening.movie.title}' ({self.booker.seats_available} seats available)\n"
            "[2] Check Bookings\n"
            "[3] Exit\n"
            "\n"
            "Please enter your selection (Press Tab to view available options): ",
            completer=self.menu_completer
        )
        return user_input
    
    def prompt_seat_count(self):
        user_input = prompt(
            f"\nPlease enter the number of seats you would like to book (1-{self.booker.seats_available}), or enter blank to go back to the main menu:\n"
        )
        return user_input
    
    def prompt_seat_position(self):
        user_input = prompt(
            f"\nEnter 'confirm' to accept seat selection, or select a seating position (e.g. A1, B2, C3), or enter 'cancel' to cancel booking:\n"
            "(Hint: Press tab to show options)\n"
            "Seat: ",
            completer = self.booking_select_completer,
            validator = self.validator
        )
        return user_input

    def prompt_booking_id(self):
        booking_id = prompt(
            "Enter booking ID to check booking details, or enter blank to go back to the main menu.\n"
            "Hint: Press tab for an example ID\n"
            "Booking ID: ",
            completer = self.booking_check_completer,
        )
        return booking_id

    def run(self):
        while True:
            menu_choice = self.display_menu()
            match menu_choice:
                case "1":
                    
                    if self.booker.seats_available == 0:
                        print(f"Sorry, this screening has been fully booked.")
                        time.sleep(2) # block the thread to make sure the user reads the message
                    
                    else:
                        # Prompt user for number of seats
                        input_seats = self.prompt_seat_count()
                        if input_seats.isdigit() and 1 <= int(input_seats) <= self.booker.seats_available:
                            
                            # Reserve number of seats
                            seat_count = int(input_seats)
                            print(f"\nBooking {seat_count} seats for {self.screening.movie.title}...")
                            
                            # Create a booking object and generate an id
                            booking = self.booker.new_booking()
                            
                            self.booker.seats_available -= int(input_seats)
                            print(f"\nSuccessfully reserved {input_seats} seats for {self.screening.movie.title} at {self.screening.start_time}.\nBooking ID: {booking.id} \n")
                            
                            # Prompt user to select seats
                            selected_seats = None
                            seat_input = None
                            while True:
                                
                                if selected_seats is None:
                                    # Determine the default seat selection - rear and center
                                    selected_seats = self.booker.select_seats_from_center(seat_count, None)
                                else:
                                    # Determine the seat selection based on user input
                                    selected_seats = self.booker.determine_seats_from_user_selection(seat_count, seat_input)
                                
                                # Preview seating selection
                                print(f"Selected Seats: {selected_seats}\n")
                                self.seating_display.display(selected_seats)
                                
                                # Prompt user to select a custom seat, confirm, or cancel
                                seat_input = self.prompt_seat_position()
                                if seat_input.lower() == "confirm":
                                    # Update models and commit transactions
                                    booking.seats = selected_seats
                                    self.screening.booking_data.append(booking)
                                    self.booker.save_booking(booking)
                                    print(f"\nBooking confirmed! Booking ID: {booking.id} Seats: {selected_seats}\n")
                                    time.sleep(2) # block the thread to make sure the user reads the message
                                    break
                                elif seat_input.lower() == "cancel":
                                    self.booker.seats_available += seat_count
                                    print("\nCancelling booking...")
                                    break
                                
                        elif input_seats.isdigit() and int(input_seats) > self.booker.seats_available:
                            print(f"Sorry, there are only {self.booker.seats_available} seats available. Please try again.")
                            time.sleep(2) # block the thread to make sure the user reads the message
                        
                case "2":
                    
                    while True:
                        booking_id = self.prompt_booking_id()
                        
                        if booking_id:
                            booking = next((booking for booking in self.screening.booking_data if booking.id == booking_id), None)
                            if booking:
                                print(f"\nBooking ID: {booking.id}")
                                print(f"Seats: {booking.seats}")
                                self.seating_display.display(booking.seats)
                            else:
                                print("\nBooking not found.")
                        else:
                            break
                
                case "3":
                    print("\nThank you for using GIC Cinemas System. Bye!")
                    break
                
                case _:
                    print("\nInvalid choice, please try again.")
                    
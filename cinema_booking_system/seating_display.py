from typing import List
from cinema_booking_system.models.seating_config import SeatingConfig
from cinema_booking_system.models.booking import Booking

SELECTED_SYMBOL = "o"
AVAILABLE_SYMBOL = "."
UNAVAILABLE_SYMBOL = "x"

class SeatingDisplay:
    def __init__(self, seating_config: SeatingConfig, booking_data: List[Booking]):
        self.seating_config = seating_config
        self.booking_data = booking_data

    @property
    def seat_config(self) -> SeatingConfig:
        return self._seat_config
    
    @seat_config.setter
    def seat_config(self, value):
        self._seat_config = value
    
    @property
    def booking_data(self) -> List[Booking]:
        return self._booking_data
    
    @booking_data.setter
    def booking_data(self, value):
        self._booking_data = value
    
    def display(self, selected_seats: List[str] = []):
        # Calculate the total length of the horizontal rule
        hr_length = self.seating_config.seat_count_per_row * 3 + 1
        
        # Calculate the length of the "SCREEN" text
        screen_text = "SCREEN"
        screen_length = len(screen_text)
        
        # Calculate the number of spaces needed on each side of the "SCREEN" text
        whitespace_each_side = (hr_length - screen_length) // 2
        screen_whitespace = " " * whitespace_each_side
        
        # Print the screen
        print(f"{screen_whitespace}{screen_text}{screen_whitespace}")
        
        # Print the horizontal rule
        hr_string = "-" * hr_length
        print(hr_string)
        
        # Print the row letters and seats
        for i in range(self.seating_config.row_count):
            row_letter = chr(65 + (self.seating_config.row_count - 1 - i))  # Reverse the row letters
            row = f"{row_letter} "
            for j in range(self.seating_config.seat_count_per_row):
                seat = f"{chr(65+(self.seating_config.row_count - 1 - i))}{j+1}"
                if seat in selected_seats:
                    row += f" {SELECTED_SYMBOL} "
                elif any(seat in booking.seats for booking in self.booking_data):
                    row += f" {UNAVAILABLE_SYMBOL} "
                else:
                    row += f" {AVAILABLE_SYMBOL} "
            print(row)
        
        # Print the last row
        last_row = " "
        for i in range(self.seating_config.seat_count_per_row):
            if i < 9:
                last_row += f"  {i+1}"
            else:
                last_row += f" {i+1}"
        print(last_row)
        
        # Print the legend
        print(f"\n{SELECTED_SYMBOL} - Selected seat | {AVAILABLE_SYMBOL} - Available seat | {UNAVAILABLE_SYMBOL} - Unavailable seat\n")

# Example usage:
if __name__ == "__main__":
    seating_display = SeatingDisplay(SeatingConfig(26, 20), [])
    seating_display.display(["A1", "B2", "C3"])
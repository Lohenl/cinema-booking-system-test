import re
from typing import List
from cinema_booking_system.models.screening import Screening
from cinema_booking_system.models.booking import Booking

class BookingController:
    
    def __init__(self, screening: Screening):
        self.screening = screening
        self.total_seats = screening.seat_config.row_count * screening.seat_config.seat_count_per_row
        self.seats_available = self.total_seats - len(screening.booking_data) # fix me
        
    @property
    def seats_available(self) -> List[Booking]:
        return self._seats_available
    
    @seats_available.setter
    def seats_available(self, value):
        self._seats_available = value
    
    def is_seat_booked(self, seat: str) -> bool:
        # for booking in self.screening.booking_data:
            # print(f'Seats already booked for: booking.id: {booking.id}, booking.seats: {booking.seats}')
        return any(seat in booking.seats for booking in self.screening.booking_data)

    # The basic default algo, fills from the back and left to right, doesn't hit the brief
    def determine_seats_basic(self, seat_count: int) -> List[str]:
        seats_per_row = self.screening.seat_config.seat_count_per_row
        selected_seats: List[str] = []
        reserved_seat_offset = 0 # tallies number of seats to skip when a seat was already booked by someone else
        
        # Loop until we find the number of seats required
        for i in range(seat_count):
            while True:
            
                seat_number = i + reserved_seat_offset
                # Determine row (last row of a 0-based index, moving down by number of rows based on number of seats per row)
                row_index = (seat_number // seats_per_row)
                seat_row = chr(ord('A') + row_index)
                
                # Determine seat number (left-most starting from 1-based index)
                seat = (seat_number % seats_per_row) + 1
                
                # Check if seat is available
                seat_str = f"{seat_row}{seat}"
                if not self.is_seat_booked(seat_str):
                    print(f"Seat {seat_str} is available.")
                    selected_seats.append(seat_str)
                    print(f"reserved_seat_offset: {reserved_seat_offset}")
                    break
                else:
                    # Update reserved seat tally and move to the next seat
                    print(f"Seat {seat_str} is already booked. Trying next seat...")
                    reserved_seat_offset += 1
                    print(f"reserved_seat_offset: {reserved_seat_offset}")
                       
        return selected_seats

    # The basic user-specified algo, fills from the back and left to right, doesn't hit the brief
    def determine_seats_from_position_basic(self, seat_count: int, user_input: str) -> List[str]:
        seats_per_row = self.screening.seat_config.seat_count_per_row
        selected_seats: List[str] = []
        reserved_seat_offset = 0                # tallies number of seats to skip when a seat was already booked by someone else
        
        # Use regular expression to split the user input into row and seat number
        match = re.match(r"([A-Za-z]+)(\d+)", user_input)
        row_input = match.group(1).upper()
        seat_input = int(match.group(2))
        row_offset = ord(row_input) - ord('A')  # offset to determine the row based on user input
        seat_offset = seat_input - 1            # offset to determine the seat based on user input
        
        # print(f"ord('A'): {ord('A')}, ord(row_input): {ord(row_input)}, row_offset: {row_offset}")
        
        # Loop until we find the number of seats required
        for i in range(seat_count):
            while True:
            
                seat_number = i + seat_offset + reserved_seat_offset
                # Determine row (last row of a 0-based index, moving down by number of rows based on number of seats per row)
                row_index = (seat_number // seats_per_row)
                seat_row = chr(ord('A') + row_offset + row_index)

                # Determine seat number (left-most starting from 1-based index)
                seat = (seat_number % seats_per_row) + 1
                
                # Check if seat is available
                seat_str = f"{seat_row}{seat}"
                if not self.is_seat_booked(seat_str):
                    print(f"Seat {seat_str} is available.")
                    selected_seats.append(seat_str)
                    print(f"reserved_seat_offset: {reserved_seat_offset}")
                    break
                else:
                    # Update reserved seat tally and move to the next seat
                    print(f"Seat {seat_str} is already booked. Trying next seat...")
                    reserved_seat_offset += 1
                    print(f"reserved_seat_offset: {reserved_seat_offset}")
            
        return selected_seats
    
    # The better default algo that hits the brief:
    #   - TODO: Fix the bug where the seat selection algorithm doesn't fill up all the seats
    def select_seats_from_center(self, seat_count: int, starting_row: str) -> List[str]:
        seats_per_row = self.screening.seat_config.seat_count_per_row
        selected_seats: List[str] = []
        reserved_seat_offset = 0 # tallies number of seats to skip when a seat was already booked by someone else
        
        # Calculate the center column
        center_column = seats_per_row // 2

        # Loop until we find the number of seats required
        for i in range(seat_count):
            while True:

                seat_number = i + reserved_seat_offset
                # Determine row (last row of a 0-based index, moving down by number of rows based on number of seats per row)
                row_offset = ord(starting_row) - ord('A') if starting_row is not None else 0
                row_index = (seat_number // seats_per_row)
                seat_row = chr(ord('A') + row_offset + row_index)
                
                # Determine seat number (starting from the center column and moving outwards)
                # NOTE: this is the harder part
                # more clever way that centers the seats, but misses some seats
                #   - even seats_per_row: All seats 1 unfilled across all rows 
                #   - odd seats_per_row: seats 1 and last unfilled across alternating rows 
                column_offset = (seat_number % seats_per_row) // 2
                seat = center_column + column_offset * (-1 if seat_number % 2 == 0 else 1) + 1
                print(f'seat_number: {seat_number}, row_index: {row_index}, seat_row: {seat_row}, column_offset: {column_offset}, seat: {seat}')
                
                # Check if seat is available
                seat_str = f"{seat_row}{seat}"
                if not self.is_seat_booked(seat_str) and seat_str not in selected_seats:
                    print(f"Seat {seat_str} is available.")
                    selected_seats.append(seat_str)
                    print(f"reserved_seat_offset: {reserved_seat_offset}")
                    break
                else:
                    # Update reserved seat tally and move to the next seat
                    print(f"Seat {seat_str} is already booked or unavailable. Trying next seat...")
                    reserved_seat_offset += 1
                    print(f"reserved_seat_offset: {reserved_seat_offset}")
        return selected_seats

    # The better user-specified algo that hits the brief:
    def determine_seats_from_user_selection(self, seat_count: int, user_input: str) -> List[str]:
        seats_per_row = self.screening.seat_config.seat_count_per_row
        selected_seats: List[str] = []
        
        # Use regular expression to split the user input into row and seat number
        match = re.match(r"([A-Za-z]+)(\d+)", user_input)
        row_input = match.group(1).upper()
        seat_input = int(match.group(2))
        row_offset = ord(row_input) - ord('A')  # offset to determine the row based on user input
        seat_offset = seat_input - 1            # offset to determine the seat based on user input
        first_row_filled = False
        
        # print(f"ord('A'): {ord('A')}, ord(row_input): {ord(row_input)}, row_offset: {row_offset}")
        
        # Only for the first row, fill up empty seats in the same row all the way to the right
        # Loop until we fill up the row towards the right
        for i in range(seat_count):
            
            # Break out of loop if we have filled up the first row
            if first_row_filled == True:
                # print(f"First row filled. Moving to next row...")
                break
            
            while True:
            
                seat_number = i + seat_offset
                # Determine row (last row of a 0-based index, moving down by number of rows based on number of seats per row)
                row_index = (seat_number // seats_per_row)
                seat_row = chr(ord('A') + row_offset + row_index)
                
                # Determine seat number (left-most starting from 1-based index)
                seat = (seat_number % seats_per_row) + 1
                # Prepare to break out of main loop when eaching end of the row  
                if seat == seats_per_row:
                    first_row_filled = True
                
                # Check if seat is available
                seat_str = f"{seat_row}{seat}"
                if not self.is_seat_booked(seat_str):
                    # print(f"Seat {seat_str} is available, adding to selection.")
                    selected_seats.append(seat_str)
                    break
                    
        # For subsequent rows, fill from the center first, then move outwards
        next_row = chr(ord(row_input) + 1)
        # print(f"next_row: {next_row}")
        remaining_selected_seats: List[str] = self.select_seats_from_center(seat_count - len(selected_seats), next_row)
        selected_seats.extend(remaining_selected_seats)
        
        return selected_seats
    
    def new_booking(self) -> Booking:
        new_id = "GIC" + str(len(self.screening.booking_data) + 1).zfill(4) # should be date + uuid in practice
        # TODO: Update backend and/or perform database transactions for seat reservations here
        new_booking = Booking(new_id, [])
        return new_booking
    
    def save_booking(self, booking: Booking) -> None:
        # TODO: Update backend and/or perform database transactions for booking confirmations here
        print(booking)
        return None
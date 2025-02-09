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

    def select_seats_from_center(self, seat_count: int, starting_row: str) -> List[str]:
        seats_per_row = self.screening.seat_config.seat_count_per_row
        selected_seats: List[str] = []
        
        # Calculate the center column
        center_column = seats_per_row // 2
        
        # Initialize row
        # row_offset = ord(starting_row) - ord('A') if starting_row is not None else 0
        starting_row = 'A' if starting_row is None else starting_row
        current_row = starting_row
        seats_needed = seat_count
        
        # print(f"starting_row: {starting_row}, current_row:{current_row}, seats_needed:{seats_needed}")
        
        while seats_needed > 0:
            # For each row, start from center and expand outwards
            left_ptr = center_column
            right_ptr = center_column + 1
            row_seats: List[str] = []
            
            while len(row_seats) < min(seats_per_row, seats_needed):
                
                # print(f"row_seats: {row_seats}")
                
                # Try center-left seat
                if left_ptr >= 0:
                    seat_str = f"{current_row}{left_ptr + 1}"
                    if not self.is_seat_booked(seat_str) and seat_str not in selected_seats:
                        row_seats.append(seat_str)
                    left_ptr -= 1
                    # print(f"left_ptr: {left_ptr}")
                
                # If we still need seats, try center-right seat
                if len(row_seats) < min(seats_per_row, seats_needed) and right_ptr < seats_per_row:
                    seat_str = f"{current_row}{right_ptr + 1}"
                    if not self.is_seat_booked(seat_str) and seat_str not in selected_seats:
                        row_seats.append(seat_str)
                    right_ptr += 1
                    # print(f"right_ptr: {right_ptr}")
                    
                # Skip to the next row if both pointers reached the end (the row is full)
                if (left_ptr < 0) and (right_ptr == seats_per_row):
                    # print(f"Row {current_row} is full, unable to assign more seats")
                    break
            
            # Add the seats found in this row to our selection
            selected_seats.extend(row_seats)
            seats_needed -= len(row_seats)
            
            # Move to next row if we still need more seats
            if seats_needed > 0:
                # print(f"selected_seats: {selected_seats}, seats_needed: {seats_needed}")
                current_row = chr(ord(current_row) + 1)
                
                # Wrap around to the last row again if the front row of the cinema has been reached
                if current_row == chr(ord('A') + self.screening.seat_config.row_count):
                    current_row = 'A'
                #   - TODO: There is an edge case unlikely encountered in production workloads, but is a bug
                #       - SeatConfig: Movie 11 11
                #       - Book 11 seats from position B1
                #       - Book 110 seats from anywhere in the middle of the cinema (e.g. H9)
                #       - Seats get missed as a result (default assignments wrap around nicely)
                #       - NOTE: Doesnt have to be a complete row, any booking needing a wraparound will have this bug
        
        return selected_seats

    def determine_seats_from_user_selection(self, seat_count: int, user_input: str) -> List[str]:
        seats_per_row = self.screening.seat_config.seat_count_per_row
        selected_seats: List[str] = []
        
        # Use regular expression to split the user input into row and seat number
        match = re.match(r"([A-Za-z]+)(\d+)", user_input)
        row_input = match.group(1).upper()
        seat_input = int(match.group(2))
        row_offset = ord(row_input) - ord('A')  # offset to determine the row based on user input
        seat_offset = seat_input - 1            # offset to determine the seat based on user input
        # print(f"ord('A'): {ord('A')}, ord(row_input): {ord(row_input)}, row_offset: {row_offset}")
        
        first_row_filled = False
        # NOTE: (Bug) if the existing row is fully filled, the algo enters an infinite loop
        # Nominally, this can be handled with menu/frontend validation to prevent selecting a booked seat.
        # However, as a big precaution, I'll put this check here until the exact scenario is reproduced, again
        booked_seats_for_given_row: List[str] = []
        for booking in self.screening.booking_data:
            for seat in booking.seats:
                if seat.startswith(user_input):
                    booked_seats_for_given_row.append(seat)
        if len(booked_seats_for_given_row) == seats_per_row:
            first_row_filled = False
        
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
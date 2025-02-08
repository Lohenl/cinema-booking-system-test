class Seating:
    def __init__(self, row_number: int, seat_number: int, is_booked: bool = False, booking_id: str = None):
        self._row_number = row_number
        self._seat_number = seat_number
        self._is_booked = is_booked
        self._booking_id = booking_id

    @property
    def row_number(self) -> int:
        return self._row_number

    @row_number.setter
    def row_number(self, value: int) -> None:
        self._row_number = value

    @property
    def seat_number(self) -> int:
        return self._seat_number

    @seat_number.setter
    def seat_number(self, value: int) -> None:
        self._seat_number = value

    @property
    def is_booked(self) -> bool:
        return self._is_booked

    @is_booked.setter
    def is_booked(self, value: bool) -> None:
        self._is_booked = value

    @property
    def booking_id(self) -> str:
        return self._booking_id

    @booking_id.setter
    def booking_id(self, value: str) -> None:
        self._booking_id = value

    @property
    def row_count(self):
        return self._row_count
    
    @row_count.setter
    def row_count(self, value):
        self._row_count = value
    
    @property
    def seat_count_per_row(self):
        return self._seat_count_per_row
    
    @seat_count_per_row.setter
    def seat_count_per_row(self, value):
        self._seat_count_per_row = value

    def __str__(self) -> str:
        return f"Row: {self.row_number}, Seat: {self.seat_number}, Booked: {self.is_booked}, Booking ID: {self.booking_id}"
# filepath: /c:/Users/winso/cinema-booking-system-test/cinema_booking_system/booking.py
class Booking:
    def __init__(self, user, screening, seats):
        self.user = user
        self.screening = screening
        self.seats = seats

    def __str__(self):
        return f"Booking for {self.user.name} to see {self.screening.movie.title} at {self.screening.start_time} for {self.seats} seats"
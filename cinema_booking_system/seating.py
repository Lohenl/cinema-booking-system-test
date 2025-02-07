# filepath: /c:/Users/winso/cinema-booking-system-test/cinema_booking_system/user.py
class Seating:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"{self.name} ({self.email})"
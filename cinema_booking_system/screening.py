# filepath: /c:/Users/winso/cinema-booking-system-test/cinema_booking_system/screening.py
from datetime import datetime

class Screening:
    def __init__(self, movie, start_time):
        self.movie = movie
        self.start_time = start_time

    def __str__(self):
        return f"{self.movie.title} at {self.start_time}"
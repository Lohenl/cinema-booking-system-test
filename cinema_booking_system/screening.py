from datetime import datetime
from typing import List
from cinema_booking_system.movie import Movie
from cinema_booking_system.seating_config import SeatingConfig
from cinema_booking_system.booking import Booking
from cinema_booking_system.seating import Seating

class Screening:
    def __init__(self, start_time, seat_config: SeatingConfig, movie: Movie, seating_data:List[Seating], booking_data: List[Booking] = []):
        self.start_time = start_time
        self.seat_config = seat_config
        self.movie = movie
        self.seating_data = seating_data
        self.booking_data = booking_data

    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, value):
        self._start_time = value
    
    @property
    def seat_config(self):
        return self._seat_config
    
    @seat_config.setter
    def seat_config(self, value):
        self._seat_config = value
    
    @property
    def movie(self):
        return self._movie
    
    @movie.setter
    def movie(self, value):
        self._movie = value
    
    def __str__(self):
        return f"{self.movie.title} at {self.start_time}"
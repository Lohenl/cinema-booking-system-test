from typing import List

class Booking:
    def __init__(self, id: str, seats: List[str]):
        self.id = id
        self.seats = seats

    @property
    def id(self) -> str:
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
        
    @property
    def seats(self) -> List[str]:
        return self._seats
    
    @seats.setter
    def seats(self, value):
        self._seats = value
        
    def __str__(self):
        return f"Booking ID: {self.id}, Seats: {self.seats}"
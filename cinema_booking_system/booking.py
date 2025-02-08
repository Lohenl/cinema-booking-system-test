class Booking:
    def __init__(self, id, screening, seats):
        self.id = id
        self.screening = screening
        self.seats = seats

    def __str__(self):
        return f"Booking for {self.id.name} to see {self.screening.movie.title} at {self.screening.start_time} for {self.seats} seats"
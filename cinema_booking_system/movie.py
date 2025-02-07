class Movie:
    def __init__(self, title, duration, rating):
        self.title = title
        self.duration = duration
        self.rating = rating

    def __str__(self):
        return f"{self.title} ({self.duration} mins, {self.rating})"
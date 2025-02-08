class Movie:
    def __init__(self, title):
        self.title = title
        # self.duration = duration
        # self.rating = rating
        
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._title = value
        
    # @property
    # def duration(self):
    #     return self._duration

    # @duration.setter
    # def duration(self, value):
    #     self._duration = value

    # @property
    # def rating(self):
    #     return self._rating

    # @rating.setter
    # def rating(self, value):
    #     self._rating = value

    def __str__(self):
        return f"{self.title} ({self.duration} mins, {self.rating})"
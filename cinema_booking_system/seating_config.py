class SeatingConfig:
    def __init__(self, row_count, seat_count_per_row):
        self.row_count = row_count
        self.seat_count_per_row = seat_count_per_row

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
    
    def __str__(self):
        return f"{self.name} ({self.email})"
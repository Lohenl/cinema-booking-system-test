from cinema_booking_system import Movie, Screening, Booking, Seating, Menu
from datetime import datetime

# Create some example data
movie = Movie("Inception", 148, "PG-13")
user = Seating("John Doe", "john.doe@example.com")
screening = Screening(movie, datetime(2025, 2, 8, 19, 30))
booking = Booking(user, screening, 2)

# Print the booking details
# print(booking)

# Check whether the script is being run directly or being imported as a module
if __name__ == "__main__":
    menu = Menu()
    menu.run()
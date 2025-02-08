from cinema_booking_system import Movie, Screening, Booking, SeatingConfig, BookingMenu, ConfigMenu
from datetime import datetime
# from typing import List

# Create some example data
# movies: List[Movie] = []
movie = Movie("Inception")
# movies.append(movie)

seating_config = SeatingConfig(10, 20)
# screening = Screening(movie, datetime(2025, 2, 8, 19, 30))
# booking = Booking(user, screening, 2)

# Check whether the script is being run directly or being imported as a module
if __name__ == "__main__":
    
    # run the initial config menu
    config_menu = ConfigMenu()
    user_input = config_menu.display_menu()
    
    if user_input.lower() == "exit":
        print("Exiting Configuration Menu\n")
    else:
        print(f"Configured: {user_input}")
        parts = user_input.split()
        title = parts[0]
        row_count = parts[1]
        seat_count_per_row = parts[2]
        movie = Movie(title)
        seating_config = SeatingConfig(row_count, seat_count_per_row)
    
    # run the booking menu
    menu = BookingMenu(movie, seating_config)
    menu.run()

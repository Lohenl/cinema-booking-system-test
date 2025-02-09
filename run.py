from cinema_booking_system import BookingMenu, ConfigMenu
from cinema_booking_system.models import Movie, Screening, SeatingConfig
from datetime import datetime

# Check whether the script is being run directly or being imported as a module
if __name__ == "__main__":
    
    # This part skips all the data retrieval from backend, so you just have a config menu instead of a backend data fetch
    
    # Run the initial config menu
    config_menu = ConfigMenu()
    user_input = config_menu.prompt_config()
    
    # Alternatively, you can replace the above steps with either of the following to skip entering configs
    # user_input = "Down 10 10" # Test with even number of seats
    # user_input = "Down 11 11" # Test with odd number of seats
    
    print(f"Configured: {user_input}")
    parts = user_input.split()
    title = parts[0]
    row_count = int(parts[1])
    seat_count_per_row = int(parts[2])
    movie = Movie(title)
    seating_config = SeatingConfig(row_count, seat_count_per_row)
    screening = Screening(datetime.now(), seating_config, movie, [])
    
    # Run the booking menu
    menu = BookingMenu(screening) # normally screening details would be pulled from a database
    menu.run()

from cinema_booking_system import Movie, Screening, SeatingConfig, BookingMenu, ConfigMenu
from datetime import datetime

# Check whether the script is being run directly or being imported as a module
if __name__ == "__main__":
    
    # run the initial config menu
    config_menu = ConfigMenu()
    user_input = config_menu.prompt_config()
    
    if user_input.lower() == "exit":
        print("Exiting Configuration Menu\n")
    else:
        print(f"Configured: {user_input}")
        parts = user_input.split()
        title = parts[0]
        row_count = int(parts[1])
        seat_count_per_row = int(parts[2])
        movie = Movie(title)
        seating_config = SeatingConfig(row_count, seat_count_per_row)
        screening = Screening(datetime.now(), seating_config, movie, [])
    
    # run the booking menu
    menu = BookingMenu(screening) # normally screening details would be pulled from a database
    menu.run()

# filepath: /c:/Users/winso/cinema-booking-system-test/cinema_booking_system/menu.py
from simple_term_menu import TerminalMenu

class Menu:
    def __init__(self):
        self.options = ["Option 1", "Option 2", "Option 3", "Exit"]

    def display_menu(self):
        terminal_menu = TerminalMenu(self.options)
        menu_entry_index = terminal_menu.show()
        return menu_entry_index

    def run(self):
        while True:
            choice = self.display_menu()
            if choice == 0:
                print("You selected Option 1")
            elif choice == 1:
                print("You selected Option 2")
            elif choice == 2:
                print("You selected Option 3")
            elif choice == 3:
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")
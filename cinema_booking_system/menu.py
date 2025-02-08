from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

class Menu:
    def __init__(self):
        self.options = ["1", "2", "3"]
        self.completer = WordCompleter(self.options, ignore_case=True)

    def display_menu(self):
        user_input = prompt(
            "\n"
            "Welcome to GIC Cinemas\n"
            "[1] Book Tickets for 'Inception' (64 seats available)\n"
            "[2] Check Bookings\n"
            "[3] Exit\n"
            "\n"
            "Please enter your selection (Press Tab to view available options):\n"
            "\n",
            completer=self.completer
        )
        return user_input

    def run(self):
        while True:
            choice = self.display_menu()
            match choice:
                case "1":
                    print(f"\nBook Tickets for 'Inception' (64 seats available)")
                case "2":
                    print("\nCheck Bookings")
                case "3":
                    print("\nThank you for using GIC Cinemas System. Bye!")
                    break
                case _:
                    print("\nInvalid choice, please try again.")
                    
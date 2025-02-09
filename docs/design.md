# Design Documentation

## Class Design

### Entities
- The `Movie` and `Booking` classes directly represent their entities
- The `SeatingConfig` class is simplified from a cinema hall, which can have different number of seats, or class of cinema hall. However for this assignment I've kept it as simple as possible.
- `Screening` is a compound class representing a screening which has a 'has-a'/'has-many' relationships with the abovementioned:
    - A `Screening` can take place in a movie hall (`SeatingConfig`) for a `Movie`.
    - A `Screening` also has multiple `Booking`s associated with it

- Note that in this project ORM is not done - its not in the assignment scope, but it would be done in these classes

### Controllers
- `BookingController` handles booking logic, and simulates transaction control and coordination

### Runtime
- `ConfigMenu` handles prompts and prompt validation for configuring the application - in this case, it simply prompts the user to provide a movie name and the seating configuration of an X-by-Y cinema.
- `BookingMenu` handles prompts and prompt validation for booking seats and viewing booking details
- `SeatingDisplay` provides a visual representation of the cinema booking status when selecting seats or checking booking details

## Assumptions made

The following assumptions have been made for the scope of the assignment.

### Logical assumptions based on `run.py`:

- Movies titles do not contain any whitespace in their name
- There is only 1 cinema that has a rectangular X-by-Y configuration
- There is no center aisle in between the rows of seats
- The default seat selection algorithm assumes the user is OK with the selected seats being split up when there are existing seat bookings in the way
- The custom seat selection algorithm assumes the user is OK with the seats being filled towards the right on the first row, and following the default seat selection algorithm on subsequent rows
- The seat selection algorithm assumes that the user wants to fill the backmost rows next after the seat selection reaches the first and rightmost seat
- There can be up to 9999 bookings made for a given movie screening, thus a 4-digit numbering for a `Booking`'s id is sufficient

### Business / Operational assumptions:

- The user is a cinema operator, and not the cinema-goer
- Payment is processed and validated elsewhere prior to the booking of seats
- There is only 1 running client managing the cinema's booking, i.e., there is no need to check for concurrent seat reservations and new bookings during seat selection
- There is only up to 1 movie screening registered in the system at any given time

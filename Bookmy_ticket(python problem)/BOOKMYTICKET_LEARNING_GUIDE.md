# BookMyTicket Learning Guide

## Introduction
This guide explains every part of `Bookmy_ticket(python problem).py` for beginners. You will learn what each section does, why it is written that way, and how the program works from start to finish.

---

## Rating and Beginner Suitability
- Overall rating: **8 / 10** for a beginner-friendly project.
- Why this is good for beginners:
  - It uses real Python concepts like classes, enums, dataclasses, and functions.
  - It shows how to build a small menu-driven application.
  - It includes input validation and simple error handling.
  - It keeps the example small enough to understand, while still showing a complete booking flow.

---

## File Purpose
This Python script is a simple ticket booking app. It lets a user:
- view available movies,
- select a movie,
- pick seats,
- choose a payment method,
- book seats,
- and receive a booking ID and receipt.

It is a strong learning exercise for:
- object-oriented programming,
- user input handling,
- control flow,
- and data modeling.

---

## Full Code Walkthrough
Below is a section-by-section explanation. Each part of the code is explained in a beginner-friendly way.

### 1. Header Comments
```python
# =====================================================
# BOOKMYTICKETs TICKET BOOKING APPLICATION
# =====================================================
# This simplified ticket booking app uses classes to
# represent movies, shows, seats, and booking logic.
# All comments are preserved and easy to follow.
# =====================================================
```
- These lines are comments. They do not run as code.
- Comments explain the purpose of the script.
- This kind of header is useful for remembering what the file does.

### 2. Imports
```python
from dataclasses import dataclass
from enum import Enum
```
- `from dataclasses import dataclass` imports the `dataclass` decorator.
- `dataclass` makes simple classes easier to write by automatically generating methods like `__init__`.
- `from enum import Enum` imports the base class for enums.
- `Enum` makes named constants like `AVAILABLE` and `BOOKED` easier to use.

### 3. SeatStatus Enum
```python
class SeatStatus(Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"
```
- `SeatStatus` is an enum class.
- Each member (`AVAILABLE`, `BOOKED`) is a named constant.
- This helps avoid using plain strings in the code.
- Enums make the code safer and clearer.

### 4. Seat Dataclass
```python
@dataclass
class Seat:
    seat_id: str
    price: int
    status: SeatStatus = SeatStatus.AVAILABLE
```
- `@dataclass` tells Python to create constructor and helper methods automatically.
- `Seat` stores three values:
  - `seat_id`: a string like `A1`, `B2`.
  - `price`: an integer representing cost.
  - `status`: a `SeatStatus` value, defaulting to `AVAILABLE`.
- This class models one seat in the theatre.

### 5. Movie Dataclass
```python
@dataclass
class Movie:
    movie_name: str
```
- `Movie` stores one piece of data: the movie name.
- It is also a dataclass, so Python automatically creates the constructor.
- This makes the movie easy to pass around in the program.

### 6. Show Class
```python
class Show:
    def __init__(self, movie: Movie):
        self.movie = movie
        self.seats = self._create_seats()
```
- `Show` represents one movie showtime.
- `__init__` is the constructor that runs when a new `Show` is created.
- It stores:
  - `self.movie`: the movie for this show.
  - `self.seats`: a dictionary of seat objects.

#### 6.1 Create Seats
```python
    def _create_seats(self) -> dict[str, Seat]:
        return {
            **{f"A{i}": Seat(f"A{i}", 200) for i in range(1, 4)},
            **{f"B{i}": Seat(f"B{i}", 300) for i in range(1, 4)},
        }
```
- `_create_seats()` returns a dictionary of seats.
- It uses dictionary comprehensions to build seat objects quickly.
- Seats `A1`, `A2`, `A3` cost `200`.
- Seats `B1`, `B2`, `B3` cost `300`.
- The dictionary key is the seat ID and the value is a `Seat` object.

#### 6.2 Display Available Seats
```python
    def display_available_seats(self) -> None:
        print("\nAvailable Seats")
        for seat in self.seats.values():
            if seat.status == SeatStatus.AVAILABLE:
                print(f"{seat.seat_id} - ₹{seat.price}")
```
- `display_available_seats()` prints only seats that are not booked.
- It loops through all seats.
- It checks each seat's status and prints available ones.
- This helps the user know which seats they can pick.

### 7. BookingService Class
```python
class BookingService:
    booking_id = 1
```
- `BookingService` handles the booking logic.
- `booking_id` is a class variable shared across all bookings.
- It starts at `1` and increments after each booking.

#### 7.1 Book Ticket Method
```python
    @classmethod
    def book_ticket(cls, show: Show, seat_ids: list[str]) -> bool:
        selected_seats = []
        total = 0

        for seat_id in seat_ids:
            if seat_id not in show.seats:
                print(f"{seat_id} is invalid.")
                return False

            seat = show.seats[seat_id]
            if seat.status == SeatStatus.BOOKED:
                print(f"{seat_id} is already booked.")
                return False

            selected_seats.append(seat)
            total += seat.price

        for seat in selected_seats:
            seat.status = SeatStatus.BOOKED

        seat_display = ", ".join(seat_ids)
        print("\nBooking Successful")
        print("---------------------------")
        print(f"Booking ID : BK{cls.booking_id}")
        print(f"Movie      : {show.movie.movie_name}")
        print(f"Seats      : {seat_display}")
        print(f"Amount     : ₹{total}")

        cls.booking_id += 1
        return True
```
- `@classmethod` means the method receives the class itself as `cls`.
- This allows the method to access `booking_id` on the class.
- `seat_ids` is a list of seat strings the user entered.
- The method checks each requested seat:
  - If the seat does not exist, it prints an error and returns `False`.
  - If the seat is already booked, it prints an error and returns `False`.
- If all seats are valid and free, it marks them as booked.
- It prints a receipt with booking ID, movie name, seat list, and amount.
- Finally, it increments `booking_id` for the next booking.

### 8. Input Helper Functions
These functions make menu input easier to manage.

#### 8.1 choose_option
```python
def choose_option(prompt: str, valid_choices: list[str]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please try again.")
```
- This function asks the user to type an option.
- It strips spaces from the input.
- If the input is valid, it returns it.
- Otherwise, it repeats until a valid option is entered.
- This prevents invalid menu choices from crashing the program.

#### 8.2 choose_movie
```python
def choose_movie(movies: list[Movie]) -> Movie:
    print("\nSelect Movie")
    for index, movie in enumerate(movies, start=1):
        print(f"{index}. {movie.movie_name}")

    while True:
        try:
            movie_number = int(input("\nEnter Movie Number: ").strip())
            if 1 <= movie_number <= len(movies):
                return movies[movie_number - 1]
        except ValueError:
            pass
        print("Invalid movie number. Please enter a valid number.")
```
- This function prints the movie list with numbers.
- It reads user input and converts it to an integer.
- If the number is valid, it returns the selected `Movie`.
- The `try/except` block catches invalid numbers like `abc`.
- This keeps the app from crashing on bad input.

#### 8.3 parse_seat_ids
```python
def parse_seat_ids(seat_input: str) -> list[str]:
    return [seat.strip().upper() for seat in seat_input.split(",") if seat.strip()]
```
- This function converts the seat input string into a list.
- It splits the input on commas.
- It removes spaces around each seat ID.
- It converts all seat IDs to uppercase.
- This makes input flexible: `a1`, ` A2`, `b3` all work.

---

## 9. Main Function
This is the core loop that runs the application.

```python
def main() -> None:
    movies = [Movie("Interstellar"), Movie("Inception"), Movie("Titanic")]
    shows = {movie.movie_name: Show(movie) for movie in movies}

    while True:
        print("\n==============================")
        print("      BOOKMYTICKETs APP")
        print("==============================")
        print("1. View Movies")
        print("2. Book Ticket")
        print("3. Exit")

        choice = choose_option("\nEnter Choice: ", ["1", "2", "3"])

        if choice == "1":
            print("\nAvailable Movies")
            for index, movie in enumerate(movies, start=1):
                print(f"{index}. {movie.movie_name}")

        elif choice == "2":
            selected_movie = choose_movie(movies)
            selected_show = shows[selected_movie.movie_name]
            selected_show.display_available_seats()

            seat_ids = parse_seat_ids(input("\nEnter Seats (comma separated): "))
            if not seat_ids:
                print("No seats selected.")
                continue

            print("\nPayment Options")
            print("1. UPI")
            print("2. Card")
            payment_choice = choose_option("\nChoose Payment Method: ", ["1", "2"])
            payment_method = "UPI" if payment_choice == "1" else "Card"
            print(f"\n{payment_method} Payment Successful")

            BookingService.book_ticket(selected_show, seat_ids)

        else:
            print("\nThank you.")
            break
```
```
- The first two lines create the list of movies and a dictionary of shows.
- `shows` uses the movie name as the dictionary key.
- The `while True` loop keeps the program running until the user chooses `Exit`.
- The menu displays three choices.
- `choose_option()` validates the menu selection.
- If the user chooses `1`, the app prints the movie list.
- If the user chooses `2`, the app begins the booking flow:
  1. choose a movie,
  2. display available seats,
  3. ask for seat IDs,
  4. ask for payment method,
  5. call `BookingService.book_ticket()`.
- If the user chooses `3`, the app prints a thank-you message and stops.

### 9.1 Why `continue` is used
- After entering no seats, the code prints `No seats selected.` and then `continue` restarts the loop.
- This avoids running the payment and booking logic with an empty seat list.

---

## 10. Entry Point
```python
if __name__ == "__main__":
    main()
```
- This line checks whether the file is being run directly.
- If yes, it calls `main()` and starts the app.
- If the file is imported into another Python program, this block does not run.
- This is a standard Python pattern for scripts.

---

## Key Python Concepts Used Here
### Dataclasses
- `@dataclass` automatically creates `__init__`, `__repr__`, and other helpful methods.
- It is ideal for classes that mostly store values.

### Enums
- `Enum` defines fixed constants.
- It is safer than using strings or numbers directly.
- `SeatStatus.AVAILABLE` is easier to understand than `"Available"`.

### Classmethods
- `@classmethod` receives the class as `cls`, not a specific instance.
- It is useful for shared behavior or shared state like `booking_id`.

### Dictionary Comprehensions
- `{f"A{i}": Seat(f"A{i}", 200) for i in range(1, 4)}` is a concise way to build dictionaries.
- It is faster to write than creating each seat one by one.

### Input Validation
- `choose_option()` prevents invalid menu selections.
- `choose_movie()` catches `ValueError` if the user types text instead of a number.
- `parse_seat_ids()` normalizes user input.

---

## What the Program Does Not Do Yet
This version is simple, so it intentionally leaves out some more advanced features:
- It does not store bookings between program runs.
- It does not support multiple show times for the same movie.
- It does not allow canceling a ticket.
- It does not lock seats while payment is in progress.
- It does not reject duplicate seat IDs in one booking.

These are useful next steps to improve your skills.

---

## Suggested Beginner Exercises
Try these changes to learn more:

1. Add a `cancel_booking()` method.
   - Store each booking in a list.
   - Find the booked seats and mark them available again.

2. Add booked seat display.
   - Print both available and booked seats.
   - This helps the user know which seats are already taken.

3. Add show times.
   - Allow the user to choose a movie and a specific show time.
   - Use a class like `ShowTime` or add a `time` field to `Show`.

4. Refactor the `main()` function.
   - Move code into smaller functions such as:
     - `view_movies()`
     - `book_ticket_flow()`
     - `print_menu()`

5. Improve seat validation.
   - Reject duplicate seat IDs.
   - Let the user re-enter only invalid seats instead of failing the whole booking.

---

## Practical Notes for Beginners
- Always keep the user interface separate from the core logic when you can.
- Use small helper functions for repeated tasks.
- Write comments for complex steps, but avoid commenting obvious lines.
- Run the script often and test each menu option.
- Change one thing at a time, then verify the result.

---

## Summary
This guide turns the script into a full beginner learning resource.
- You now know what each major section does.
- You understand the Python features used.
- You have ideas for next exercises.
- The app is a great foundation for learning how to build interactive Python programs.

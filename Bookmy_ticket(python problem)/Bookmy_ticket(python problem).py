# =====================================================
# BOOKMYTICKETs TICKET BOOKING APPLICATION
# =====================================================
# This simplified ticket booking app uses classes to
# represent movies, shows, seats, and booking logic.
# All comments are preserved and easy to follow.
# =====================================================

from dataclasses import dataclass
from enum import Enum


# =====================================================
# STATUS ENUM
# =====================================================
# Seat can be either AVAILABLE or BOOKED.
# =====================================================

#This Enum class represents the status of a seat in the theatre.
class SeatStatus(Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"



# =====================================================
# SEAT CLASS
# =====================================================
# Represents one seat in the theatre.
# Seat has an ID, a price, and a status.
# =====================================================

# This dataclass represents a seat in the theatre with its ID, price, and status.
#@dataclass means that the class will automatically generate special methods like __init__() and __repr__() based on the defined attributes.,we use SeatStatus Enum to represent the status of the seat, which can be either AVAILABLE or BOOKED.
@dataclass
class Seat:
    seat_id: str
    price: int
    status: SeatStatus = SeatStatus.AVAILABLE


# =====================================================
# MOVIE CLASS
# =====================================================
# Represents a movie by its name.
# =====================================================
@dataclass
class Movie:
    movie_name: str


# =====================================================
# SHOW CLASS
# =====================================================
# Represents one show of a movie and its seats.
# =====================================================
class Show:
    def __init__(self, movie: Movie):
        self.movie = movie
        self.seats = self._create_seats()

    # Create the seat layout for this show.
    def _create_seats(self) -> dict[str, Seat]:
        return {
            **{f"A{i}": Seat(f"A{i}", 200) for i in range(1, 4)},
            **{f"B{i}": Seat(f"B{i}", 300) for i in range(1, 4)},
        }

    # Display only seats that are still available.
    def display_available_seats(self) -> None:
        print("\nAvailable Seats")
        for seat in self.seats.values():
            if seat.status == SeatStatus.AVAILABLE:
                print(f"{seat.seat_id} - ₹{seat.price}")


# =====================================================
# BOOKING SERVICE
# =====================================================
# Handles booking seats and generating booking IDs.
# =====================================================
class BookingService:
    booking_id = 1

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


# =====================================================
# INPUT HELPERS
# =====================================================
# These helper functions keep the menu input logic clean.
# =====================================================

def choose_option(prompt: str, valid_choices: list[str]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please try again.")


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


def parse_seat_ids(seat_input: str) -> list[str]:
    return [seat.strip().upper() for seat in seat_input.split(",") if seat.strip()]


# =====================================================
# MAIN FUNCTION
# =====================================================
# Entry point for the application.
# =====================================================

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


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    main()

#This main function serves as the entry point for the application. 
#It initializes a list of movies and their corresponding shows, then enters a loop to display the main menu. Users can view available movies, book tickets, or exit the application.
#The booking process includes selecting a movie, displaying available seats, choosing seats, selecting a payment method, and confirming the booking.
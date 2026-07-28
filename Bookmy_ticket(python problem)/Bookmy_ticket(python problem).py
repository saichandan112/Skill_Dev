# =====================================================
# BOOKMYTICKETs TICKET BOOKING APPLICATION
# =====================================================
# Concepts Covered:
#
# 1. Classes and Objects
# 2. Constructors (__init__)
# 3. Enum
# 4. Dictionary
# 5. List
# 6. Loops
# 7. Conditional Statements
# 8. User Input
# 9. Class Methods
# 10. Class Variables
# =====================================================


# Import Enum so that we can create constant values
from enum import Enum


# =====================================================
# ENUM
# =====================================================
# Enum is used when we have a fixed set of values.
#
# Instead of:
# seat.status = "BOOKED"
#
# We use:
# seat.status = SeatStatus.BOOKED
#
# This avoids spelling mistakes.
# =====================================================

class SeatStatus(Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"


# =====================================================
# SEAT CLASS
# =====================================================
# Represents one seat in the theatre.
# Example:
# A1 -> ₹200
# B1 -> ₹300
# =====================================================

class Seat:

    # Constructor
    # Automatically called when object is created
    def __init__(self, seat_id, price):

        # Store seat number
        self.seat_id = seat_id

        # Store seat price
        self.price = price

        # Every seat starts as AVAILABLE
        self.status = SeatStatus.AVAILABLE


# =====================================================
# MOVIE CLASS
# =====================================================
# Represents a movie.
#
# Example:
# Movie("Interstellar")
# =====================================================

class Movie:

    def __init__(self, movie_name):

        # Store movie name
        self.movie_name = movie_name


# =====================================================
# SHOW CLASS
# =====================================================
# Represents one show of a movie.
#
# A show contains:
# 1. Movie
# 2. Seats
#
# Every movie gets its own seats.
# =====================================================

class Show:

    def __init__(self, movie):

        # Store movie object
        self.movie = movie

        # Dictionary
        #
        # Key   -> Seat ID
        # Value -> Seat Object
        #
        # Example:
        # {
        #   "A1": Seat Object,
        #   "A2": Seat Object
        # }
        #
        self.seats = {

            "A1": Seat("A1", 200),
            "A2": Seat("A2", 200),
            "A3": Seat("A3", 200),

            "B1": Seat("B1", 300),
            "B2": Seat("B2", 300),
            "B3": Seat("B3", 300)
        }

    # =================================================
    # DISPLAY AVAILABLE SEATS
    # =================================================
    def display_seats(self):

        print("\nAvailable Seats")

        # Loop through all seat objects
        for seat in self.seats.values():

            # Show only available seats
            if seat.status == SeatStatus.AVAILABLE:

                print(
                    f"{seat.seat_id} - ₹{seat.price}"
                )


# =====================================================
# BOOKING SERVICE
# =====================================================
# Responsible for booking seats.
# =====================================================

class BookingService:

    # Class Variable
    #
    # Shared across all bookings.
    #
    # First Booking  -> BK1
    # Second Booking -> BK2
    #
    booking_id = 1

    # Class Method
    # cls refers to class itself
    @classmethod
    def book_ticket(cls, show, seat_ids):

        # Stores selected seat objects
        selected = []

        # Stores total ticket price
        total = 0

        # Loop through seat numbers entered by user
        for seat_id in seat_ids:

            # Check if seat exists
            if seat_id not in show.seats:

                print(f"{seat_id} is invalid")
                return

            # Get seat object
            seat = show.seats[seat_id]

            # Check if already booked
            if seat.status == SeatStatus.BOOKED:

                print(f"{seat_id} already booked")
                return

            # Add seat into selected list
            selected.append(seat)

            # Calculate total amount
            total += seat.price

        # Mark selected seats as booked
        for seat in selected:
            seat.status = SeatStatus.BOOKED

        # Show booking details
        print("\nBooking Successful")
        print("---------------------------")

        print(
            f"Booking ID : BK{cls.booking_id}"
        )

        print(
            f"Movie      : {show.movie.movie_name}"
        )

        print(
            f"Seats      : {seat_ids}"
        )

        print(
            f"Amount     : ₹{total}"
        )

        # Increment booking id
        cls.booking_id += 1


# =====================================================
# MAIN FUNCTION
# =====================================================
# Program execution starts here.
# =====================================================

def main():

    # ================================================
    # CREATE MOVIES
    # ================================================

    movies = [

        Movie("Interstellar"),

        Movie("Inception"),

        Movie("Titanic")

    ]

    # ================================================
    # CREATE SHOWS
    # ================================================
    # Dictionary:
    #
    # {
    #   "Interstellar": ShowObject,
    #   "Inception": ShowObject
    # }
    #
    # ================================================

    shows = {}

    for movie in movies:

        shows[movie.movie_name] = Show(movie)

    # ================================================
    # MENU LOOP
    # ================================================
    # Runs forever until user chooses Exit
    # ================================================

    while True:

        print("\n==============================")
        print("      BOOKMYTICKETs APP")
        print("==============================")

        print("1. View Movies")
        print("2. Book Ticket")
        print("3. Exit")

        # Read user choice
        choice = input(
            "\nEnter Choice : "
        )

        # ============================================
        # VIEW MOVIES
        # ============================================
        if choice == "1":

            print("\nAvailable Movies")

            # enumerate gives index + value
            for i, movie in enumerate(
                    movies,
                    start=1):

                print(
                    i,
                    movie.movie_name
                )

        # ============================================
        # BOOK TICKET
        # ============================================
        elif choice == "2":

            print("\nSelect Movie")

            for i, movie in enumerate(
                    movies,
                    start=1):

                print(
                    i,
                    movie.movie_name
                )

            # Take movie number
            movie_choice = int(

                input(
                    "\nEnter Movie Number : "
                )

            )

            # Convert numbered choice into list index
            #
            # User enters 1
            # Python index is 0
            #
            selected_movie = movies[
                movie_choice - 1
            ]

            # Get corresponding show
            selected_show = shows[
                selected_movie.movie_name
            ]

            # Display available seats
            selected_show.display_seats()

            # ========================================
            # SEAT INPUT
            # ========================================
            #
            # Example:
            # A1,B2
            #
            # ========================================

            seat_input = input(
                "\nEnter Seats "
                "(comma separated): "
            )

            # Convert String to List
            #
            # "A1,B2"
            #
            # becomes
            #
            # ['A1', 'B2']
            #
            seat_ids = [

                seat.strip().upper()

                for seat in seat_input.split(",")

            ]

            # ========================================
            # PAYMENT SECTION
            # ========================================

            print("\nPayment Options")
            print("1. UPI")
            print("2. Card")

            payment_choice = input(
                "\nChoose Payment Method : "
            )

            if payment_choice == "1":

                print(
                    "\nUPI Payment Successful"
                )

            else:

                print(
                    "\nCard Payment Successful"
                )

            # Call booking service
            BookingService.book_ticket(

                selected_show,

                seat_ids

            )

        # ============================================
        # EXIT
        # ============================================
        elif choice == "3":

            print("\nThank You")

            # Stop menu loop
            break

        # ============================================
        # INVALID OPTION
        # ============================================
        else:

            print(
                "\nInvalid Choice"
            )


# =====================================================
# ENTRY POINT
# =====================================================
# This ensures execution starts from main()
# =====================================================

if __name__ == "__main__":

    main()

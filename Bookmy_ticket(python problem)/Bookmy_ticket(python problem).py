from enum import Enum


class SeatStatus(Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"


class Seat:
    def __init__(self, seat_id, price):
        self.seat_id = seat_id
        self.price = price
        self.status = SeatStatus.AVAILABLE


class Movie:
    def __init__(self, movie_name):
        self.movie_name = movie_name


class Show:

    def __init__(self, movie):
        self.movie = movie

        self.seats = {
            "A1": Seat("A1", 200),
            "A2": Seat("A2", 200),
            "A3": Seat("A3", 200),
            "B1": Seat("B1", 300),
            "B2": Seat("B2", 300),
            "B3": Seat("B3", 300),
        }

    def display_seats(self):

        print("\nAvailable Seats")

        for seat in self.seats.values():

            if seat.status == SeatStatus.AVAILABLE:
                print(
                    f"{seat.seat_id}"
                    f" - ₹{seat.price}"
                )


class BookingService:

    booking_id = 1

    @classmethod
    def book_ticket(cls, show, seat_ids):

        selected = []
        total = 0

        for seat_id in seat_ids:

            if seat_id not in show.seats:
                print(f"{seat_id} invalid")
                return

            seat = show.seats[seat_id]

            if seat.status == SeatStatus.BOOKED:
                print(f"{seat_id} already booked")
                return

            selected.append(seat)
            total += seat.price

        for seat in selected:
            seat.status = SeatStatus.BOOKED

        print("\nBooking Successful")
        print("-------------------")
        print(f"Booking ID : BK{cls.booking_id}")
        print(f"Movie      : {show.movie.movie_name}")
        print(f"Seats      : {seat_ids}")
        print(f"Amount     : ₹{total}")

        cls.booking_id += 1


def main():

    movies = [
        Movie("Interstellar"),
        Movie("Inception"),
        Movie("Titanic")
    ]

    shows = {}

    for movie in movies:
        shows[movie.movie_name] = Show(movie)

    while True:

        print("\n========== BOOKMYSHOW ==========")
        print("1. View Movies")
        print("2. Book Ticket")
        print("3. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            print("\nMovies")

            for i, movie in enumerate(movies, start=1):
                print(i, movie.movie_name)

        elif choice == "2":

            print("\nSelect Movie")

            for i, movie in enumerate(movies, start=1):
                print(i, movie.movie_name)

            movie_choice = int(
                input("\nEnter Movie Number : ")
            )

            selected_movie = movies[
                movie_choice - 1
            ]

            selected_show = shows[
                selected_movie.movie_name
            ]

            selected_show.display_seats()

            seat_input = input(
                "\nEnter Seats "
                "(comma separated) : "
            )

            seat_ids = [
                seat.strip().upper()
                for seat in seat_input.split(",")
            ]

            print("\nPayment Options")
            print("1. UPI")
            print("2. Card")

            payment_choice = input(
                "Choose Payment Method : "
            )

            if payment_choice == "1":
                print("\nUPI Payment Successful")
            else:
                print("\nCard Payment Successful")

            BookingService.book_ticket(
                selected_show,
                seat_ids
            )

        elif choice == "3":

            print("\nThank You")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()
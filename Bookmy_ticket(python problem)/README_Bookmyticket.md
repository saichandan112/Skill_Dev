# BookMyShow-Style Ticket Booking System

A Python implementation of a movie ticket booking system, modeled after platforms like BookMyShow/Fandango. Built as **Exercise 2** in a self-directed Low-Level Design (LLD) learning series, following a Parking Lot system (Exercise 1).

## Overview

This project focuses on two of the trickiest parts of ticket-booking LLD interviews:

- **Per-show seat state** — the same physical seat is tracked independently for every show, not globally across a theatre.
- **Seat locking with expiry** — seats are temporarily locked (not booked) while a user is paying, so two people can't purchase the same seat. If payment isn't completed in time, the lock expires and the seat returns to the available pool.

## Architecture

**Catalog layer** (static data)
- `Movie` — movie metadata
- `Seat` — a physical seat definition (row, number, tier)
- `Screen` — a screen within a theatre, with a fixed seat layout
- `Theatre` — a venue containing one or more screens

**Show layer**
- `Show` — binds a `Movie` to a `Screen` at a specific date/time
- `ShowSeat` — per-show availability record for each seat (this is the key design insight: seat A1 for the 3 PM show and seat A1 for the 6 PM show are independent records)

**Booking flow**
- `lock_seats()` — temporarily reserves selected seats (`AVAILABLE → LOCKED`), guarded by a `threading.Lock` to prevent race conditions
- `confirm_seats()` — on successful payment, flips locked seats to `BOOKED` and creates a `Booking`
- `release_seats()` — called on lock expiry or cancellation, returns seats to `AVAILABLE`
- `Booking` — a confirmed reservation record
- `Payment` — a stub payment gateway

**Facade**
- `BookMyShowSystem` — the single entry point a client app would use: `search_shows()`, `select_seats()`, `checkout()`, `cancel_booking()`

## Seat State Machine

```
AVAILABLE → LOCKED → BOOKED
    ↑          |
    └──────────┘
   (lock expiry or cancellation)
```

## Demo

Running the file executes five scenarios that exercise the full state machine:

1. User A locks 2 seats
2. User B tries to lock one of User A's locked seats → correctly rejected
3. User A completes payment → seats flip to `BOOKED`
4. User C locks seats but never pays → lock expires → seats return to `AVAILABLE`
5. User A cancels a confirmed booking → seats are freed again

```bash
python bookmyshow_system.py
```

## Design Patterns Used

| Pattern | Where |
|---|---|
| Facade | `BookMyShowSystem` hides all internal complexity behind a clean API |
| State | Seat lifecycle (`AVAILABLE` / `LOCKED` / `BOOKED`) |

## Possible Extensions

These are natural next steps for continuing the exercise:

- **Strategy pattern** — pluggable `PricingStrategy` for discounts/coupons
- **Payment abstraction** — turn `Payment` into an abstract base with `CardPayment`, `UPIPayment`, etc.
- **Real concurrency test** — race actual `threading.Thread`s against the same seat instead of sequential calls
- **Observer pattern** — notify users via email/SMS on booking confirmation or cancellation

## Part of the LLD Series

1. Parking Lot System
2. **BookMyShow-Style Ticket Booking** (this project)
3. *(next up: rate limiter / expense-sharing system)*

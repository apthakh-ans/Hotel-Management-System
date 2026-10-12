# 🏨 Hotel Management System

A comprehensive Hotel Management System built with Python (Streamlit) for the frontend and MySQL as the backend database.

## 🔧 Fixes Applied
- **`requirements.txt` was empty** — `pip install -r requirements.txt` installed nothing, so the
  app couldn't even start. Populated with the actual runtime dependencies.
- **DB credentials were hardcoded in source** (and three different files disagreed on the
  database name: `hotel_management` in the README, `hotel_db` in `db.py`, `hotel_mgmt` in a stray
  SQL file) — moved to `.env` (see `.env.example`), read via `python-dotenv`.
- **Login passwords were stored and compared in plaintext** (`SELECT * FROM UserLogin WHERE
  Username = %s AND Password = %s`) — switched to PBKDF2-HMAC-SHA256 hashing with a random
  per-user salt; the default admin seed row now stores a hash, not `admin123` in the clear.
- **Dashboard's "Revenue per Month" chart was a labeled hack** (`PaymentID % 12`, with a comment
  admitting "real one needs payment date") — `Payment.PaymentDate` already existed in the schema
  but wasn't being queried; now it's fetched and used for real month grouping.
- **Removed three dead/misleading files**: `connector.py` (an unused, unimported duplicate of the
  DB connection logic with yet another hardcoded password), `Frontend.py` (empty, unreferenced),
  and `HOTEL MANAGEMENT SYSTEM.sql` (an entirely different, incompatible schema — `hotel_mgmt`
  with snake_case tables — left over from an earlier draft; following it instead of `SQLTABLES.sql`
  would set up a database the app can't actually use).
- **README setup instructions pointed at code that didn't exist** (a `DB_CONFIG` dict supposedly
  in `app.py` lines 18–24, a `CREATE DATABASE hotel_management` that didn't match any table
  definitions anywhere) — rewritten to match what the code actually does.

## Features

- **Guest Management**: Full CRUD operations for guest information
- **Room Management**: Manage room details, availability, and pricing
- **Booking Management**: Create and manage bookings with date validation
- **Payment Management**: Track payments for bookings
- **Data Validation**: Ensures data integrity (e.g., check-in < check-out, room availability)
- **Sample Data**: Automatically inserts sample data on first run

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL Database:**
   - Make sure MySQL server is running
   - Create the database and all tables by running the schema script (this also creates
     the `hotel_db` database and seeds a default admin login):
     ```bash
     mysql -u root -p < SQLTABLES.sql
     ```

4. **Configure database credentials:**
   - Copy `.env.example` to `.env` and fill in your MySQL credentials:
     ```bash
     cp .env.example .env
     ```
     ```env
     DB_HOST=localhost
     DB_PORT=3306
     DB_USER=root
     DB_PASSWORD=your_mysql_password
     DB_NAME=hotel_db
     ```
   - `db.py` reads these via `python-dotenv`; nothing is hardcoded in source. `.env` is
     gitignored, so your credentials never get committed.

## Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't, navigate to the URL shown in the terminal

## Database Schema

The authoritative schema is `SQLTABLES.sql` (run it to set up the database — see Installation).
It defines: `Guest`, `Room`, `Booking`, `Payment`, `Staff`, `ServiceRequest`, `Amenity`,
`RoomAmenity`, `Review`, `TravelPackage`, `RoomMaintenance`, and `UserLogin`.

### Guest
- `GuestID` (INT, PRIMARY KEY, AUTO_INCREMENT), `Name`, `Email`, `Phone`

### Room
- `RoomID` (INT, PRIMARY KEY, AUTO_INCREMENT), `RoomNumber`, `Type`, `Price` (DECIMAL), `IsAvailable` (BOOLEAN)

### Booking
- `BookingID` (INT, PRIMARY KEY, AUTO_INCREMENT), `GuestID` → Guest, `RoomID` → Room,
  `CheckInDate`, `CheckOutDate`

### Payment
- `PaymentID` (INT, PRIMARY KEY, AUTO_INCREMENT), `BookingID` → Booking, `Amount`, `Method`,
  `PaymentDate` (TIMESTAMP, defaults to now)

### UserLogin
- `UserID` (INT, PRIMARY KEY, AUTO_INCREMENT), `Username` (UNIQUE), `Password` (PBKDF2-HMAC-SHA256
  hash, stored as `salt_hex$hash_hex` — never plaintext), `Role`

Staff, ServiceRequest, Amenity/RoomAmenity, Review, TravelPackage, and RoomMaintenance follow the
same pattern — see `SQLTABLES.sql` for exact columns.

## Tests

```bash
pytest tests/ -v
```

Covers the password-hashing logic (`db.hash_password` / `db.verify_password`) — no database or
network connection required.

## Usage

### Navigation
Use the sidebar to navigate between different sections:
- **Guests**: Manage guest information
- **Rooms**: Manage room details and availability
- **Bookings**: Create and manage bookings
- **Payments**: Track payments

### Adding Records
1. Click on the "➕ Add New [Entity]" expander
2. Fill in the required fields
3. Click the submit button

### Viewing Records
All records are displayed in tables below the add forms.

### Updating Records
1. Select the record ID from the dropdown
2. Modify the fields in the update form
3. Click the update button

### Deleting Records
1. Select the record ID from the dropdown
2. Click the delete button
3. Confirm the deletion

## Validation Rules

- **Bookings**: 
  - Check-out date must be after check-in date
  - Room must be available for the selected dates
- **Payments**: 
  - Amount must be greater than 0
- **Guests**: 
  - Email must be unique
- **Rooms**: 
  - Room number must be unique
  - Price must be greater than 0

## Sample Data

The application automatically inserts sample data on first run:
- 5 sample guests
- 8 sample rooms (various types)
- 3 sample bookings
- 3 sample payments

## Security Notes

- All SQL queries use parameterized statements to prevent SQL injection
- Database credentials are read from `.env` (see `.env.example`), never hardcoded in source
- Login passwords are hashed with PBKDF2-HMAC-SHA256 (100,000 iterations, random per-user salt),
  not stored or compared in plaintext
- The default `admin` / `admin123` login is meant for local/demo use only — change it (or add a
  new user via `db.insert_user`) before using this anywhere beyond your own machine

## Troubleshooting

### Connection Errors
- Ensure MySQL server is running
- Verify database credentials in `app.py`
- Check that the `hotel_management` database exists

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### Port Already in Use
- Streamlit uses port 8501 by default
- Use `streamlit run app.py --server.port 8502` to use a different port

## License

This project is open source and available for educational purposes.

## Author

Created as a comprehensive Hotel Management System demonstration.


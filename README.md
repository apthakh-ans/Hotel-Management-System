# 🏨 Hotel Management System

A comprehensive Hotel Management System built with Python (Streamlit) for the frontend and MySQL as the backend database.

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
   - Create a database named `hotel_management`:
     ```sql
     CREATE DATABASE hotel_management;
     ```
   - Update the database configuration in `app.py` (lines 18-24):
     ```python
     DB_CONFIG = {
         'host': 'localhost',
         'database': 'hotel_management',
         'user': 'root',          # Change to your MySQL username
         'password': 'root',       # Change to your MySQL password
         'port': 3306
     }
     ```

## Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't, navigate to the URL shown in the terminal

## Database Schema

### Guest Table
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `name` (VARCHAR(100), NOT NULL)
- `email` (VARCHAR(100), UNIQUE, NOT NULL)
- `phone` (VARCHAR(20), NOT NULL)
- `created_at` (TIMESTAMP)

### Room Table
- `room_number` (INT, PRIMARY KEY)
- `type` (VARCHAR(50), NOT NULL)
- `availability` (BOOLEAN, DEFAULT TRUE)
- `price` (DECIMAL(10, 2), NOT NULL)
- `created_at` (TIMESTAMP)

### Booking Table
- `booking_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `guest_id` (INT, FOREIGN KEY → Guest.id)
- `room_number` (INT, FOREIGN KEY → Room.room_number)
- `check_in` (DATE, NOT NULL)
- `check_out` (DATE, NOT NULL)
- `status` (VARCHAR(20), DEFAULT 'confirmed')
- `created_at` (TIMESTAMP)

### Payment Table
- `payment_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `booking_id` (INT, FOREIGN KEY → Booking.booking_id)
- `amount` (DECIMAL(10, 2), NOT NULL)
- `method` (VARCHAR(50), NOT NULL)
- `status` (VARCHAR(20), DEFAULT 'pending')
- `payment_date` (TIMESTAMP)

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
- Database credentials should be stored securely in production (use environment variables)
- Consider implementing user authentication for production use

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


import mysql.connector
from mysql.connector import Error

def get_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="hotel_db"
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

# ==================== GUEST FUNCTIONS ====================

def insert_guest(name, email, phone):
    """Add a new guest"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO Guest (Name, Email, Phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Guest added successfully"
    except Error as e:
        return False, f"Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def fetch_all_guests():
    """Get all guests"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT GuestID, Name, Email, Phone FROM Guest")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching guests: {e}")
        return []

def get_guest_options():
    """Get guest options for dropdowns"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT GuestID, Name FROM Guest")
        guests = cursor.fetchall()
        cursor.close()
        conn.close()
        return guests
    except Error as e:
        print(f"Error fetching guest options: {e}")
        return []

def update_guest(guest_id, name, email, phone):
    """Update guest information"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "UPDATE Guest SET Name = %s, Email = %s, Phone = %s WHERE GuestID = %s"
        cursor.execute(query, (name, email, phone, guest_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Guest updated successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def delete_guest_by_id(guest_id):
    """Delete a guest - Handles cascading deletes"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Delete all reviews by the guest
        cursor.execute("DELETE FROM Review WHERE GuestID = %s", (guest_id,))
        # 2. Delete all service requests by the guest
        cursor.execute("DELETE FROM ServiceRequest WHERE GuestID = %s", (guest_id,))
        # 3. Delete all bookings by the guest (after deleting their payments)
        cursor.execute("SELECT BookingID FROM Booking WHERE GuestID = %s", (guest_id,))
        bookings = cursor.fetchall()
        for (booking_id,) in bookings:
            cursor.execute("DELETE FROM Payment WHERE BookingID = %s", (booking_id,))
        cursor.execute("DELETE FROM Booking WHERE GuestID = %s", (guest_id,))
        # 4. Delete the guest
        cursor.execute("DELETE FROM Guest WHERE GuestID = %s", (guest_id,))
        conn.commit()
        return True, "Guest and all related records deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== ROOM FUNCTIONS ====================

def insert_room(room_number, room_type, price, is_available):
    """Add a new room"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO Room (RoomNumber, Type, Price, IsAvailable) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (room_number, room_type, price, is_available))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Room added successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_all_rooms():
    """Get all rooms"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT RoomID, RoomNumber, Type, Price, IsAvailable FROM Room")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching rooms: {e}")
        return []

def get_room_options():
    """Get room options for dropdowns"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT RoomID, RoomNumber FROM Room")
        rooms = cursor.fetchall()
        cursor.close()
        conn.close()
        return rooms
    except Error as e:
        print(f"Error fetching room options: {e}")
        return []

def get_available_rooms():
    """Get only available rooms"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT RoomID, RoomNumber FROM Room WHERE IsAvailable = TRUE")
        rooms = cursor.fetchall()
        cursor.close()
        conn.close()
        return rooms
    except Error as e:
        print(f"Error fetching available rooms: {e}")
        return []

def update_room(room_id, room_number, room_type, price, is_available):
    """Update room information"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "UPDATE Room SET RoomNumber = %s, Type = %s, Price = %s, IsAvailable = %s WHERE RoomID = %s"
        cursor.execute(query, (room_number, room_type, price, is_available, room_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Room updated successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def delete_room(room_id):
    """Delete a room - Handles cascading deletes"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Delete amenities for the room
        cursor.execute("DELETE FROM RoomAmenity WHERE RoomID = %s", (room_id,))
        # 2. Delete maintenance logs
        cursor.execute("DELETE FROM RoomMaintenance WHERE RoomID = %s", (room_id,))
        # 3. Delete service requests for the room
        cursor.execute("DELETE FROM ServiceRequest WHERE RoomID = %s", (room_id,))
        # 4. Delete reviews for the room
        cursor.execute("DELETE FROM Review WHERE RoomID = %s", (room_id,))
        # 5. Delete all bookings (and each payment)
        cursor.execute("SELECT BookingID FROM Booking WHERE RoomID = %s", (room_id,))
        bookings = cursor.fetchall()
        for (booking_id,) in bookings:
            cursor.execute("DELETE FROM Payment WHERE BookingID = %s", (booking_id,))
        cursor.execute("DELETE FROM Booking WHERE RoomID = %s", (room_id,))
        # 6. Delete the room
        cursor.execute("DELETE FROM Room WHERE RoomID = %s", (room_id,))
        conn.commit()
        return True, "Room and all related records deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== BOOKING FUNCTIONS ====================

def insert_booking(guest_id, room_id, checkin, checkout):
    """Create a new booking and mark room as unavailable"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO Booking (GuestID, RoomID, CheckInDate, CheckOutDate) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (guest_id, room_id, checkin, checkout))

        # Mark room as unavailable
        cursor.execute("UPDATE Room SET IsAvailable = FALSE WHERE RoomID = %s", (room_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Booking created successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_all_bookings():
    """Get all bookings with guest and room details"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
        SELECT b.BookingID, g.Name, r.RoomNumber, b.CheckInDate, b.CheckOutDate
        FROM Booking b
        JOIN Guest g ON b.GuestID = g.GuestID
        JOIN Room r ON b.RoomID = r.RoomID
        ORDER BY b.CheckInDate DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching bookings: {e}")
        return []

def get_booking_options():
    """Get booking options for dropdowns"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
        SELECT b.BookingID, g.Name, r.RoomNumber
        FROM Booking b
        JOIN Guest g ON b.GuestID = g.GuestID
        JOIN Room r ON b.RoomID = r.RoomID
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching booking options: {e}")
        return []

def get_booking_price_details(booking_id):
    """Get booking dates and room price"""
    try:
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        query = """
        SELECT b.CheckInDate, b.CheckOutDate, r.Price
        FROM Booking b
        JOIN Room r ON b.RoomID = r.RoomID
        WHERE b.BookingID = %s
        """
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Error as e:
        print(f"Error fetching booking price details: {e}")
        return None

def cancel_booking(booking_id):
    """Cancel a booking and free up the room"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get room ID first
        cursor.execute("SELECT RoomID FROM Booking WHERE BookingID = %s", (booking_id,))
        room = cursor.fetchone()

        if room:
            room_id = room[0]
            # Delete payments first
            cursor.execute("DELETE FROM Payment WHERE BookingID = %s", (booking_id,))
            # Delete booking
            cursor.execute("DELETE FROM Booking WHERE BookingID = %s", (booking_id,))
            # Free the room
            cursor.execute("UPDATE Room SET IsAvailable = TRUE WHERE RoomID = %s", (room_id,))

        conn.commit()
        return True, "Booking cancelled successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def update_booking(booking_id, checkin, checkout):
    """Update booking dates"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "UPDATE Booking SET CheckInDate = %s, CheckOutDate = %s WHERE BookingID = %s"
        cursor.execute(query, (checkin, checkout, booking_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Booking updated successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def delete_booking(booking_id):
    """Delete a booking - Handles cascading deletes"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get room ID first to free it
        cursor.execute("SELECT RoomID FROM Booking WHERE BookingID = %s", (booking_id,))
        room = cursor.fetchone()

        # Delete payments first
        cursor.execute("DELETE FROM Payment WHERE BookingID = %s", (booking_id,))
        # Delete the booking
        cursor.execute("DELETE FROM Booking WHERE BookingID = %s", (booking_id,))

        # Free the room if found
        if room:
            room_id = room[0]
            cursor.execute("UPDATE Room SET IsAvailable = TRUE WHERE RoomID = %s", (room_id,))

        conn.commit()
        return True, "Booking and related payments deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== PAYMENT FUNCTIONS ====================

def insert_payment(booking_id, amount, method):
    """Record a payment"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO Payment (BookingID, Amount, Method) VALUES (%s, %s, %s)"
        cursor.execute(query, (booking_id, amount, method))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Payment recorded successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_all_payments():
    """Get all payments with booking and guest details"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
        SELECT p.PaymentID, g.Name, r.RoomNumber, p.Amount, p.Method
        FROM Payment p
        JOIN Booking b ON p.BookingID = b.BookingID
        JOIN Guest g ON b.GuestID = g.GuestID
        JOIN Room r ON b.RoomID = r.RoomID
        ORDER BY p.PaymentID DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching payments: {e}")
        return []

# ==================== STAFF FUNCTIONS ====================

def insert_staff(name, role, phone, email):
    """Add a new staff member"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO Staff (Name, Role, Phone, Email) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, role, phone, email))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Staff member added successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_all_staff():
    """Get all staff members"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT StaffID, Name, Role, Phone, Email FROM Staff")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching staff: {e}")
        return []

def delete_staff(staff_id):
    """Delete a staff member"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Staff WHERE StaffID = %s", (staff_id,))
        conn.commit()
        return True, "Staff member deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== SERVICE REQUEST FUNCTIONS ====================

def insert_service_request(guest_id, room_id, service_type):
    """Create a new service request"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO ServiceRequest (GuestID, RoomID, ServiceType, Status) VALUES (%s, %s, %s, 'Pending')"
        cursor.execute(query, (guest_id, room_id, service_type))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Service request created successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_all_service_requests():
    """Get all service requests"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
        SELECT sr.RequestID, g.Name, r.RoomNumber, sr.ServiceType, sr.Status, sr.RequestTime
        FROM ServiceRequest sr
        JOIN Guest g ON sr.GuestID = g.GuestID
        JOIN Room r ON sr.RoomID = r.RoomID
        ORDER BY sr.RequestTime DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching service requests: {e}")
        return []

def delete_service_request(request_id):
    """Delete a service request"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ServiceRequest WHERE RequestID = %s", (request_id,))
        conn.commit()
        return True, "Service request deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== AMENITY FUNCTIONS ====================

def insert_amenity(name):
    """Add a new amenity"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        cursor.execute("INSERT INTO Amenity (Name) VALUES (%s)", (name,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Amenity added successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_all_amenities():
    """Get all amenities"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT AmenityID, Name FROM Amenity")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching amenities: {e}")
        return []

def assign_amenity_to_room(room_id, amenity_id):
    """Assign amenity to a room"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        cursor.execute("INSERT IGNORE INTO RoomAmenity (RoomID, AmenityID) VALUES (%s, %s)", (room_id, amenity_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Amenity assigned successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_room_amenities():
    """Get all room-amenity relationships"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
        SELECT r.RoomNumber, a.Name
        FROM RoomAmenity ra
        JOIN Room r ON ra.RoomID = r.RoomID
        JOIN Amenity a ON ra.AmenityID = a.AmenityID
        ORDER BY r.RoomNumber
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching room amenities: {e}")
        return []

def delete_amenity(amenity_id):
    """Delete an amenity"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Delete from junction table first
        cursor.execute("DELETE FROM RoomAmenity WHERE AmenityID = %s", (amenity_id,))
        # Then delete amenity
        cursor.execute("DELETE FROM Amenity WHERE AmenityID = %s", (amenity_id,))
        conn.commit()
        return True, "Amenity deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== REVIEW FUNCTIONS ====================

def insert_review(guest_id, room_id, rating, comment, review_date):
    """Add a new review"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO Review (GuestID, RoomID, Rating, Comment, ReviewDate) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (guest_id, room_id, rating, comment, review_date))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Review added successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_all_reviews():
    """Get all reviews"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
        SELECT rv.ReviewID, g.Name, r.RoomNumber, rv.Rating, rv.Comment, rv.ReviewDate
        FROM Review rv
        JOIN Guest g ON rv.GuestID = g.GuestID
        JOIN Room r ON rv.RoomID = r.RoomID
        ORDER BY rv.ReviewDate DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching reviews: {e}")
        return []

def delete_review(review_id):
    """Delete a review"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Review WHERE ReviewID = %s", (review_id,))
        conn.commit()
        return True, "Review deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== TRAVEL PACKAGE FUNCTIONS ====================

def insert_travel_package(title, description, price, duration_days):
    """Add a new travel package"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO TravelPackage (Title, Description, Price, DurationDays) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, description, price, duration_days))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Travel package added successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_all_travel_packages():
    """Get all travel packages"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT PackageID, Title, Description, Price, DurationDays FROM TravelPackage ORDER BY PackageID DESC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching travel packages: {e}")
        return []

def delete_travel_package(package_id):
    """Delete a travel package"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM TravelPackage WHERE PackageID = %s", (package_id,))
        conn.commit()
        return True, "Travel package deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== ROOM MAINTENANCE FUNCTIONS ====================

def insert_maintenance_log(room_id, issue, reported_date):
    """Add a maintenance log"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO RoomMaintenance (RoomID, Issue, ReportedDate, Status) VALUES (%s, %s, %s, 'Open')"
        cursor.execute(query, (room_id, issue, reported_date))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Maintenance log created successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

def fetch_maintenance_logs():
    """Get all maintenance logs"""
    try:
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
        SELECT rm.MaintenanceID, r.RoomNumber, rm.Issue, rm.ReportedDate, rm.Status
        FROM RoomMaintenance rm
        JOIN Room r ON rm.RoomID = r.RoomID
        ORDER BY rm.ReportedDate DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Error as e:
        print(f"Error fetching maintenance logs: {e}")
        return []

def delete_maintenance_log(maintenance_id):
    """Delete a maintenance log"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM RoomMaintenance WHERE MaintenanceID = %s", (maintenance_id,))
        conn.commit()
        return True, "Maintenance log deleted successfully"
    except Error as e:
        conn.rollback()
        return False, f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# ==================== USER AUTHENTICATION ====================

def validate_user(username, password):
    """Authenticate user"""
    try:
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        query = "SELECT * FROM UserLogin WHERE Username = %s AND Password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Error as e:
        print(f"Error validating user: {e}")
        return None

def insert_user(username, password, role='Admin'):
    """Create a new user"""
    try:
        conn = get_connection()
        if not conn:
            return False, "Database connection failed"

        cursor = conn.cursor()
        query = "INSERT INTO UserLogin (Username, Password, Role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, role))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "User created successfully"
    except Error as e:
        return False, f"Error: {str(e)}"

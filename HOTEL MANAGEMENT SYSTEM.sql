CREATE DATABASE hotel_mgmt;
USE hotel_mgmt;
CREATE TABLE hotels (
  hotel_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  address VARCHAR(200),
  phone VARCHAR(20)
);
CREATE TABLE room_types (
  room_type_id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT,
  type_name VARCHAR(50),
  price DECIMAL(10,2),
  capacity INT,
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);
CREATE TABLE rooms (
  room_id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT,
  room_type_id INT,
  room_number VARCHAR(10),
  status VARCHAR(20),
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),
  FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id)
);
CREATE TABLE guests (
  guest_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  phone VARCHAR(20),
  email VARCHAR(100)
);
CREATE TABLE bookings (
  booking_id INT AUTO_INCREMENT PRIMARY KEY,
  guest_id INT,
  room_id INT,
  check_in DATE,
  check_out DATE,
  status VARCHAR(20),
  FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
  FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);
CREATE TABLE payments (
  payment_id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT,
  amount DECIMAL(10,2),
  method VARCHAR(20),
  payment_date DATE,
  FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);
CREATE TABLE staff (
  staff_id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT,
  name VARCHAR(100),
  role VARCHAR(50),
  phone VARCHAR(20),
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);
CREATE TABLE services (
  service_id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT,
  service_name VARCHAR(100),
  price DECIMAL(10,2),
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);
CREATE TABLE booking_services (
  id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT,
  service_id INT,
  quantity INT,
  total_price DECIMAL(10,2),
  FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
  FOREIGN KEY (service_id) REFERENCES services(service_id)
);
CREATE TABLE amenities (
  amenity_id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT,
  name VARCHAR(100),
  is_free BOOLEAN,
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);
CREATE TABLE room_amenities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  room_id INT,
  amenity_id INT,
  FOREIGN KEY (room_id) REFERENCES rooms(room_id),
  FOREIGN KEY (amenity_id) REFERENCES amenities(amenity_id)
);
CREATE TABLE reviews (
  review_id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT,
  rating INT,
  comment VARCHAR(255),
  FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);
-- 1. Insert into Hotels
INSERT INTO hotels (name, address, phone)
VALUES
('Hotel Sunshine', 'MG Road, Delhi', '9876543210'),
('Ocean View Resort', 'Juhu Beach, Mumbai', '9988776655');
-- 2. Insert into Room Types
INSERT INTO room_types (hotel_id, type_name, price, capacity)
VALUES
(1, 'Single', 1500.00, 1),
(1, 'Double', 2500.00, 2),
(2, 'Deluxe', 4000.00, 3),
(2, 'Suite', 6000.00, 4);
-- 3. Insert into Rooms
INSERT INTO rooms (hotel_id, room_type_id, room_number, status)
VALUES
(1, 1, '101', 'available'),
(1, 2, '102', 'occupied'),
(2, 3, '201', 'available'),
(2, 4, '202', 'maintenance');
-- 4. Insert into Guests
INSERT INTO guests (first_name, last_name, phone, email)
VALUES
('Aarav', 'Sharma', '9898989898', 'aarav@gmail.com'),
('Diya', 'Kapoor', '9871234567', 'diya@gmail.com'),
('Rohan', 'Verma', '9123456789', 'rohan@gmail.com');
-- 5. Insert into Bookings
INSERT INTO bookings (guest_id, room_id, check_in, check_out, status)
VALUES
(1, 1, '2025-11-10', '2025-11-12', 'booked'),
(2, 2, '2025-11-05', '2025-11-08', 'checked_out'),
(3, 3, '2025-11-07', '2025-11-09', 'checked_in');
-- 6. Insert into Payments
INSERT INTO payments (booking_id, amount, method, payment_date)
VALUES
(1, 3000.00, 'cash', '2025-11-09'),
(2, 7500.00, 'card', '2025-11-04'),
(3, 4000.00, 'upi', '2025-11-06');
-- 7. Insert into Staff
INSERT INTO staff (hotel_id, name, role, phone)
VALUES
(1, 'Ravi Kumar', 'Manager', '9812345678'),
(1, 'Simran Kaur', 'Receptionist', '9822334455'),
(2, 'Amit Singh', 'Housekeeping', '9876543211');
-- 8. Insert into Services
INSERT INTO services (hotel_id, service_name, price)
VALUES
(1, 'Laundry', 200.00),
(1, 'Room Service', 150.00),
(2, 'Spa', 1200.00),
(2, 'Airport Pickup', 800.00);
-- 9. Insert into Booking Services
INSERT INTO booking_services (booking_id, service_id, quantity, total_price)
VALUES
(1, 1, 2, 400.00),
(2, 2, 1, 150.00),
(3, 3, 1, 1200.00);
-- 10. Insert into Amenities
INSERT INTO amenities (hotel_id, name, is_free)
VALUES
(1, 'WiFi', TRUE),
(1, 'Parking', TRUE),
(2, 'Swimming Pool', FALSE),
(2, 'Gym', TRUE);
-- 11. Insert into Room Amenities
INSERT INTO room_amenities (room_id, amenity_id)
VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 3),
(4, 4);
-- 12. Insert into Reviews
INSERT INTO reviews (booking_id, rating, comment)
VALUES
(1, 5, 'Excellent stay and friendly staff!'),
(2, 4, 'Good experience, food can be better.'),
(3, 3, 'Average service, room was clean though.');

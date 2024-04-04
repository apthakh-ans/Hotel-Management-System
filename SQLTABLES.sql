CREATE DATABASE hotel_db;
USE hotel_db;

CREATE TABLE Guest (
  GuestID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100),
  Email VARCHAR(100),
  Phone VARCHAR(20)
);

CREATE TABLE Room (
  RoomID INT AUTO_INCREMENT PRIMARY KEY,
  RoomNumber VARCHAR(10),
  Type VARCHAR(50),
  Price DECIMAL(10,2),
  IsAvailable BOOLEAN
);

CREATE TABLE Booking (
  BookingID INT AUTO_INCREMENT PRIMARY KEY,
  GuestID INT,
  RoomID INT,
  CheckInDate DATE,
  CheckOutDate DATE,
  FOREIGN KEY (GuestID) REFERENCES Guest(GuestID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Payment (
  PaymentID INT AUTO_INCREMENT PRIMARY KEY,
  BookingID INT,
  Amount DECIMAL(10,2),
  Method VARCHAR(50),
  FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
);

CREATE TABLE Staff (
  StaffID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100),
  Role VARCHAR(50),
  Phone VARCHAR(20),
  Email VARCHAR(100)
);

CREATE TABLE ServiceRequest (
  RequestID INT AUTO_INCREMENT PRIMARY KEY,
  GuestID INT,
  RoomID INT,
  ServiceType VARCHAR(50),
  Status VARCHAR(20) DEFAULT 'Pending',
  RequestTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (GuestID) REFERENCES Guest(GuestID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE Amenity (
  AmenityID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100)
);

CREATE TABLE RoomAmenity (
  RoomID INT,
  AmenityID INT,
  PRIMARY KEY (RoomID, AmenityID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID),
  FOREIGN KEY (AmenityID) REFERENCES Amenity(AmenityID)
);

CREATE TABLE Review (
  ReviewID INT AUTO_INCREMENT PRIMARY KEY,
  GuestID INT,
  RoomID INT,
  Rating INT CHECK (Rating BETWEEN 1 AND 5),
  Comment TEXT,
  ReviewDate DATE,
  FOREIGN KEY (GuestID) REFERENCES Guest(GuestID),
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

CREATE TABLE TravelPackage (
  PackageID INT AUTO_INCREMENT PRIMARY KEY,
  Title VARCHAR(100),
  Description TEXT,
  Price DECIMAL(10,2),
  DurationDays INT
);

CREATE TABLE UserLogin (
  UserID INT AUTO_INCREMENT PRIMARY KEY,
  Username VARCHAR(50) UNIQUE,
  Password VARCHAR(255),  -- You can hash this later
  Role VARCHAR(20) DEFAULT 'Admin'
);

CREATE TABLE RoomMaintenance (
  MaintenanceID INT AUTO_INCREMENT PRIMARY KEY,
  RoomID INT,
  Issue TEXT,
  ReportedDate DATE,
  Status VARCHAR(20) DEFAULT 'Open',
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

INSERT INTO UserLogin (Username, Password, Role)
VALUES ('admin', 'admin123', 'Admin');



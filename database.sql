CREATE DATABASE airline_tickets;
USE airline_tickets;

-- Flights Table
CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    airline VARCHAR(50),
    airline_logo VARCHAR(255),
    flight_number VARCHAR(20),
    plane_number VARCHAR(50),
    tail_number VARCHAR(20),
    from_city VARCHAR(50),
    from_airport VARCHAR(100),
    from_terminal VARCHAR(5),
    to_city VARCHAR(50),
    to_airport VARCHAR(100),
    to_terminal VARCHAR(5),
    departure_time VARCHAR(10),
    arrival_time VARCHAR(10),
    travel_date DATE
);

-- Classes Table (with baggage allowance)
CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT,
    class_name VARCHAR(20),
    baggage_checkin VARCHAR(20),
    baggage_cabin VARCHAR(20),
    FOREIGN KEY(flight_id) REFERENCES flights(id)
);

-- Passengers Table
CREATE TABLE passengers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT,
    class_name VARCHAR(20),
    name VARCHAR(50),
    age INT,
    seat_no VARCHAR(5),
    eticket_no VARCHAR(20),
    FOREIGN KEY(flight_id) REFERENCES flights(id)
);

-- Insert 5 Emirates flights
INSERT INTO flights (airline, airline_logo, flight_number, plane_number, tail_number,
    from_city, from_airport, from_terminal, to_city, to_airport, to_terminal,
    departure_time, arrival_time, travel_date)
VALUES
('Emirates', 'logos/emirates.png', 'EK 511', 'Airbus A380-800', 'A6-EUE',
 'New Delhi', 'Indira Gandhi International', '3', 'Dubai', 'Dubai International', '3',
 '04:30', '06:30', '2025-07-23'),

('Emirates', 'logos/emirates.png', 'EK 503', 'Boeing 777-300ER', 'A6-ENX',
 'Mumbai', 'Chhatrapati Shivaji Maharaj', '2', 'Dubai', 'Dubai International', '3',
 '02:45', '04:45', '2025-07-25'),

('Emirates', 'logos/emirates.png', 'EK 567', 'Boeing 777-300ER', 'A6-ENY',
 'Bengaluru', 'Kempegowda International', '1', 'Dubai', 'Dubai International', '3',
 '10:30', '12:30', '2025-07-28'),

('Emirates', 'logos/emirates.png', 'EK 545', 'Boeing 777-300ER', 'A6-ENZ',
 'Chennai', 'Chennai International', '2', 'Dubai', 'Dubai International', '3',
 '08:00', '10:00', '2025-07-29'),

('Emirates', 'logos/emirates.png', 'EK 531', 'Boeing 777-300ER', 'A6-EOA',
 'Kochi', 'Cochin International', '3', 'Dubai', 'Dubai International', '3',
 '14:00', '16:00', '2025-08-01');

-- Add class data with baggage allowance for each flight
INSERT INTO classes (flight_id, class_name, baggage_checkin, baggage_cabin) VALUES
(1, 'Economy', '30 Kg', '7 Kg'), (1, 'Business', '40 Kg', '10 Kg'), (1, 'First', '50 Kg', '12 Kg'),
(2, 'Economy', '30 Kg', '7 Kg'), (2, 'Business', '40 Kg', '10 Kg'), (2, 'First', '50 Kg', '12 Kg'),
(3, 'Economy', '30 Kg', '7 Kg'), (3, 'Business', '40 Kg', '10 Kg'), (3, 'First', '50 Kg', '12 Kg'),
(4, 'Economy', '30 Kg', '7 Kg'), (4, 'Business', '40 Kg', '10 Kg'), (4, 'First', '50 Kg', '12 Kg'),
(5, 'Economy', '30 Kg', '7 Kg'), (5, 'Business', '40 Kg', '10 Kg'), (5, 'First', '50 Kg', '12 Kg');
-- Add 5 more Emirates flights (European Routes)
INSERT INTO flights (airline, airline_logo, flight_number, plane_number, tail_number,
    from_city, from_airport, from_terminal, to_city, to_airport, to_terminal,
    departure_time, arrival_time, travel_date)
VALUES
('Emirates', 'logos/emirates.png', 'EK 701', 'Airbus A380-800', 'A6-EOX',
 'New Delhi', 'Indira Gandhi International', '3', 'London', 'Heathrow Airport', '4',
 '02:30', '07:30', '2025-08-12'),

('Emirates', 'logos/emirates.png', 'EK 715', 'Boeing 777-300ER', 'A6-EOY',
 'Mumbai', 'Chhatrapati Shivaji Maharaj', '2', 'Paris', 'Charles de Gaulle Airport', '2',
 '03:15', '08:15', '2025-08-14'),

('Emirates', 'logos/emirates.png', 'EK 729', 'Boeing 777-300ER', 'A6-EOZ',
 'Bengaluru', 'Kempegowda International', '1', 'Frankfurt', 'Frankfurt Airport', '1',
 '01:45', '07:00', '2025-08-16'),

('Emirates', 'logos/emirates.png', 'EK 741', 'Airbus A380-800', 'A6-EUA',
 'Hyderabad', 'Rajiv Gandhi International', '3', 'Zurich', 'Zurich Airport', 'E',
 '04:00', '08:30', '2025-08-18'),

('Emirates', 'logos/emirates.png', 'EK 755', 'Boeing 777-300ER', 'A6-EUB',
 'Chennai', 'Chennai International', '2', 'Rome', 'Leonardo da Vinci International', '3',
 '05:10', '09:30', '2025-08-20');

-- Add class data for these 5 new flights
INSERT INTO classes (flight_id, class_name, baggage_checkin, baggage_cabin) VALUES
(11, 'Economy', '30 Kg', '7 Kg'), (11, 'Business', '40 Kg', '10 Kg'), (11, 'First', '50 Kg', '12 Kg'),
(12, 'Economy', '30 Kg', '7 Kg'), (12, 'Business', '40 Kg', '10 Kg'), (12, 'First', '50 Kg', '12 Kg'),
(13, 'Economy', '30 Kg', '7 Kg'), (13, 'Business', '40 Kg', '10 Kg'), (13, 'First', '50 Kg', '12 Kg'),
(14, 'Economy', '30 Kg', '7 Kg'), (14, 'Business', '40 Kg', '10 Kg'), (14, 'First', '50 Kg', '12 Kg'),
(15, 'Economy', '30 Kg', '7 Kg'), (15, 'Business', '40 Kg', '10 Kg'), (15, 'First', '50 Kg', '12 Kg');

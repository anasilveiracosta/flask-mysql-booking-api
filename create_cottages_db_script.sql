-- Creating the database and populating it with our table information.
CREATE DATABASE cottages;
USE cottages;
-- ----------------------------------------------------------------------------
CREATE TABLE `cottages_bookings` (
  `cottage_name` varchar(45) DEFAULT NULL,
  `booking_id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `booking_date` date NOT NULL,
  `availability` varchar(45) DEFAULT NULL
);

-- ----------------------------------------------------------------------------
-- Store procedure to insert table info
-- Exemple of how to use it:
-- CALL filldates('2026-06-01', '2026-06-30', 'Sunrise', 'available');
-- CALL filldates('2026-06-01', '2026-06-30', 'Rainbow', 'available');

DELIMITER $$
CREATE PROCEDURE `filldates`(
	in dateStart DATE,
    in dateEnd DATE,
    in cottage_name VARCHAR(45),
    in availability varchar(45)
)
BEGIN
  WHILE dateStart <= dateEnd DO
    INSERT INTO cottages_bookings (cottage_name, booking_date, availability)
    VALUES (cottage_name, dateStart, availability);
    SET dateStart = date_add(dateStart, INTERVAL 1 DAY);
  END WHILE;
END$$
DELIMITER ;


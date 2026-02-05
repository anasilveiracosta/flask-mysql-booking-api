# Flask & Mysql Booking Api

This project is part of the Data Science & Machine Learning/AI course by Code First Girls.
Assignment 03 – Cottage Lodge Booking API

## CREATIVE SCENARIO: Cottage Lodge Booking API

The Cottage Lodge Booking API demonstrates a simple example of how booking systems work, integrating Python, Flask, and MySQL to manage reservations dynamically.

This project simulates a small lodge with two holiday cottages available for rent.

It was built using Python with Flask to create a simple API that connects to a MySQL database, which stores the availability for June 2026, including which cottage is free or booked on each date.

#### The API allows users to:

- Check availability: View the booking status (available or unavailable) for each cottage within a selected date range.
- Flask API endpoints: Includes endpoints for GET (checking availability) and POST (booking).
- Book by date range: The booking is made for the entire period between start_date and end_date.
- Data persistence: Availability status is updated directly in the MySQL database using an UPDATE statement.

The main goal is to demonstrate how a simple API can manage real-world booking data and interact dynamically with a SQL database.
Users can check cottage availability for a given period and make a booking that updates the status directly in the database.

## SETUP AND INSTALLATION
### Requirements

- Python 3 (with Flask installed)
- MySQL
- Database credentials saved in the cottages_config.py file (HOST, USER,PASSWORD, DATABASE)

### Database Setup

To create the database used in this project, run the SQL script create_cottages_db_script.sql.
This file contains instructions to:

- Create the database named cottages
- Create the stored procedure "filldates" to populate the table with all days in June 2026 and their default availability for each cottage

#### Table Structure:

```
CREATE TABLE cottages_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cottage_name VARCHAR(100) NOT NULL,
    booking_date DATE NOT NULL,
    availability VARCHAR(45) DEFAULT 'available'
    -- Values: 'available' or 'unavailable'
);
```
#### Example of populating the table:
```
CALL filldates('2026-06-01', '2026-06-30', 'Sunrise', 'available');
CALL filldates('2026-06-01', '2026-06-30', 'Rainbow', 'available');
```

After running the procedure, your database structure will include:
- Database: cottages
- Table: cottages_bookings
- Columns: id, cottage_name, booking_date, availability

## API ENDPOINTS
Three routes were created: two GET and one POST:
 ### 1) GET: /availability/<date>

Returns the availability of all cottages for a single date.
Example:
```
http://127.0.0.1:5000/availability/2026-06-16
```
 ### 2) GET: /availability_range/<start_date>/<end_date>

Returns the availability of all cottages within the specified date range.
Example:
```
http://127.0.0.1:5000/availability_range/2026-06-18/2026-06-22
```
 ### 3) POST: /book_cottage

Books a cottage for the selected date range and updates the database.
Example request Json body:
```
{
  "cottage_name": "Sunrise",
  "start_date": "2026-06-18",
  "end_date": "2026-06-22"
}
```
## PYTHON FILE STRUCTURE AND DESCRIPTION
The project is organized into four main files, following separation of concerns (configuration, database logic, API, and client side).
 ### 1) cottages_config.py
Contains the database configuration variables for the MySQL connection. You should use your own MySQL information in this file:

- HOST: MySQL server (e.g. "localhost")
- USEER: your own username (e.g. "root")
- PASSWORD: your own password
- DATABASE: database name (e.g. "cottages")

 ### 2) cottages_db_utils.py

Handles all functions responsible for direct queries interaction with the MySQL database.

- def connect_to_db( ): Establishes and returns a connection to MySQL using cottages_config.
- def get_all_booking_availability(_date): Fetches availability for all cottages on a single date. (Referenced in cottages_app.py) 
- def get_date_range_booking_availability(start_date, end_date): Executes a SELECT with BETWEEN to get availability for all cottages within a date range. (Referenced in cottages_app.py) 
- def book_cottage_in_db(name, start_date, end_date): Executes an UPDATE to set availability = 'unavailable' for the chosen cottage and period, returning success status and affected row count. (Referenced in cottages_app.py) 

 ### 3) cottages_app.py

Handles the Flask API server to define routes and logic for client interaction.

- #### /availability_range/<start>/<end> (GET):
 Gets info from the function get_date_range_booking_availability(start_date, end_date) from cottages_db_utils.py file, and returns availability for all cottages in the given range.

- #### /availability/<date> (GET):
Gets info from the function get_all_booking_availability(_date) from cottages_db_utils.py file, and returns availability for all cottages on a specific date.

- #### /book_cottage (POST):
Gets booking details from the function book_cottage_in_db(cottage_name, start_date, end_date) from the cottages_db_utils.py file, updates MySQL, and returns a success or error response.

- ####  if __ name __ == '__ main __':
 Runs the Flask server in debug mode.

 ### 4) cottages_main.py
Contains the client-side script that interacts with the API via terminal input.

- #### def get_your_availability_by_date(date): 
Sends a GET request to the API route (/availability/<date>) and displays availability.

- #### def get_your_availability_by_date_range(start_date, end_date): 
Sends a GET request to the API route (/availability_range/<start>/<end>) and displays availability.

- #### def  book_your_cottage(): 
Gets info from user input and POST request to the API (/book_cottage) with booking details.

- #### def run(): 
Guides the user, asks for input, shows availability, and handles booking interaction with functions from the cottages_main.py file to update the SQL database file.

## User input interaction exemple:
```
------------------------------
Hello, welcome to our Cottages Page
------------------------------

When would you like to check-in our Cottages? (YYYY-MM-DD): 2026-06-01
When would you like to check-out our Cottages? (YYYY-MM-DD): 2026-06-02

####### AVAILABILITY: #######

Availability from 2026-06-01 to 2026-06-02:
---------------------------------------
Cottage: Sunrise
Date: 2026-06-01 -> STATUS: Available
Cottage: Sunrise
Date: 2026-06-02 -> STATUS: Available
Cottage: Rainbow
Date: 2026-06-01 -> STATUS: Available
Cottage: Rainbow
Date: 2026-06-02 -> STATUS: Available
---------------------------------------

 Would you like to book ? (y/n): y

--- Book Cottage ---
Type the name of the cottage you want to book (Sunrise or Rainbow): Sunrise
Enter the check-in date (YYYY-MM-DD): 2026-06-01
Enter the check-out date (YYYY-MM-DD): 2026-06-02

===== Booking Status =====
Status: SUCCESS
Message: Total of 2 booked days updated for cottage Sunrise.
=============================

Thank you!

```

- #### def if __ name __ == '__ main __': 
Ensures the def run() function executes when the script starts.



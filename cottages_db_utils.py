import mysql.connector
from cottages_config import USER, PASSWORD, HOST, DATABASE

#01)  Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=DATABASE
    )
        print("Database connected")
        return connection
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        return None
#################################################################################################################

#02)  Function get availability by single date
def get_all_booking_availability(_date):
    try:
        db_name = "cottages"
        db_connection = connect_to_db()
        cursor = db_connection.cursor()

        query = """SELECT cottage_name, booking_date, availability
            FROM cottages_bookings
            WHERE booking_date = '{}'
            """.format(_date)

        cursor.execute(query)
        results = cursor.fetchall()

        # To format the dates and crate a tuples output
        formatted_availability_output = []
        for result in results:
            cottage_name, booking_date, availability = result
            formatted_availability_output.append((cottage_name, booking_date.strftime('%Y-%m-%d'),availability))

        cursor.close()
        return formatted_availability_output

    except Exception:
        print(f"Error reading data from database: {e}")
        raise DbConnectionError("Failed to read DB data")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

#################################################################################################################

# 03) Function get availability by date range
def get_date_range_booking_availability(start_date, end_date):

    try:
        db_name = "cottages"
        db_connection = connect_to_db()
        cursor = db_connection.cursor()

        query = """SELECT cottage_name, booking_date, availability
            FROM cottages_bookings
            WHERE booking_date BETWEEN %s AND %s
            """

        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()

        # To format the dates and crate a tuples output
        formatted_range_availability_output = []
        for result in results:
            cottage_name, booking_date, availability = result
            formatted_range_availability_output.append((cottage_name, booking_date.strftime('%Y-%m-%d'),availability))

        cursor.close()
        # print(formatted_range_availability_output)
        return formatted_range_availability_output

    except Exception as e:
        print(f"Error reading data from database: {e}")
        raise DbConnectionError("Failed to read DB data")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")
#################################################################################################################

# 04) Function to Update the availability of a specific cottage booked
def book_cottage_in_db(cottage_name: str, start_date: str, end_date: str):
    try:
        db_name = "cottages"
        db_connection = connect_to_db()
        cursor = db_connection.cursor()

        query = """UPDATE cottages_bookings
            SET availability = 'unavailable'
            WHERE cottage_name = %s AND booking_date BETWEEN %s AND %s
            """

        cursor.execute(query, (cottage_name, start_date, end_date))
        db_connection.commit()

        # rowcount to check how many dates has been updated
        if cursor.rowcount == 0:
            return False, "No bookings available"
        return True, f"Total of {cursor.rowcount} booked days updated for cottage {cottage_name}."

    except Exception as e:
        print(f"Error reading data from database: {e}")
        raise DbConnectionError("Failed to read DB data")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")



if __name__ == '__main__':
    get_date_range_booking_availability('2026-06-18', '2026-06-22')
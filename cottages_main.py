import requests
import json

# 01) Function to get availability by a specif date calling API rout
def get_availability_by_date(date):
    result = requests.get(
        'http://127.0.0.1:5000/availability/{}'.format(date)
    )
    return result.json()

#################################################################################################################

# 02) Function to get availability by a range date calling API rout
def get_your_availability_by_date_range(start_date, end_date):
    url = f'http://127.0.0.1:5000/availability_range/{start_date}/{end_date}'
    result = requests.get(url)
    return result.json()

#################################################################################################################

# 03) Function to book cottage
def book_your_cottage(cottage_name: str, start_date: str, end_date: str):
    url = f'http://127.0.0.1:5000/book_cottage'
    booking_info = {
        "cottage_name": cottage_name,
        "start_date": start_date,
        "end_date": end_date
    }
    try:
        response = requests.post(url, json=booking_info)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"Error {e}")

#################################################################################################################

# 04) Function to get user input and check availability by date range
def run():
    print('------------------------------')
    print('Hello, welcome to our Cottages Page')
    print('------------------------------')
    print()
    start_date = input('When would you like to check-in our Cottages? (YYYY-MM-DD): ')
    end_date = input('When would you like to check-out our Cottages? (YYYY-MM-DD): ')
    print()
    print('####### AVAILABILITY: #######')
    print()

    availability_info = get_your_availability_by_date_range(start_date, end_date)
    # get the results from Json list
    results = availability_info.get('results', [])

    # to print organized
    if results:
        print(f"Availability from {start_date} to {end_date}:")
        print("---------------------------------------")

        for item in results:
            cottage_name, booking_date, available = item
            if available.lower() == "available":
                status = 'Available'
            else:
                status = "Booked"

            print(f"Cottage: {cottage_name}")
            print(f"Date: {booking_date} -> STATUS: {status}")

        print("---------------------------------------")
    else:
        print("No availability during this period")


    if input("\n Would you like to book ? (y/n): ").lower() == 'y':
        print("\n--- Book Cottage ---")

        cottage_to_book = input("Type the name of the cottage you want to book (Sunrise or Rainbow): ")
        start_date_to_book = input("Enter the check-in date (YYYY-MM-DD): ")
        end_date_to_book = input("Enter the check-out date (YYYY-MM-DD): ")

        booking_result = book_your_cottage(
            cottage_to_book,
            start_date_to_book,
            end_date_to_book
        )

        print("\n===== Booking Status =====")
        print(f"Status: {booking_result.get('status', 'ERROR').upper()}")
        print(f"Message: {booking_result.get('message', 'Invalid response from API')}")
        print("=============================")

    print()
    print('Thank you!')

#################################################################################################################

if __name__ == '__main__':
    run()
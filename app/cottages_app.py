from flask import Flask, jsonify, request
from db.cottages_db_utils import get_all_booking_availability, get_date_range_booking_availability, book_cottage_in_db


app = Flask(__name__)

# http://127.0.0.1:5000/ Home Page rout
@app.route('/', methods=['GET'])
def home_page():
    """Retruns a welcome message and Ok status"""
    return jsonify({
        "status": "API is running",
        "message": "Welcome to the Cottages Booking API!",
        "endpoints": {
            "GET /availability/<date>": "List all available cottages by a specific date (YYYY-MM-DD)",
            "GET /availability_range/<start>/<end>": "Returns availability for all cottages in the given range",
            "POST /book_cottage": "Receives booking details (cottage name, start_date, end_date), updates MySQL."
        }
    })

#################################################################################################################

# http://127.0.0.1:5000/availability/2026-06-16 Rout page to check availability by single date
@app.route('/availability/<date>', methods=['GET'])
def get_availability(date):
    # Get the data from get_all_booking_availability function from cottages_db_utils
    availability = get_all_booking_availability(date)
    return jsonify(availability)

#################################################################################################################

# Rout 02 = http://127.0.0.1:5000/availability_range/2026-06-18/2026-06-22 (Rout page to check availability by date range)
@app.route('/availability_range/<start_date>/<end_date>', methods=['GET'])
def get_availability_by_range(start_date, end_date):
    # Get the data from get_date_range_booking_availability function from cottages_db_utils
    availability_range = get_date_range_booking_availability(start_date, end_date)
    response_data = {
        "start_date": start_date,
        "end_date": end_date,
        "results": availability_range
    }
    return jsonify(response_data)

#################################################################################################################

# Rout 03 = http://127.0.0.1:5000/availability_range/2026-06-18/2026-06-22 (Rout page to check availability by date range)
@app.route('/book_cottage', methods=['POST'])
def book_cottage_route():
    data = request.get_json()
    if (not data or 'cottage_name' not in data or
     'start_date' not in data or 'end_date' not in data):
        return jsonify({
            "error": "Incomplete info",
        }), 400

    cottage_name = data['cottage_name']
    start_date = data['start_date']
    end_date = data['end_date']

    # Get the data from book_cottage_in_db function from cottages_db_utils
    success, message = book_cottage_in_db(cottage_name, start_date, end_date)

    if success:
        return jsonify({
            "status": "success",
            "message": message,
            "booked_cottage": cottage_name,
            "booked_period": f"from {start_date} to {end_date}"
        }), 201
    else:
        status_code = 409 if "found" in message else 500
        return jsonify({
            "status": "error",
            "message": message
        }), status_code

#################################################################################################################

if __name__ == '__main__':

    app.run(debug=True)

from flask import Blueprint, jsonify, request
from config.jwt_auth import token_required
from controllers.bookings import (
    get_bookings_controller,
    update_booking_controller,
    create_booking_controller,
    generate_booking_vacancy_controller,
    get_bookings_available_dates_controller,
    get_bookings_available_times_controller,
    cancel_booking_controller
)

bookings_bp = Blueprint('booking', __name__, url_prefix='/booking')

@bookings_bp.route('/query/<id_user>', methods=['GET'])
@token_required
def get_bookings(current_user, id_user):
    response, status_code = get_bookings_controller(current_user, id_user)
    return jsonify(response), status_code

@bookings_bp.route('/update/<id_user>', methods=['PUT'])
@token_required
def update_booking_route(current_user, id_user):
    data = request.json

    booking_id = data.get('bookingId')
    status = data.get('status')

    updated_booking, status_code = update_booking_controller(current_user, id_user, booking_id, status)

    return jsonify(updated_booking), status_code

@bookings_bp.route('/insert/<id_user>', methods=['POST'])
@token_required
def create_booking_route(current_user, id_user):
    data = request.json

    service_id = data.get('serviceId')
    id_booking = data.get('bookingId')
    nr_price = data.get('nrPrice')

    booking, status_code = create_booking_controller(current_user, id_user, service_id, nr_price, id_booking)

    return jsonify(booking), status_code

@bookings_bp.route('/generate', methods=['POST'])
def generate_booking_vacancy_route():
    result, status_code = generate_booking_vacancy_controller()
    return jsonify(result), status_code

@bookings_bp.route('/query-dates/<id_barber>', methods=['GET'])
@token_required
def get_bookings_dates_route(current_user, id_barber):
    response, status_code = get_bookings_available_dates_controller(id_barber)
    return jsonify(response), status_code

@bookings_bp.route('/query-times/<date>/<id_barber>', methods=['GET'])
@token_required
def get_bookings_times_route(current_user, date, id_barber):
    response, status_code = get_bookings_available_times_controller(date, id_barber)
    return jsonify(response), status_code

@bookings_bp.route('/cancel/<id_user>', methods=['PUT'])
@token_required
def cancel_booking_route(current_user, id_user):
    data = request.json

    booking_id = data.get('bookingId')

    response, status_code = cancel_booking_controller(current_user, id_user, booking_id)

    return jsonify(response), status_code
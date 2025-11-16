from flask import Blueprint, jsonify, request
from config.jwt_auth import token_required
from controllers.bookings import (
    get_bookings_controller,
    update_booking_controller,
    create_booking_controller,
    generate_booking_vacancy_controller
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

    date = data.get('date')
    time = data.get('time')
    service_id = data.get('serviceId')
    barber_id = data.get('barberId')
    payment_type = data.get('paymentType')
    nr_price = data.get('nrPrice')

    booking, status_code = create_booking_controller(current_user, id_user, date, time, service_id, barber_id, payment_type, nr_price)

    return jsonify(booking), status_code

@bookings_bp.route('/generate', methods=['POST'])
def generate_bookin_vacancy_route():
    result, status_code = generate_booking_vacancy_controller()
    return jsonify(result), status_code
from flask import Blueprint, jsonify, request
from controllers.service import get_service_controller

service_bp = Blueprint('service', __name__, url_prefix='/service')

@service_bp.route('/query', methods=['GET'])
def get_bookings():
    response, status_code = get_service_controller()
    return jsonify(response), status_code

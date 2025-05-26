from flask import Blueprint, jsonify, request
from controllers.barber import get_barber_controller
from config.jwt_auth import token_required

barber_bp = Blueprint('barber', __name__, url_prefix='/barber')

@barber_bp.route('/list', methods=['GET'])
@token_required
def get_barber(current_user):
    response, status_code = get_barber_controller(current_user)
    return jsonify(response), status_code
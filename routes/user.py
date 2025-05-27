from flask import Blueprint, jsonify
from controllers.user import get_user_controller, update_user_controller
from config.jwt_auth import token_required

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/query/<id_user>', methods=['GET'])
@token_required
def get_bookings(current_user, id_user):
    response, status_code = get_user_controller(current_user, id_user)
    return jsonify(response), status_code

@user_bp.route('/update/<id_user>', methods=['PUT'])
@token_required
def update_user_route(current_user, id_user):
    return update_user_controller(current_user, id_user)
from flask import Blueprint, request, jsonify, render_template_string
from static.html_template import html_template

from controllers.auth import (
    login_controller,
    register_controller,
    validate_token_controller,
    get_user_by_activation_token_controller,
    activate_account_controller,
    request_password_reset_controller,
    reset_password_controller
)

activation_bp = Blueprint('activation', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    senha = data.get('password')

    response, status_code = login_controller(email, senha)
    return jsonify(response), status_code

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    senha = data.get('password')

    response, status_code = register_controller(email, senha)
    return jsonify(response), status_code

@auth_bp.route('/validate-token', methods=['GET'])
def validate_token():
    token = None

    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]


    response, status_code = validate_token_controller(token)
    return jsonify(response), status_code

@activation_bp.route('/activate/<activation_token>', methods=['GET'])
def activate_account(activation_token):
    try:
        user, status_code = get_user_by_activation_token_controller(activation_token)

        if status_code == 404 or status_code == 400:
            return render_template_string(html_template(
                "Invalid or expired token!",
                "The activation link is invalid or has already been used.",
                "error"
            ))

        activate_account_controller(user['id_user'])

        return render_template_string(html_template(
            "Account activated successfully!",
            "Your account has been activated. You can now use our services.",
            "success"
        ))

    except Exception as e:
        return render_template_string(html_template(
            "An error occurred!",
            str(e),
            "error"
        ))

@auth_bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()

    email = data.get('email')

    response, status_code = request_password_reset_controller(email)
    return jsonify(response), status_code

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json(token)
    new_password = data.get('newPassword')

    response, status_code = reset_password_controller(token, new_password)
    return jsonify(response), status_code
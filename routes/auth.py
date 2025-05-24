from flask import Blueprint, request, jsonify
from controllers.auth import login_controller, register_controller, validate_token_controller

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rota de autenticação
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    senha = data.get('password')

    response, status_code = login_controller(email, senha)
    return jsonify(response), status_code

# Endpoint para cadastro de usuário
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    senha = data.get('password')

    response, status_code = register_controller(email, senha)
    return jsonify(response), status_code

# 🔑 Endpoint para validar o token
@auth_bp.route('/validate-token', methods=['GET'])
def validate_token():
    response, status_code = validate_token_controller()
    return jsonify(response), status_code
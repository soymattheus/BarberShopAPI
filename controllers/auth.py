from flask import request
import bcrypt
import datetime
import jwt
import uuid
from models.auth import fetch_user_auth, insert_user_auth
from config.jwt_auth import SECRET_KEY

def login_controller(emial, senha):
    try:
        user = fetch_user_auth(emial)

        if user:
            user_id, name, email, password, birth_date, phone, created_at, updated_at, loyalty_package, avaliable_services_number, fl_status = user

            if fl_status == 'A':
                if bcrypt.checkpw(senha.encode('utf-8'), password.encode('utf-8')):
                    # ✅ Gerar o token JWT
                    payload = {
                        'user_id': str(user_id),
                        'email': email,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Expira em 1 hora
                    }

                    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

                    return {
                        'message': 'Login bem-sucedido',
                        'token': token,
                        'user': {
                            'id': user_id,
                            'name': name,
                            'email': email,
                            'birthDate': birth_date,
                            'phone': phone,
                            'createdAt': created_at,
                            'updatedAt': updated_at,
                            'loyaltyPackage': loyalty_package,
                            'avaliableServicesNumber': avaliable_services_number,
                            'flStatus': fl_status
                        }
                    }, 200
                else:
                    return {'error': 'Senha incorreta'}, 401
            else:
                return {'error': 'Usuário inativo'}, 401
        else:
            return {'error': 'Usuário não encontrado'}, 404

    except Exception as e:
        return {'error': str(e)}, 500

def register_controller(email, senha):
    try:
        existing_user = fetch_user_auth(email)

        if existing_user:
            return {'error': 'Email já cadastrado'}, 409

        # Gerar hash da senha
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Gerar uuid
        user_id = str(uuid.uuid4())

        inserted_id = insert_user_auth(user_id, email, hashed_password)

        return {
            'message': 'Usuário cadastrado com sucesso',
            'user': {
                'id': inserted_id,
                'email': email
            }
        }, 201

    except Exception as e:
        return {'error': str(e)}, 500

def validate_token_controller():
    token = None

    # Captura o token do header Authorization
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

    if not token:
        return {'error': 'Token não fornecido'}, 401

    try:
        # Decodifica o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        return {
            'message': 'Token válido',
            'user': {
                'user_id': payload['user_id'],
                'email': payload['email']
            }
        }, 200

    except jwt.ExpiredSignatureError:
        return {'error': 'Token expirado'}, 401

    except jwt.InvalidTokenError:
        return {'error': 'Token inválido'}, 401
from dotenv import load_dotenv
import os
import bcrypt
from datetime import datetime, timedelta
import jwt
import uuid
import pytz
from config.jwt_auth import SECRET_KEY
from utils.email_service import send_email
from utils.send_password_reset_email import send_password_reset_email

from utils.send_email import (
    send_activation_email,
    send_resend_activation_email,
    send_completed_activation_email,
    send_password_updated_email
)

from models.auth import (
    fetch_user_auth,
    insert_user_auth,
    fetch_user_by_activation_token,
    activate_user,
    fetch_user_by_email,
    set_password_reset_token,
    get_user_by_reset_token,
    update_user_password
)

# Define Brasilia timezone
tz = pytz.timezone('America/Sao_Paulo')
load_dotenv()

def login_controller(emial, password):
    try:
        user = fetch_user_auth(emial)

        if user:
            if user[10] == 'A':
                if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):

                    payload = {
                        'user_id': str(user[0]),
                        'email': user[2],
                        'exp': datetime.utcnow() + timedelta(hours=24)
                    }

                    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

                    return {
                        'message': 'Logged in successfully',
                        'token': token,
                        'user': {
                            'id': user[0],
                            'name': user[1],
                            'email': user[2],
                            'birthDate': user[4],
                            'phone': user[5],
                            'createdAt': user[6],
                            'updatedAt': user[7],
                            'loyaltyPackage': user[8],
                            'avaliableServicesNumber': user[9],
                            'status': user[10]
                        }
                    }, 200
                else:
                    return {'error': 'Incorrect password'}, 401
            else:
                return {'error': 'Inactive user'}, 401
        else:
            return {'error': 'User not found'}, 404

    except Exception as e:
        return {'error': str(e)}, 500

def register_controller(email, password):
    try:
        existing_user = fetch_user_auth(email)

        if existing_user:
            if existing_user[11] != None:
                api_base_url = os.getenv('API_URL')
                # api_base_url = http://127.0.0.1:5000

                activation_link = f"{api_base_url}/activate/{existing_user[11]}"

                send_resend_activation_email(email, activation_link)

            return {'error': 'Email already registered'}, 409

        if len(password) < 8:
            return {"message": "Password must be at least 8 characters long"}, 400
        if not any(char.isdigit() for char in password):
            return {"message": "Password must contain at least one numeric digit"}, 400
        if not any(char.isupper() for char in password):
            return {"message": "Password must contain at least one uppercase letter"}, 400
        if not any(char.islower() for char in password):
            return {"message": "Password must contain at least one lowercase letter"}, 400
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password):
            return {"message": "Password must contain at least one special character"}, 400

        # Generate password hash
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Generate uuid
        user_id = str(uuid.uuid4())

        # Generate activation token
        activation_token = str(uuid.uuid4())

        inserted_id = insert_user_auth(user_id, email, hashed_password, activation_token)

        api_base_url = os.getenv('API_URL')
        # api_base_url = 'http://127.0.0.1:5000/activate'

        # Activation link
        activation_link = f"{api_base_url}/activate/{activation_token}"

        send_activation_email(email, activation_link)

        return {
            'message': 'Usuário cadastrado com sucesso',
            'user': {
                'id': inserted_id,
                'email': email
            }
        }, 201

    except Exception as e:
        return {'error': str(e)}, 500

def validate_token_controller(token):
    if not token:
        return {'error': 'Token not provided'}, 401

    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        return {
            'message': 'Valid token',
            'user': {
                'userId': payload['user_id'],
                'email': payload['email']
            }
        }, 200

    except jwt.ExpiredSignatureError:
        return {'error': 'Expired token'}, 401

    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}, 401

def get_user_by_activation_token_controller(activation_token):
    try:
        if not activation_token:
            return {'message': 'Token not provided'}, 400

        user = fetch_user_by_activation_token(activation_token)

        if not user:
            return {'message': 'Invalid or expired token'}, 404

        return {
            'userId': user[0],
            'status': user[1],
            'activationToken': user[2]
        }, 200

    except Exception as e:
        print(f"Token error: {e}")
        return {'message': f'Erro: {str(e)}'}, 500

def activate_account_controller(user_id):
    try:
        if not user_id:
            return {'message': 'User ID not provided'}, 400

        response = activate_user(user_id)

        send_completed_activation_email(response[0])

        return {'message': 'Account activated successfully'}, 200

    except Exception as e:
        return {'message': f'Error activating account: {str(e)}'}, 500

def request_password_reset_controller(email):
    try:
        user = fetch_user_by_email(email)
        if not user:
            return {"message": "User not found"}, 404

        reset_token = str(uuid.uuid4())

        # Current date and time in Brasilia timezone
        now = datetime.now(tz)

        # Expiration date (1 hour ahead)
        expiration = now + timedelta(hours=1)

        set_password_reset_token(user[0], reset_token, expiration)

        #front_base_url = os.getenv('FRONT_URL')
        front_base_url = 'http://localhost:3000'

        reset_link = f"{front_base_url}/passwordReset/{reset_token}"

        send_password_reset_email(email, reset_link)

        return {
            "message": "Password reset email sent successfully"
        }, 200

    except Exception as e:
        print(f"Request reset password error: {e}")
        return {'message': f'Request reset password error: {str(e)}'}, 500

def reset_password_controller(token, new_password):
    if not new_password:
        return {"message": "New password is required"}, 400

    user = get_user_by_reset_token(token)
    if not user:
        return {"message": "Invalid or expired token"}, 400
    
    if len(new_password) < 8:
        return {"message": "Password must be at least 8 characters long"}, 400
    if not any(char.isdigit() for char in new_password):
        return {"message": "Password must contain at least one numeric digit"}, 400
    if not any(char.isupper() for char in new_password):
        return {"message": "Password must contain at least one uppercase letter"}, 400
    if not any(char.islower() for char in new_password):
        return {"message": "Password must contain at least one lowercase letter"}, 400
    if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in new_password):
        return {"message": "Password must contain at least one special character"}, 400

    # Use bcrypt to hash the new password
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    response = update_user_password(user[0], hashed_password)

    send_password_updated_email(response[0])

    return {"message": "Password reset successfully"}, 200
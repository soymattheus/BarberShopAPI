from flask import Blueprint, jsonify, request
from config.jwt_auth import token_required
from dotenv import load_dotenv
import mercadopago
import os

mercado_pago_bp = Blueprint('mercado-pago', __name__, url_prefix='/mercado-pago')
load_dotenv()
sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_ACCESS_TOKEN"))

@mercado_pago_bp.route('/order/<id_user>', methods=['POST'])
@token_required
def cancel_booking_route(current_user, id_user):
    if id_user != current_user['user_id']:
        return {'error': 'Unauthorized access'}, 403

    data = request.json

    try:
        # Mercado Pago
        # Cria um item na preferência
        preference_data = {
            "items": data,
            "back_urls": {
                "success": "https://barbershop-ten-wheat.vercel.app/success",
                "failure": "https://barbershop-ten-wheat.vercel.app/failure",
                "pending": "https://barbershop-ten-wheat.vercel.app/pendings"
            },
            "auto_return": "approved"
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return jsonify(preference), 200
    except Exception as e:
        return {'error': str(e)}, 500
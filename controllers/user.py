from flask import jsonify, request
from models.user import fetch_user_model, update_user_model

def get_user_controller(current_user, id_user):
    try:
        if id_user != current_user['user_id']:
            return {'error': 'Unauthorized access'}, 403

        user = fetch_user_model(id_user)

        if user:
            user_id, name, email, birth_date, phone, created_at, updated_at, loyalty_package, avaliable_services_number, fl_status = user
            print(user_id)

            return {
                'userId': user_id,
                'name': name,
                'email': email,
                'birthDate': birth_date,
                'phone': phone,
                'createdAt': created_at,
                'updatedAt': updated_at,
                'loyaltyPackage': loyalty_package,
                'avaliableServicesNumber': avaliable_services_number,
                'status': fl_status
            }, 200

        else:
            return {'error': 'User not found'}, 404

    except Exception as e:
        return {'error': str(e)}, 500

def update_user_controller(current_user, id_user):
    data = request.json

    try:
        if id_user != current_user['user_id']:
            return {'error': 'Unauthorized access'}, 403

        response = update_user_model(
            user_id=id_user,
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            birth_date=data.get('birthDate'),
            loyalty_package=data.get('loyaltyPackage'),
            avaliable_services_number=data.get('avaliableServicesNumber')
        )
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
from models.bookings import get_bookings_model, update_booking_model, create_booking_model

def get_bookings_controller(current_user, id_user):
    if id_user != current_user['user_id']:
        return {'error': 'Unauthorized access'}, 403

    try:
        rows = get_bookings_model(id_user)

        bookings = []
        for row in rows:
            bookings.append({
                'id_booking': str(row[0]),
                'date': row[1].isoformat(),
                'time': row[2],
                'service': row[3],
                'barber_name': row[4],
                'status': row[5],
                'payment_type': rows[6],
                'nr_price': rows[7]
            })

        return {
            'id_user': id_user,
            'bookings': bookings
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500

def update_booking_controller(current_user, id_user, booking_id, status):
    try:
        if id_user != current_user['user_id']:
            return {'error': 'Unauthorized access'}, 403

        response = update_booking_model(
            booking_id=booking_id,
            status=status
        )
        return response, 200

    except Exception as e:
        return {'error': str(e)}, 500

def create_booking_controller(current_user, id_user, date, time, service_id, barber_id, payment_type, nr_price):
    try:
        if id_user != current_user['user_id']:
            return {'error': 'Unauthorized access'}, 403

        response = create_booking_model(
            id_user=id_user,
            date=date,
            time=time,
            service_id=service_id,
            barber_id=barber_id,
            payment_type=payment_type,
            nr_price=nr_price
        )
        return response, 200

    except Exception as e:
        return {'error': str(e)}, 500
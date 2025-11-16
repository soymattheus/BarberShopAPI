from datetime import datetime
from utils.send_email import send_booking_confirmation_email
from models.bookings import (
    get_bookings_model,
    update_booking_model,
    create_booking_model,
    get_booking_data_for_email_model,
    get_barber_model,
    generate_booking_vacency_model,
    check_booking_generation_model
)

def get_bookings_controller(current_user, id_user):
    if id_user != current_user['user_id']:
        return {'error': 'Unauthorized access'}, 403

    try:
        rows = get_bookings_model(id_user)

        bookings = []
        for row in rows:
            bookings.append({
                'bookingId': str(row[0]),
                'date': row[1].isoformat(),
                'time': row[2],
                'service': row[3],
                'barberName': row[4],
                'status': row[5],
                'paymentType': row[6],
                'price': row[7]
            })

        return {
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

        appointment_id = response[0]

        appointment_email_data = get_booking_data_for_email_model(appointment_id)

        service_name = appointment_email_data[0]
        barber = appointment_email_data[1]
        user_name = appointment_email_data[2]

        send_booking_confirmation_email(current_user['email'], user_name, barber, date, time, service_name, appointment_id)
        return {
            'userName': user_name,
            'barberName': barber,
            'date': date,
            'time': time,
            'service': service_name
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500

def generate_booking_vacancy_controller():
    try:
        today = datetime.now()
        formatted_date = today.strftime("%Y-%m-%d")

        has_data = check_booking_generation_model(formatted_date)

        if has_data[0] > 0:
            return {'msg': 'Already Created'}, 200

        barbers = get_barber_model()
        for barber in barbers:
            generate_booking_vacency_model(barber[0], formatted_date)
            print(barber[0])

        return {'msg': 'Created'}, 200

    except Exception as e:
        return {'error': str(e)}, 500
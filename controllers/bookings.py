from zoneinfo import ZoneInfo
from datetime import datetime
import pytz
from utils.send_email import send_booking_confirmation_email
from models.bookings import (
    get_bookings_model,
    update_booking_model,
    create_booking_model,
    get_booking_data_for_email_model,
    get_barber_model,
    generate_booking_vacency_model,
    check_booking_generation_model,
    get_bookings_available_dates_model,
    get_bookings_available_times_model,
    cancel_booking_model
)

# Definir o fuso horário de São Paulo
fuso_horario_sp = pytz.timezone('America/Sao_Paulo')

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
                'price': row[6]
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

def create_booking_controller(current_user, id_user, service_id, nr_price, id_booking):
    try:
        if id_user != current_user['user_id']:
            return {'error': 'Unauthorized access'}, 403

        response = create_booking_model(
            id_user=id_user,
            service_id=service_id,
            nr_price=nr_price,
            id_booking=id_booking
        )

        dt_date, tx_time = response[0]

        appointment_email_data = get_booking_data_for_email_model(id_booking)

        service_name = appointment_email_data[0]
        barber = appointment_email_data[1]
        user_name = appointment_email_data[2]

        new_time = tx_time.replace(' AM', '').replace(' PM', '')
        new_date = dt_date.strftime('%Y-%m-%d')

        send_booking_confirmation_email(current_user['email'], user_name, barber, new_date, new_time, service_name, id_booking)
        return {
            'userName': user_name,
            'barberName': barber,
            'date': dt_date,
            'time': tx_time,
            'service': service_name
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500

def cancel_booking_controller(current_user, id_user, id_booking):
    try:
        if id_user != current_user['user_id']:
            return {'error': 'Unauthorized access'}, 403

        response = cancel_booking_model(id_booking=id_booking)

        id_booking = response[0]

        return {
            'id': id_booking,
            'status': 'Canceled'
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500

def generate_booking_vacancy_controller(date):
    try:
        has_data = check_booking_generation_model(date)

        if has_data[0] > 0:
            return {'msg': 'Already Created'}, 200

        barbers = get_barber_model()
        for barber in barbers:
            generate_booking_vacency_model(barber[0], date)

        return {'msg': 'Created'}, 200

    except Exception as e:
        return {'error': str(e)}, 500

def get_bookings_available_dates_controller(id_barber):
    try:
        rows = get_bookings_available_dates_model(id_barber)

        dates = []
        for row in rows:
            dates.append({
                'date': row[0]
            })

        return {
            'dates': dates
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500

def get_bookings_available_times_controller(date, id_barber):
    try:
        sao_paulo_tz = ZoneInfo("America/Sao_Paulo")
        now_sp = datetime.now(sao_paulo_tz)
        today_sp = now_sp.date()
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        if date_obj == today_sp:
            start_date = now_sp
        else:
            start_date = date_obj
        rows = get_bookings_available_times_model(start_date, date, id_barber)

        times = []
        for row in rows:
            times.append({
                'id_booking': row[0],
                'time': row[1]
            })

        return {
            'times': times
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500
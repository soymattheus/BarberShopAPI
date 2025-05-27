import uuid
from config.db import get_db_connection

def get_barber_model():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            SELECT 
                b.id_barber,
                b.tx_nome,
                b.tx_specialty,
                b.tx_url_img,
                b.fl_status
            FROM tb_barber b
        """

        cur.execute(query)
        rows = cur.fetchall()

        return rows

    except Exception as e:
        print(f"Error searching for barbers: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def update_booking_model(booking_id, status):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            UPDATE tb_booking
            SET
                fl_status = %s
            WHERE id_booking = %s
        """

        cur.execute(query, (
            status,
            booking_id
        ))

        conn.commit()

        return {'message': 'Schedule updated successfully'}

    except Exception as e:
        print(f"Error updating booking {booking_id}: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def create_booking_model(id_user, date, time, service_id, barber_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        booking_id = str(uuid.uuid4())

        query = """
            INSERT INTO tb_booking (
                id_booking,
                id_user,
                dt_date,
                tx_time,
                id_service,
                id_barber,
                fl_status
            ) VALUES (%s, %s, %s, %s, %s, %s, 'scheduled')
        """

        cur.execute(query, (
            booking_id,
            id_user,
            date,
            time,
            service_id,
            barber_id
        ))

        conn.commit()

        return {
            'message': 'Appointment created successfully',
            'bookingId': booking_id
        }

    except Exception as e:
        print(f"Error creating booking: {e}")
        raise e

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
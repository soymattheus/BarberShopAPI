import uuid
from config.db import get_db_connection

def get_bookins_model(id_user):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            SELECT 
                b.id_booking, 
                b.dt_date, 
                b.tx_time, 
                tsl.tx_name AS service, 
                tb.tx_nome AS barber_name, 
                b.fl_status 
            FROM tb_booking b
            LEFT JOIN tb_service_list tsl ON tsl.id_service = b.id_service
            LEFT JOIN tb_barber tb ON tb.id_barber = b.id_barber
            WHERE b.id_user = %s
        """

        cur.execute(query, (id_user,))
        rows = cur.fetchall()

        return rows

    except Exception as e:
        print(f"Erro ao buscar bookings do usuário {id_user}: {e}")
        raise e  # Opcional: repassa a exceção para ser tratada no controller

    finally:
        if cur:
            cur.close()
        if conn:
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

        return {'message': 'Agendamento atualizado com sucesso'}

    except Exception as e:
        print(f"Erro ao atualizar booking {booking_id}: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def create_booking_model(id_user, date, time, service_id, barber_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        booking_id = str(uuid.uuid4())  # Gerando UUID para o booking

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
            'message': 'Agendamento criado com sucesso',
            'bookingId': booking_id
        }

    except Exception as e:
        print(f"Erro ao criar booking: {e}")
        raise e

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
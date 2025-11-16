import uuid
from config.db import get_db_connection

def get_bookings_model(id_user):
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
                b.fl_status,
                b.tx_payment_type,
                b.nr_price
            FROM tb_booking b
            LEFT JOIN tb_service_list tsl ON tsl.id_service = b.id_service
            LEFT JOIN tb_barber tb ON tb.id_barber = b.id_barber
            WHERE b.id_user = %s
        """

        cur.execute(query, (id_user,))
        rows = cur.fetchall()

        return rows

    except Exception as e:
        print(f"Error fetching user bookings {id_user}: {e}")
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

def create_booking_model(id_user, date, time, service_id, barber_id, payment_type, nr_price):
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
                fl_status,
                tx_payment_type,
                nr_price
            ) VALUES (%s, %s, %s, %s, %s, %s, 'scheduled', %s, %s)
            RETURNING id_booking
        """

        cur.execute(query, (
            booking_id,
            id_user,
            date,
            time,
            service_id,
            barber_id,
            payment_type,
            nr_price
        ))

        conn.commit()
        rows = cur.fetchone()

        return rows

    except Exception as e:
        print(f"Error creating booking: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def get_booking_data_for_email_model(id_booking):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            SELECT
                tsl.tx_name as service,
                tb.tx_nome as barber_name,
                tu.tx_name as user_name
            from tb_booking b
            left join tb_service_list tsl on tsl.id_service = b.id_service
            left join tb_barber tb on tb.id_barber = b.id_barber
            left join tb_user tu on tu.id_user = b.id_user
            WHERE b.id_booking = %s
        """

        cur.execute(query, (id_booking,))
        rows = cur.fetchone()

        return rows

    except Exception as e:
        print(f"Error fetching user bookings {id_booking}: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def get_barber_model():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            select tb.id_barber
            from tb_barber tb
            where tb.fl_status = 'A'
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

def generate_booking_vacency_model(barber_id, date):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            insert into tb_booking_new
            (id_booking, id_barber, dt_date, tx_time, fl_status) values
            (%s, %s, %s, '10:00', 'empty'),
            (%s, %s, %s, '11:00', 'empty'),
            (%s, %s, %s, '12:00', 'empty'),
            (%s, %s, %s, '13:30', 'empty'),
            (%s, %s, %s, '14:30', 'empty'),
            (%s, %s, %s, '15:30', 'empty'),
            (%s, %s, %s, '16:30', 'empty')
        """

        cur.execute(query, (
            str(uuid.uuid4()), barber_id, date,
            str(uuid.uuid4()), barber_id, date,
            str(uuid.uuid4()), barber_id, date,
            str(uuid.uuid4()), barber_id, date,
            str(uuid.uuid4()), barber_id, date,
            str(uuid.uuid4()), barber_id, date,
            str(uuid.uuid4()), barber_id, date,
        ))

        conn.commit()
        return

    except Exception as e:
        print(f"Error creating booking: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def check_booking_generation_model(date):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            select count(tbn.id_booking)
            from tb_booking_new tbn
            where tbn.dt_date = %s
        """

        cur.execute(query, (date,))
        row = cur.fetchone()

        return row

    except Exception as e:
        print(f"Error checking booking generation: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

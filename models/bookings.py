import uuid
from datetime import datetime
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
                b.nr_price
            FROM tb_booking_new b
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

def create_booking_model(id_user, service_id, nr_price, id_booking):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            UPDATE tb_booking_new tbn 
            set id_user = %s,
            fl_status = 'scheduled',
            id_service = %s,
            nr_price = %s
            WHERE id_booking = %s
            returning dt_date, tx_time
        """

        cur.execute(query, (
            id_user,
            service_id,
            nr_price,
            id_booking
        ))

        conn.commit()
        rows = cur.fetchall()

        return rows

    except Exception as e:
        print(f"Error creating booking: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def cancel_booking_model(id_booking):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            UPDATE tb_booking_new tbn 
            set id_user = null,
            fl_status = 'empty',
            id_service = null,
            nr_price = null
            WHERE id_booking = %s
            returning id_booking
        """

        cur.execute(query, (id_booking,))

        conn.commit()
        rows = cur.fetchall()

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
            from tb_booking_new b
            join tb_service_list tsl on tsl.id_service = b.id_service
            join tb_barber tb on tb.id_barber = b.id_barber
            join tb_user tu on tu.id_user = b.id_user
            where b.id_booking = %s
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
                    (%s, %s, %s, '10:00 AM', 'empty'),
                    (%s, %s, %s, '11:00 AM', 'empty'),
                    (%s, %s, %s, '12:00 PM', 'empty'),
                    (%s, %s, %s, '1:30 PM', 'empty'),
                    (%s, %s, %s, '2:30 PM', 'empty'),
                    (%s, %s, %s, '3:30 PM', 'empty'),
                    (%s, %s, %s, '4:30 PM', 'empty')
                """

        cur.execute(query, (
            str(uuid.uuid4()), barber_id, datetime.strptime(date + " 13:00:00", "%Y-%m-%d %H:%M:%S"),
            str(uuid.uuid4()), barber_id, datetime.strptime(date + " 14:00:00", "%Y-%m-%d %H:%M:%S"),
            str(uuid.uuid4()), barber_id, datetime.strptime(date + " 15:00:00", "%Y-%m-%d %H:%M:%S"),
            str(uuid.uuid4()), barber_id, datetime.strptime(date + " 16:30:00", "%Y-%m-%d %H:%M:%S"),
            str(uuid.uuid4()), barber_id, datetime.strptime(date + " 17:30:00", "%Y-%m-%d %H:%M:%S"),
            str(uuid.uuid4()), barber_id, datetime.strptime(date + " 18:30:00", "%Y-%m-%d %H:%M:%S"),
            str(uuid.uuid4()), barber_id, datetime.strptime(date + " 19:30:00", "%Y-%m-%d %H:%M:%S"),
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

def get_bookings_available_dates_model(id_barber):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            select distinct dt_date from tb_booking_new tbn
            where tbn.dt_date >= current_timestamp
            and tbn.id_barber = %s
            and tbn.id_user is null
            or tbn.id_user = ''
            order by tbn.dt_date
        """

        cur.execute(query, (id_barber,))
        rows = cur.fetchall()

        return rows

    except Exception as e:
        print(f"Error fetching baeber bookings available dates {id_barber}: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def get_bookings_available_times_model(start_date, date, id_barber):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        end_date = datetime.strptime(date + " 23:59:59", "%Y-%m-%d %H:%M:%S")

        query = """
            select tbn.id_booking, tbn.tx_time
            from tb_booking_new tbn
            where tbn.dt_date between %s::timestamp AND %s::timestamp
            and tbn.id_barber = %s
            and (tbn.id_user IS null OR tbn.id_user = '')
            order by tbn.dt_date
        """

        cur.execute(query, (start_date, end_date, id_barber))
        rows = cur.fetchall()

        return rows

    except Exception as e:
        print(f"Error fetching barber bookings available times {id_barber}: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

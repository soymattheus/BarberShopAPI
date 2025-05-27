from config.db import get_db_connection

def get_services_model():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            SELECT 
                id_service,
                tx_name,
                tx_description,
                nr_price,
                tx_service_type
            FROM tb_service_list
            WHERE fl_status = 'A'
            ORDER BY tx_service_type, tx_name
        """

        cur.execute(query)
        rows = cur.fetchall()

        return rows

    except Exception as e:
        print(f"Error when searching for services: {e}")
        raise e

    finally:
        cur.close()
        conn.close()


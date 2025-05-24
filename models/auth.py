from config.db import get_db_connection

def fetch_user_auth(email):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """SELECT 
                    u.id_user as id,
                    u.tx_name as name,
                    u.tx_email as email,
                    u.tx_password as password,
                    u.dt_birth_date as birthDate,
                    u.tx_phone as phone,
                    u.dt_created_at as createdAt,
                    u.dt_updated_at as updatedAt,
                    u.tx_loyalty_package as loyaltyPackage,
                    u.tx_avaliable_services_number as avaliableServicesNumber,
                    u.fl_status
                    FROM tb_user u 
                    WHERE tx_email = %s"""

        cur.execute(query, (email,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        return user

    except Exception as e:
        print(f"Erro ao buscar usuário {email}: {e}")
        raise e  # Opcional: repassa a exceção para ser tratada no controller

    finally:
        cur.close()
        conn.close()

def insert_user_auth(user_id, email, hashed_password):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Inserir usuário no banco
        insert_query = """
                    INSERT INTO tb_user (id_user, tx_email, tx_password, dt_created_at, fl_status)
                    VALUES (%s, %s, %s, CURRENT_DATE, 'I')
                    RETURNING id_user
                """
        cur.execute(insert_query, (user_id, email, hashed_password))
        user_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return user_id

    except Exception as e:
        print(f"Erro ao cadastrar usuário {email}: {e}")
        raise e  # Opcional: repassa a exceção para ser tratada no controller

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
from datetime import datetime, timedelta
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
                    u.fl_status,
                    u.tx_activation_token
                    FROM tb_user u 
                    WHERE tx_email = %s"""

        cur.execute(query, (email,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        return user

    except Exception as e:
        print(f"Erro ao buscar usuário {email}: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def insert_user_auth(user_id, email, hashed_password, activation_token):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = """
                    INSERT INTO tb_user (id_user, tx_email, tx_password, dt_created_at, fl_status, tx_activation_token)
                    VALUES (%s, %s, %s, CURRENT_DATE, 'I', %s)
                    RETURNING id_user
                """
        cur.execute(insert_query, (user_id, email, hashed_password, activation_token))
        user_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return user_id

    except Exception as e:
        print(f"Error registering user {email}: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def fetch_user_by_activation_token(token):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            SELECT 
                id_user,
                fl_status,
                tx_activation_token
            FROM tb_user
            WHERE tx_activation_token = %s
        """

        cur.execute(query, (token,))
        user = cur.fetchone()

        return user

    except Exception as e:
        print(f"Error searching for user by activation_token: {e}")
        return None

    finally:
        cur.close()
        conn.close()

def activate_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            UPDATE tb_user
            SET 
                fl_status = 'A',
                tx_activation_token = NULL,
                dt_updated_at = %s
            WHERE id_user = %s
        """

        cur.execute(query, (datetime.utcnow(), user_id))
        conn.commit()

        print(f"User {user_id} actives successfully.")

    except Exception as e:
        print(f"Error activating user {user_id}: {e}")
        raise e

    finally:
        cur.close()
        conn.close()

def fetch_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT id_user FROM tb_user WHERE tx_email = %s"
        cursor.execute(query, (email,))
        row = cursor.fetchone()

        return row

    except Exception as e:
        print(f"Error when searching for user {email}: {e}")
        raise e

    finally:
        cursor.close()
        conn.close()

def set_password_reset_token(user_id, token, expiration):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE tb_user
            SET tx_reset_pw_token = %s, dt_reset_pw_token_exp = %s 
            WHERE id_user = %s
        """
        cursor.execute(query, (token, expiration, user_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_user_by_reset_token(token):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT id_user FROM tb_user
            WHERE tx_reset_pw_token = %s AND dt_reset_pw_token_exp > NOW()
        """
        cursor.execute(query, (token,))
        row = cursor.fetchone()
        return row

    finally:
        cursor.close()
        conn.close()

def update_user_password(user_id, hashed_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE tb_user 
            SET tx_password = %s, tx_reset_pw_token = NULL, dt_reset_pw_token_exp = NULL, dt_updated_at = %s 
            WHERE id_user = %s
        """
        cursor.execute(query, (hashed_password, datetime.utcnow(), user_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
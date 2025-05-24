from config.db import get_db_connection

def fetch_user_model(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """SELECT
                    u.id_user as id,
                    u.tx_name as name,
                    u.tx_email as email,
                    u.dt_birth_date as birthDate,
                    u.tx_phone as phone,
                    u.dt_created_at as createdAt,
                    u.dt_updated_at as updatedAt,
                    u.tx_loyalty_package as loyaltyPackage,
                    u.tx_avaliable_services_number as avaliableServicesNumber,
                    u.fl_status
                    FROM tb_user u
                    WHERE id_user = %s"""

        cur.execute(query, (user_id,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        return user

    except Exception as e:
        print(f"Erro ao buscar usuário {user_id}: {e}")
        raise e  # Opcional: repassa a exceção para ser tratada no controller

    finally:
        cur.close()
        conn.close()

def update_user_model(user_id, name, email, phone, birth_date, loyalty_package, avaliable_services_number):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            UPDATE tb_user
            SET 
                tx_name = %s,
                tx_email = %s,
                tx_phone = %s,
                dt_birth_date = %s,
                tx_loyalty_package = %s,
                tx_avaliable_services_number = %s,
                dt_updated_at = NOW()
            WHERE id_user = %s
        """

        cur.execute(query, (
            name,
            email,
            phone,
            birth_date,
            loyalty_package,
            avaliable_services_number,
            user_id
        ))

        conn.commit()  # Importante para efetivar a alteração no banco

        return {'message': 'Usuário atualizado com sucesso'}

    except Exception as e:
        print(f"Erro ao atualizar usuário {user_id}: {e}")
        raise e

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

from models.barber import get_barber_model

def get_barber_controller(current_user):
    try:
        rows = get_barber_model()

        barbers = []
        for row in rows:
            barbers.append({
                'barberId': str(row[0]),
                'name': row[1],
                'specialty': row[2],
                'urlImg': row[3],
                'status': row[4]
            })

        return {
            'barbers': barbers
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500

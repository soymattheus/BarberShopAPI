from models.service import get_services_model

def get_service_controller():
    try:
        rows = get_services_model()

        # Group by category (tx_service_type)
        grouped = {}
        for row in rows:
            id_service, name, description, price, category = row

            if category not in grouped:
                grouped[category] = []

            grouped[category].append({
                "id": id_service,
                "name": name,
                "description": description,
                "price": float(price)
            })

        # Format in expected model
        result = [
            {
                "title": category,
                "services": services
            }
            for category, services in grouped.items()
        ]

        return {
            'services': result
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500

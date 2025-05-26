from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from routes.bookings import bookings_bp
from routes.auth import auth_bp
from routes.user import user_bp
from routes.barber import barber_bp

from extensions import mail

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = (
        os.getenv('MAIL_DEFAULT_SENDER_NAME'),
        os.getenv('MAIL_DEFAULT_SENDER_EMAIL')
    )

    mail.init_app(app)

    # pip freeze > requirements.txt
    # pip install -r requirements.txt

    # Build dos containers
    # docker-compose build

    # Subir os containers
    # docker-compose up

    # Derrubar os containers
    # docker-compose down

    # Configurar CORS global
    CORS(app)
    # Configurar CORS para apenas essas origens
    #CORS(app, origins=["https://meusite.com", "http://localhost:3000"])

    # Registrar blueprints
    app.register_blueprint(bookings_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(barber_bp)


    # Configuração do Swagger
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'  # Caminho do arquivo swagger.yaml na pasta static

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Booking API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

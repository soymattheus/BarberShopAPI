from dotenv import load_dotenv
import json
import os
import uuid
from datetime import datetime
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, request, jsonify
from flask_socketio import (
    SocketIO,
    join_room,
    leave_room,
    emit
)

from routes.bookings import bookings_bp
from routes.auth import auth_bp, activation_bp
from routes.user import user_bp
from routes.barber import barber_bp
from routes.service import service_bp

from extensions import mail
from redis_client import redis_client


def create_app():
    load_dotenv()
    app = Flask(__name__)
    sio = SocketIO(cors_allowed_origins="*")
    sio.init_app(app)
    # app.config['SECRET_KEY'] = 'secret!'
    # sio.init_app(app, cors_allowed_origins="*")

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

    # Configure global CORS
    CORS(app)
    # Configure CORS for only these origins
    #CORS(app, origins=["https://meusite.com", "http://localhost:3000"])

    # Register blueprints
    app.register_blueprint(bookings_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(activation_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(barber_bp)
    app.register_blueprint(service_bp)

    # Configure Swagger
    swagger_url = '/swagger'
    api_url = '/static/swagger.yaml'

    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': "Booking API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

    # POST /message - Enviar mensagem
    @app.post("/message")
    def send_message():
        data = request.json

        id = str(uuid.uuid4())
        room = data["room"]
        text = data["text"]
        sender = data["sender"]

        agora = datetime.now()
        data_hora_formatada = agora.strftime("%Y-%m-%d %H:%M")

        msg = {
            "id": id,
            "room": room,
            "text": text,
            "sender": sender,
            "created_at": data_hora_formatada
        }

        # 👉 chave da sala
        key = f"chat:room:{room}:messages"
        print('AQUI')

        redis_client.rpush(key, json.dumps(msg))

        # Emitir para websockets
        sio.emit("new_message", {
            "id": msg['id'],
            "room": msg['room'],
            "text": msg['text'],
            "sender": msg['sender'],
            "created_at": msg['created_at']
        }, to=room)

        return jsonify({"status": "ok"})

    # GET /messages/<room>
    @app.get("/messages/<room>")
    def get_messages(room):
        # 👉 chave da sala
        key = f"chat:room:{room}:messages"

        raw_messages = redis_client.lrange(key, 0, -1)

        messages = [json.loads(m) for m in raw_messages]

        return jsonify([
            {
                "id": m['id'],
                "room": m['room'],
                "sender": m['sender'],
                "text": m['text'],
                "created_at": m['created_at'],
            }
            for m in messages
        ])

    # WebSocket events
    @sio.on("join_room")
    def handle_join(data):
        room = data["room"]
        join_room(room)

        emit("system", {"msg": f"Usuário entrou na sala {room}"}, to=room)

    @sio.on("leave_room")
    def handle_leave(data):
        room = data["room"]
        leave_room(room)

    return app

if __name__ == '__main__':
    app = create_app()
    #app.run(debug=True)
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

# pip freeze > requirements.txt
# pip install -r requirements.txt

# Build containers
# docker-compose build

# Run containers
# docker-compose up

# Stop containers
# docker-compose down
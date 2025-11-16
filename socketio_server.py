from flask_socketio import SocketIO
import os

socketio = SocketIO(
    cors_allowed_origins="*",
    message_queue=os.getenv("REDIS_URL"),  # redis://localhost:6379
    async_mode="eventlet"
)

from flask import Flask
from flask_cors import CORS
from routes.bookings import bookings_bp
from routes.auth import auth_bp
from routes.user import user_bp

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)

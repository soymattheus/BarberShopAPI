import psycopg2
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT')
}

def get_db_connection():
    return psycopg2.connect(**db_config)

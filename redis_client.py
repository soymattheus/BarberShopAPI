import os
import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_client = redis.from_url(url=REDIS_URL, decode_responses=True)
    redis_client.ping()
    print("Conexão com o Redis no Railway estabelecida com sucesso!")
except redis.exceptions.ConnectionError as e:
        print(f"Erro de conexão com o Redis: {e}")

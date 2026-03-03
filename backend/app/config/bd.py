import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    # Render usará esta URL automáticamente
    url = os.getenv("DATABASE_URL")
    
    if url:
        return psycopg2.connect(url)
    else:
        # Esto es solo para cuando trabajes en tu PC
        return psycopg2.connect(
            host="localhost",
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port="5432"
        )
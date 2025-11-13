import os
os.environ['PYTHONUTF8'] = '1'

import psycopg2
from decouple import config

try:
    conn = psycopg2.connect(
        dbname=config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST'),
        port=config('DB_PORT', default='5432'),
        client_encoding='UTF8'
    )
    print("✓ Conexión exitosa a PostgreSQL!")
    print(f"Base de datos: {config('DB_NAME')}")
    conn.close()
except Exception as e:
    print(f"✗ Error de conexión:")
    print(f"  {type(e).__name__}: {e}")

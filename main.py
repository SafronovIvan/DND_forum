import psycopg2
import os
from dotenv import load_dotenv


def open_DataBase(env_file="bd.end"):
    try:
        load_dotenv(env_file)
        bd = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT'),
            database = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD')
        )
        cursor = database.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        return bd, cursor
            
    except Exception as e:
        print(e)

database, cursor = open_DataBase()
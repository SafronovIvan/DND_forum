import psycopg2
import os
from dotenv import load_dotenv


class DataBase():
    def __init__(self, env_file="bd.env"):
        try:
            load_dotenv(env_file)
            self.database = psycopg2.connect(
                host = os.getenv('DB_HOST'),
                port = os.getenv('DB_PORT'),
                database = os.getenv('DB_NAME'),
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD')
            )
            self.cursor = self.database.cursor()
            self.cursor.execute("SELECT version();")
            self.version = self.cursor.fetchone()[0]
            
        except Exception as e:
            print(e)

    def insert(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        values = tuple(data.values())
        self.cursor.execute(query, values)
        self.database.commit()

    def select(self, table, columns, data={}):
        columns = ', '.join(columns)
        if type(data) == dict and data!={}:
            values = tuple(data.values())
            params = '=%s AND '.join(list(data.keys())) + '=%s'
            query = f"SELECT {columns} FROM {table} WHERE {params}"
            self.cursor.execute(query, values)
        elif type(data) == str:
            query = f"SELECT {columns} FROM {table} WHERE {data}"
            self.cursor.execute(query)
        else:
            query = f"SELECT {columns} FROM {table}"
            self.cursor.execute(query)
        self.database.commit()
        return self.cursor.fetchall()
    
    def update(self, table, data_new, data_old):
        columns_old = '=%s AND '.join(data_old.keys()) + ' = %s'
        columns_new = ' = %s, '.join(data_new.keys()) + ' = %s'
        query = f"UPDATE {table} SET {columns_new} WHERE {columns_old}"
        values = tuple(list(data_new.values()) + list(data_old.values()))
        self.cursor.execute(query, values)
        self.database.commit()

    def delete(self, table, data):
        columns = '=%s AND '.join(data.keys()) + '=%s'
        values = tuple(data.values())
        query = f"DELETE FROM {table} WHERE {columns}"
        self.cursor.execute(query, values)
        self.database.commit()

        

bd = DataBase()

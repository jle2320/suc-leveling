import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
            "use_pure": True
        }

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            self.conn = None
            self.cursor = None

    def execute(self, query, params=None):
        self.connect()
        if not self.conn or not self.cursor:
            print("No DB connection or cursor")
            return None  
        self.cursor.execute(query, params or ())

        if query.strip().split()[0].lower() in ('insert', 'update', 'delete'):
            self.conn.commit()

        return self.cursor


    def fetchone(self):
        return self.cursor.fetchone() if self.cursor else None

    def fetchall(self):
        return self.cursor.fetchall() if self.cursor else None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

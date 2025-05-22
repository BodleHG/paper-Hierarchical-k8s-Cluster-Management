import os
import pymysql
from .db_strategy import DatabaseStrategy

class MySQLStrategy(DatabaseStrategy):
    def __init__(self):
        host = os.getenv("MYSQL_HOST", "localhost")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "")
        database = os.getenv("MYSQL_DATABASE", "testdb")

        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"[MySQL] Connected to {host}:{port}/{database}")

    def create(self, data):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO test_table (name, value) VALUES (%s, %s)"
            cursor.execute(sql, (data["name"], data["value"]))
        self.conn.commit()

    def read(self, query):
        with self.conn.cursor() as cursor:
            sql = f"SELECT * FROM test_table WHERE {query}"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return result

    def update(self, query, update):
        with self.conn.cursor() as cursor:
            sql = f"UPDATE test_table SET {update} WHERE {query}"
            cursor.execute(sql)
        self.conn.commit()

    def delete(self, query):
        with self.conn.cursor() as cursor:
            sql = f"DELETE FROM test_table WHERE {query}"
            cursor.execute(sql)
        self.conn.commit()

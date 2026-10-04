import sqlite3
from contextlib import contextmanager


@contextmanager
def get_connection():
    connection =  sqlite3.connect("./database.db")
    
    try:
        yield connection
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                password TEXT,
                age INTEGER
            )
        """)


def print_database():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * F  ROM users;")

        rows = cursor.fetchall()

        print(rows)

from config import Database
import mysql.connector

def get_db_connection(with_db=True):
    return mysql.connector.connect(
        host=Database.HOST,
        port=Database.PORT,
        user=Database.USERNAME,
        password=Database.PASSWORD,
        database=Database.DB_NAME if with_db else None
    )



def init_db():
    conn = get_db_connection(with_db=False)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Database.DB_NAME}")
    cursor.close()
    conn.close()

    
    print("Database and tables initialized.")

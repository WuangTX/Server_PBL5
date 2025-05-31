# db.py
import mysql.connector
from mysql.connector import Error

db_connection = None

def init_db_connection():
    global db_connection
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pbl5_db"
        )
        if db_connection.is_connected():
            print("✅ Kết nối database thành công")
    except Error as e:
        print(f"❌ Lỗi kết nối DB: {e}")
        db_connection = None

def get_db_connection():
    global db_connection
    if db_connection is None or not db_connection.is_connected():
        print("⚠️ DB connection mất, thử kết nối lại...")
        init_db_connection()
    return db_connection

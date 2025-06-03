import mysql.connector
from mysql.connector import Error
import configparser
from typing import Optional, Tuple

def read_db_config():
    """Read database configuration from config.ini file"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    return {
        'host': config['Database']['Host'],
        'database': config['Database']['Database'],
        'port': config['Database']['Port'],
        'user': config['Database']['User'],
        'password': config['Database']['Password']
    }

def create_db_connection():
    """Create a database connection"""
    try:
        db_config = read_db_config()
        connection = mysql.connector.connect(
            host=db_config['host'],
            database=db_config['database'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def verify_teacher(national_code: str, password: str) -> Optional[Tuple]:
    """Verify teacher credentials and return teacher data if valid"""
    connection = create_db_connection()
    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT teacher_name, teacher_family, teacher_national_code 
            FROM teachers 
            WHERE teacher_national_code = %s AND teacher_password = %s
        """
        cursor.execute(query, (national_code, password))
        teacher = cursor.fetchone()
        
        if teacher:
            full_name = f"{teacher['teacher_name']} {teacher['teacher_family']}"
            return (teacher['teacher_national_code'], full_name)
        return None
        
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
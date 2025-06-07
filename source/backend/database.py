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
            SELECT teacher_name, teacher_family, teacher_national_code, teacher_password, lesson, id
            FROM teachers 
            WHERE teacher_national_code = %s AND teacher_password = %s
        """
        cursor.execute(query, (national_code, password))
        teacher = cursor.fetchone()
        print(teacher)

        if teacher:
            return [True, teacher] # valid data
        else:
            return [False, 0] # invalid data
        
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_teacher_classes(teacher_id):
    """Getting teacher classes"""
    connection = create_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        query = """
            SELECT class_id FROM teacher_class
            WHERE teacher_id = %s
        """
        cursor.execute(query, (teacher_id,))
        teacher_classes = cursor.fetchall()

        if teacher_classes:
            class_ids = [class_id for (class_id,) in teacher_classes]
            return [True, class_ids]  # valid data
        else:
            return [False, 0]  # invalid data
        
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_class_name(class_id):
    """Getting class name"""
    connection = create_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT id, class_name, school_id FROM classes
            WHERE id = %s
        """
        cursor.execute(query, (class_id,))
        class_info = cursor.fetchone()

        if class_info:
            return class_info # valid data
        else:
            return 0 # invalid data
        
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_students_list_by_class_code(class_id) :
    """Getting students national codes list"""
    connection = create_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT id, student_national_code, student_name, student_family FROM students WHERE class_id = %s
        """
        cursor.execute(query, (class_id,))
        students_list = cursor.fetchall()

        if students_list:
            return students_list # valid data
        else:
            return 0 # invalid data
        
    except Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # uname = input("user: ")
    # password = input("password: ")
    # verify_teacher(national_code=uname, password=password)

    # print(get_teacher_classes(1,))

    # print(get_class_name('1'))

    print(get_students_list_by_class_code('1'))
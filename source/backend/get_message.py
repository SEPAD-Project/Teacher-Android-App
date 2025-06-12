import requests
import os 
import configparser

config_path = os.path.join(os.path.dirname(__file__), '../config.ini')
config = configparser.ConfigParser()
config.read(config_path)

ip_address = config['Server']['IP']
port = int(config['Server']['student_status_port'])

# server address 185.4.28.110
server_url = f"http://{ip_address}:{port}"

# getting students message and show them
def fetch_messages(national_code: str, school_code: str, class_code: str):
    """Retrieves messages for a student from specified school and class records.
    
    Fetches student messages by validating their national code, school code, and class name.
    Returns operation status along with messages or error description.

    Args:
        national_code (str): Student's unique national identification code (e.g., "0929538503")
        school_code (str): Unique numerical identifier for the school (e.g., "123")
        class_name (str): Official name of the class (e.g., "1052")

    Returns:
        list[bool, str]: A list containing:
            - bool: Success status (True if messages found, False if error occurs)
            - str: Either error message string or retrieved messages
        
    Examples:
        >>> get_student_messages("1234567890", "123", "1052")
        (True, ["Looking at the monitor"])

        >>> get_student_messages("invalid_code", '9999', "Non-existent Class")
        (False, "Student not found")
    """
    response = requests.post(f"{server_url}/get_last_message", json={
            "school_name": school_code,
            "class_code": class_code,
            "student_name": national_code
    }, timeout=5)
    if response.status_code == 200:
        data = response.json()
        return [True, data['message']]
    elif response.status_code == 404:
        data = response.json()
        return [False, data['error']]
    else:
        return [False, 'Error']
        


if __name__ == '__main__' :
    print(fetch_messages(
        national_code='123',
        school_code='1',
        class_code='1'
    ))
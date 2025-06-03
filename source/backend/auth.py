from .database import verify_teacher
from typing import Optional, Tuple

def authenticate_user(username: str, password: str) -> Optional[Tuple]:
    """Authenticate user using teacher credentials"""
    return verify_teacher(username, password)
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext
from app.core import config
from app.schemas.auth import TokenPayload

# Secret key and hashing
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: TokenPayload, expires_delta: timedelta = None):
    """
    Create a new access token.

    Args:
        data (TokenPayload): The payload data for the token.
        expires_delta (timedelta, optional): The expiration time for the token. Defaults to None.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.model_copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.exp = expire
    return jwt.encode(to_encode.model_dump(), SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> TokenPayload | None:
    """
    Decode an access token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        TokenPayload | None: The decoded payload, or None if decoding fails.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload.model_validate(payload)
    except PyJWTError:
        return None

class AuthServices:
    pass

AuthServices.hash_password = hash_password
AuthServices.verify_password = verify_password
AuthServices.create_access_token = create_access_token
AuthServices.decode_access_token = decode_access_token
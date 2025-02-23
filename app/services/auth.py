from datetime import datetime, timedelta
import jwt
from jwt import InvalidTokenError, PyJWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app import config
from app.models.auth import TokenPayload

# Secret key and hashing
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: TokenPayload, expires_delta: timedelta = None):
    to_encode = data.model_copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.exp = expire
    # to_encode.update({"exp": expire})
    return jwt.encode(to_encode.model_dump(), SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload.model_validate(payload)
    except PyJWTError:
        return None

from passlib.context import CryptContext
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_pw(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_pw(password: str, hashed: str) -> bool:
    return pwd_ctx.verify(password, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # TODO: add expiration logic here
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

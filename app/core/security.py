from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sh256", "bcrypt"],
    deprecated="auto"
)

def get_hash_password(password: str):
    return pwd_context.hash(password)

def verify_hashed_password(normal_password, hashed_password):
    return pwd_context.verify(normal_password, hashed_password)


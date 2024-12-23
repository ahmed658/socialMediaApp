from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str):
    return pwd_context.hash(password)

def verify_password(password:str, hashedpassword: str):
    return pwd_context.verify(password, hashedpassword)
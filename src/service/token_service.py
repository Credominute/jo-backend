from fastapi import HTTPException, Request
from jose import jwt, JWTError
from starlette import status
from src.config.hash import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from src.schema.token_schema import Token
from datetime import datetime, timedelta

def create_token(data: dict) -> Token:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return Token(access_token = jwt.encode(to_encode,
                                           SECRET_KEY,
                                           algorithm = ALGORITHM),
                                           token_type="Bearer")

def verify_token(request: Request):
    authorization : str = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token manquant ou format incorrect."
        )
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide : 'sub' manquant."
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré."
        )
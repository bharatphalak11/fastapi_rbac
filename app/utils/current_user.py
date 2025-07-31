from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from sqlmodel import Session
from app.config import SECRET_KEY, ALGORITHM
from app.crud.user import get_user_by_username
from app.database import get_session
from app.models.user import User

def get_current_user(request: Request) -> User:

    # Extract Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    # Extract token
    token = auth_header.split(" ")[1]

    # Decode and validate token
    try:
        session_generator = get_session()
        session: Session = next(session_generator)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")

        if username is None:
            raise HTTPException(status_code=401, detail="Token payload invalid")

        # Fetch user from DB
        user = get_user_by_username(session, username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

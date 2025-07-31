from sqlmodel import Session, select
from app.models.user import User

def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()

def get_user_by_id(session: Session, user_id: int):
    return session.exec(select(User).where(User.id == user_id)).first()

def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user_by_object(session: Session, user: User):
    session.delete(user)
    session.commit()
    return True
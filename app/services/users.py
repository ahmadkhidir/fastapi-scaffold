from sqlmodel import select
from app.database import Session
from app.models.users import User, UserCreate
from app.services.auth import hash_password

def create_user(session: Session, user: UserCreate):
    user.password = hash_password(user.password)
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user(session: Session, username: str) -> User:
    return session.exec(select(User).filter(User.username == username)).first()

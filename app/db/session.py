from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from app.core import config


connect_args = ({"check_same_thread": False}
                if (config.DATABASE_URL and config.DATABASE_URL.startswith("sqlite"))
                else {})

assert config.DATABASE_URL, "DATABASE_URL is not set in the environment"
engine = create_engine(
    config.DATABASE_URL, connect_args=connect_args
)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

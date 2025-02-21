from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Annotated
from . import config


connect_args = ({"check_same_thread": False}
                if config.DATABASE_URL.startswith("sqlite")
                else {})

engine = create_engine(
    config.DATABASE_URL, connect_args=connect_args
)


def init_db():
    '''Create the database tables (call if not using alembic)'''
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

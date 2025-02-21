from sqlmodel import SQLModel
from datetime import datetime


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenPayload(SQLModel):
    sub: str | None = None
    exp: datetime | None = None
    scopes: list[str] = []


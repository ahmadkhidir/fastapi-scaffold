from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str
    disabled: bool | None = Field(default=True)


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
    disabled: bool
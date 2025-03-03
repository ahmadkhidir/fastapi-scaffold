from app.db.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Table, Column, Integer, ForeignKey


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("role_id", Integer, ForeignKey("role.id"))
)

role_scope = Table(
    "role_scope",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("role.id")),
    Column("scope_id", Integer, ForeignKey("scope.id"))
)

class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(default="")
    users: Mapped[set["User"]] = relationship(back_populates="roles", secondary=user_role)
    scopes: Mapped[set["Scope"]] = relationship(back_populates="roles", secondary=role_scope)

class Scope(Base):
    __tablename__ = "scope"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(default="")
    roles: Mapped[set["Role"]] = relationship(back_populates="scopes", secondary=role_scope)

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[set[Role]] = relationship(back_populates="users", secondary=user_role)
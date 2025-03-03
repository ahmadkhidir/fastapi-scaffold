from pydantic import BaseModel
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class RoleCreate(RoleBase):
    users: list[str] = []
    scopes: list[str] = []

class RoleUpdate(RoleBase):
    name: str | None = None
    description: str | None = None
    users: list[str] | None
    scopes: list[str] | None

class RolePublic(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

class RolePublic_Admin(RolePublic):
    users: list["UserPublic_Admin"]
    scopes: list["ScopePublic"]

class ScopeBase(BaseModel):
    name: str
    description: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class ScopeCreate(ScopeBase):
    roles: list[str] = []

class ScopeUpdate(ScopeBase):
    name: str | None = None
    description: str | None = None
    roles: list[str] | None

class ScopePublic(ScopeBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ScopePublic_Admin(ScopePublic):
    roles: list["RolePublic_Admin"]

class UserBase(BaseModel):
    first_name: str
    last_name: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

class UserCreate(UserBase):
    username: str
    password: str

class UserUpdate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None

class UserUpdate_Admin(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None
    roles: list[str] | None = None

class UserPublic(UserBase):
    id: int
    username: str
    disabled: bool
    created_at: datetime
    updated_at: datetime

class UserPublic_Admin(UserPublic):
    roles: list[RolePublic]
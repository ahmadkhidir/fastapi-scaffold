from sqlmodel import SQLModel, Field, Relationship


class UserRole(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)


class RoleScope(SQLModel, table=True):
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    scope_id: int = Field(foreign_key="scope.id", primary_key=True)


class RoleBase(SQLModel):
    name: str
    description: str = Field(default="")

class Role(RoleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRole)
    scopes: list["Scope"] = Relationship(back_populates="roles", link_model=RoleScope)


class RoleCreate(RoleBase):
    users: list[str]
    scopes: list[str]


class RoleUpdate(RoleCreate):
    pass


class RolePublic(RoleBase):
    id: int

class RolePublic_Admin(RolePublic):
    users: list["UserPublic_Admin"]
    scopes: list["Scope"]

class ScopeBase(SQLModel):
    name: str
    description: str = Field(default="")

class Scope(ScopeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    roles: list["Role"] = Relationship(back_populates="scopes", link_model=RoleScope)


class ScopeCreate(ScopeBase):
    roles: list[str]


class ScopeUpdate(ScopeCreate):
    pass


class ScopePublic(ScopeBase):
    id: int


class ScopePublic_Admin(ScopePublic):
    roles: list["Role"]


class UserBase(SQLModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str
    disabled: bool | None = Field(default=False)
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRole)


class UserCreate(UserBase):
    username: str = Field(index=True)
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserUpdate_Admin(UserBase):
    disabled: bool | None = None
    roles: list[str] | None = None


class UserPublic(UserBase):
    id: int
    username: str = Field(index=True)
    disabled: bool


class UserPublic_Admin(UserPublic):
    roles: list[RolePublic]
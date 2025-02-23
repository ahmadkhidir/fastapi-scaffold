from fastapi import APIRouter, Depends, Security
from app.dependencies import get_current_active_user
from app.models.users import *
from typing import Annotated
from app.services import users
from app.database import SessionDep

router = APIRouter(
    tags=["users"],
    prefix="/users",
)

# Current User


@router.get("/me", response_model=UserPublic)
def read_current_user(current_user: Annotated[User, Security(
    get_current_active_user,
    scopes=["user:read"]
)]):
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_current_user(
        session: SessionDep,
        current_user: Annotated[User, Security(
            get_current_active_user, scopes=["user:update"]
        )],
        form_data: UserUpdate):
    return users.update_user(session, current_user, form_data)

# User Role


@router.post("/roles", response_model=RolePublic_Admin)
def create_role(session: SessionDep, form_data: RoleCreate, _: Annotated[User, Security(
            get_current_active_user, scopes=["role:create"]
        )],):
    return users.create_role(session, form_data)


@router.get("/roles/{id}", response_model=RolePublic_Admin)
def read_role(session: SessionDep, id: int, _: Annotated[User, Security(
            get_current_active_user, scopes=["role:read"]
        )],):
    return users.get_role(session, id)


@router.patch("/roles/{id}", response_model=RolePublic_Admin)
def update_role(session: SessionDep, id: int, form_data: RoleUpdate, _: Annotated[User, Security(
            get_current_active_user, scopes=["role:update"]
        )],):
    return users.update_role(session, id, form_data)


@router.delete("/roles/{id}")
def delete_role(session: SessionDep, id: int, _: Annotated[User, Security(
            get_current_active_user, scopes=["role:delete"]
        )],):
    return users.delete_role(session, id)


@router.get("/roles", response_model=list[RolePublic_Admin])
def list_roles(session: SessionDep, _: Annotated[User, Security(
            get_current_active_user, scopes=["role:read"]
        )],):
    return users.get_all_roles(session)

# User Scope


@router.post("/scopes", response_model=ScopePublic_Admin)
def create_scope(session: SessionDep, form_data: ScopeCreate, _: Annotated[User, Security(
            get_current_active_user, scopes=["scope:create"]
        )],):
    return users.create_scope(session, form_data)


@router.get("/scopes/{id}", response_model=ScopePublic_Admin)
def read_scope(session: SessionDep, id: int, _: Annotated[User, Security(
            get_current_active_user, scopes=["scope:read"]
        )],):
    return users.get_scope(session, id)


@router.patch("/scopes/{id}", response_model=ScopePublic_Admin)
def update_scope(session: SessionDep, id: int, form_data: ScopeUpdate, _: Annotated[User, Security(
            get_current_active_user, scopes=["scope:update"]
        )],):
    return users.update_scope(session, id, form_data)


@router.delete("/scopes/{id}")
def delete_scope(session: SessionDep, id: int, _: Annotated[User, Security(
            get_current_active_user, scopes=["scope:delete"]
        )],):
    return users.delete_scope(session, id)


@router.get("/scopes", response_model=list[ScopePublic_Admin])
def list_scopes(session: SessionDep, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:read"]
)]):
    return users.get_all_scopes(session)

# User


@router.patch("/{username}",
              tags=['admin'],
              response_model=UserPublic_Admin)
def update_user(
        session: SessionDep,
        username: str,
        _: Annotated[User, Security(
            get_current_active_user, scopes=["admin:update"]
        )],
        form_data: UserUpdate_Admin):
    return users.admin_update_user(session, username, form_data)


@router.get("", response_model=list[UserPublic])
def list_users(session: SessionDep, _: Annotated[User, Security(
    get_current_active_user,
    scopes=["admin:read"]
)]):
    return users.get_all_users(session)

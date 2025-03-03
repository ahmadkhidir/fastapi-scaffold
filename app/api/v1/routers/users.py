from fastapi import APIRouter, Depends, Security
from app.core.security import get_current_active_user
from app.schemas.users import *
from typing import Annotated
from app.services.users import UserServices, RoleServices, ScopeServices
from app.db.models.users import Role, User
from app.db.session import SessionDep

router = APIRouter(
    tags=["users"],
    prefix="/users",
)


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
    return UserServices.update_user(session, current_user, form_data)


@router.post("/roles", response_model=RolePublic_Admin)
def create_role(session: SessionDep, form_data: RoleCreate, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:create"]
)],):
    return RoleServices.create_role(session, form_data)


@router.get("/roles/{id}", response_model=RolePublic_Admin)
def read_role(session: SessionDep, id: int, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:read"]
)],):
    return RoleServices.get_role(session, id)


@router.patch("/roles/{id}", response_model=RolePublic_Admin)
def update_role(session: SessionDep, id: int, form_data: RoleUpdate, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:update"]
)],):
    return RoleServices.update_role(session, id, form_data)


@router.delete("/roles/{id}")
def delete_role(session: SessionDep, id: int, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:delete"]
)],):
    return RoleServices.delete_role(session, id)


@router.get("/roles", response_model=list[RolePublic])
def list_roles(session: SessionDep, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:read"]
)],):
    return RoleServices.get_all_roles(session)


@router.post("/scopes", response_model=ScopePublic_Admin)
def create_scope(session: SessionDep, form_data: ScopeCreate, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:create"]
)],):
    return ScopeServices.create_scope(session, form_data)


@router.get("/scopes/{id}", response_model=ScopePublic_Admin)
def read_scope(session: SessionDep, id: int, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:read"]
)],):
    return ScopeServices.get_scope(session, id)


@router.patch("/scopes/{id}", response_model=ScopePublic_Admin)
def update_scope(session: SessionDep, id: int, form_data: ScopeUpdate, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:update"]
)],):
    return ScopeServices.update_scope(session, id, form_data)


@router.delete("/scopes/{id}")
def delete_scope(session: SessionDep, id: int, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:delete"]
)],):
    return ScopeServices.delete_scope(session, id)


@router.get("/scopes", response_model=list[ScopePublic])
def list_scopes(session: SessionDep, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:read"]
)]):
    return ScopeServices.get_all_scopes(session)


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
    return UserServices.admin_update_user(session, username, form_data)


@router.get("", response_model=list[UserPublic])
def list_users(session: SessionDep, _: Annotated[User, Security(
    get_current_active_user,
    scopes=["admin:read"]
)]):
    return UserServices.get_all_users(session)

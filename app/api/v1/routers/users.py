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
    """
    Get the current authenticated user's information.

    Returns:
        UserPublic: The public information of the current user.
    """
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_current_user(
        session: SessionDep,
        current_user: Annotated[User, Security(
            get_current_active_user, scopes=["user:update"]
        )],
        form_data: UserUpdate):
    """
    Update the current authenticated user's information.

    Args:
        form_data (UserUpdate): Data to update the user.

    Returns:
        UserPublic: The updated public information of the current user.
    """
    return UserServices.update_user(session, current_user, form_data)


@router.post("/roles", response_model=RolePublic_Admin)
def create_role(session: SessionDep, form_data: RoleCreate, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:create"]
)],):
    """
    Create a new role.

    Args:
        form_data (RoleCreate): Data to create a new role.

    Returns:
        RolePublic_Admin: The created role's public information.
    """
    return RoleServices.create_role(session, form_data)


@router.get("/roles/{id}", response_model=RolePublic_Admin)
def read_role(session: SessionDep, id: int, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:read"]
)],):
    """
    Get a role by ID.

    Args:
        id (int): The ID of the role to retrieve.

    Returns:
        RolePublic_Admin: The public information of the retrieved role.
    """
    return RoleServices.get_role(session, id)


@router.patch("/roles/{id}", response_model=RolePublic_Admin)
def update_role(session: SessionDep, id: int, form_data: RoleUpdate, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:update"]
)],):
    """
    Update a role by ID.

    Args:
        id (int): The ID of the role to update.
        form_data (RoleUpdate): Data to update the role.

    Returns:
        RolePublic_Admin: The updated public information of the role.
    """
    return RoleServices.update_role(session, id, form_data)


@router.delete("/roles/{id}")
def delete_role(session: SessionDep, id: int, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:delete"]
)],):
    """
    Delete a role by ID.

    Args:
        id (int): The ID of the role to delete.

    Returns:
        dict: A message indicating successful role deletion.
    """
    return RoleServices.delete_role(session, id)


@router.get("/roles", response_model=list[RolePublic])
def list_roles(session: SessionDep, _: Annotated[User, Security(
    get_current_active_user, scopes=["role:read"]
)],):
    """
    List all roles.

    Returns:
        list[RolePublic]: A list of all roles' public information.
    """
    return RoleServices.get_all_roles(session)


@router.post("/scopes", response_model=ScopePublic_Admin)
def create_scope(session: SessionDep, form_data: ScopeCreate, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:create"]
)],):
    """
    Create a new scope.

    Args:
        form_data (ScopeCreate): Data to create a new scope.

    Returns:
        ScopePublic_Admin: The created scope's public information.
    """
    return ScopeServices.create_scope(session, form_data)


@router.get("/scopes/{id}", response_model=ScopePublic_Admin)
def read_scope(session: SessionDep, id: int, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:read"]
)],):
    """
    Get a scope by ID.

    Args:
        id (int): The ID of the scope to retrieve.

    Returns:
        ScopePublic_Admin: The public information of the retrieved scope.
    """
    return ScopeServices.get_scope(session, id)


@router.patch("/scopes/{id}", response_model=ScopePublic_Admin)
def update_scope(session: SessionDep, id: int, form_data: ScopeUpdate, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:update"]
)],):
    """
    Update a scope by ID.

    Args:
        id (int): The ID of the scope to update.
        form_data (ScopeUpdate): Data to update the scope.

    Returns:
        ScopePublic_Admin: The updated public information of the scope.
    """
    return ScopeServices.update_scope(session, id, form_data)


@router.delete("/scopes/{id}")
def delete_scope(session: SessionDep, id: int, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:delete"]
)],):
    """
    Delete a scope by ID.

    Args:
        id (int): The ID of the scope to delete.

    Returns:
        dict: A message indicating successful scope deletion.
    """
    return ScopeServices.delete_scope(session, id)


@router.get("/scopes", response_model=list[ScopePublic])
def list_scopes(session: SessionDep, _: Annotated[User, Security(
    get_current_active_user, scopes=["scope:read"]
)]):
    """
    List all scopes.

    Returns:
        list[ScopePublic]: A list of all scopes' public information.
    """
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
    """
    Update a user by username.

    Args:
        username (str): The username of the user to update.
        form_data (UserUpdate_Admin): Data to update the user.

    Returns:
        UserPublic_Admin: The updated public information of the user.
    """
    return UserServices.admin_update_user(session, username, form_data)


@router.get("", response_model=list[UserPublic])
def list_users(session: SessionDep, _: Annotated[User, Security(
    get_current_active_user,
    scopes=["admin:read"]
)]):
    """
    List all users.

    Returns:
        list[UserPublic]: A list of all users' public information.
    """
    return UserServices.get_all_users(session)

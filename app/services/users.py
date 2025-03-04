from sqlalchemy import select
from app.db.session import Session
from app.schemas import users
from app.db.models.users import User, Role, Scope
from app.db.repositories.users import UserRepository, RoleRepository, ScopeRepository
from app.services.auth import hash_password
from app.core import config
from fastapi.exceptions import HTTPException


class UserServices:
    @staticmethod
    def create_user(session: Session, data: users.UserCreate):
        """
        Create a new user.

        Args:
            session (Session): Database session.
            data (UserCreate): Data to create a new user.

        Returns:
            User: The created user.

        Raises:
            HTTPException: If the username already exists.
        """
        if UserRepository.get_user_by_username(session, data.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        data.password = hash_password(data.password)
        user = UserRepository.create_user(session, data)
        user = UserServices.admin_update_user(session, user.username, users.UserUpdate_Admin(roles=[config.BASIC_ROLE_NAME]))
        return user

    @staticmethod
    def get_user(session: Session, username: str):
        """
        Retrieve a user by their username.

        Args:
            session (Session): Database session.
            username (str): Username.

        Returns:
            User: The user with the specified username.
        """
        return UserRepository.get_user_by_username(session, username)

    @staticmethod
    def get_all_users(session: Session):
        """
        Retrieve all users.

        Args:
            session (Session): Database session.

        Returns:
            list[User]: A list of all users.
        """
        return UserRepository.get_all_users(session)

    @staticmethod
    def update_user(session: Session, user: User, data: users.UserUpdate):
        """
        Update an existing user.

        Args:
            session (Session): Database session.
            user (User): The user to update.
            data (UserUpdate): Data to update the user.

        Returns:
            User: The updated user.
        """
        return UserRepository.update_user(session, user.id, data)

    @staticmethod
    def admin_update_user(session: Session, username: str, data: users.UserUpdate_Admin):
        """
        Update a user by an admin.

        Args:
            session (Session): Database session.
            username (str): The username of the user to update.
            data (UserUpdate_Admin): Data to update the user.

        Returns:
            User: The updated user.
        """
        user = UserRepository.get_user_by_username(session, username)
        user = UserRepository.update_user_by_admin(session, user.id, data)
        return user


class RoleServices:
    @staticmethod
    def create_role(session: Session, role: users.RoleCreate):
        """
        Create a new role.

        Args:
            session (Session): Database session.
            role (RoleCreate): Data to create a new role.

        Returns:
            Role: The created role.

        Raises:
            HTTPException: If the role already exists.
        """
        if RoleRepository.get_role_by_name(session, role.name):
            raise HTTPException(status_code=400, detail="Role already exists")
        return RoleRepository.create_role(session, role)

    @staticmethod
    def get_all_roles(session: Session):
        """
        Retrieve all roles.

        Args:
            session (Session): Database session.

        Returns:
            list[Role]: A list of all roles.
        """
        return RoleRepository.get_all_roles(session)

    @staticmethod
    def get_role(session: Session, id: int):
        """
        Retrieve a role by its ID.

        Args:
            session (Session): Database session.
            id (int): Role ID.

        Returns:
            Role: The role with the specified ID.
        """
        return RoleRepository.get_role_by_id(session, id)

    @staticmethod
    def update_role(session: Session, id: int, data: users.RoleUpdate):
        """
        Update an existing role.

        Args:
            session (Session): Database session.
            id (int): Role ID.
            data (RoleUpdate): Data to update the role.

        Returns:
            Role: The updated role.
        """
        return RoleRepository.update_role(session, id, data)

    @staticmethod
    def delete_role(session: Session, id: int):
        """
        Delete a role.

        Args:
            session (Session): Database session.
            id (int): Role ID.

        Raises:
            HTTPException: If the role is not found.
        """
        if not RoleRepository.get_role_by_id(session, id):
            raise HTTPException(status_code=404, detail="Role not found")
        return RoleRepository.delete_role(session, id)

    @staticmethod
    def create_default_role_with_scope(session: Session,
                                    *,
                                    perms: list[tuple[str, str]],
                                    role_name: str,
                                    role_desc: str):
        """
        Create the default role and scopes.

        Args:
            session (Session): Database session.
            perms (list[tuple[str, str]]): List of permissions (scope name and description).
            role_name (str): Name of the role.
            role_desc (str): Description of the role.
        """
        crud_scopes = perms.copy()
        scope_objects: list[Scope] = []

        for scope_name, scope_desc in crud_scopes:
            scope = ScopeRepository.get_scope_by_name(session, scope_name)
            if not scope:
                scope = ScopeRepository.create_scope(session, users.ScopeCreate(name=scope_name, description=scope_desc, roles=[]))
            scope_objects.append(scope)
        role = RoleRepository.get_role_by_name(session, role_name)
        if not role:
            role = RoleRepository.create_role(session, users.RoleCreate(name=role_name, description=role_desc))
        role.scopes.update(scope_objects)
        session.commit()


class ScopeServices:
    @staticmethod
    def create_scope(session: Session, scope: users.ScopeCreate):
        """
        Create a new scope.

        Args:
            session (Session): Database session.
            scope (ScopeCreate): Data to create a new scope.

        Returns:
            Scope: The created scope.

        Raises:
            HTTPException: If the scope already exists.
        """
        if ScopeRepository.get_scope_by_name(session, scope.name):
            raise HTTPException(status_code=400, detail="Scope already exists")
        return ScopeRepository.create_scope(session, scope)

    @staticmethod
    def get_user_scopes(session: Session, username: str) -> set[str]:
        """
        Retrieve all scopes for a user.

        Args:
            session (Session): Database session.
            username (str): Username.

        Returns:
            set[str]: A set of scope names.
        """
        user = UserServices.get_user(session, username)
        return set(scope.name for role in user.roles for scope in role.scopes)

    @staticmethod
    def get_all_scopes(session: Session):
        """
        Retrieve all scopes.

        Args:
            session (Session): Database session.

        Returns:
            list[Scope]: A list of all scopes.
        """
        return ScopeRepository.get_all_scopes(session)

    @staticmethod
    def get_all_scopes_dict(session: Session) -> dict[str, str]:
        """
        Retrieve all scopes as a dictionary.

        Args:
            session (Session): Database session.

        Returns:
            dict[str, str]: A dictionary of scope names and descriptions.
        """
        try:
            return {scope.name: scope.description for scope in ScopeServices.get_all_scopes(session)}
        except Exception as e:
            print("get_all_scopes_dict", e)
            return {}

    @staticmethod
    def get_scope(session: Session, id: int):
        """
        Retrieve a scope by its ID.

        Args:
            session (Session): Database session.
            id (int): Scope ID.

        Returns:
            Scope: The scope with the specified ID.
        """
        return ScopeRepository.get_scope_by_id(session, id)

    @staticmethod
    def update_scope(session: Session, id: int, data: users.ScopeUpdate):
        """
        Update an existing scope.

        Args:
            session (Session): Database session.
            id (int): Scope ID.
            data (ScopeUpdate): Data to update the scope.

        Returns:
            Scope: The updated scope.
        """
        return ScopeRepository.update_scope(session, id, data)

    @staticmethod
    def delete_scope(session: Session, id: int):
        """
        Delete a scope.

        Args:
            session (Session): Database session.
            id (int): Scope ID.

        Raises:
            HTTPException: If the scope is not found.
        """
        if not ScopeRepository.get_scope_by_id(session, id):
            raise HTTPException(status_code=404, detail="Scope not found")
        return ScopeRepository.delete_scope(session, id)
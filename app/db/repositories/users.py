from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, insert
from app.db.models.users import User, Role, Scope
from app.schemas import users as users_schema


class UserRepository:
    @staticmethod
    def get_user_by_id(session: Session, id: int) -> User:
        """
        Retrieve a user by their ID.

        Args:
            session (Session): Database session.
            id (int): User ID.

        Returns:
            User: The user with the specified ID.
        """
        return session.get(User, id)
    
    @staticmethod
    def get_user_by_username(session: Session, username: str) -> User:
        """
        Retrieve a user by their username.

        Args:
            session (Session): Database session.
            username (str): Username.

        Returns:
            User: The user with the specified username.
        """
        return session.scalar(select(User).where(User.username == username))
    
    @staticmethod
    def get_all_users(session: Session) -> list[User]:
        """
        Retrieve all users.

        Args:
            session (Session): Database session.

        Returns:
            list[User]: A list of all users.
        """
        return session.scalars(select(User)).all()
    
    @staticmethod
    def create_user(session: Session, data: users_schema.UserCreate) -> User:
        """
        Create a new user.

        Args:
            session (Session): Database session.
            data (UserCreate): Data to create a new user.

        Returns:
            User: The created user.
        """
        user = User(**data.model_dump())
        session.add(user)
        session.commit()
        return user
    
    @staticmethod
    def update_user(session: Session, user_id: int, data: users_schema.UserUpdate) -> User:
        """
        Update an existing user.

        Args:
            session (Session): Database session.
            user_id (int): User ID.
            data (UserUpdate): Data to update the user.

        Returns:
            User: The updated user.
        """
        update_stmt = update(User).where(User.id == user_id).values(**data.model_dump(exclude_unset=True))
        session.execute(update_stmt)
        session.commit()
        user = UserRepository.get_user_by_id(session, user_id)
        return user
    
    @staticmethod
    def update_user_by_admin(session: Session, user_id: int, data: users_schema.UserUpdate_Admin) -> User:
        """
        Update a user by an admin.

        Args:
            session (Session): Database session.
            user_id (int): User ID.
            data (UserUpdate_Admin): Data to update the user.

        Returns:
            User: The updated user.
        """
        roles = session.scalars(select(Role).where(Role.name.in_(data.roles))).all()
        update_stmt = update(User).where(User.id == user_id).values(**data.model_dump(exclude_unset=True, exclude=["roles"]))
        session.execute(update_stmt)
        user = UserRepository.get_user_by_id(session, user_id)
        user.roles.update(roles)
        session.commit()
        return user
    
    @staticmethod
    def delete_user(session: Session, user_id: int):
        """
        Delete a user.

        Args:
            session (Session): Database session.
            user_id (int): User ID.
        """
        user = UserRepository.get_user_by_id(session, user_id)
        session.delete(user)
        session.commit()
    

class RoleRepository:
    @staticmethod
    def get_role_by_id(session: Session, role_id: int) -> Role:
        """
        Retrieve a role by its ID.

        Args:
            session (Session): Database session.
            role_id (int): Role ID.

        Returns:
            Role: The role with the specified ID.
        """
        return session.get(Role, role_id)
    
    @staticmethod
    def get_role_by_name(session: Session, role_name: str) -> Role:
        """
        Retrieve a role by its name.

        Args:
            session (Session): Database session.
            role_name (str): Role name.

        Returns:
            Role: The role with the specified name.
        """
        return session.scalar(select(Role).where(Role.name == role_name))
    
    @staticmethod
    def get_all_roles(session: Session) -> list[Role]:
        """
        Retrieve all roles.

        Args:
            session (Session): Database session.

        Returns:
            list[Role]: A list of all roles.
        """
        return session.scalars(select(Role)).all()
    
    @staticmethod
    def create_role(session: Session, data: users_schema.RoleCreate) -> Role:
        """
        Create a new role.

        Args:
            session (Session): Database session.
            data (RoleCreate): Data to create a new role.

        Returns:
            Role: The created role.
        """
        users = session.scalars(select(User).where(User.username.in_(data.users))).all()
        scopes = session.scalars(select(Scope).where(Scope.name.in_(data.scopes))).all()
        
        role = Role(**data.model_dump(exclude=['users', 'scopes']), users=set(users), scopes=set(scopes))
        session.add(role)
        session.commit()
        return role
    
    @staticmethod
    def update_role(session: Session, role_id: int, data: users_schema.RoleUpdate) -> Role:
        """
        Update an existing role.

        Args:
            session (Session): Database session.
            role_id (int): Role ID.
            data (RoleUpdate): Data to update the role.

        Returns:
            Role: The updated role.
        """
        users = session.scalars(select(User).where(User.username.in_(data.users))).all()
        scopes = session.scalars(select(Scope).where(Scope.name.in_(data.scopes))).all()
        
        update_stmt = update(Role).where(Role.id == role_id).values(**data.model_dump(exclude_unset=True, exclude=["users", "scopes"]))
        session.execute(update_stmt)
        role = RoleRepository.get_role_by_id(session, role_id)
        role.users.update(users)
        role.scopes.update(scopes)
        session.commit()
        return role
    
    @staticmethod
    def delete_role(session: Session, role_id: int):
        """
        Delete a role.

        Args:
            session (Session): Database session.
            role_id (int): Role ID.
        """
        role = RoleRepository.get_role_by_id(session, role_id)
        session.delete(role)
        session.commit()


class ScopeRepository:
    @staticmethod
    def get_scope_by_id(session: Session, scope_id: int) -> Scope:
        """
        Retrieve a scope by its ID.

        Args:
            session (Session): Database session.
            scope_id (int): Scope ID.

        Returns:
            Scope: The scope with the specified ID.
        """
        return session.get(Scope, scope_id)
    
    @staticmethod
    def get_scope_by_name(session: Session, scope_name: str) -> Scope:
        """
        Retrieve a scope by its name.

        Args:
            session (Session): Database session.
            scope_name (str): Scope name.

        Returns:
            Scope: The scope with the specified name.
        """
        return session.scalar(select(Scope).where(Scope.name == scope_name))
    
    @staticmethod
    def get_all_scopes(session: Session) -> list[Scope]:
        """
        Retrieve all scopes.

        Args:
            session (Session): Database session.

        Returns:
            list[Scope]: A list of all scopes.
        """
        return session.scalars(select(Scope)).all()
    
    @staticmethod
    def create_scope(session: Session, data: users_schema.ScopeCreate) -> Scope:
        """
        Create a new scope.

        Args:
            session (Session): Database session.
            data (ScopeCreate): Data to create a new scope.

        Returns:
            Scope: The created scope.
        """
        roles = session.scalars(select(Role).where(Role.name.in_(data.roles))).all()
        scope = Scope(**data.model_dump(exclude=['roles']), roles=set(roles))
        session.add(scope)
        session.commit()
        session.refresh(scope)
        return scope
    
    @staticmethod
    def update_scope(session: Session, scope_id: int, data: users_schema.ScopeUpdate) -> Scope:
        """
        Update an existing scope.

        Args:
            session (Session): Database session.
            scope_id (int): Scope ID.
            data (ScopeUpdate): Data to update the scope.

        Returns:
            Scope: The updated scope.
        """
        roles = session.scalars(select(Role).where(Role.name.in_(data.roles))).all()
        
        update_stmt = update(Scope).where(Scope.id == scope_id).values(**data.model_dump(exclude_unset=True, exclude=["roles"]))
        session.execute(update_stmt)
        scope = ScopeRepository.get_scope_by_id(session, scope_id)
        scope.roles.update(roles)
        session.commit()
        return scope
    
    @staticmethod
    def delete_scope(session: Session, scope_id: int):
        """
        Delete a scope.

        Args:
            session (Session): Database session.
            scope_id (int): Scope ID.
        """
        scope = ScopeRepository.get_scope_by_id(session, scope_id)
        session.delete(scope)
        session.commit()
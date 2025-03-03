from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, insert
from app.db.models.users import User, Role, Scope
from app.schemas import users as users_schema


class UserRepository:
    @staticmethod
    def get_user_by_id(session: Session, id: int) -> User:
        return session.get(User, id)
    
    @staticmethod
    def get_user_by_username(session: Session, username: str) -> User:
        return session.scalar(select(User).where(User.username == username))
    
    @staticmethod
    def get_all_users(session: Session) -> list[User]:
        return session.scalars(select(User)).all()
    
    @staticmethod
    def create_user(session: Session, data: users_schema.UserCreate) -> User:
        user = User(**data.model_dump())
        session.add(user)
        session.commit()
        return user
    
    @staticmethod
    def update_user(session: Session, user_id: int, data: users_schema.UserUpdate) -> User:
        update_stmt = update(User).where(User.id == user_id).values(**data.model_dump(exclude_unset=True))
        session.execute(update_stmt)
        session.commit()
        user = UserRepository.get_user_by_id(session, user_id)
        return user
    
    @staticmethod
    def update_user_by_admin(session: Session, user_id: int, data: users_schema.UserUpdate_Admin) -> User:
        roles = session.scalars(select(Role).where(Role.name.in_(data.roles))).all()
        update_stmt = update(User).where(User.id == user_id).values(**data.model_dump(exclude_unset=True, exclude=["roles"]))
        session.execute(update_stmt)
        user = UserRepository.get_user_by_id(session, user_id)
        user.roles.update(roles)
        session.commit()
        return user
    
    @staticmethod
    def delete_user(session: Session, user_id: int):
        user = UserRepository.get_user_by_id(session, user_id)
        session.delete(user)
        session.commit()
    

class RoleRepository:
    @staticmethod
    def get_role_by_id(session: Session, role_id: int) -> Role:
        return session.get(Role, role_id)
    
    @staticmethod
    def get_role_by_name(session: Session, role_name: str) -> Role:
        return session.scalar(select(Role).where(Role.name == role_name))
    
    @staticmethod
    def get_all_roles(session: Session) -> list[Role]:
        return session.scalars(select(Role)).all()
    
    @staticmethod
    def create_role(session: Session, data: users_schema.RoleCreate) -> Role:
        users = session.scalars(select(User).where(User.username.in_(data.users))).all()
        scopes = session.scalars(select(Scope).where(Scope.name.in_(data.scopes))).all()
        
        role = Role(**data.model_dump(exclude=['users', 'scopes']), users=set(users), scopes=set(scopes))
        session.add(role)
        session.commit()
        return role
    
    @staticmethod
    def update_role(session: Session, role_id: int, data: users_schema.RoleUpdate) -> Role:
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
        role = RoleRepository.get_role_by_id(session, role_id)
        session.delete(role)
        session.commit()


class ScopeRepository:
    @staticmethod
    def get_scope_by_id(session: Session, scope_id: int) -> Scope:
        return session.get(Scope, scope_id)
    
    @staticmethod
    def get_scope_by_name(session: Session, scope_name: str) -> Scope:
        return session.scalar(select(Scope).where(Scope.name == scope_name))
    
    @staticmethod
    def get_all_scopes(session: Session) -> list[Scope]:
        return session.scalars(select(Scope)).all()
    
    @staticmethod
    def create_scope(session: Session, data: users_schema.ScopeCreate) -> Scope:
        roles = session.scalars(select(Role).where(Role.name.in_(data.roles))).all()
        scope = Scope(**data.model_dump(exclude=['roles']), roles=set(roles))
        session.add(scope)
        session.commit()
        session.refresh(scope)
        return scope
    
    @staticmethod
    def update_scope(session: Session, scope_id: int, data: users_schema.ScopeUpdate) -> Scope:
        roles = session.scalars(select(Role).where(Role.name.in_(data.roles))).all()
        
        update_stmt = update(Scope).where(Scope.id == scope_id).values(**data.model_dump(exclude_unset=True, exclude=["roles"]))
        session.execute(update_stmt)
        scope = ScopeRepository.get_scope_by_id(session, scope_id)
        scope.roles.update(roles)
        session.commit()
        return scope
    
    @staticmethod
    def delete_scope(session: Session, scope_id: int):
        scope = ScopeRepository.get_scope_by_id(session, scope_id)
        session.delete(scope)
        session.commit()
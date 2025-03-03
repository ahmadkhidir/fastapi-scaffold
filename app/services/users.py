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
        if UserRepository.get_user_by_username(session, data.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        data.password = hash_password(data.password)
        user = UserRepository.create_user(session, data)
        user = UserServices.admin_update_user(session, user.username, users.UserUpdate_Admin(roles=[config.BASIC_ROLE_NAME]))
        return user

    @staticmethod
    def get_user(session: Session, username: str):
        return UserRepository.get_user_by_username(session, username)

    @staticmethod
    def get_all_users(session: Session):
        return UserRepository.get_all_users(session)

    @staticmethod
    def update_user(session: Session, user: User, data: users.UserUpdate):
        return UserRepository.update_user(session, user.id, data)

    @staticmethod
    def admin_update_user(session: Session, username: str, data: users.UserUpdate_Admin):
        user = UserRepository.get_user_by_username(session, username)
        user = UserRepository.update_user_by_admin(session, user.id, data)
        return user


class RoleServices:
    @staticmethod
    def create_role(session: Session, role: users.RoleCreate):
        if RoleRepository.get_role_by_name(session, role.name):
            raise HTTPException(status_code=400, detail="Role already exists")
        return RoleRepository.create_role(session, role)

    @staticmethod
    def get_all_roles(session: Session):
        return RoleRepository.get_all_roles(session)

    @staticmethod
    def get_role(session: Session, id: int):
        return RoleRepository.get_role_by_id(session, id)

    @staticmethod
    def update_role(session: Session, id: int, data: users.RoleUpdate):
        return RoleRepository.update_role(session, id, data)

    @staticmethod
    def delete_role(session: Session, id: int):
        if not RoleRepository.get_role_by_id(session, id):
            raise HTTPException(status_code=404, detail="Role not found")
        return RoleRepository.delete_role(session, id)

    @staticmethod
    def create_default_role_with_scope(session: Session,
                                    *,
                                    perms: list[tuple[str, str]],
                                    role_name: str,
                                    role_desc: str):
        '''Create the default role and scopes'''
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
        if ScopeRepository.get_scope_by_name(session, scope.name):
            raise HTTPException(status_code=400, detail="Scope already exists")
        return ScopeRepository.create_scope(session, scope)

    @staticmethod
    def get_user_scopes(session: Session, username: str) -> set[str]:
        user = UserServices.get_user(session, username)
        return set(scope.name for role in user.roles for scope in role.scopes)

    @staticmethod
    def get_all_scopes(session: Session):
        return ScopeRepository.get_all_scopes(session)

    @staticmethod
    def get_all_scopes_dict(session: Session) -> dict[str, str]:
        try:
            return {scope.name: scope.description for scope in ScopeServices.get_all_scopes(session)}
        except Exception as e:
            print("get_all_scopes_dict", e)
            return {}

    @staticmethod
    def get_scope(session: Session, id: int):
        return ScopeRepository.get_scope_by_id(session, id)

    @staticmethod
    def update_scope(session: Session, id: int, data: users.ScopeUpdate):
        return ScopeRepository.update_scope(session, id, data)

    @staticmethod
    def delete_scope(session: Session, id: int):
        if not ScopeRepository.get_scope_by_id(session, id):
            raise HTTPException(status_code=404, detail="Scope not found")
        return ScopeRepository.delete_scope(session, id)
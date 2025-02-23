from sqlmodel import select
from app.database import Session
from app.models import users
from app.services.auth import hash_password
from app import config


# User
def create_user(session: Session, user: users.UserCreate):
    user.password = hash_password(user.password)
    db_user = users.User.model_validate(user)
    user_role = session.exec(select(users.Role).where(
        users.Role.name == config.BASIC_ROLE_NAME)).first()
    db_user.roles.append(user_role)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(session: Session, username: str) -> users.User:
    return session.exec(select(users.User).filter(users.User.username == username)).first()


def get_all_users(session: Session) -> list[users.User]:
    return session.exec(select(users.User)).all()


def update_user(session: Session, user: users.User, data: users.UserUpdate) -> users.User:
    db_user = users.User.model_validate(
        user, update=data.model_dump(exclude_unset=True))
    db_user.password = hash_password(
        data.password) if data.password else db_user.password
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def admin_update_user(session: Session, username: str, data: users.UserUpdate_Admin) -> users. User:
    db_user = get_user(session, username)
    # data_dict = data.model_dump(exclude_unset=True)
    # print("data_dict", data_dict)
    if data.roles:
        print("data.roles", data.roles)
        roles = session.exec(select(users.Role).where(
            users.Role.name.in_(data.roles))).all()
        db_user.roles = roles
    #     data_dict["roles"] = roles
    # db_user = db_user.sqlmodel_update(data_dict)
    print("db_user", db_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# Role
def create_role(session: Session, role: users.RoleCreate):
    db_users = session.exec(select(users.User).where(
        users.User.username.in_(role.users))).all()
    db_scopes = session.exec(select(users.Scope).where(
        users.Scope.name.in_(role.scopes))).all()

    db_role = users.Role.model_validate(
        role, update={"users": db_users, "scopes": db_scopes})

    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role


def get_all_roles(session: Session) -> list[users.Role]:
    return session.exec(select(users.Role)).all()


def get_role(session: Session, id: int) -> users.Role:
    return session.get(users.Role, id)


def update_role(session: Session, id: int, data: users.RoleUpdate):
    data_dict = data.model_dump(exclude_unset=True)
    if data.users:
        data_dict['users'] = session.exec(
            select(users.User).where(users.User.id.in_(data.users))).all()
    if data.scopes:
        data_dict['scopes'] = session.exec(
            select(users.Scope).where(users.Scope.id.in_(data.scopes))).all()
    role = get_role(session, id)
    db_role = users.Role.model_validate(role, update=data_dict)
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role


def delete_role(session: Session, id: int):
    role = get_role(session, id)
    session.delete(role)
    session.commit()
    session.refresh()


def create_default_role_with_scope(session: Session,
                                   *,
                                   perms: list[tuple[str, str]],
                                   role_name: str,
                                   role_desc: str):
    '''Create the default role and scopes'''
    crud_scopes = perms
    scope_objects = []

    for scope_name, scope_desc in crud_scopes:
        scope = session.exec(select(users.Scope).filter(
            users.Scope.name == scope_name)).first()
        if not scope:
            scope = users.Scope(name=scope_name, description=scope_desc)
            session.add(scope)
            session.commit()
            session.refresh(scope)
        scope_objects.append(scope)

    role: users.Role = session.exec(
        select(users.Role).filter(users.Role.name == role_name)).first()
    if role:
        role.scopes.extend(scope_objects)
    else:
        role = users.Role(
            name=role_name,
            description=role_desc,
            scopes=scope_objects
        )
    session.add(role)
    session.commit()


# Scope
def create_scope(session: Session, scope: users.ScopeCreate):
    db_roles = session.exec(select(users.Role).where(
        users.Role.name.in_(scope.roles))).all()

    db_scope = users.Scope.model_validate(scope, update={"roles": db_roles})

    session.add(db_scope)
    session.commit()
    session.refresh(db_scope)
    return db_scope


def get_user_scopes(session: Session, username: str) -> set[str]:
    db_user = get_user(session, username)
    return set(scope.name for role in db_user.roles for scope in role.scopes)


def get_all_scopes(session: Session) -> list[users.Scope]:
    return session.exec(select(users.Scope)).all()


def get_all_scopes_dict(session: Session) -> dict[str, str]:
    try:
        return {scope.name: scope.description for scope in get_all_scopes(session)}
    except Exception as e:
        print("get_all_scopes_dict", e)
        return {}


def get_scope(session: Session, id: int) -> users.Scope:
    return session.get(users.Scope, id)


def update_scope(session: Session, id: int, data: users.ScopeUpdate):
    data_dict = data.model_dump(exclude_unset=True)
    if data.roles:
        data_dict['roles'] = session.exec(
            select(users.Role).where(users.Role.id.in_(data.roles))).all()
    scope = get_scope(session, id)
    db_scope = users.Scope.model_validate(scope, update=data_dict)
    session.add(db_scope)
    session.commit()
    session.refresh(db_scope)
    return db_scope


def delete_scope(session: Session, id: int):
    scope = get_scope(session, id)
    session.delete(scope)
    session.commit()
    session.refresh()

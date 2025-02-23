import getpass
from sqlmodel import select
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import get_session
from app.models.users import User, Role, Scope
from app.services.auth import hash_password
from app import config
from app.services.users import create_default_role_with_scope

def create_admin_user():
    with next(get_session()) as session:

        def get_admin_role(): return session.exec(
            select(Role).filter(Role.name == config.ADMIN_ROLE_NAME)).first()
        

        def get_user_role(): return session.exec(
            select(Role).filter(Role.name == config.BASIC_ROLE_NAME)).first()
        
        user_role = get_user_role()
        admin_role = get_admin_role()
        
        if not user_role:
            print("User role does not exist.")
            return
        
        if not admin_role:
            print("Admin role does not exist.")
            return
            # print("Creating admin role...")
            # create_admin_role()
            # admin_role = get_admin_role()

        username = input("Enter username: ")
        user = session.exec(select(User).filter(
            User.username == username)).first()
        if user:
            print("User already exists.")
            return
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match.")
            return
        first_name = input("Enter first name (optional): ")
        last_name = input("Enter last name (optional): ")

        new_user = User(
            username=username,
            password=hash_password(password),
            first_name=first_name if first_name.isalpha() else None,
            last_name=last_name if last_name.isalpha() else None,
            roles=[user_role, admin_role]
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print("Admin user created successfully.")


# def create_admin_role():
#     with next(get_session()) as session:
#         admin_role = session.exec(
#             select(Role).filter(Role.name == "admin")).first()
#         if admin_role:
#             print("Admin role already exists.")
#             return

#         # Define the CRUD scopes
#         crud_scopes = [("admin:create", "Admin create scope"),
#                         ("admin:read", "Admin read scope"),
#                         ("admin:update", "Admin update scope"),
#                         ("admin:delete", "Admin delete scope"),]
#         scope_objects = []

#         for scope_name, scope_desc in crud_scopes:
#             scope = session.exec(select(Scope).filter(
#                 Scope.name == scope_name)).first()
#             if not scope:
#                 scope = Scope(name=scope_name, description=scope_desc)
#                 session.add(scope)
#                 session.commit()
#                 session.refresh(scope)
#             scope_objects.append(scope)

#         new_role = Role(
#             name="admin",
#             description="Admin role",
#             scopes=scope_objects
#         )
#         session.add(new_role)
#         session.commit()
#         print("Admin role created successfully.")


def init_db():
    '''Create the default roles and scopes'''
    print("Creating default roles and scopes...")
    with next(get_session()) as session:
        create_default_role_with_scope(
            session,
            perms=config.BASIC_DEFAULT_PERMISSIONS,
            role_name=config.BASIC_ROLE_NAME,
            role_desc=config.BASIC_ROLE_DESC
        )

        create_default_role_with_scope(
            session,
            perms=config.ADMIN_DEFAULT_PERMISSIONS,
            role_name=config.ADMIN_ROLE_NAME,
            role_desc=config.ADMIN_ROLE_DESC,
        )
    print("Default roles and scopes created successfully.")



commands = {
    "create_admin_user": create_admin_user,
    # "create_admin_role": create_admin_role,
    "init_db": init_db
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in commands:
        commands[sys.argv[1]]()

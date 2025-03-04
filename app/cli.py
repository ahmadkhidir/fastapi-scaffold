import getpass
from sqlmodel import select
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.session import get_session
from app.db.models.users import User, Role, Scope
from app.services.auth import hash_password
from app.core import config
from app.services.users import RoleServices
from app.db.repositories.users import RoleRepository, ScopeRepository, UserRepository

def create_admin_user():
    """
    Create an admin user by prompting for user details.

    Raises:
        SystemExit: If the user already exists or passwords do not match.
    """
    with next(get_session()) as session:
        user_role = RoleRepository.get_role_by_name(session, config.BASIC_ROLE_NAME)
        admin_role = RoleRepository.get_role_by_name(session, config.ADMIN_ROLE_NAME)
        
        if not user_role:
            print("User role does not exist.")
            return
        
        if not admin_role:
            print("Admin role does not exist.")
            return

        username = input("Enter username: ")
        user = UserRepository.get_user_by_username(session, username)
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
            roles={user_role, admin_role}
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print("Admin user created successfully.")

def init_db():
    """
    Initialize the database by creating default roles and scopes.
    """
    print("Creating default roles and scopes...")
    with next(get_session()) as session:
        RoleServices.create_default_role_with_scope(
            session,
            perms=config.BASIC_DEFAULT_PERMISSIONS,
            role_name=config.BASIC_ROLE_NAME,
            role_desc=config.BASIC_ROLE_DESC
        )

        RoleServices.create_default_role_with_scope(
            session,
            perms=config.ADMIN_DEFAULT_PERMISSIONS,
            role_name=config.ADMIN_ROLE_NAME,
            role_desc=config.ADMIN_ROLE_DESC,
        )
    print("Default roles and scopes created successfully.")

commands = {
    "create_admin_user": create_admin_user,
    "init_db": init_db
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in commands:
        commands[sys.argv[1]]()

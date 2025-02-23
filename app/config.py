import os


SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

ALLOW_ORIGINS = [i for i in os.getenv("ALLOW_ORIGINS", "").split(",") if i]
ALLOW_METHODS = [i for i in os.getenv("ALLOW_METHODS", "").split(",") if i]
ALLOW_HEADERS = [i for i in os.getenv("ALLOW_HEADERS", "").split(",") if i]
ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS", "false").lower() == "true"

DATABASE_URL = os.getenv("DATABASE_URL")


BASIC_DEFAULT_PERMISSIONS = [("user:create", "can create user"),
                            ("user:read", "can read user"),
                            ("user:update", "can update user"),
                            ("user:delete", "can delete user"),
                            ]

ADMIN_DEFAULT_PERMISSIONS = [("admin:create", "can create admin"),
                             ("admin:read", "can read admin"),
                             ("admin:update", "can update admin"),
                             ("admin:delete", "can delete admin"),
                             # role
                             ("role:create", "can create role"),
                             ("role:read", "can read role"),
                             ("role:update", "can update role"),
                             ("role:delete", "can delete role"),
                             #  scope
                             ("scope:create", "can create scope"),
                             ("scope:read", "can read scope"),
                             ("scope:update", "can update scope"),
                             ("scope:delete", "can delete scope"),
                             ]

ADMIN_ROLE_NAME = os.getenv("ADMIN_ROLE_NAME", "admin")
BASIC_ROLE_NAME = os.getenv("BASIC_ROLE_NAME", "basic")
ADMIN_ROLE_DESC = os.getenv("ADMIN_ROLE_DESC", "Admin role")
BASIC_ROLE_DESC = os.getenv("BASIC_ROLE_DESC", "Basic role")

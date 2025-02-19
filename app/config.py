import os


ALLOW_ORIGINS = [i for i in os.getenv("ALLOW_ORIGINS", "").split(",") if i]
ALLOW_METHODS = [i for i in os.getenv("ALLOW_METHODS", "").split(",") if i]
ALLOW_HEADERS = [i for i in os.getenv("ALLOW_HEADERS", "").split(",") if i]
ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS", "false").lower() == "true"


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
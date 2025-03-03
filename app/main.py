from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import auth, users
from app.core import config
from app.core.security import oauth2_scheme


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOW_ORIGINS,
    allow_credentials=config.ALLOW_CREDENTIALS,
    allow_methods=config.ALLOW_METHODS,
    allow_headers=config.ALLOW_HEADERS,
)

app.include_router(auth.router)
app.include_router(users.router)

# api = APIRouter(
#     prefix="/api",
# )

# app.include_router(api)

@app.get("/")
def read_root():
    return {"Hello": "World"}


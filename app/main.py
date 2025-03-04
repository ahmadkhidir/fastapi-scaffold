from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.api.v1.routers import auth, users
from app.core import config
from app.core.security import oauth2_scheme

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application lifespan events.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # startup
    yield
    # shutdown

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOW_ORIGINS,
    allow_credentials=config.ALLOW_CREDENTIALS,
    allow_methods=config.ALLOW_METHODS,
    allow_headers=config.ALLOW_HEADERS,
)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """
    Render the root HTML page.

    Args:
        request (Request): The request object.

    Returns:
        HTMLResponse: The rendered HTML response.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "FastAPI Scaffold by @ahmadkhidir"},
    )


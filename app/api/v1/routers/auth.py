from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import SessionDep
from app.services.users import UserServices
from app.services.auth import verify_password, create_access_token
from app.schemas.auth import Token, TokenPayload
from app.schemas.users import UserCreate
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login", response_model=Token)
def login_user(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Authenticate a user and return an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
        Token: Access token and token type.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    user = UserServices.get_user(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(
        TokenPayload(sub=user.username, scopes=form_data.scopes),
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=None)
def register_user(session: SessionDep, form_data: UserCreate):
    """
    Register a new user.

    Args:
        form_data (UserCreate): Data required to create a new user.

    Returns:
        dict: A message indicating successful user creation.
    """
    UserServices.create_user(session, form_data)
    return {"detail": "User created successfully"}
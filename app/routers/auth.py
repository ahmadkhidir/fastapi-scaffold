from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database import SessionDep
from app.services.users import get_user, create_user
from app.services.auth import verify_password, create_access_token
from app.models.auth import Token, TokenPayload
from app.models.users import UserCreate
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login", response_model=Token)
def login_user(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(
        TokenPayload(sub=user.username, scopes=form_data.scopes),
    )
    return Token(access_token=access_token, token_type="bearer")
    # return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register_user(session:SessionDep, form_data: UserCreate):
    create_user(session, form_data)
    return {"message": "User created successfully"}
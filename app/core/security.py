from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from app.db.session import SessionDep, get_session
from app.services.auth import decode_access_token
from app.services.users import UserServices, ScopeServices, RoleServices
from app.db.models.users import User
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes=ScopeServices.get_all_scopes_dict(next(get_session())),
)


def get_current_user(
        db: SessionDep,
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
    user = UserServices.get_user(db, payload.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": authenticate_value},
        )
    user_scopes = ScopeServices.get_user_scopes(db, user.username)
    for scope in security_scopes.scopes:
        # validate against payload scopes if provided
        if len(payload.scopes) != 0:
            # verify if the authenticity of the payload scopes
            valid_payload_scopes = [
                s for s in payload.scopes if s in user_scopes]
            if scope not in valid_payload_scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You did not provide the necessary permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        # validate against user scopes
        elif scope not in user_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
        security_scopes: SecurityScopes):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user

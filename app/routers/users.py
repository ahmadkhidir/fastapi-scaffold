from fastapi import APIRouter
from app.dependencies import CurrentActiveUserDep
from app.models.users import UserPublic

router = APIRouter(
    tags=["users"],
    prefix="/users",
)

@router.get("/me", response_model=UserPublic)
def get_current_user_profile(current_user: CurrentActiveUserDep):
    return current_user

from typing import Annotated
from fastapi import APIRouter, Depends

from wapang.app.users.schemas import UserSignupRequest, UserResponse
from wapang.app.users.services import UserService

user_router = APIRouter()


@user_router.post("/", status_code=201)
async def signup(
    signup_request: UserSignupRequest, user_service: Annotated[UserService, Depends()]
) -> UserResponse:
    user = await user_service.create_user(
        signup_request.email, signup_request.password,
    )
    return UserResponse(
        id=user.id,
        email=user.email,
        nickname=user.nickname,
        address=user.address,
        phone_number=user.phone_number,
    )
from http.client import CREATED, FORBIDDEN, NOT_FOUND

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from msio.logme.api.dependencies import (
    get_current_user,
    get_user_repository,
)
from msio.logme.core.config import settings
from msio.logme.domain.entities import User, UserRegistrationRequest
from msio.logme.domain.repositories import UserRepository
from msio.logme.schemas.users import (
    IdentitySchema,
    PasswordSchema,
    UserBase,
    UserLookupResults,
    UserRegistration,
)

router = APIRouter()


def user_to_api_adapter(user: User) -> UserBase:
    return UserBase(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
    )


@router.get("/users/")
async def list_users(
    offset: int = 0,
    limit: int = settings.API_PAGES_SIZE,
    logged_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    if logged_user.email != settings.FIRST_USER_EMAIL:
        raise HTTPException(
            status_code=FORBIDDEN, detail="Permission denied."
        )
    users_list = await user_repository.fetch_all_users(
        offset=offset, limit=limit
    )
    return UserLookupResults(
        results=[
            user_to_api_adapter(single_user) for single_user in users_list
        ]
    )


@router.get("/users/{user_id}/")
async def get_user(
    user_id: int,
    logged_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    observed_user = await user_repository.find_user_by_id(user_id)
    # if user is not found
    if not observed_user:
        raise HTTPException(status_code=NOT_FOUND, detail="Not found.")
    # only first user can read others data, otherwise hide it
    # (we could also return a 403)
    if (
        observed_user.id != logged_user.id
        and logged_user.email != settings.FIRST_USER_EMAIL
    ):
        raise HTTPException(status_code=NOT_FOUND, detail="Not found.")
    return user_to_api_adapter(observed_user)


@router.post("/users/")
async def create_user(
    user_data: UserRegistration,
    logged_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    if logged_user.email != settings.FIRST_USER_EMAIL:
        raise HTTPException(
            status_code=FORBIDDEN, detail="Permission denied."
        )
    registration_request = UserRegistrationRequest(**user_data.dict())
    created_user = await user_repository.register_user(
        registration_request
    )

    return JSONResponse(
        status_code=CREATED,
        content=user_to_api_adapter(created_user).dict(),
    )

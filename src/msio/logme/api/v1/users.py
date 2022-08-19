from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import Response

from msio.logme.api.dependencies import (
    USER_API_DEFAULT_RESPONSES,
    get_current_user,
    get_logged_admin,
    get_token_repository,
    get_user_repository,
)
from msio.logme.core.config import settings
from msio.logme.domain.entities import User, UserRegistrationRequest
from msio.logme.domain.repositories import TokenRepository, UserRepository
from msio.logme.domain.schemas import (
    Identity,
    Password,
    UserBase,
    UserLookupResults,
    UserRegistration,
)
from msio.logme.use_cases import (
    ForgetUserUseCase,
    IdentityChangeUseCase,
    ResetPasswordUseCase,
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


@router.get("/users/", responses=USER_API_DEFAULT_RESPONSES)
async def list_users(
    offset: int = 0,
    limit: int = settings.API_PAGES_SIZE,
    _logged_admin: User = Depends(get_logged_admin),
    user_repository: UserRepository = Depends(get_user_repository),
):
    """Get list of existing users.

    Constraints: Admin rights required
    """
    users_list = await user_repository.fetch_all_users(
        offset=offset, limit=limit
    )
    return UserLookupResults(
        results=[
            user_to_api_adapter(single_user) for single_user in users_list
        ]
    )


@router.get("/users/{user_id}/", responses=USER_API_DEFAULT_RESPONSES)
async def get_user(
    user_id: int,
    logged_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserBase:
    """Get user information given his id.

    Constraints: Admin rights required or resource ownership
    """
    observed_user = await user_repository.find_user_by_id(user_id)
    # if user is not found
    if not observed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found."
        )

    # Permission check:
    # only first user can read others data, otherwise hide it
    # (we could also return a 403)
    if (
        observed_user.id != logged_user.id
        and logged_user.email != settings.FIRST_USER_EMAIL
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found."
        )

    # if checks are OK, return found user
    return user_to_api_adapter(observed_user)


@router.post("/users/", responses=USER_API_DEFAULT_RESPONSES)
async def create_user(
    user_data: UserRegistration,
    logged_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
):
    """Update user identity or password.

    Constraints: Admin rights required or ownership on user
    """
    if logged_user.email != settings.FIRST_USER_EMAIL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied.",
        )
    registration_request = UserRegistrationRequest(**user_data.dict())
    created_user = await user_repository.register_user(
        registration_request
    )

    return Response(
        status_code=status.HTTP_201_CREATED,
        content=user_to_api_adapter(created_user),
    )


@router.delete(
    "/users/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=USER_API_DEFAULT_RESPONSES,
)
async def delete_user(
    user_id: int,
    logged_admin: User = Depends(get_logged_admin),
    user_repository: UserRepository = Depends(get_user_repository),
    token_repository: TokenRepository = Depends(get_token_repository),
):
    await ForgetUserUseCase(user_repository, token_repository)(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/users/{user_id}/", responses=USER_API_DEFAULT_RESPONSES)
async def update_user(
    user_id: int,
    new_identity: Identity = None,
    new_password: Password = None,
    logged_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repository),
    token_repository: TokenRepository = Depends(get_token_repository),
):
    """Get user information given his id.

    Constraints: Admin rights required or resource ownership
    """
    # permission check
    if (
        logged_user.email != settings.FIRST_USER_EMAIL
        and logged_user.id != user_id
    ):
        raise HTTPException(status_code=403, detail="Permission denied.")

    if not (new_identity or new_password):
        raise HTTPException(
            status_code=422, detail="Must provide something in the body."
        )

    if new_identity:
        await IdentityChangeUseCase(user_repository)(user_id, new_identity)
    if new_password:
        await ResetPasswordUseCase(user_repository, token_repository)(
            requester_id=logged_user.id,
            user_id=user_id,
            new_password=new_password,
        )
    # we could run update operations in parallel (could be good,
    # could be bad...) I just wanted to point out the fact that
    # we can. Especially if the token repository is slow or if
    # passwords are stored in a different table.
    # await asyncio.gather(*updates)

    # return an-up-to date version of the user
    return await user_repository.find_user_by_id(user_id)

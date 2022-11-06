
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api.deps import get_async_session, get_current_user
from app.crud.crud_user import crud_user

router = APIRouter()


# TODO: need to add e-mail verification/validation and ratelimits
@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    session: AsyncSession = Depends(get_async_session),
    user_in: schemas.UserCreate,
):
    """
    Create new user.
    """
    user = await crud_user.get_by_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud_user.create(session, obj_in=user_in)

    return user


@router.get("/me", response_model=schemas.User)
async def read_users_me(
        current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    patch: schemas.UserUpdate,
    *,
    session: AsyncSession = Depends(get_async_session),
    current_user: models.user = Depends(get_current_user),
):
    """
    Update own user.
    """

    user = await crud_user.update(
        session, current_user=current_user, patch=patch)

    return user

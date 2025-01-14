from uuid import UUID
from hashlib import sha256
from datetime import timedelta
from loguru import logger
from typing import List, MutableSequence

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException


from ... import app, manager
from ...config import URLPathsConfig, user_login_config

from ..services.user import (
    check_user_auth,
    get_all_users,
    register_new_user,
    create_login_password_user
)
from ..schemas.user import User, UserCreate, LoginLinkData


@app.post(
    URLPathsConfig.PREFIX + '/auth/register/',
    tags=['Authentication'],
    response_model=User
)
async def register_route(
    create_user_data: UserCreate
) -> User:
    """Endpoint for register user in system"""
    logger.info(
        f'Register user: login="{create_user_data.login}" '
        f'email="{create_user_data.email}"'
    )
    user = await register_new_user(create_user_data)
    return user


@app.post(
    URLPathsConfig.PREFIX + '/auth/login/',
    tags=['Authentication']
)
async def login_route(
    data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """Endpoint for login user"""
    login = data.username
    password = data.password
    logger.info(f"name: {login}")
    logger.info(f"password: {password}")
    logger.info(f"pass encoded: {sha256(password.encode()).hexdigest()}")

    user = check_user_auth(email_login_tg_link=login)

    logger.info(f"found user: {user}")

    if not user:
        # you can also use your own HTTPException
        raise InvalidCredentialsException
    elif sha256(password.encode()).hexdigest() != user.password_hash:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=login), expires=timedelta(
            hours=user_login_config.TOKEN_EXPIRY_TIME_HOURS
        )
    )

    return {'access_token': access_token,
            'token_type': 'bearer', }


@app.post(
    URLPathsConfig.PREFIX + '/auth/login_by_tg/',
    tags=['Authentication']
)
async def login_by_tg_route(data: LoginLinkData) -> dict:
    """Endpoint for login user"""
    link = data.link
    logger.info(f"link: {link}")
    logger.info(f"type(link): {type(link)}")

    user = check_user_auth(email_login_tg_link=link)

    if not user:
        # you can also use your own HTTPException
        raise InvalidCredentialsException

    logger.info(f"user.tg_id: {user.tg_id}")
    access_token = manager.create_access_token(
        data=dict(sub=str(user.tg_id)), expires=timedelta(
            hours=user_login_config.TOKEN_EXPIRY_TIME_HOURS
        )
    )
    logger.info(f"access_token: {access_token}")
    return {'access_token': access_token,
            'token_type': 'bearer', }


@app.post(
    URLPathsConfig.PREFIX + '/users/',
    tags=['Users'],
    response_model=User
)
async def create_login_password_route(
    create_user_data: UserCreate, user=Depends(manager)
) -> User:
    """Create login and password for existed user"""
    logger.info(
        f'Register user: login="{create_user_data.login}" '
    )
    user = await create_login_password_user(
        user_id=user.id, user_data=create_user_data
    )
    return user


@app.get(
    URLPathsConfig.PREFIX + "/users/",
    tags=['Users'],
    response_model=List[User]
)
async def read_users_route(user=Depends(manager)) -> List[User]:
    """
    Retrieve users.
    """
    users: List[User] = await get_all_users()
    return users


@app.get(
    URLPathsConfig.PREFIX + "/user/",
    tags=['Users'],
    response_model=User
)
async def read_user_profile_route(
    user=Depends(manager)
) -> User:
    """
    Retrieve user profile.
    """
    logger.info(f"user.password_hash: {user.password_hash}")
    if user.password_hash:
        user.password = "*****"
    return user

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
    load_user,
    get_all_users,
    register_new_user
)
from ..schemas.user import User, UserCreate


@app.post(
    URLPathsConfig.PREFIX + '/auth/register',
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
    user = register_new_user(create_user_data)

    return user


@app.post(
    URLPathsConfig.PREFIX + '/auth/login',
    tags=['Authentication']
)
def login_route(
    data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """Endpoint for login user"""
    name = data.username
    password = data.password
    logger.info(f"name: {name}")
    logger.info(f"password: {password}")
    # if name != "admin" or password != "admin":
    logger.info(f"pass encoded: {sha256(password.encode()).hexdigest()}")
    
    user = load_user(name)
    
    if not user:
        # you can also use your own HTTPException
        raise InvalidCredentialsException
    elif sha256(password.encode()).hexdigest() != user.password_hash:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=name), expires=timedelta(
            hours=user_login_config.TOKEN_EXPIRY_TIME
        )
    )

    return {'access_token': access_token,
            'token_type': 'bearer', }


@app.get(
    URLPathsConfig.PREFIX + "/users",
    tags=['Users'],
    response_model=List[User]
)
async def read_users_route() -> List[User]:
    """
    Retrieve users.
    """
    users: List[User] = await get_all_users()
    return users

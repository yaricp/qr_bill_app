from datetime import timedelta
from hashlib import sha256
from typing import List
from uuid import UUID

from fastapi import BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from ....infra.email.email_client import EmailClient
from ....infra.telegram.tg_utils import send_verify_link_to_tg
from ... import app, manager
from ...config import URLPathsConfig, app_config, user_login_config
from ..schemas.user import LoginLinkData, User, UserCreate, UserUpdate
from ..services.login_link import delete_link
from ..services.user import (check_user_auth, create_login_password_user,
                             create_temp_link, delete_user, get_all_users,
                             get_user_by_login, register_new_user, update_user,
                             verify_email_tg)


@app.post(
    URLPathsConfig.PREFIX + "/auth/register/",
    tags=["Authentication"],
    response_model=dict,
)
async def register_route(create_user_data: UserCreate) -> dict:
    """Endpoint for register user in system"""
    user = get_user_by_login(create_user_data.login)

    if user:
        return {"message": "Sorry, this login is already in use!"}

    user = await register_new_user(create_user_data)
    if user:
        return {"message": "User registered successfull"}
    return {"message": "Something wrong with registatrion!"}


@app.post(URLPathsConfig.PREFIX + "/auth/verify/", tags=["Authentication"])
async def verify_route(verify_data: LoginLinkData) -> User | dict:
    """Endpoint for verify email or tg"""
    link = verify_data.link
    link_id = await verify_email_tg(link=link)

    user = check_user_auth(email_login_tg_link=link)

    if not user:
        raise InvalidCredentialsException

    if link_id:
        delete_link(id=link_id)

    access_token = manager.create_access_token(
        data=dict(sub=str(user.tg_id)),
        expires=timedelta(hours=user_login_config.TOKEN_EXPIRY_TIME_HOURS),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post(
    URLPathsConfig.PREFIX + "/auth/link_to_email/",
    tags=["Authentication"],
    response_model=User,
)
async def send_verify_link_to_email_route(
    data: dict, background_tasks: BackgroundTasks, user=Depends(manager)
) -> dict | User:
    """Endpoint for sending verify link to email"""
    str_user_link = await create_temp_link(
        user_id=user.id, email=data["email"], action="verify"
    )

    if str_user_link == "User not found":
        return {"message": "User not found"}

    email_client = EmailClient(
        email=data["email"],
        subject=f"{app_config.APP_NAME} Temporary link for login",
        template="temp_link_email.html",
        template_vars={"temp_link": str_user_link},
    )

    background_tasks.add_task(email_client.send)

    return user


@app.post(
    URLPathsConfig.PREFIX + "/auth/link_to_tg/",
    tags=["Authentication"],
    response_model=User,
)
async def send_verify_link_to_tg_route(
    data: dict, background_tasks: BackgroundTasks, user=Depends(manager)
) -> User | dict:
    """Endpoint for sending verify link to tg"""
    str_user_link = await create_temp_link(
        user_id=user.id, tg_id=data["tg_id"], action="verify"
    )

    if str_user_link == "User not found":
        return {"message": "User not found"}

    background_tasks.add_task(
        send_verify_link_to_tg, tg_id=data["tg_id"], user_link=str_user_link
    )

    return user


@app.post(URLPathsConfig.PREFIX + "/auth/login/", tags=["Authentication"])
async def login_route(data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """Endpoint for login user"""
    login = data.username
    password = data.password
    user = check_user_auth(email_login_tg_link=login)

    if not user:
        # you can also use your own HTTPException
        raise InvalidCredentialsException
    elif sha256(password.encode()).hexdigest() != user.password_hash:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=login),
        expires=timedelta(hours=user_login_config.TOKEN_EXPIRY_TIME_HOURS),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post(URLPathsConfig.PREFIX + "/auth/login_by_tg/", tags=["Authentication"])
async def login_by_tg_route(data: LoginLinkData) -> dict:
    """Endpoint for login user"""
    link = data.link
    user = check_user_auth(email_login_tg_link=link)

    if not user:
        # you can also use your own HTTPException
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=str(user.tg_id)),
        expires=timedelta(hours=user_login_config.TOKEN_EXPIRY_TIME_HOURS),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post(URLPathsConfig.PREFIX + "/users/", tags=["Users"], response_model=User)
async def create_login_password_route(
    create_user_data: UserCreate, user=Depends(manager)
) -> User:
    """Enpoint for creating login and password for existed user"""
    return await create_login_password_user(user_id=user.id, user_data=create_user_data)


@app.get(URLPathsConfig.PREFIX + "/users/", tags=["Users"], response_model=List[User])
async def read_users_route(user=Depends(manager)) -> List[User]:
    """Endpoint for retrieving users"""
    users: List[User] = []
    if user.is_admin:
        users = await get_all_users()
    return users


@app.get(URLPathsConfig.PREFIX + "/user/", tags=["Users"], response_model=User)
async def read_user_profile_route(user=Depends(manager)) -> User:
    """Endpoint to retrieve a user profile"""
    if user.password_hash:
        user.password = "******"
    return user


@app.put(URLPathsConfig.PREFIX + "/user/", tags=["Users"], response_model=User)
async def update_user_profile_route(
    user_profile: UserUpdate, user=Depends(manager)
) -> User:
    """
    Endpoint to update a user profile
    """
    user_profile.id = user.id
    return await update_user(user_profile)


@app.delete(URLPathsConfig.PREFIX + "/users/{id}", tags=["Users"], response_model=User)
async def delete_user_profile_route(id: UUID, user=Depends(manager)) -> User:
    """Endpoint to delete a user profile"""
    return await delete_user(id)

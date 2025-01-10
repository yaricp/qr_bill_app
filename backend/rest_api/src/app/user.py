from requests import get
from uuid import UUID, uuid4
from hashlib import sha256
from datetime import datetime
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import(
    User as UserORM, LoginLink as LoginLinkORM
)

from .entities.user import User, UserCreate, UserUpdate
from .config import login_link_config, rest_api_config


class UserViews:

    def __init__(self):
        pass


class UserQueries:

    def __init__(self):
        pass

    def get_user_by_login_link(self, link: str) -> User | None:
        db_link = LoginLinkORM.query.filter_by(link=link).first()
        if db_link:
            return db_link.user
        return None

    def get_user_by_email(self, email: str) -> User:
        user = UserORM.query.filter_by(email=email).first()
        return user

    def get_user_by_login(self, login: str) -> User:
        user = UserORM.query.filter_by(login=login).first()
        return user

    def get_user_by_tg_id(self, tg_id: int) -> User:
        user = UserORM.query.filter_by(tg_id=tg_id).first()
        return user

    def get_all_users(self):
        return UserORM.query.all()


class UserCommands:

    def __init__(self):
        pass

    async def create_login_password_user(
        self, user_id: UUID, user_data: UserCreate
    ) -> User:
        user = UserORM.query.get(user_id)
        if user:
            password_hash = sha256(
                user_data.password.encode()
            ).hexdigest()
            user.login = user_data.login
            user.password_hash = password_hash
            db_session.commit()
            db_session.refresh(user)
            logger.info(f"user: {user}")
        return user

    async def register_user_by_email(
        self, incoming_item: UserCreate
    ) -> User:
        user = UserORM.query.filter_by(
            email=incoming_item.email
        ).first()
        if user:
            return user
        user = UserORM(
            email=incoming_item.email,
            password_hash=sha256(incoming_item.password.encode()).hexdigest()
        )
        db_session.add(user)
        db_session.commit()
        logger.info(f"user: {user}")
        return user

    async def register_user_by_tg_id(self, tg_id: str) -> User:
        user = UserORM.query.filter_by(tg_id=tg_id).first()
        if user:
            return user
        user = UserORM(tg_id=tg_id)
        db_session.add(user)
        db_session.commit()
        logger.info(f"user: {user}")
        return user

    async def edit_user(
        self, incoming_item: UserUpdate
    ) -> User:
        found_user = UserORM.query.get(incoming_item.id)
        incoming_item_dict = incoming_item.dict()
        for key, value in incoming_item_dict.items():
            if value != None:
                setattr(found_user, key, value)
        db_session.commit()
        return found_user

    async def create_temp_login_link_by_tg_id(
        self, tg_id: int
    ) -> str:
        found_user = UserORM.query.filter_by(tg_id=tg_id).first()
        link = uuid4()
        login_link = LoginLinkORM(
            link=link,
            created=datetime.now(),
            user_id=found_user.id
        )
        db_session.add(login_link)
        db_session.commit()
        logger.info(f"ID login_link: {login_link.id}")
        try:
            api_host = rest_api_config.REST_API_HOST
            api_port = rest_api_config.REST_API_PORT
            api_prefix = rest_api_config.REST_API_PREFIX
            link_countdown_uri = rest_api_config.REST_API_LOGIN_LINK_URI
            full_url_countdown = f"{api_host}:{api_port}{api_prefix}"\
                                f"{link_countdown_uri}{login_link.id}"
            logger.info(f"full_url_countdown: {full_url_countdown}")
            response = get(full_url_countdown)
            logger.info(f"response: {response}")
        except Exception as err:
            logger.error(f"Error: {err}")
        frontend_prefix = login_link_config.FRONTEND_APP_LOGIN_LINK_PREFIX
        result_link = f"{frontend_prefix}{login_link.link}"
        logger.info(f"result_link: {result_link}")
        return result_link

from requests import get
from uuid import UUID, uuid4
from hashlib import sha256
from datetime import datetime
from loguru import logger

from ..infra.database import db_session
from ..infra.database.models import (
    User as UserORM, LoginLink as LoginLinkORM
)

from .entities.user import User, UserCreate, UserUpdate
from .config import login_link_config, rest_api_config
from .metrics.users import (
    metric_user_track_action,
    metric_user_track_action_duration
)


class UserViews:

    def __init__(self):
        pass


class UserQueries:

    def __init__(self):
        pass

    def get_user_by_login_link(self, link: str) -> User | None:
        db_link = LoginLinkORM.query.filter_by(
            link_uuid=link, link_for=""
        ).first()
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

    async def get_all_users(self):
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
            metric_user_track_action("create_login_password_user")
        return user

    async def register_user_by_login(
        self, incoming_item: UserCreate
    ) -> User:
        user = UserORM.query.filter_by(login=incoming_item.login).first()
        if user:
            return user
        user = UserORM(
            login=incoming_item.login,
            password_hash=sha256(incoming_item.password.encode()).hexdigest()
        )
        db_session.add(user)
        db_session.commit()
        logger.info(f"user: {user}")
        metric_user_track_action("register_user_by_login")
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
        metric_user_track_action("register_user_by_email")
        return user

    async def register_user_by_tg_id(self, tg_id: str) -> User:
        user = UserORM.query.filter_by(tg_id=tg_id).first()
        if user:
            return user
        user = UserORM(tg_id=tg_id, tg_verified=True)
        db_session.add(user)
        db_session.commit()
        logger.info(f"user: {user}")
        metric_user_track_action("register_user_by_tg_id")
        return user

    async def edit_user(
        self, incoming_item: UserUpdate
    ) -> User:
        found_login_link = None
        found_user = UserORM.query.get(incoming_item.id)
        incoming_item_dict = incoming_item.dict()
        logger.info(f"incoming_item_dict: {incoming_item_dict}")
        logger.info(f"found_user: {found_user}")
        for key, value in incoming_item_dict.items():
            if value != None:
                if key == "email" and found_user.email != value:
                    found_user.email_verified = False
                    found_login_links = list(filter(
                        lambda x: x.link_for == "email",
                        found_user.links
                    ))
                    logger.info(f"found_login_links: {found_login_links}")
                    if len(found_login_links) > 0:
                        found_login_link = found_login_links[0]
                    logger.info(f"found_login_link: {found_login_link}")
                if key == "tg_id" and found_user.tg_id != value:
                    found_user.tg_verified = False
                    found_login_links = list(filter(
                        lambda x: x.link_for == "tg",
                        found_user.links
                    ))
                    logger.info(f"found_login_links: {found_login_links}")
                    if len(found_login_links) > 0:
                        found_login_link = found_login_links[0]
                    logger.info(f"found_login_link: {found_login_link}")
                setattr(found_user, key, value)
        if found_login_link:
            result_deleting = db_session.delete(found_login_link)
            logger.info(f"deleted : {found_login_link}")
            logger.info(f"result_deleting : {result_deleting}")
        logger.info(f"found_user.lang: {found_user.lang}")
        db_session.commit()
        db_session.refresh(found_user)
        logger.info(f"refreshed found_user: {found_user}")
        return found_user

    async def create_temp_login_link(
        self,
        user_id: int | None = None,
        tg_id: int | None = None,
        email: str | None = None,
        action: str = "login"
    ) -> str:
        if user_id:
            found_user = UserORM.query.get(user_id)
        else:
            if tg_id:
                found_user = UserORM.query.filter_by(tg_id=tg_id).first()
            if email:
                found_user = UserORM.query.filter_by(email=email).first()

        if action == "login":
            link_for = ""
        elif tg_id:
            link_for = "tg"
        elif email:
            link_for = "email"
        logger.info(f"found_user: {found_user}")
        if not found_user:
            return "User not found"

        link = uuid4()
        login_link = LoginLinkORM(
            link_uuid=link,
            link_for=link_for,
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
        if action == "login":
            frontend_prefix = login_link_config.FRONTEND_APP_LOGIN_LINK_PREFIX
        else:
            frontend_prefix = login_link_config.FRONTEND_APP_VERIFY_LINK_PREFIX
        result_link = f"{frontend_prefix}{login_link.link_uuid}"
        logger.info(f"result_link: {result_link}")
        return result_link

    async def verify_email_tg(self, link: UUID) -> UUID | None:
        found_link = LoginLinkORM.query.filter_by(
            link_uuid=link
        ).first()
        logger.info(f"found_link: {found_link}")
        if not found_link:
            return None
        delta_time = (
            datetime.now() - found_link.created
        ).total_seconds() / 60
        logger.info(f"delta_time: {delta_time}")
        if not found_link or delta_time > 5:
            db_session.delete(found_link)
            db_session.commit()
            return None
        user = found_link.user
        logger.info(f"found_link.link_for: {found_link.link_for}")
        if found_link.link_for == "tg":
            if not user.tg_id:
                return None
            elif user.tg_verified:
                return found_link.id
            user.tg_verified = True
            db_session.delete(found_link)
            db_session.commit()
            metric_user_track_action("verify_user_by_tg")
            return found_link.id
        if found_link.link_for == "email":
            if not user.email:
                return None
            elif user.email_verified:
                return found_link.id
            user.email_verified = True
            db_session.delete(found_link)
            db_session.commit()
            metric_user_track_action("verify_user_by_email")
            return found_link.id
        return None

    async def delete_user(self, id: UUID) -> User:
        user = UserORM.query.get(id)
        if user:
            db_session.delete(user)
            db_session.commit()
            metric_user_track_action("delete_user")
        return user

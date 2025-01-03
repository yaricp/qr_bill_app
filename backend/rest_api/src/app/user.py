from uuid import UUID
from hashlib import sha256
from datetime import datetime
from loguru import logger

from .entities.user import User
from ..infra.database import db_session
from ..infra.database.models import User as UserORM

from .entities.user import User, UserCreate


class UserViews:

    def __init__(self):
        pass


class UserQueries:

    def __init__(self):
        pass

    def get_user_by_email(self, email: str) -> User:
        user = UserORM.query.filter_by(email=email).first()
        return user

    def get_all_users(self):
        pass


class UserCommands:

    def __init__(self):
        pass

    async def register_user(self, user_data: UserCreate) -> User:
        user = User(
            email=user_data.email,
            login=user_data.login,
            password_hash=sha256(user_data.password.encode()).hexdigest()
        )
        return user

from pydantic_settings import BaseSettings


class LoginLinkConfig(BaseSettings):
    TIME_LIFE_TEMP_LOGIN_LINK_MIN: int


login_link_conf: LoginLinkConfig = LoginLinkConfig()

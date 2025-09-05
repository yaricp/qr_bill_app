from pydantic_settings import BaseSettings


class BillConfig(BaseSettings):
    FISCAL_SERVICE_HOSTNAME: str
    FISCAL_SERVICE_URI: str
    FISCAL_SERVICE_API_URI: str


class LoginLinkConfig(BaseSettings):
    FRONTEND_APP_LOGIN_LINK_PREFIX: str
    FRONTEND_APP_VERIFY_LINK_PREFIX: str
    TIME_LIFE_TEMP_LOGIN_LINK_MIN: int


class RestApiConfig(BaseSettings):
    REST_API_HOST: str
    REST_API_PORT: str
    REST_API_PREFIX: str
    REST_API_LOGIN_LINK_URI: str


class MetricsConfig(BaseSettings):
    METRICS_PREFIX: str = "my_app"


bill_config: BillConfig = BillConfig()
login_link_config: LoginLinkConfig = LoginLinkConfig()
rest_api_config: RestApiConfig = RestApiConfig()
metric_config: MetricsConfig = MetricsConfig()

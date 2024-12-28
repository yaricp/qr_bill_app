from pydantic_settings import BaseSettings


class BillConfig(BaseSettings):
    FISCAL_SERVICE_HOSTNAME: str
    FISCAL_SERVICE_URI: str
    FISCAL_SERVICE_API_URI: str


bill_config: BillConfig = BillConfig()

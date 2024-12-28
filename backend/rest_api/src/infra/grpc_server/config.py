from pydantic_settings import BaseSettings


class GRPCServerConfig(BaseSettings):
    GRPC_SERVER_HOST: str = '[::]'
    GRPC_SERVER_PORT: int = 50051


grpc_server_config: GRPCServerConfig = GRPCServerConfig()

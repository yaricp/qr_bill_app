#!/bin/sh

echo "Prepare GRPC server"

# poetry run python -m grpc_tools.protoc -I /grpc_proto --python_out=/backend/infra/grpc_server --pyi_out=/backend/infra/grpc_server --grpc_python_out=/backend/infra/grpc_server /grpc_proto/grpc.proto

echo "Start GRPC Server"

poetry run python start_grpc_server.py &


echo "Migrations"

poetry run alembic revision --autogenerate -m 'init'
poetry run alembic upgrade head

# echo "nameserver 8.8.8.8" >> /etc/resolv.conf

# product start
# echo "scripts prepare"
# scripts/prepare_data_in_db.sh

echo "DEBUG: $DEBUG";
if test "$DEBUG" = "true" || test "$DEBUG" = "True"
  then
    echo "start in reload mode"
    poetry run uvicorn src.api:app --host $UNICORN_HOST --port $UNICORN_PORT --reload --workers $UNICORN_WORKERS
  else
    echo "start in work mode"
    poetry run uvicorn src.api:app --host $UNICORN_HOST --port $UNICORN_PORT --workers $UNICORN_WORKERS --forwarded-allow-ips='*'
fi


#!/bin/sh

# echo "Prepare GRPC server"

# bash /scripts/prepare_grpc_proto.sh

# echo "change /src/infra/grpc_server/grpc_pb2_grpc.py"
# echo "  from: 'import grpc_pb2 as grpc__pb2'"
# echo " to: 'from . import grpc_pb2 as grpc__pb2'"
# cp /src/infra/grpc_server/grpc_pb2_grpc.py /src/infra/grpc_server/grpc_pb2_grpc.py.orig
# sed 's/import grpc_pb2/from . import grpc_pb2/g' /src/infra/grpc_server/grpc_pb2_grpc.py.orig > /src/infra/grpc_server/grpc_pb2_grpc.py

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

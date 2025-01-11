#!/bin/bash

echo "Prepare GRPC server"

bash /scripts/prepare_grpc_proto.sh

echo "change /src/infra/grpc_server/grpc_pb2_grpc.py"
echo "  from: 'import grpc_pb2 as grpc__pb2'"
echo " to: 'from . import grpc_pb2 as grpc__pb2'"
sed 's/import grpc_pb2 as grpc__pb2/from . import grpc_pb2 as grpc__pb2/' /src/infra/grpc_server/grpc_pb2_grpc.py


echo "Start main TG bot"

poetry run python3 /bot/main.py



#!/bin/bash

echo "Prepare GRPC server"

bash /scripts/prepare_grpc_proto.sh

echo "change /bot/app/grpc_client/grpc_pb2_grpc.py"
echo "  from: 'import grpc_pb2 as grpc__pb2'"
echo " to: 'from . import grpc_pb2 as grpc__pb2'"
cp /bot/app/grpc_client/grpc_pb2_grpc.py /bot/app/grpc_client/grpc_pb2_grpc.py.orig
sed 's/import grpc_pb2/from . import grpc_pb2/g' /bot/app/grpc_client/grpc_pb2_grpc.py.orig > /bot/app/grpc_client/grpc_pb2_grpc.py

echo "Start main TG bot"

poetry run python3 /bot/main.py

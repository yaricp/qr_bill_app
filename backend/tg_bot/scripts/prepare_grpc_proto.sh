#!/bin/bash

poetry run python -m grpc_tools.protoc -I /grpc_proto --python_out=/bot/grpc_client/ --pyi_out=/bot/grpc_client/ --grpc_python_out=/bot/grpc_client/ /grpc_proto/grpc.proto

#!/bin/bash

poetry run python -m grpc_tools.protoc -I /grpc_proto --python_out=/src/infra/grpc_server --pyi_out=/src/infra/grpc_server --grpc_python_out=/src/infra/grpc_server /grpc_proto/grpc.proto

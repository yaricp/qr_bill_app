#!/bin/bash

poetry run python -m grpc_tools.protoc -I /grpc_proto --python_out=/backend/infra/grpc_server --pyi_out=/backend/infra/grpc_server --grpc_python_out=/backend/infra/grpc_server /grpc_proto/grpc.proto

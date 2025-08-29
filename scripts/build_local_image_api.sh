#!/bin/bash

echo "Building local image for API";
mkdir -p ./backend/rest_api/grpc_proto;
cp ./backend/grpc_proto/* ./backend/rest_api/grpc_proto/grpc.proto;
ls -a ./backend/rest_api/grpc_proto/;
# docker-compose build api;
rm -rf ./backend/rest_api/grpc_proto;
ls -a ./backend/rest_api;
echo "Done.";
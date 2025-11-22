#!/bin/bash

echo "Building local image for API";
mkdir -p ./backend/rest_api/grpc_proto;
cp ./backend/grpc_proto/* ./backend/rest_api/grpc_proto/grpc.proto;
ls -a ./backend/rest_api/grpc_proto/;
docker-compose build api;
rm -rf ./backend/rest_api/grpc_proto;
mkdir -p ./backend/tg_bot/grpc_proto;
cp ./backend/grpc_proto/* ./backend/tg_bot/grpc_proto/grpc.proto;
docker-compose build tg;
rm -rf ./backend/tg_bot/grpc_proto;
echo "Done.";

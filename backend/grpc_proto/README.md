# gRPC Protocol Definitions

This directory holds the Protocol Buffer (.proto) files that define the gRPC services and messages used for inter-service communication within the QR Bill application backend.

## Files

- **grpc.proto**: The primary Protocol Buffer definition file, specifying the service contracts and data structures for gRPC communication.

## Purpose

The gRPC protocol definitions enable efficient and strongly-typed communication between different microservices or components of the backend, such as the REST API and the Telegram bot, ensuring data consistency and reliable interactions.

## How it Works

These .proto files are used to generate client and server-side code in various programming languages (e.g., Python) that can then be used to implement gRPC services and clients. This approach facilitates a clear contract between services and simplifies integration.

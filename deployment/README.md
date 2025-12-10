# Deployment

The QR Bill App is deployed using Docker and Docker Compose.

## Docker Compose

The `docker-compose.yml` file defines the services that make up the application, including the backend, frontend, and database.

To start the application, you can run the following command:

`docker-compose up -d`

This will start all the services in the background.

## Dockerfiles

The `backend/Dockerfile` and `frontend/Dockerfile` files define the Docker images for the backend and frontend, respectively.

The Docker images are built automatically when you run the `docker-compose up` command.

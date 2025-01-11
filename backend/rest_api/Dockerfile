FROM python:3.12

RUN apt update && apt upgrade -y
# RUN apt install -y protobuf-compiler

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

COPY pyproject.toml /
COPY poetry.lock /

RUN poetry install

RUN mkdir /src

WORKDIR /

COPY /alembic /alembic
COPY alembic.ini /
COPY /src /src
COPY /scripts /scripts
COPY start.sh /
COPY start_grpc_server.py /

# Changing permissions for correct work inside docker:
RUN chmod +x /start.sh
RUN chmod +x /scripts/*

RUN bash /scripts/prepare_grpc_proto.sh
RUN cp /src/infra/grpc_server/grpc_pb2_grpc.py /src/infra/grpc_server/grpc_pb2_grpc.py.orig
RUN sed 's/import grpc_pb2/from . import grpc_pb2/g' /src/infra/grpc_server/grpc_pb2_grpc.py.orig > /src/infra/grpc_server/grpc_pb2_grpc.py

RUN cat start.sh

ENTRYPOINT [ "/bin/bash", "-l", "-c" ]

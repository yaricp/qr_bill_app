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
RUN mkdir -p /grpc_proto

WORKDIR /

COPY /alembic /alembic
COPY alembic.ini /
COPY /src /src
COPY /scripts /scripts

COPY ./grpc_proto /grpc_proto

RUN ls -la /grpc_proto

COPY start.sh /
COPY start_tests.sh /
COPY start_grpc_server.py /

RUN chmod +x /start.sh
RUN chmod +x /start_tests.sh
RUN chmod +x /scripts/*

ENTRYPOINT [ "/bin/bash", "-l", "-c" ]

FROM python:3.12

RUN apt update && apt upgrade -y
RUN apt-get install -y libgl1 libzbar0

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

COPY pyproject.toml /
COPY poetry.lock /

RUN poetry install

RUN mkdir /bot

WORKDIR /

COPY /app /bot
COPY /scripts /scripts
COPY start.sh /

RUN chmod +x /start.sh
RUN chmod +x /scripts/*

RUN bash /scripts/prepare_grpc_proto.sh
RUN cp /src/infra/grpc_server/grpc_pb2_grpc.py /src/infra/grpc_server/grpc_pb2_grpc.py.orig
RUN sed 's/import grpc_pb2/from . import grpc_pb2/g' /src/infra/grpc_server/grpc_pb2_grpc.py.orig > /src/infra/grpc_server/grpc_pb2_grpc.py

ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
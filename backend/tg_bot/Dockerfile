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
RUN mkdir /grpc_proto

WORKDIR /

COPY /app /bot
COPY /scripts /scripts
COPY start.sh /
COPY /grpc_proto /grpc_proto

RUN chmod +x /start.sh
RUN chmod +x /scripts/*

ENTRYPOINT [ "/bin/bash", "-l", "-c" ]


#!/bin/sh

echo "Migrations"

poetry run alembic revision --autogenerate -m 'init'
poetry run alembic upgrade head

# echo "nameserver 8.8.8.8" >> /etc/resolv.conf

# product start
# echo "scripts prepare"
# scripts/prepare_data_in_db.sh

echo "DEBUG: $DEBUG";
if test "$DEBUG" = "true" || test "$DEBUG" = "True"
  then
    echo "start in reload mode"
    poetry run uvicorn backend.api:app --host 0.0.0.0 --port 80 --reload --workers $UVICORN_WORKERS
  else
    echo "start in work mode"
    poetry run uvicorn backend.api:app --host 0.0.0.0 --port 80 --workers $UVICORN_WORKERS --forwarded-allow-ips='*'
fi

#!/bin/bash

docker-compose exec api env PYTHONPATH=$PYTHONPTH:/src poetry run pytest /src/tests/api/smoke_tests
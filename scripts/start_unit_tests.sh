#!/bin/bash

docker-compose exec api env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/app
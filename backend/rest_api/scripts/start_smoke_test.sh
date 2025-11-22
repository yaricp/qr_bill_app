#!/bin/bash

env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/api/smoke_tests;
env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/api;

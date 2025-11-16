#!/bin/bash

echo "TEST_MODE: $TEST_MODE";
if test "$TEST_MODE" = "true" || test "$TEST_MODE" = "True"
  then
    echo "Install test dependencies"
    poetry install --with test
    echo "start in test mode"

    export PYTHONPATH="/src:$PYTHONPATH"
    poetry run pytest /src/tests --maxfail=1 --disable-warnings -q
  else
    echo "This is not test mode"
fi
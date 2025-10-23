#!/bin/bash

echo "Starting test_bill.py";
env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/app/test_bill.py;
echo "Starting test_category.py";
env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/app/test_category.py;
echo "Starting test_goods.py";
env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/app/test_goods.py;
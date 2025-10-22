#!/bin/bash

env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/app/test_bill.py
env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/app/test_category.py
env PYTHONPATH=$PYTHONPATH:/src poetry run pytest /src/tests/app/test_goods.py
#!/bin/sh

poetry run alembic revision --autogenerate -m 'rev_$(date +%Y%m%d_%H%M%S)'
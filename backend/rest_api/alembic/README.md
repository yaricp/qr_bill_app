# Alembic Database Migrations

This directory contains the database migration scripts managed by Alembic for the FastAPI REST API. Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.

## Purpose

Database migrations are essential for evolving the database schema over time without losing existing data. Alembic allows for version-controlled changes to the database, making it easy to upgrade or downgrade the schema as the application develops.

## Files

- **README**: This file, providing an overview of Alembic within this project.
- **env.py**: The environment script that Alembic uses to connect to the database and set up the migration environment.
- **script.py.mako**: A Mako template file used by Alembic to generate new migration scripts.
- **versions/**: This directory contains all the individual migration scripts, each representing a specific change to the database schema. Files are named with a timestamp and a descriptive name (e.g., `0072c3016538_init.py`).

## Key Interactions

- When a new migration is needed, `alembic revision -m "Description of change"` is used to create a new script in the `versions/` directory.
- The `env.py` script determines how the migration engine connects to the database and applies changes.
- Migration scripts in `versions/` define `upgrade()` and `downgrade()` functions to apply and revert schema changes, respectively.

## Usage

- To generate a new migration: `alembic revision -m "Your description here"`
- To apply all pending migrations: `alembic upgrade head`
- To revert the last migration: `alembic downgrade -1`

For more detailed usage, refer to the official Alembic documentation.

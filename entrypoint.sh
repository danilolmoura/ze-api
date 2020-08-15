#!/bin/sh

# Apply migrations in dev database
alembic upgrade head

# run tests
pytest tests/

# start application
python app.py
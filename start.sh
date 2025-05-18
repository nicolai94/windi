# bin/sh

echo "Running migrations..."
poetry run alembic upgrade head
echo "Starting server..."
export PYTHONPATH=$(pwd)
python3 src/main.py

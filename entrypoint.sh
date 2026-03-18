#!/bin/bash
set -e

ls -la
mkdir -p /app/staticfiles
python3 manage.py makemigrations
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
exec gunicorn --bind 0.0.0.0:8000 --workers 2 tovelka.wsgi:application

#!/bin/sh
python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py makemigrations publications
python manage.py migrate
python manage.py loaddata fixtures.json

gunicorn config.wsgi:application --bind 0.0.0.0
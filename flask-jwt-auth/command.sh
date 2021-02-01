#!/bin/bash
python manage.py db migrate
gunicorn --bind 0.0.0.0:5000 wsgi:app
#!/bin/bash
python manage.py makemigrations --merge
python manage.py makemigrations
python manage.py migrate

#!/usr/bin/env bash


echo "Look Makemigrations"
python kamping/manage.py makemigrations

echo "Start Migrate"
python kamping/manage.py migrate

echo "Start Project"
python kamping/manage.py runserver 0.0.0.0:8000
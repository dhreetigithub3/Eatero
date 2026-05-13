#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python eatero/manage.py collectstatic --no-input
python eatero/manage.py migrate

#!/bin/bash

set -e

# until ./wait-for-it.sh db:5432; do
#   >&2 echo "Postgres is unavailable - sleeping"
#   sleep 1
# done

>&2 echo "Postgres is up - executing command"

echo "running ----> app ---> main.py".

if [ $ENVIRONMENT == 'production' ]; then
  servercmd='gunicorn --workers 2 --bind 0.0.0.0:5000 --log-level=warning main:app'
else
  servercmd='python -u main.py'
fi

$servercmd

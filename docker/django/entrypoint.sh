#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST 5432; do
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata myshop_data.json 


exec "$@"
release: python manage.py makemigrations
release: python manage.py migrate

web: gunicorn BookList.wsgi --log-file -

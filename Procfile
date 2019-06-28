release: python manage.py migrate

web: gunicorn app.wsgi --log-file -
clock: python app/clock.py
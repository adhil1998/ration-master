python manage.py migrate
web: gunicorn money_track.wsgi:application --log-file - --log-level debug
worker: gunicorn --bind 0.0.0.0:8000 money_track.wsgi:application
heroku ps:scale web=1

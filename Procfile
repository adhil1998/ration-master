python manage.py migrate
web: gunicorn ration_master.wsgi:application --log-file - --log-level debug
worker: gunicorn --bind 0.0.0.0:8000 ration_master.wsgi:application
heroku ps:scale web=1

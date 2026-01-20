web: gunicorn airbnb.wsgi:application --log-file -
worker: celery -A airbnb worker -l info
beat: celery -A airbnb beat -l info

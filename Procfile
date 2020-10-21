release: python manage.py migrate
web: gunicorn gibele.wsgi
worker: celery -A gibele worker -l info
